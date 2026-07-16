# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class GpsService(models.Model):
    """Servicio de instalación/atención de GPS.

    Un servicio avanza por estados (state machine). Cada botón mueve el
    servicio al siguiente estado y lo ejecuta el rol correspondiente:

        draft -> assigned -> accepted -> in_progress -> to_validate -> done
                                                                        |
                                                                  post_service

    FASE 1: solo el flujo. Las evidencias fotográficas y la validación de
    "no finalizar sin fotos" se agregan en la fase 2.
    """

    _name = "gps.service"
    _description = "Servicio de GPS"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "scheduled_date desc, id desc"

    name = fields.Char(
        string="Folio",
        required=True,
        copy=False,
        readonly=True,
        default=lambda self: _("Nuevo"),
    )

    # ------------------------------------------------------------------
    # Datos del servicio (los captura quien agenda)
    # ------------------------------------------------------------------
    partner_id = fields.Many2one(
        "res.partner",
        string="Cliente",
        required=True,
        tracking=True,
    )
    unidad_id = fields.Many2one(
        "ubitec.unidad",
        string="Unidad / Equipo",
        domain="[('partner_id', '=', partner_id)]",
        help="Unidad GPS del cliente. Al elegirla se toman IMEI, serie y marca.",
    )
    # Datos que se toman de la unidad (related, solo lectura)
    imei = fields.Char(
        string="IMEI", related="unidad_id.imei", store=True, readonly=True
    )
    serial_number = fields.Char(
        string="Número de serie",
        related="unidad_id.numero_serie",
        store=True,
        readonly=True,
    )
    unit_brand = fields.Char(
        string="Marca / Modelo",
        related="unidad_id.marca",
        store=True,
        readonly=True,
    )
    # Placas: propio del servicio (ubitec.unidad no las guarda)
    plates = fields.Char(string="Placas", tracking=True)
    location = fields.Char(
        string="Ubicación del servicio",
        help="Dirección o lugar donde se realizará la instalación.",
        tracking=True,
    )
    scheduled_date = fields.Datetime(
        string="Fecha programada",
        tracking=True,
    )
    notes = fields.Text(string="Indicaciones")

    # ------------------------------------------------------------------
    # Asignación y estado
    # ------------------------------------------------------------------
    technician_id = fields.Many2one(
        "res.users",
        string="Técnico asignado",
        tracking=True,
    )
    state = fields.Selection(
        selection=[
            ("draft", "Borrador"),
            ("assigned", "Asignado"),
            ("accepted", "Aceptado"),
            ("in_progress", "En sitio"),
            ("to_validate", "Por validar"),
            ("done", "Completado"),
            ("post_service", "Post-servicio"),
        ],
        string="Estado",
        default="draft",
        required=True,
        tracking=True,
        copy=False,
    )

    # ------------------------------------------------------------------
    # Tiempos (automáticos)
    # ------------------------------------------------------------------
    start_time = fields.Datetime(string="Inicio en sitio", readonly=True, copy=False)
    end_time = fields.Datetime(string="Fin del servicio", readonly=True, copy=False)
    duration = fields.Float(
        string="Duración (horas)",
        compute="_compute_duration",
        store=True,
        help="Tiempo entre iniciar y finalizar el servicio, en horas.",
    )

    # ------------------------------------------------------------------
    # Validación
    # ------------------------------------------------------------------
    validated_by = fields.Many2one(
        "res.users", string="Validado por", readonly=True, copy=False
    )
    validation_date = fields.Datetime(string="Fecha de validación", readonly=True, copy=False)

    # ==================================================================
    # Cálculos
    # ==================================================================
    @api.depends("start_time", "end_time")
    def _compute_duration(self):
        for service in self:
            if service.start_time and service.end_time:
                delta = service.end_time - service.start_time
                service.duration = delta.total_seconds() / 3600.0
            else:
                service.duration = 0.0

    # ==================================================================
    # Folio (secuencia)
    # ==================================================================
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get("name") or vals["name"] == _("Nuevo"):
                vals["name"] = self.env["ir.sequence"].next_by_code(
                    "gps.service"
                ) or _("Nuevo")
        return super().create(vals_list)

    # ==================================================================
    # Botones del flujo (state machine)
    # ==================================================================
    def action_assign(self):
        """Quien agenda: confirma la asignación al técnico."""
        for service in self:
            if not service.technician_id:
                raise UserError(_("Asigna un técnico antes de continuar."))
            service.state = "assigned"

    def action_accept(self):
        """El técnico acepta el servicio que le fue asignado."""
        for service in self:
            service._check_is_technician()
            if service.state != "assigned":
                raise UserError(_("Solo puedes aceptar un servicio asignado."))
            service.state = "accepted"

    def action_start(self):
        """El técnico llegó a sitio e inicia el servicio (marca la hora)."""
        for service in self:
            service._check_is_technician()
            if service.state != "accepted":
                raise UserError(_("Acepta el servicio antes de iniciarlo."))
            service.write({
                "state": "in_progress",
                "start_time": fields.Datetime.now(),
            })

    def action_finish(self):
        """El técnico termina: marca la hora de fin y pasa a validación.

        En fase 2 aquí se validará que estén todas las fotos requeridas.
        """
        for service in self:
            service._check_is_technician()
            if service.state != "in_progress":
                raise UserError(_("Inicia el servicio antes de finalizarlo."))
            service.write({
                "state": "to_validate",
                "end_time": fields.Datetime.now(),
            })

    def action_validate(self):
        """Quien valida aprueba el servicio finalizado."""
        for service in self:
            if service.state != "to_validate":
                raise UserError(_("Solo se validan servicios por validar."))
            service.write({
                "state": "done",
                "validated_by": self.env.user.id,
                "validation_date": fields.Datetime.now(),
            })

    def action_post_service(self):
        """Quien valida reabre el servicio para reatender (post-servicio)."""
        for service in self:
            if service.state not in ("to_validate", "done"):
                raise UserError(
                    _("Solo se puede mandar a post-servicio un servicio "
                      "por validar o completado.")
                )
            service.state = "post_service"

    def action_reopen_assign(self):
        """Desde post-servicio: reasignar para volver a atender."""
        for service in self:
            if service.state != "post_service":
                raise UserError(_("Solo se reabre desde post-servicio."))
            service.state = "assigned"

    def action_reset_draft(self):
        """Regresar a borrador (solo agenda/manager)."""
        for service in self:
            service.state = "draft"

    # ==================================================================
    # Helpers
    # ==================================================================
    def _check_is_technician(self):
        """Solo el técnico asignado (o un manager) puede mover su servicio."""
        self.ensure_one()
        is_manager = self.env.user.has_group("gps_service.group_gps_manager")
        if not is_manager and self.technician_id != self.env.user:
            raise UserError(
                _("Solo el técnico asignado puede realizar esta acción.")
            )
