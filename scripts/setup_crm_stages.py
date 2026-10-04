# -*- coding: utf-8 -*-
# Renombra las etapas nativas de crm.lead al ciclo de venta real de Ubitec
# y crea las 2 etapas nuevas que faltan. Correr dentro del contenedor odoo:
#   docker exec <contenedor-odoo> python3 /tmp/setup_crm_stages.py
#
# No se hace via XML de datos porque Odoo protege (noupdate) las etapas
# default del modulo crm contra sobreescritura por otros modulos.

import odoo
from odoo.tools import config

config["db_host"] = "db"
config["db_port"] = "5432"
config["db_user"] = "odoo"
config["db_password"] = "odoo_ubitec_pass"

registry = odoo.registry("ubitec")
with registry.cursor() as cr:
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
            print("Renombrada:", xmlid, "->", nombre)
        else:
            print("ERROR: no se encontro", xmlid)

    nuevas = [("Negociación", 4), ("Instalación agendada", 5)]
    for nombre, seq in nuevas:
        existe = Stage.search([("name", "=", nombre)], limit=1)
        if existe:
            existe.write({"sequence": seq})
            print("Ya existia:", nombre)
        else:
            Stage.create({"name": nombre, "sequence": seq})
            print("Creada:", nombre)

    cr.commit()
    print("--- Etapas finales ---")
    for s in Stage.search([], order="sequence"):
        print(s.sequence, s.name)
