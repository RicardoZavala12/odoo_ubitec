import odoo


def migrate(cr, version):
    env = odoo.api.Environment(cr, odoo.SUPERUSER_ID, {})

    # Recupera el codigo viejo guardado en pre-migrate y lo convierte al
    # nuevo Many2one (gps.service.photo.type), usando el catalogo que ya
    # se cargo en este mismo -u (data/photo_types.xml).
    tipos = env["gps.service.photo.type"].search([])
    code_to_id = {t.code: t.id for t in tipos}

    cr.execute(
        "SELECT id, photo_type_code_bak FROM gps_service_photo "
        "WHERE photo_type_code_bak IS NOT NULL"
    )
    for photo_id, code in cr.fetchall():
        tipo_id = code_to_id.get(code)
        if tipo_id:
            env["gps.service.photo"].browse(photo_id).write({"photo_type": tipo_id})

    cr.execute("ALTER TABLE gps_service_photo DROP COLUMN IF EXISTS photo_type_code_bak")
