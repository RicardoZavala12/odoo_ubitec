import odoo


def migrate(cr, version):
    env = odoo.api.Environment(cr, odoo.SUPERUSER_ID, {"lang": "es_MX"})

    # Odoo arma el remitente de notificaciones (chatter/mail) con el email
    # del partner del usuario que ejecuta la accion, no con el de la
    # compania. Los usuarios de Ubitec tienen su correo como login pero
    # nunca se copio al campo email de su contacto -> sin eso, cualquier
    # accion que notifique (ej. crear factura recurrente) truena.
    logins = [
        "admin.ubitec@ubitec.mx",
        "ventas@ubitec.mx",
        "tecnico@ubitec.mx",
        "soporte@ubitec.mx",
    ]
    users = env["res.users"].search([("login", "in", logins)])
    for user in users:
        if not user.partner_id.email:
            user.partner_id.write({"email": user.login})
