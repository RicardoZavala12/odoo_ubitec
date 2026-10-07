# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request


SERVICE_TYPES = [
    ("installation", "Instalación"),
    ("reinstallation", "Reinstalación"),
    ("deinstallation", "Desinstalación"),
    ("review", "Revisión"),
    ("migration", "Migración"),
]
# Campos de texto simple: se guardan tal cual (vacío -> False).
TEXT_FIELDS = (
    "client_name", "phone", "email", "service_type", "location", "unit_type", "plates", "description",
)


class GpsServiceRequestController(http.Controller):
    """Recepción de solicitudes sin una cuenta de usuario."""

    @http.route("/solicitud-servicio", type="http", auth="public", methods=["GET"], csrf=True)
    def service_request_form(self, **kwargs):
        return request.render("gps_service.service_request_form", {
            "service_types": SERVICE_TYPES, "values": {}, "error": False,
        })

    @http.route("/solicitud-servicio", type="http", auth="public", methods=["POST"], csrf=True)
    def service_request_submit(self, **post):
        values = {field: (post.get(field) or "").strip() for field in TEXT_FIELDS}
        requested_date_raw = (post.get("requested_date") or "").strip()
        unit_count_raw = (post.get("unit_count") or "").strip()
        error = False

        if not values["client_name"] or not values["service_type"]:
            error = "Indica el nombre de quien solicita y el tipo de servicio."
        elif values["service_type"] not in dict(SERVICE_TYPES):
            error = "Selecciona un tipo de servicio válido."

        unit_count = 1
        if not error and unit_count_raw:
            try:
                unit_count = int(unit_count_raw)
                if unit_count < 1:
                    raise ValueError
            except ValueError:
                error = "La cantidad de unidades debe ser un número mayor a 0."

        if not error and values["phone"] and not values["phone"].isdigit():
            error = "El teléfono solo debe contener números."

        if error:
            values["requested_date"] = requested_date_raw
            values["unit_count"] = unit_count_raw
            return request.render("gps_service.service_request_form", {
                "service_types": SERVICE_TYPES, "values": values, "error": error,
            })

        create_vals = dict(values)
        create_vals["unit_count"] = unit_count
        # El input type="date" manda YYYY-MM-DD, formato que el ORM acepta
        # directo para un campo Date; si viene vacío se omite (False).
        if requested_date_raw:
            create_vals["requested_date"] = requested_date_raw

        # sudo() es intencional: el usuario público sin cuenta no tiene permisos
        # de escritura; este create solo acepta los campos del formulario.
        request.env["gps.service.request"].sudo().create(create_vals)
        return request.render("gps_service.service_request_thanks", {})
