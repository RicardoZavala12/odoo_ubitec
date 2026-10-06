# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError


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
    service_state = fields.Selection(
        related="service_id.state",
        string="Estado del servicio",
    )
    # Tipo de foto: cual de las evidencias es. Relacion real al catalogo
    # gps.service.photo.type (en vez de lista fija) para que el campo se
    # filtre en automatico segun la Etapa elegida (domain reactivo).
    photo_type = fields.Many2one(
        "gps.service.photo.type",
        string="Tipo de evidencia",
        required=True,
        domain="[('stage', '=', stage)]",
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

    # ------------------------------------------------------------------
    # Etapa guiada por el estado del servicio
    # ------------------------------------------------------------------
    # Etapas permitidas según el estado del servicio padre. Al finalizar el
    # técnico puede subir tanto "install" como "after" en el estado in_progress.
    _STAGES_ALLOWED_BY_STATE = {
        "accepted": ["before"],
        "in_progress": ["install", "after"],
    }

    @api.model
    def default_get(self, fields_list):
        """Prellenar la ETAPA según el estado del servicio al abrir el form.

        - Servicio Aceptado → etapa 'Antes de instalar'.
        - Servicio En sitio → etapa 'Instalación' (el técnico puede cambiar
          a 'Al terminar', ambas válidas en ese estado).
        """
        res = super().default_get(fields_list)
        service_id = self.env.context.get("default_service_id")
        if service_id:
            service = self.env["gps.service"].browse(service_id)
            if service.state == "accepted":
                res["stage"] = "before"
            elif service.state == "in_progress":
                res["stage"] = "install"
        return res

    @api.constrains("stage", "service_id")
    def _check_stage_matches_state(self):
        """Impedir subir una foto de una etapa que no corresponde al estado."""
        for photo in self:
            service = photo.service_id
            allowed = self._STAGES_ALLOWED_BY_STATE.get(service.state)
            # Si el servicio ya está más avanzado (to_validate/done) no
            # restringimos (permite corregir), solo bloqueamos en el flujo activo.
            if allowed is not None and photo.stage not in allowed:
                labels = dict(self._fields["stage"].selection)
                permitidas = ", ".join(labels[s] for s in allowed)
                raise UserError(_(
                    "En este momento solo puedes subir fotos de la etapa: %s.\n"
                    "La etapa '%s' no corresponde al estado actual del servicio."
                ) % (permitidas, labels.get(photo.stage, photo.stage)))
