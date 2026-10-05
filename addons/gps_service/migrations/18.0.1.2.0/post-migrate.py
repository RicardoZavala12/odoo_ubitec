import odoo


def migrate(cr, version):
    env = odoo.api.Environment(cr, odoo.SUPERUSER_ID, {})

    # Antes de este cambio, Telegram se enviaba siempre que hubiera token y
    # chat_id configurados (sin un check explicito). Para no apagar algo que
    # ya estaba funcionando, el nuevo check "activo" arranca en True ya que
    # hoy hay credenciales reales cargadas.
    icp = env["ir.config_parameter"].sudo()
    if icp.get_param("gps_service.telegram_enabled") in (False, None, ""):
        icp.set_param("gps_service.telegram_enabled", "True")
