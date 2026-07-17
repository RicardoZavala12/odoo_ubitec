# -*- coding: utf-8 -*-
from odoo import fields, models


class GpsServicePhoto(models.Model):
    """Evidencia fotográfica de un servicio de GPS.

    Las 6 fotos obligatorias se organizan por etapa:
      - before  (antes de instalar): unidad, placa, serie, tablero cerrado
      - install (durante):           evidencia de instalación
      - after   (al terminar):       tablero armado
    Cada foto se guarda como Binary con attachment=True (se ve en miniatura
    en el formulario) — mismo patrón que las evidencias de garantía.
    """

    _name = "gps.service.photo"
    _description = "Evidencia fotográfica de servicio GPS"
    _order = "service_id, sequence, id"

    service_id = fields.Many2one(
        "gps.service",
        string="Servicio",
        required=True,
        ondelete="cascade",
        index=True,
    )
    # Tipo de foto: define cuál de las 6 evidencias es
    photo_type = fields.Selection(
        selection=[
            ("unit", "Unidad"),
            ("plate", "Placa"),
            ("serial", "Número de serie"),
            ("dash_closed", "Tablero cerrado"),
            ("install", "Evidencia de instalación"),
            ("dash_assembled", "Tablero armado"),
        ],
        string="Tipo de evidencia",
        required=True,
    )
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
    image = fields.Image(
        string="Foto",
        max_width=1920,
        max_height=1920,
        required=True,
    )
    note = fields.Char(string="Nota")
