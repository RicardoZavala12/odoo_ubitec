# -*- coding: utf-8 -*-
from odoo import fields, models


class GpsServicePhotoType(models.Model):
    """Catálogo de tipos de evidencia fotográfica, cada uno ligado a su etapa.

    Reemplaza la lista fija (Selection) de photo_type: al ser una relación
    real, el campo "Tipo de evidencia" del formulario se filtra en automático
    según la Etapa elegida (domain reactivo), en vez de depender de un
    cálculo de Python que Odoo solo evalúa al cargar la pantalla.
    """

    _name = "gps.service.photo.type"
    _description = "Tipo de evidencia fotográfica (catálogo)"
    _order = "sequence, id"

    name = fields.Char(string="Nombre", required=True)
    code = fields.Char(string="Código", required=True)
    stage = fields.Selection(
        selection=[
            ("before", "Antes de instalar"),
            ("install", "Instalación"),
            ("after", "Al terminar"),
        ],
        string="Etapa",
        required=True,
    )
    sequence = fields.Integer(string="Orden", default=10)
