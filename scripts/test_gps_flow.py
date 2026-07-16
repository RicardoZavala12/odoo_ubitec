# Prueba del flujo de gps.service — se corre con: odoo shell -d ubitec
# Crea un servicio y lo avanza por todos los estados verificando cada paso.

env = env  # noqa (inyectado por odoo shell)

Service = env["gps.service"]

# buscar un cliente cualquiera para la prueba
partner = env["res.partner"].search([], limit=1)
print("Cliente de prueba:", partner.name)

# 1. crear (debe asignar folio SRV-)
svc = Service.create({
    "partner_id": partner.id,
    "plates": "ABC-1234",
    "location": "Bodega centro",
})
print("1. Creado:", svc.name, "| estado:", svc.state)
assert svc.name.startswith("SRV-"), "El folio no se generó"
assert svc.state == "draft"

# 2. asignar técnico = el usuario actual del entorno (así _check_is_technician pasa)
tech = env.user
print("   Técnico asignado (env.user):", tech.name)
svc.technician_id = tech.id
svc.action_assign()
print("2. Asignado -> estado:", svc.state)
assert svc.state == "assigned"

# 3. aceptar
svc.action_accept()
print("3. Aceptado -> estado:", svc.state)
assert svc.state == "accepted"

# 4. iniciar (marca start_time)
svc.action_start()
print("4. Iniciado -> estado:", svc.state, "| inicio:", svc.start_time)
assert svc.state == "in_progress"
assert svc.start_time

# 5. finalizar (marca end_time + duración)
svc.action_finish()
print("5. Finalizado -> estado:", svc.state, "| fin:", svc.end_time, "| duración(h):", svc.duration)
assert svc.state == "to_validate"
assert svc.end_time

# 6. validar
svc.action_validate()
print("6. Validado -> estado:", svc.state, "| validado por:", svc.validated_by.name)
assert svc.state == "done"
assert svc.validated_by == env.user

# 7. post-servicio
svc.action_post_service()
print("7. Post-servicio -> estado:", svc.state)
assert svc.state == "post_service"

# 8. reabrir/reasignar
svc.action_reopen_assign()
print("8. Reabierto -> estado:", svc.state)
assert svc.state == "assigned"

print("\n>>> TODOS LOS PASOS DEL FLUJO PASARON <<<")
# limpiar la prueba
svc.unlink()
print("Servicio de prueba eliminado.")
env.cr.commit()
