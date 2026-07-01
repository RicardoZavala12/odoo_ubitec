# -*- coding: utf-8 -*-
from odoo import fields, models


class UbitecUnidad(models.Model):
    _name = "ubitec.unidad"
    _description = "Unidad / Equipo GPS de un cliente Ubitec"
    _rec_name = "imei"

    partner_id = fields.Many2one(
        "res.partner", string="Cliente", ondelete="cascade", index=True
    )
    imei = fields.Char(string="IMEI", index=True)
    folio = fields.Char(string="Folio", index=True)
    numero_serie = fields.Char(string="Número de serie")
    marca = fields.Char(string="Marca / Modelo")
    unidad = fields.Char(
        string="Unidad / Vehículo",
        help="Vehículo donde está instalado el GPS (ej. Freightliner blanco).",
    )
    plataforma = fields.Char(string="Plataforma")
    sim = fields.Char(string="SIM / Línea")
    icc = fields.Char(string="ICC")
    fecha_activacion = fields.Date(string="Fecha de activación")
    esquema = fields.Selection(
        selection=[
            ("venta", "Venta"),
            ("comodato", "Comodato"),
            ("migracion", "Migración"),
            ("otro", "Otro"),
        ],
        string="Esquema",
    )
    costo = fields.Float(string="Costo")
    forma_pago = fields.Char(string="Forma de pago")
    fecha_llegada = fields.Date(string="Fecha de llegada")
    fecha_instalacion = fields.Date(string="Fecha de instalación")
    estado = fields.Selection(
        selection=[
            ("stock", "En stock"),
            ("instalado", "Instalado"),
            ("baja", "Dado de baja"),
        ],
        string="Estado",
        default="instalado",
    )
    notas = fields.Text(string="Notas")
