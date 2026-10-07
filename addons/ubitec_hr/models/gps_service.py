# -*- coding: utf-8 -*-
from odoo import api, fields, models


class GpsService(models.Model):
    _inherit = "gps.service"

    technician_on_leave = fields.Boolean(
        string="Técnico de vacaciones",
        compute="_compute_technician_on_leave",
        help="Verdadero si el técnico asignado tiene una ausencia aprobada "
             "que cubre la fecha programada de este servicio.",
    )

    @api.depends("technician_id", "scheduled_date")
    def _compute_technician_on_leave(self):
        for service in self:
            service.technician_on_leave = False
            if not service.technician_id or not service.scheduled_date:
                continue
            employee = self.env["hr.employee"].search(
                [("user_id", "=", service.technician_id.id)], limit=1
            )
            if not employee:
                continue
            conflict = self.env["hr.leave"].search([
                ("employee_id", "=", employee.id),
                ("state", "=", "validate"),
                ("date_from", "<=", service.scheduled_date),
                ("date_to", ">=", service.scheduled_date),
            ], limit=1)
            service.technician_on_leave = bool(conflict)
