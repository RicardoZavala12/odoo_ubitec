# -*- coding: utf-8 -*-
import logging

import requests

from odoo import api, fields, models, _
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


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

    # ------------------------------------------------------------------
    # Evidencias fotográficas (Fase 2)
    # ------------------------------------------------------------------
    photo_ids = fields.One2many(
        "gps.service.photo", "service_id", string="Evidencias fotográficas", copy=False
    )
    photos_complete = fields.Boolean(
        string="Fotos completas",
        compute="_compute_photos_complete",
        help="Verdadero cuando están las 6 fotos obligatorias.",
    )

    # Fotos obligatorias agrupadas por ETAPA del flujo:
    #   before  (Antes de instalar) → se validan al INICIAR el servicio
    #   install (Instalación) + after (Al terminar) → se validan al FINALIZAR
    _PHOTOS_BY_STAGE = {
        "before": ["unit", "plate", "serial", "dash_closed"],
        "install": ["install"],
        "after": ["dash_assembled"],
    }
    # Todos los tipos obligatorios (para el compute global de "completas")
    _REQUIRED_PHOTOS = [
        "unit", "plate", "serial", "dash_closed", "install", "dash_assembled",
    ]

    # Etapa de fotos que corresponde según el estado actual del servicio.
    # La usa el form de la foto para prellenar la etapa correcta.
    current_stage = fields.Selection(
        selection=[
            ("before", "Antes de instalar"),
            ("install", "Instalación"),
            ("after", "Al terminar"),
        ],
        string="Etapa actual de fotos",
        compute="_compute_current_stage",
    )

    @api.depends("state")
    def _compute_current_stage(self):
        for service in self:
            if service.state == "accepted":
                service.current_stage = "before"
            elif service.state == "in_progress":
                service.current_stage = "install"
            else:
                service.current_stage = False

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

    @api.depends("photo_ids", "photo_ids.photo_type")
    def _compute_photos_complete(self):
        for service in self:
            tipos = set(service.photo_ids.mapped("photo_type"))
            service.photos_complete = all(
                t in tipos for t in service._REQUIRED_PHOTOS
            )

    def _missing_photos(self):
        """Devuelve las etiquetas de TODAS las fotos obligatorias que faltan."""
        self.ensure_one()
        labels = dict(
            self.env["gps.service.photo"]._fields["photo_type"].selection
        )
        tipos = set(self.photo_ids.mapped("photo_type"))
        return [labels[t] for t in self._REQUIRED_PHOTOS if t not in tipos]

    def _missing_photos_for_stages(self, stages):
        """Etiquetas de las fotos que faltan SOLO para las etapas indicadas.

        Ej: _missing_photos_for_stages(['before']) → fotos de "antes" que faltan.
        """
        self.ensure_one()
        labels = dict(
            self.env["gps.service.photo"]._fields["photo_type"].selection
        )
        tipos = set(self.photo_ids.mapped("photo_type"))
        requeridas = []
        for stage in stages:
            requeridas += self._PHOTOS_BY_STAGE.get(stage, [])
        return [labels[t] for t in requeridas if t not in tipos]

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
        services = super().create(vals_list)
        # Notificar a Telegram cada servicio creado (no rompe si falla)
        for service in services:
            service._notify_telegram_created()
        return services

    # ==================================================================
    # Notificaciones Telegram
    # ==================================================================
    def _telegram_config(self):
        """Lee token y chat_id de los parámetros de sistema.

        Se configuran en Ajustes → Técnico → Parámetros del sistema:
          gps_service.telegram_token  y  gps_service.telegram_chat_id
        """
        icp = self.env["ir.config_parameter"].sudo()
        token = icp.get_param("gps_service.telegram_token")
        chat_id = icp.get_param("gps_service.telegram_chat_id")
        return token, chat_id

    def _send_telegram(self, text):
        """Envía un mensaje al grupo de Telegram. Silencioso si no hay config
        o si falla (no debe interrumpir la creación del servicio)."""
        token, chat_id = self._telegram_config()
        if not token or not chat_id:
            return
        try:
            requests.post(
                "https://api.telegram.org/bot%s/sendMessage" % token,
                data={
                    "chat_id": chat_id,
                    "parse_mode": "HTML",
                    "text": text,
                },
                timeout=10,
            )
        except Exception as e:  # noqa: BLE001 - no romper el flujo por Telegram
            _logger.warning("No se pudo enviar notificación a Telegram: %s", e)

    def _notify_telegram_created(self):
        """Mensaje de 'nuevo servicio creado' al grupo."""
        self.ensure_one()
        fecha = self.scheduled_date and fields.Datetime.to_string(self.scheduled_date) or "—"
        text = (
            "🆕 <b>Nuevo servicio GPS: %s</b>\n"
            "👤 Cliente: %s\n"
            "🚚 Unidad: %s\n"
            "🔧 Técnico: %s\n"
            "📍 Ubicación: %s\n"
            "📅 Programado: %s"
        ) % (
            self.name,
            self.partner_id.display_name or "—",
            self.unidad_id.display_name or (self.unit_brand or "—"),
            self.technician_id.name or "sin asignar",
            self.location or "—",
            fecha,
        )
        self._send_telegram(text)

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
        """El técnico llegó a sitio e inicia el servicio (marca la hora).

        Bloquea si faltan las fotos de la etapa "Antes de instalar".
        """
        for service in self:
            service._check_is_technician()
            if service.state != "accepted":
                raise UserError(_("Acepta el servicio antes de iniciarlo."))
            faltantes = service._missing_photos_for_stages(["before"])
            if faltantes:
                raise UserError(
                    _("No puedes iniciar el servicio: primero sube las fotos "
                      "de 'Antes de instalar':\n- %s") % "\n- ".join(faltantes)
                )
            service.write({
                "state": "in_progress",
                "start_time": fields.Datetime.now(),
            })

    def action_finish(self):
        """El técnico termina: marca la hora de fin y pasa a validación.

        Bloquea si faltan las fotos de 'Instalación' o 'Al terminar'.
        """
        for service in self:
            service._check_is_technician()
            if service.state != "in_progress":
                raise UserError(_("Inicia el servicio antes de finalizarlo."))
            faltantes = service._missing_photos_for_stages(["install", "after"])
            if faltantes:
                raise UserError(
                    _("No puedes finalizar: primero sube las fotos de "
                      "'Instalación' y 'Al terminar':\n- %s")
                    % "\n- ".join(faltantes)
                )
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
        """Regresar a borrador (solo agenda/manager).

        Limpia los datos del flujo anterior (tiempos y validación) para que
        el servicio quede realmente como nuevo, sin datos fantasma.
        """
        for service in self:
            service.write({
                "state": "draft",
                "start_time": False,
                "end_time": False,
                "validated_by": False,
                "validation_date": False,
            })

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
