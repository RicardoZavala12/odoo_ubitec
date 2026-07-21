---
name: ubitec-m-dulo-gps-service-odoo
description: "Módulo gps_service para agendar servicios de instalación GPS en el Odoo de Ubitec; flujo de estados, fases, cómo probar"
metadata: 
  node_type: memory
  type: project
  originSessionId: eb02eef8-ae7b-4cdf-9888-8040b31f6d06
  modified: 2026-07-21T15:24:58.574Z
---

## Ubitec — Módulo `gps_service` (Odoo 18)

Módulo NUEVO desde cero (el usuario lo decidió así, NO extender fieldservice aunque OCA está instalado) para agendar servicios de instalación de GPS.

### Ubicación / entorno
- Odoo de Ubitec: `/home/dev2salogaash/Imágenes/screenshots/odoo_ubitec/` (proyecto Docker AISLADO, NO es el de salo_gaash).
- Odoo 18 community, contenedores `ubitec-odoo` (web puerto host 8090) y `ubitec-db` (postgres 17, puerto host 5440, user `odoo` pass `odoo_ubitec_pass`). BD: `ubitec`.
- Módulo en `addons/gps_service/`. Rama git: **`feature/gps-service`** (NO main; regla del proyecto).

### Flujo (state machine gps.service)
`draft → assigned → accepted → in_progress → to_validate → done`, con reapertura a `post_service` → vuelve a `assigned`.
Botones: action_assign / action_accept / action_start (graba start_time) / action_finish (graba end_time + duration) / action_validate / action_post_service / action_reopen_assign.
`_check_is_technician`: solo el técnico asignado (o manager) mueve su servicio.

### Modelo
- `gps.service`: name (folio SRV-, secuencia), partner_id, unidad_id (M2o a `ubitec.unidad` — autocompleta imei/serial_number/unit_brand por related), plates (propio del servicio, unidad no lo tiene), location, scheduled_date, technician_id, state, start_time/end_time/duration (compute horas), validated_by/validation_date. Hereda mail.thread.
- 3 grupos: group_gps_technician (solo sus servicios, record rule), group_gps_scheduler (agenda+valida, ve todo), group_gps_manager.

### Cómo instalar/probar
- Instalar: `docker exec ubitec-odoo odoo -d ubitec -i gps_service --stop-after-init --no-http` luego `docker restart ubitec-odoo`.
- Actualizar tras cambios: `-u gps_service` en vez de `-i`.
- Test de flujo: `cat scripts/test_gps_flow.py | docker exec -i ubitec-odoo odoo shell -d ubitec --no-http` (los 8 pasos deben pasar). OJO: en shell `env.user` es OdooBot; asignar el técnico = env.user para que _check_is_technician pase.

### Estado: FASE 1 y FASE 2 COMPLETAS Y PROBADAS (17-jul-2026)
- FASE 1: flujo de estados verificado en UI por el usuario (creó SRV-00003, recorrió todos los estados incl. post-servicio).
- FASE 2: modelo `gps.service.photo` con 6 evidencias (Image con miniatura) por etapa (before: unit/plate/serial/dash_closed; install: install; after: dash_assembled). `action_finish` BLOQUEA si faltan las 6 fotos. Campo computado `photos_complete` + pestaña "Evidencias fotográficas" en el form (kanban con alertas). Fix: `action_reset_draft` limpia datos fantasma (start_time/end_time/validated_by/validation_date). Todo verificado end-to-end vía shell (test_gps_photos.py).
### FASE 2.5 — Fotos guiadas por etapa (20-jul-2026, en rama dev, PROBADA)
Las fotos se guían por el estado del servicio:
- Estado `accepted` → etapa de foto se prellenar a "before" (Antes de instalar). `action_start` BLOQUEA si faltan las 4 fotos before (unit/plate/serial/dash_closed).
- Estado `in_progress` → etapa se prellenar a "install". `action_finish` BLOQUEA si faltan install + after (dash_assembled).
- `gps.service.photo.default_get` prellenar la etapa según `default_service_id` en contexto. `@api.constrains` impide subir foto de etapa que no corresponde al estado (`_STAGES_ALLOWED_BY_STATE`).
- Campo computado `current_stage` en gps.service + avisos dinámicos en el form por etapa.
- Helpers: `_PHOTOS_BY_STAGE`, `_missing_photos_for_stages(stages)`.
- Verificado con `scripts/test_gps_stages.py` (todos los bloqueos y prellenados OK). Commiteado en dev.

- **Pendiente FASE 3:** vistas móviles por rol (kanban técnico "mis servicios", filtro "por validar" del validador), y opcional: ícono/UX móvil para subir fotos desde cámara del cel.

### Credenciales de prueba (ver también [[ACCESOS]])
- `superadmin` / `super123` — TODOS los permisos.
- `tecnico@ubitec.mx` / `oscar123` — **Oscar (técnico). Pass reseteada a oscar123.** Grupos: SOLO `Usuario interno` + `Servicios GPS/Técnico` (se le quitó Ventas/Inventario/Empleados/etc). Ve SOLO sus servicios asignados (record rule). Los permisos de módulos se asignan desde Ajustes→Usuarios (estándar Odoo), NO desde el módulo GPS.
- `admin.ubitec@ubitec.mx` (id 6) — admin real del cliente, con permisos GPS.

### Git (repo remoto GitHub: RicardoZavala12/odoo_ubitec)
Ramas: `main` (existe en remoto), `dev` (local, FALTA pushear a GitHub — la terminal de Claude no tiene auth de git, el usuario debe hacer `git push -u origin dev`). Flujo: codear+probar en dev local → merge a dev → luego a main/prod. Todo el código de fotos-por-etapa está committeado en dev local.

### Gotcha resuelto: módulo no aparecía en grilla
NO era caché: era que el usuario logueado (`admin.ubitec`) no tenía los grupos del módulo → menú (requiere group_gps_technician) invisible + error de acceso. Solución: asignar grupos. La app SÍ aparece; acción directa `http://localhost:8090/odoo/action-708`.

**Why:** Ubitec (rastreo satelital) necesita gestionar instalaciones de GPS con técnicos en campo.
**How to apply:** Confirmar antes de codear fases nuevas. Técnico usa Odoo desde el cel (web responsive). No tocar core Odoo, todo en el módulo.
