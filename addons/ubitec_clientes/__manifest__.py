# -*- coding: utf-8 -*-
{
    "name": "Ubitec - Clientes",
    "summary": "Campos a la medida para clientes de Ubitec (rastreo satelital)",
    "description": """
Agrega a la ficha del cliente (res.partner) los datos comerciales propios de
Ubitec: esquema (Venta/Comodato/etc), unidades, costos, plan/mensualidad,
registro de pagos, estado (Nuevo/Activo/Inactivo automático), servicios
adicionales, unidades+IMEI e historial de servicios.
    """,
    "version": "18.0.3.7.0",
    "category": "Sales/CRM",
    "author": "Ubitec",
    "license": "LGPL-3",
    "depends": ["base", "contacts", "mail", "web", "crm", "contract", "contract_line_successor", "base_geolocalize"],
    "data": [
        "security/ir.model.access.csv",
        "data/cron.xml",
        "data/product_monitoreo.xml",
        "views/res_partner_views.xml",
        "views/ubitec_unidad_views.xml",
        "views/mail_activity_templates.xml",
        "views/login_layout.xml",
        "views/crm_lead_views.xml",
        "reports/crm_lead_reports.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "ubitec_clientes/static/src/password_toggle/password_toggle.js",
            "ubitec_clientes/static/src/password_toggle/password_toggle.xml",
        ],
    },
    "installable": True,
    "application": False,
}
