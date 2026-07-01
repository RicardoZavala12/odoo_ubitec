# -*- coding: utf-8 -*-
from dateutil.relativedelta import relativedelta
from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    # ── Generales Ubitec ──
    ubitec_es_cliente = fields.Boolean(
        string="Cliente Ubitec",
        help="Marca que este contacto fue dado de alta como cliente de Ubitec.",
    )
    ubitec_fecha_alta = fields.Date(string="Fecha de alta")
    ubitec_vendedor = fields.Char(string="Vendedor")

    # ── Esquema comercial ──
    ubitec_esquema = fields.Selection(
        selection=[
            ("venta", "Venta"),
            ("comodato", "Comodato"),
            ("migracion", "Migración"),
            ("reactivacion", "Reactivación"),
            ("demo", "Demo"),
            ("otro", "Otro"),
        ],
        string="Esquema",
        help="Comodato: se presta el equipo y se cobra mensualidad. "
        "Venta: el cliente compra el equipo.",
    )
    ubitec_unidades = fields.Integer(string="Nº de unidades (declaradas)")

    # ── Estado del cliente ──
    ubitec_estado = fields.Selection(
        selection=[
            ("nuevo", "Nuevo"),
            ("activo", "Activo"),
            ("inactivo", "Inactivo"),
        ],
        string="Estado",
        default="nuevo",
        tracking=True,
        help="Nuevo: primeros 30 días desde el alta (automático). "
        "Activo/Inactivo: se ajusta manualmente.",
    )

    # ── Costos de una sola vez ──
    ubitec_costo_equipo = fields.Float(string="Costo equipo")
    ubitec_costo_instalacion = fields.Float(string="Instalación")
    ubitec_costo_migracion = fields.Float(string="Migración")
    ubitec_costo_reinstalacion = fields.Float(string="Reinstalación")
    ubitec_costo_desinstalacion = fields.Float(string="Desinstalación")
    ubitec_costo_configuracion = fields.Float(string="Configuración")

    # ── Plan / cobro recurrente ──
    ubitec_mensualidad = fields.Float(string="Mensualidad")
    ubitec_financiamiento = fields.Float(string="Financiamiento")
    ubitec_semestre = fields.Float(string="Semestre")
    ubitec_anualidad = fields.Float(string="Anualidad")
    ubitec_bonificacion = fields.Float(string="Bonificación")

    # ── Registro de pago de mensualidad ──
    ubitec_dia_corte = fields.Integer(
        string="Día de corte",
        help="Día del mes en que le toca pagar (1-31).",
    )
    ubitec_ultimo_pago = fields.Date(string="Último pago")
    ubitec_proximo_pago = fields.Date(
        string="Próximo pago",
        compute="_compute_proximo_pago",
        store=True,
        help="Se calcula a partir del último pago + 1 mes.",
    )
    ubitec_estado_pago = fields.Selection(
        selection=[
            ("al_corriente", "Al corriente"),
            ("por_vencer", "Por vencer"),
            ("vencido", "Vencido"),
            ("sin_dato", "Sin dato"),
        ],
        string="Estado de pago",
        compute="_compute_estado_pago",
        store=True,
    )
    ubitec_pago_ids = fields.One2many(
        "ubitec.pago", "partner_id", string="Historial de pagos"
    )

    # ── Cartera vencida (Faltantes de pago) ──
    ubitec_adeudo = fields.Float(
        string="Adeudo / Atraso", help="Monto adeudado según reporte de faltantes."
    )
    ubitec_atraso_desde = fields.Char(string="Atraso desde")
    ubitec_cobranza_nota = fields.Char(string="Nota de cobranza")

    # ── Unidades y servicios (modelos ligados) ──
    ubitec_unidad_ids = fields.One2many(
        "ubitec.unidad", "partner_id", string="Unidades / Equipos"
    )
    ubitec_unidad_count = fields.Integer(
        string="Nº unidades", compute="_compute_ubitec_counts"
    )
    ubitec_servicio_ids = fields.One2many(
        "ubitec.servicio", "partner_id", string="Historial de servicios"
    )
    ubitec_servicio_count = fields.Integer(
        string="Nº servicios", compute="_compute_ubitec_counts"
    )

    # ── Servicios adicionales ──
    ubitec_serv_microfono = fields.Boolean(string="Micrófono")
    ubitec_serv_roaming = fields.Boolean(string="Roaming")
    ubitec_serv_sensor_temp = fields.Boolean(string="Sensor de temperatura")
    ubitec_serv_sensor_diesel = fields.Boolean(string="Sensor de diésel")
    ubitec_serv_sensor_puerta = fields.Boolean(string="Sensor de puerta")
    ubitec_serv_dashcam = fields.Boolean(string="Dash Cam")
    ubitec_serv_camara_int = fields.Boolean(string="Cámara interior")
    ubitec_serv_webservice = fields.Boolean(string="Web Service")

    # ── Acceso a la plataforma de rastreo ──
    ubitec_plataforma_usuario = fields.Char(string="Usuario plataforma")
    ubitec_plataforma_password = fields.Char(string="Contraseña plataforma")

    # ───────────────────── Cálculos ─────────────────────

    @api.depends("ubitec_unidad_ids", "ubitec_servicio_ids")
    def _compute_ubitec_counts(self):
        for partner in self:
            partner.ubitec_unidad_count = len(partner.ubitec_unidad_ids)
            partner.ubitec_servicio_count = len(partner.ubitec_servicio_ids)

    @api.depends("ubitec_ultimo_pago", "ubitec_dia_corte")
    def _compute_proximo_pago(self):
        for partner in self:
            if partner.ubitec_ultimo_pago:
                partner.ubitec_proximo_pago = (
                    partner.ubitec_ultimo_pago + relativedelta(months=1)
                )
            else:
                partner.ubitec_proximo_pago = False

    @api.depends("ubitec_proximo_pago")
    def _compute_estado_pago(self):
        hoy = fields.Date.context_today(self)
        for partner in self:
            if not partner.ubitec_es_cliente or not partner.ubitec_proximo_pago:
                partner.ubitec_estado_pago = "sin_dato"
            elif partner.ubitec_proximo_pago < hoy:
                partner.ubitec_estado_pago = "vencido"
            elif (partner.ubitec_proximo_pago - hoy).days <= 5:
                partner.ubitec_estado_pago = "por_vencer"
            else:
                partner.ubitec_estado_pago = "al_corriente"

    # ─────────────── Tarea programada: estado "Nuevo" 30 días ───────────────

    @api.model
    def _cron_actualizar_estado_nuevo(self):
        """Pasa de 'nuevo' a 'activo' a los clientes con más de 30 días de alta."""
        hoy = fields.Date.context_today(self)
        limite = hoy - relativedelta(days=30)
        nuevos_viejos = self.search(
            [
                ("ubitec_es_cliente", "=", True),
                ("ubitec_estado", "=", "nuevo"),
                ("ubitec_fecha_alta", "<", limite),
            ]
        )
        nuevos_viejos.write({"ubitec_estado": "activo"})
        return True
