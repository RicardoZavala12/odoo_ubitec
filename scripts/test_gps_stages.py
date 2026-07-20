# Prueba fotos guiadas por etapa — odoo shell -d ubitec
import io, base64
from PIL import Image

env = env  # noqa
Service = env["gps.service"]
Photo = env["gps.service.photo"]
partner = env["res.partner"].search([("is_company", "=", True)], limit=1)

_buf = io.BytesIO()
Image.new("RGB", (10, 10), (100, 100, 200)).save(_buf, format="PNG")
IMG = base64.b64encode(_buf.getvalue())

def add_photo(svc, ptype, stage):
    return Photo.with_context(default_service_id=svc.id).create({
        "service_id": svc.id, "photo_type": ptype, "stage": stage, "image": IMG,
    })

svc = Service.create({"partner_id": partner.id, "plates": "STG-1"})
tech = env.user
svc.technician_id = tech.id
svc.action_assign()
svc.action_accept()
print("Estado:", svc.state, "| current_stage esperado 'before':", svc.current_stage)

# 1. intentar INICIAR sin fotos de 'antes' -> debe bloquear
try:
    svc.action_start(); print("ERROR: dejó iniciar sin fotos before")
except Exception as e:
    print("OK bloqueó iniciar sin 'antes' ->", str(e)[:60])

# 2. intentar subir foto de etapa equivocada (install) estando en accepted -> bloquea
try:
    add_photo(svc, "install", "install"); print("ERROR: dejó subir install en accepted")
except Exception as e:
    print("OK bloqueó foto de etapa equivocada ->", str(e)[:60])

# 3. subir las 4 de 'antes'
for pt in ["unit", "plate", "serial", "dash_closed"]:
    add_photo(svc, pt, "before")
print("Fotos 'antes' subidas. default_get etapa en accepted:",
      Photo.with_context(default_service_id=svc.id).default_get(['stage']).get('stage'))

# 4. ahora SÍ iniciar
svc.action_start()
print("OK inició. Estado:", svc.state, "| current_stage esperado 'install':", svc.current_stage)

# 5. intentar FINALIZAR sin install/after -> bloquea
try:
    svc.action_finish(); print("ERROR: dejó finalizar sin install/after")
except Exception as e:
    print("OK bloqueó finalizar sin install/after ->", str(e)[:60])

# 6. subir install + after (ambas válidas en in_progress)
add_photo(svc, "install", "install")
add_photo(svc, "dash_assembled", "after")
print("default_get etapa en in_progress:",
      Photo.with_context(default_service_id=svc.id).default_get(['stage']).get('stage'))

# 7. finalizar
svc.action_finish()
print("OK finalizó. Estado:", svc.state)
assert svc.state == "to_validate"

print("\n>>> TODO OK: fotos guiadas por etapa + validaciones funcionan <<<")
svc.unlink()
env.cr.commit()
print("limpio.")
