import odoo


def migrate(cr, version):
    env = odoo.api.Environment(cr, odoo.SUPERUSER_ID, {"lang": "es_MX"})

    # El menu de Facturacion quedo oculto (active=False) durante la limpieza
    # del punto 2 (CRM). Lo reactivamos: sin el, no se puede navegar a los
    # contratos/suscripciones del punto 3.
    menu_finance = env.ref("account.menu_finance", raise_if_not_found=False)
    if menu_finance:
        menu_finance.write({"active": True})
