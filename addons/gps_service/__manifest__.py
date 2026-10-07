# -*- coding: utf-8 -*-
{
    "name": "GPS Service - Agenda e Instalación",
    "summary": "Agendar servicios de GPS, asignar técnicos y seguir el flujo de "
    "instalación (aceptar, iniciar, finalizar, validar).",
    "description": """
Módulo a la medida de Ubitec para gestionar servicios de instalación de GPS:

- Quien agenda captura cliente, unidad, placas y ubicación, y asigna un técnico.
- El técnico ve sus servicios asignados y avanza el flujo:
  Aceptar → Iniciar (en sitio) → Finalizar.
- Quien valida revisa el servicio finalizado y lo aprueba, con opción de
  reabrir en Post-servicio si se requiere reatender.

Incluye evidencias fotográficas obligatorias por etapa (6 fotos: antes de
instalar, instalación y al terminar) que bloquean avanzar el flujo si faltan,
y permisos por rol (Técnico / Agenda-Validación / Administrador) con reglas
de registro: el técnico solo ve sus propios servicios asignados.
    """,
    "version": "18.0.1.12.1",
    "category": "Services/Field Service",
    "author": "Ubitec",
    "license": "LGPL-3",
    "depends": ["base", "mail", "ubitec_clientes"],
    "data": [
        "security/security.xml",
        "security/ir.model.access.csv",
        "data/sequence_data.xml",
        "data/telegram_config.xml",
        "data/photo_types.xml",
        "views/gps_service_views.xml",
        "views/gps_service_menus.xml",
        "views/res_config_settings_views.xml",
        "views/gps_service_request_templates.xml",
        "views/gps_service_request_views.xml",
    ],
    "installable": True,
    "application": True,
}
