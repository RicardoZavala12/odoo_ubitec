# -*- coding: utf-8 -*-
from odoo import fields, models


class UbitecServicio(models.Model):
    _name = "ubitec.servicio"
    _description = "Servicio realizado a un cliente Ubitec (historial)"
    _order = "fecha desc"

    partner_id = fields.Many2one(
        "res.partner", string="Cliente", ondelete="cascade", index=True
    )
    fecha = fields.Date(string="Fecha")
    tipo = fields.Selection(
        selection=[
            ("instalacion", "Instalación"),
            ("desinstalacion", "Desinstalación"),
            ("reinstalacion", "Reinstalación"),
            ("revision", "Revisión"),
            ("cambio_gps", "Cambio de GPS"),
            ("migracion", "Migración"),
            ("configuracion", "Configuración"),
            ("otro", "Otro"),
        ],
        string="Tipo de servicio",
    )
    unidad_id = fields.Many2one("ubitec.unidad", string="Unidad / Equipo")
    unidad_texto = fields.Char(string="Unidad (texto)")
    tecnico = fields.Char(string="Técnico")
    domicilio = fields.Char(string="Domicilio")
    reporte = fields.Text(string="Reporte / Motivo")
    notas = fields.Text(string="Notas adicionales")
