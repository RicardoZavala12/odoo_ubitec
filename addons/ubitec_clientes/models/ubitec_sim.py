# -*- coding: utf-8 -*-
from odoo import fields, models


class UbitecSim(models.Model):
    _name = "ubitec.sim"
    _description = "SIM / Línea de datos de un equipo GPS"
    _rec_name = "sim_card"

    sim_card = fields.Char(string="SIM Card", index=True)
    linea = fields.Char(string="Línea")
    icc = fields.Char(string="ICC")
    imsi = fields.Char(string="IMSI")
    cuenta = fields.Char(string="Cuenta")
    operador = fields.Selection(
        selection=[("telcel", "Telcel"), ("claro", "Claro"), ("otro", "Otro")],
        string="Operador",
    )
    plan = fields.Char(string="Plan")
    estado = fields.Char(string="Estado")
    peticion = fields.Char(string="Petición")
    fecha_activacion = fields.Date(string="Fecha de activación")
    partner_id = fields.Many2one("res.partner", string="Cliente")
    unidad_id = fields.Many2one("ubitec.unidad", string="Equipo GPS")
    notas = fields.Text(string="Notas")
