# -*- coding: utf-8 -*-
from datetime import datetime, timedelta

import pytz

from odoo import api, fields, models
from odoo.tools import html_escape


class ContractLine(models.Model):
    _inherit = "contract.line"

    ubitec_unidad_id = fields.Many2one(
        "ubitec.unidad", string="Equipo GPS", index=True
    )

    @api.model
    def _ubitec_destinatario_alertas(self):
        return self.env["res.users"].search(
            [("login", "=", "admin.ubitec@ubitec.mx")], limit=1
        )

    @api.model
    def _ubitec_hoy_mexico(self):
        # No usamos fields.Date.context_today() porque el cron corre con el
        # usuario OdooBot, que no tiene zona horaria configurada (cae a UTC).
        # UBITEC opera en hora de Mexico, asi que fijamos la zona explicita.
        tz = pytz.timezone("America/Mexico_City")
        return datetime.now(pytz.utc).astimezone(tz).date()

    @api.model
    def _cron_alerta_cobros(self, dias_adelante, titulo):
        hoy = self._ubitec_hoy_mexico()
        hasta = hoy + timedelta(days=dias_adelante)
        lineas = self.search(
            [
                ("ubitec_unidad_id", "!=", False),
                ("is_canceled", "=", False),
                ("recurring_next_date", ">=", hoy),
                ("recurring_next_date", "<=", hasta),
            ]
        )
        self._enviar_alerta_cobros(lineas, titulo)

    @api.model
    def _enviar_alerta_cobros(self, lineas, titulo):
        hoy = self._ubitec_hoy_mexico()
        if not lineas:
            return

        destinatario = self._ubitec_destinatario_alertas()
        if not destinatario:
            return

        por_cliente = {}
        for linea in lineas:
            partner = linea.contract_id.partner_id
            por_cliente.setdefault(partner, self.env["contract.line"])
            por_cliente[partner] |= linea

        model_res_partner = self.env.ref("base.model_res_partner").id
        activity_todo = self.env.ref("mail.mail_activity_data_todo").id
        filas_html = []
        for partner, lineas_cliente in por_cliente.items():
            detalle = ", ".join(
                "%s ($%.2f, vence %s)"
                % (
                    l.ubitec_unidad_id.imei or l.ubitec_unidad_id.folio or l.ubitec_unidad_id.id,
                    l.specific_price,
                    l.recurring_next_date,
                )
                for l in lineas_cliente
            )
            self.env["mail.activity"].create(
                {
                    "res_model_id": model_res_partner,
                    "res_id": partner.id,
                    "activity_type_id": activity_todo,
                    "summary": titulo,
                    "note": "Vence(n): %s" % detalle,
                    "date_deadline": hoy,
                    "user_id": destinatario.id,
                }
            )
            filas_html.append(
                "<li><strong>%s</strong>: %s</li>"
                % (html_escape(partner.name or ""), html_escape(detalle))
            )

        cuerpo = "<p>%s</p><ul>%s</ul>" % (html_escape(titulo), "".join(filas_html))
        self.env["mail.mail"].create(
            {
                "subject": "UBITEC - %s" % titulo,
                "body_html": cuerpo,
                "email_to": destinatario.email or destinatario.login,
            }
        ).send()

    @api.model
    def cron_alerta_cobros_hoy(self):
        self._cron_alerta_cobros(0, "Cobros que vencen HOY")

    @api.model
    def cron_alerta_cobros_semana(self):
        self._cron_alerta_cobros(6, "Cobros que vencen esta semana")
