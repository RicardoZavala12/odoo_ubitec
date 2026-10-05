import odoo


def migrate(cr, version):
    env = odoo.api.Environment(cr, odoo.SUPERUSER_ID, {"lang": "es_MX"})

    # El usuario de pruebas del tecnico (tecnico@ubitec.mx) no estaba en
    # ningun grupo del modulo -> no podia ni ver el menu "Servicios GPS".
    tecnico = env["res.users"].search([("login", "=", "tecnico@ubitec.mx")], limit=1)
    grupo_tecnico = env.ref("gps_service.group_gps_technician", raise_if_not_found=False)
    if tecnico and grupo_tecnico and grupo_tecnico not in tecnico.groups_id:
        tecnico.write({"groups_id": [(4, grupo_tecnico.id)]})
