import odoo


def migrate(cr, version):
    env = odoo.api.Environment(cr, odoo.SUPERUSER_ID, {"lang": "es_MX"})

    # Sin email en la compañia, cualquier accion que intente notificar por
    # el chatter (ej. crear factura recurrente) truena con "configure la
    # direccion de correo electronico del remitente" y revierte todo,
    # incluida la factura. Le ponemos un remitente valido.
    company = env["res.company"].browse(1)
    if company.exists():
        vals = {"email": "admin.ubitec@ubitec.mx"}
        company.write(vals)
        if company.partner_id:
            company.partner_id.write(vals)
