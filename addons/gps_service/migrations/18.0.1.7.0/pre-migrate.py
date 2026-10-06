def migrate(cr, version):
    # photo_type pasa de lista fija (texto) a relacion (gps.service.photo.type).
    # Antes de que el ORM cambie el tipo de columna, guardamos el codigo viejo
    # en una columna temporal para no perder que foto era cada registro.
    cr.execute(
        "ALTER TABLE gps_service_photo ADD COLUMN IF NOT EXISTS photo_type_code_bak VARCHAR"
    )
    cr.execute(
        "UPDATE gps_service_photo SET photo_type_code_bak = photo_type "
        "WHERE photo_type_code_bak IS NULL"
    )
    # Vaciar la columna original: si no, Odoo intenta convertir el texto
    # ("unit") directo a entero al cambiar el tipo de columna y truena.
    # Primero hay que quitar el NOT NULL (el campo es required=True), el
    # ORM lo vuelve a poner solo al terminar de crear el campo Many2one.
    cr.execute("ALTER TABLE gps_service_photo ALTER COLUMN photo_type DROP NOT NULL")
    cr.execute("UPDATE gps_service_photo SET photo_type = NULL")
