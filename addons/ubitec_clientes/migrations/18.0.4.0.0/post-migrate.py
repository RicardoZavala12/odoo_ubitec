import odoo


def migrate(cr, version):
    env = odoo.api.Environment(cr, odoo.SUPERUSER_ID, {"lang": "es_MX"})

    # Snapshot inicial: el historial de movimientos arranca de hoy, los
    # equipos ya existentes no tienen como reconstruirse hacia atras. Se dar
    # un primer renglon con su estado actual para que la bitacora no quede
    # vacia, dejando claro que es un punto de partida, no historia real.
    estado_label = dict(env["ubitec.unidad"]._fields["estado"].selection)
    unidades = env["ubitec.unidad"].search([])
    vals_list = [
        {
            "unidad_id": unidad.id,
            "tipo": "entrada" if unidad.estado != "baja" else "baja",
            "estado_nuevo": estado_label.get(unidad.estado, unidad.estado),
            "partner_id": unidad.partner_id.id,
            "nota": "Snapshot inicial (antes de esta fecha no hay historial)",
        }
        for unidad in unidades
    ]
    if vals_list:
        env["ubitec.unidad.movimiento"].create(vals_list)
