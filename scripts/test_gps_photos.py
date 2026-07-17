# Prueba Fase 2 (fotos) — odoo shell -d ubitec
# Verifica que action_finish bloquea sin las 6 fotos y pasa con ellas.
import base64
import io
from PIL import Image

env = env  # noqa

Service = env["gps.service"]
Photo = env["gps.service.photo"]
partner = env["res.partner"].search([("is_company", "=", True)], limit=1)

# imagen válida de 10x10 generada con PIL
_buf = io.BytesIO()
Image.new("RGB", (10, 10), (120, 60, 200)).save(_buf, format="PNG")
PNG = _buf.getvalue()

svc = Service.create({"partner_id": partner.id, "plates": "TEST-999"})
tech = env.user
svc.technician_id = tech.id
svc.action_assign()
svc.action_accept()
svc.action_start()
print("Estado antes de finalizar:", svc.state)

# 1. intentar finalizar SIN fotos -> debe fallar
try:
    svc.action_finish()
    print("ERROR: dejó finalizar sin fotos (no debería)")
except Exception as e:
    print("OK bloqueó sin fotos ->", str(e)[:70])

# 2. subir las 6 fotos
tipos = [
    ("unit", "before"), ("plate", "before"), ("serial", "before"),
    ("dash_closed", "before"), ("install", "install"), ("dash_assembled", "after"),
]
for pt, stg in tipos:
    Photo.create({
        "service_id": svc.id, "photo_type": pt, "stage": stg,
        "image": base64.b64encode(PNG),
    })
svc.invalidate_recordset()
print("photos_complete tras subir 6:", svc.photos_complete)

# 3. finalizar CON fotos -> debe pasar
svc.action_finish()
print("Estado tras finalizar con fotos:", svc.state)
assert svc.state == "to_validate", "no pasó a validar"

# 4. probar reset_draft limpia datos fantasma
svc.action_validate()
svc.action_reset_draft()
svc.invalidate_recordset()
print("Tras reset_draft -> state:", svc.state, "| start:", svc.start_time,
      "| validated_by:", svc.validated_by.id)
assert svc.state == "draft" and not svc.start_time and not svc.validated_by, \
    "reset_draft no limpió los datos fantasma"

print("\n>>> FASE 2 OK: bloqueo de fotos + reset limpio funcionan <<<")
svc.unlink()
env.cr.commit()
print("Servicio de prueba eliminado.")
