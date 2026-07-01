# -*- coding: utf-8 -*-
from odoo import fields, models


class UbitecPago(models.Model):
    _name = "ubitec.pago"
    _description = "Pago de mensualidad de un cliente Ubitec"
    _order = "fecha desc"

    partner_id = fields.Many2one(
        "res.partner", string="Cliente", ondelete="cascade", index=True
    )
    fecha = fields.Date(string="Fecha de pago", default=fields.Date.context_today)
    monto = fields.Float(string="Monto")
    forma_pago = fields.Char(string="Forma de pago")
    referencia = fields.Char(string="Referencia")
    notas = fields.Text(string="Notas")
