# -*- coding: utf-8 -*-
from odoo import models, _
from odoo.exceptions import UserError


class HrLeave(models.Model):
    _inherit = "hr.leave"

    def action_approve(self, check_state=True):
        for leave in self:
            leave._check_pending_gps_services()
        return super().action_approve(check_state=check_state)

    def _check_pending_gps_services(self):
        self.ensure_one()
        user = self.employee_id.user_id
        if not user:
            return
        pending = self.env["gps.service"].search([
            ("technician_id", "=", user.id),
            ("state", "!=", "done"),
            ("scheduled_date", ">=", self.date_from),
            ("scheduled_date", "<=", self.date_to),
        ])
        if pending:
            raise UserError(_(
                "No puedes aprobar estas vacaciones: %(employee)s tiene "
                "servicio(s) GPS agendado(s) en esas fechas (%(folios)s). "
                "Reasigna o reprograma esos servicios antes de aprobar."
            ) % {
                "employee": self.employee_id.name,
                "folios": ", ".join(pending.mapped("name")),
            })
