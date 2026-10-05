# -*- coding: utf-8 -*-
from odoo import fields, models


class UbitecUnidadMovimiento(models.Model):
    _name = "ubitec.unidad.movimiento"
    _description = "Historial de movimientos de un equipo GPS"
    _order = "fecha desc, id desc"

    unidad_id = fields.Many2one(
        "ubitec.unidad", string="Equipo", required=True,
        ondelete="cascade", index=True,
    )
    fecha = fields.Datetime(string="Fecha", default=fields.Datetime.now, required=True)
    tipo = fields.Selection(
        selection=[
            ("entrada", "Entrada a bodega"),
            ("instalado", "Instalado"),
            ("baja", "Dado de baja"),
            ("reactivado", "Reactivado"),
            ("reasignado", "Reasignado a otro cliente"),
        ],
        string="Tipo de movimiento", required=True,
    )
    estado_anterior = fields.Char(string="Estado anterior")
    estado_nuevo = fields.Char(string="Estado nuevo")
    partner_id = fields.Many2one("res.partner", string="Cliente")
    usuario_id = fields.Many2one(
        "res.users", string="Registrado por", default=lambda self: self.env.user,
    )
    nota = fields.Char(string="Nota")
