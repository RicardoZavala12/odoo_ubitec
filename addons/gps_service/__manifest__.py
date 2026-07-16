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

FASE 1: núcleo del flujo (estados + botones + folio + enlace a unidad).
Las evidencias fotográficas y las vistas por rol llegan en fases posteriores.
    """,
    "version": "18.0.1.0.0",
    "category": "Services/Field Service",
    "author": "Ubitec",
    "license": "LGPL-3",
    "depends": ["base", "mail", "ubitec_clientes"],
    "data": [
        "security/security.xml",
        "security/ir.model.access.csv",
        "data/sequence_data.xml",
        "views/gps_service_views.xml",
        "views/gps_service_menus.xml",
    ],
    "installable": True,
    "application": True,
}
