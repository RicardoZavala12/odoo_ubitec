# -*- coding: utf-8 -*-
# Migracion 18.0.2.1.0: renombra las etapas nativas de crm.lead al ciclo
# de venta real de Ubitec (punto 2.1 del alcance) y crea las 2 que faltan.
#
# Se hace via migracion (no via data XML) porque Odoo protege las etapas
# default del modulo crm contra sobreescritura (noupdate). Odoo corre esto
# solo una vez, automaticamente, al detectar el cambio de version con -u,
# en cualquier ambiente (local, prod, dev, qa) sin correr nada a mano.

import odoo


def migrate(cr, version):
    env = odoo.api.Environment(cr, odoo.SUPERUSER_ID, {"lang": "es_MX"})
    Stage = env["crm.stage"]

    renombres = [
        ("crm.stage_lead1", "Prospecto", 1),
        ("crm.stage_lead2", "Contactado", 2),
        ("crm.stage_lead3", "Cotización enviada", 3),
        ("crm.stage_lead4", "Cliente activo", 6),
    ]
    for xmlid, nombre, seq in renombres:
        stage = env.ref(xmlid, raise_if_not_found=False)
        if stage:
            stage.write({"name": nombre, "sequence": seq})

    nuevas = [("Negociación", 4), ("Instalación agendada", 5)]
    for nombre, seq in nuevas:
        existe = Stage.search([("name", "=", nombre)], limit=1)
        if existe:
            existe.write({"sequence": seq})
        else:
            Stage.create({"name": nombre, "sequence": seq})

    # Ocultar boton "Generar leads" (funcion de pago IAP, no se usa en Ubitec)
    accion = env.ref("crm_iap_mine.crm_iap_lead_mining_request_action", raise_if_not_found=False)
    if accion:
        accion.write({"binding_view_types": False})

    # Ocultar menu "Leads" (Ubitec trabaja directo en Oportunidades/Pipeline)
    env["res.config.settings"].new({"group_use_lead": False}).execute()

    # El toggle de arriba no siempre saca a usuarios ya agregados directo al
    # grupo (por ejemplo, admin.ubitec quedo miembro desde la carga inicial).
    # Forzamos que el grupo quede sin ningun miembro.
    grupo_leads = env.ref("crm.group_use_lead", raise_if_not_found=False)
    if grupo_leads:
        grupo_leads.write({"users": [(5, 0, 0)]})

    # Ocultar menus que Ubitec no usa: Mis actividades, Mis cotizaciones, Reportes
    menus_a_ocultar = [
        "crm.crm_lead_menu_my_activities",
        "sale_crm.sale_order_menu_quotations_crm",
        "crm.crm_menu_report",
    ]
    for xmlid in menus_a_ocultar:
        menu = env.ref(xmlid, raise_if_not_found=False)
        if menu:
            menu.write({"active": False})
