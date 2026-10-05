# -*- coding: utf-8 -*-
# Migracion 18.0.3.1.0:
# - Corrige los datos de la empresa (seguia como "My Company", sin pais/estado)
# - Traduce y adapta al espanol la plantilla de correo que se manda al crear
#   un contrato de monitoreo (venia en ingles con marca generica "My Company")

import odoo


def migrate(cr, version):
    env = odoo.api.Environment(cr, odoo.SUPERUSER_ID, {"lang": "es_MX"})

    # 1) Datos de la empresa
    company = env["res.company"].browse(1)
    mexico = env.ref("base.mx", raise_if_not_found=False)
    nuevo_leon = env["res.country.state"].search([("name", "=", "Nuevo León")], limit=1)
    if company.exists():
        company.write({"name": "UBITEC"})
        if company.partner_id:
            vals_partner = {"name": "UBITEC", "city": "Monterrey"}
            if mexico:
                vals_partner["country_id"] = mexico.id
            if nuevo_leon:
                vals_partner["state_id"] = nuevo_leon.id
            company.partner_id.write(vals_partner)

    # 2) Plantilla de correo de contrato creado -- en espanol
    template = env.ref("contract.email_contract_template", raise_if_not_found=False)
    if template:
        template = template.with_context(lang="es_MX")
        template.write({
            "subject": "UBITEC - Confirmación de tu servicio de monitoreo ({{ object.name }})",
            "body_html": """
<div>
    <p>Hola <t t-out="object.partner_id.name"/>,</p>
    <p>Te confirmamos que tu contrato de monitoreo con <strong>UBITEC</strong> ya quedó registrado:</p>
    <ul>
        <li><strong>Contrato:</strong> <t t-out="object.name"/></li>
        <li><strong>Fecha de inicio:</strong> <t t-out="object.date_start"/></li>
        <li><strong>Tu contacto:</strong> <t t-out="object.user_id.name or ''"/></li>
    </ul>
    <p>Cualquier duda, con gusto te apoyamos.</p>
    <p>Gracias por confiar en UBITEC.</p>
</div>
""",
        })
