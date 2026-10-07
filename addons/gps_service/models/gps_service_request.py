# -*- coding: utf-8 -*-
import datetime

from odoo import fields, models, _
from odoo.exceptions import UserError


class GpsServiceRequest(models.Model):
    """Solicitud pública pendiente de identificación por Soporte."""

    _name = "gps.service.request"
    _description = "Solicitud de servicio GPS"
    _rec_name = "client_name"
    _order = "create_date desc, id desc"

    client_name = fields.Char(string="Nombre de quien solicita", required=True)
    phone = fields.Char(string="Teléfono")
    email = fields.Char(string="Correo electrónico")
    service_type = fields.Selection(
        selection=[
            ("installation", "Instalación"),
            ("reinstallation", "Reinstalación"),
            ("deinstallation", "Desinstalación"),
            ("review", "Revisión"),
            ("migration", "Migración"),
        ],
        string="Tipo de servicio",
        required=True,
    )
    requested_date = fields.Date(string="Fecha deseada del servicio")
    unit_count = fields.Integer(string="Cantidad de unidades", default=1)
    location = fields.Char(string="Ubicación")
    unit_type = fields.Char(string="Tipo de unidad/vehículo")
    plates = fields.Char(string="Placas")
    description = fields.Text(string="¿Qué necesitas?")
    state = fields.Selection(
        [("new", "Nueva"), ("converted", "Convertida")],
        string="Estado", default="new", required=True, readonly=True,
    )
    service_id = fields.Many2one(
        "gps.service", string="Servicio GPS generado", readonly=True, copy=False,
    )

    def action_convert_to_service(self):
        """Crea el borrador para que Soporte complete sus datos."""
        self.ensure_one()
        if self.state == "converted":
            raise UserError(_("Esta solicitud ya fue convertida a un servicio GPS."))
        # Un nombre escrito a mano no identifica de forma fiable al cliente o equipo.
        scheduled_date = (
            datetime.datetime.combine(self.requested_date, datetime.time())
            if self.requested_date else False
        )
        service = self.env["gps.service"].create({
            "service_type": self.service_type,
            "location": self.location,
            "plates": self.plates,
            "scheduled_date": scheduled_date,
            "notes": (
                "Solicitud recibida de: %s\n"
                "Teléfono: %s\n"
                "Correo: %s\n\n"
                "Detalle: %s\n"
                "Tipo de unidad: %s\n"
                "Cantidad de unidades solicitadas: %s"
            ) % (
                self.client_name,
                self.phone or "",
                self.email or "",
                self.description or "",
                self.unit_type or "",
                self.unit_count or 1,
            ),
        })
        self.write({"state": "converted", "service_id": service.id})
        return {
            "type": "ir.actions.act_window",
            "name": _("Servicio de GPS"),
            "res_model": "gps.service",
            "view_mode": "form",
            "res_id": service.id,
            "target": "current",
        }

    def action_view_service(self):
        """Abre el servicio GPS ya generado por esta solicitud."""
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": _("Servicio de GPS"),
            "res_model": "gps.service",
            "view_mode": "form",
            "res_id": self.service_id.id,
            "target": "current",
        }
