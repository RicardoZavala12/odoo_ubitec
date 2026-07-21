# Memoria Principal — Índice de proyectos

## ⚠️ REGLAS CRÍTICAS DEL USUARIO
- **JAMÁS INVENTAR DATA** — nunca inyectar datos demo/falsos en BD del usuario, solo data real de sus archivos (ver [ubitec/feedback_ubitec_jamas_inventar_data.md](ubitec/feedback_ubitec_jamas_inventar_data.md))
- **NUNCA hacer cambios en producción (VPS Traccar 194.238.29.167)** — solo lectura/seguridad
- **NUNCA hacer cambios automáticos** — siempre consultar antes de modificar cualquier archivo
- **NO ejecutar comandos de GitHub** (push, PR, etc.) sin pedirlo
- El usuario habla en español, informal, usa mayúsculas cuando se frustra — tenerle paciencia y ser directo

---

## 📁 ESTRUCTURA — memoria organizada por proyecto
Los contextos están en subcarpetas. Cada una tiene un **`ACCESOS.md`** (vault con TODAS las credenciales: SSH, BD, paneles) + archivos de contexto.

**Ruta base del directorio de memorias:**
`/home/dev2salogaash/.claude/projects/-home-dev2salogaash/memory/`

### 🛰️ [traccar/](traccar/) — VPS Traccar / FullTrack GPS (PRODUCCIÓN)
- **[traccar/ACCESOS.md](traccar/ACCESOS.md)** — 🔐 SSH (`root` / `mtyTRACCAR@120201#11.25#09` ✅), Postgres, pgAdmin, VNC, Contabo, Traccar admin
- [traccar/vps_traccar_credenciales_seguridad.md](traccar/vps_traccar_credenciales_seguridad.md) — estado del server, seguridad, notas
- Backup completo en USB KINGSTON: `screenshots/media/tonrk/` (memory/, vps-backup/, traccar/, traccar-web/)

### 📡 [ubitec/](ubitec/) — Odoo 18 Ubitec (rastreo satelital)
- **[ubitec/ACCESOS.md](ubitec/ACCESOS.md)** — 🔐 usuarios Odoo (`superadmin`/`super123`, `tecnico@ubitec.mx`/`tecnico123`…), Postgres, Docker
- **[ubitec/DESPLIEGUE_contabo_dev_prod.md](ubitec/DESPLIEGUE_contabo_dev_prod.md)** — 🚀 Odoo en Contabo con dev/prod separados, scripts, reglas (Traccar NO se toca), fix "se queda cargando"
- [ubitec/project_ubitec_gps_service.md](ubitec/project_ubitec_gps_service.md) — módulo gps_service (Fase 1+2 listas, Fase 3 pendiente)
- [ubitec/feedback_ubitec_jamas_inventar_data.md](ubitec/feedback_ubitec_jamas_inventar_data.md) — regla: nunca inventar datos

### 💌 [eventriver/](eventriver/) — Invitaciones digitales (PRODUCCIÓN, en Vercel)
- **[eventriver/ACCESOS.md](eventriver/ACCESOS.md)** — 🔐 Supabase (BD pass `2521260015xvfz`), Vercel, admins del panel
- [eventriver/project_eventriver_contexto.md](eventriver/project_eventriver_contexto.md) — stack, arquitectura, eventos
- [eventriver/project_eventriver_local_db.md](eventriver/project_eventriver_local_db.md) — correr con Postgres local
- [eventriver/project_eventriver_supabase_pausa.md](eventriver/project_eventriver_supabase_pausa.md) — BD se pausa sola; revivir con Resume project

### 🗓️ [dates/](dates/) — MVP viejo de invitaciones (multi-tenant, sprint abril 2026)
- Contexto del MVP: visión multi-tenant, catálogo, sesiones 8-9 abril, reglas de super admin. (Proyecto distinto a EventRiver.)

### 📦 [otros/](otros/)
- [otros/proyecto_cotizacion_israel_sorteo.md](otros/proyecto_cotizacion_israel_sorteo.md) — cotización plataforma sorteo Tierra Santa + plantilla

---

## 🎨 Catálogo de estilos custom (Traccar web)
### "glass-dark" — Glassmorphism iOS
- Bg `rgba(15-20,15-20,20-25,0.55)` dark · `backdrop-filter: blur(32px) saturate(180%)` · border `1px solid rgba(255,255,255,0.08-0.12)` · radius 12-20px. Aplicado a sidebar, BottomMenu, StatusCard, LoginLayout.
### "glass-scroll" — scrollbar sutil
- Ancho 6px · thumb `rgba(255,255,255,0.15)` · track transparent · radius 3px. Global en styles.css y DeviceList.jsx.
