---
name: l-eme-primero-montar-todo-en-otra-pc
description: "Guía maestra para clonar y levantar TODOS los proyectos en una PC nueva, con repos, llaves SSH y credenciales"
metadata: 
  node_type: memory
  type: reference
  originSessionId: eb02eef8-ae7b-4cdf-9888-8040b31f6d06
  modified: 2026-07-31T08:25:35.971Z
---

# 🖥️ LÉEME PRIMERO — Montar todo en una PC nueva

Guía maestra. Todos los repos son **privados** de la cuenta personal **RicardoZavala12** en GitHub.
Las credenciales completas de cada proyecto están en las subcarpetas (traccar/, ubitec/, eventriver/, dates/, otros/).

---

## 📦 LOS 3 REPOSITORIOS (GitHub, privados, cuenta RicardoZavala12)

| Proyecto | Repo | Rama principal | Qué es |
|----------|------|----------------|--------|
| **Odoo Ubitec** | `git@github-ricardo:RicardoZavala12/odoo_ubitec.git` | `dev` (trabajo), `main` (prod) | Módulo gps_service (servicios GPS, fotos, Telegram) + toda la memoria/contexto en `memorias/` |
| **EventRiver** (invitaciones) | `git@github-ricardo:RicardoZavala12/invitacion_digital.git` | `main` | Next.js + Prisma + Supabase |
| **Traccar local** | `git@github-ricardo:RicardoZavala12/traccar-local.git` | `main` | Instalación compilada de Traccar (302M) |

> La memoria/contexto de TODO vive DENTRO de `odoo_ubitec/memorias/` (además de la USB).

---

## 🔑 PASO 1 — Configurar acceso a GitHub (SSH) en la PC nueva

Las cuentas GitHub del usuario (por si hay que recrear las llaves):
- `~/.ssh/github_ricardo` → **RicardoZavala12** (PERSONAL, dueña de los 3 repos). ESTA es la que se usa.
- `~/.ssh/id_ed25519` → RoyDevVi (otra cuenta, no se usa para estos repos)
- `gh` CLI está logueado como `dev2-sg` (cuenta del TRABAJO, NO tiene acceso a los repos personales)

### Generar llave nueva y conectar:
```bash
ssh-keygen -t ed25519 -C "pc-nueva" -f ~/.ssh/github_ricardo -N ""
cat ~/.ssh/github_ricardo.pub    # copiar y agregar en https://github.com/settings/keys
# configurar el host SSH:
cat >> ~/.ssh/config <<'EOF'
Host github-ricardo
    HostName github.com
    User git
    IdentityFile ~/.ssh/github_ricardo
    IdentitiesOnly yes
EOF
ssh -T git@github-ricardo   # debe decir "Hi RicardoZavala12!"
```

---

## 📥 PASO 2 — Clonar los repos
```bash
git clone git@github-ricardo:RicardoZavala12/odoo_ubitec.git
git clone git@github-ricardo:RicardoZavala12/invitacion_digital.git eventriver
git clone git@github-ricardo:RicardoZavala12/traccar-local.git
```

---

## 🚀 PASO 3 — Levantar cada proyecto

### ODOO UBITEC (local dev) — Docker
```bash
cd odoo_ubitec && git checkout dev
docker compose -p ubitec-dev -f docker-compose.dev.yml up -d   # (o docker-compose con guion)
docker exec ubitec-dev-db psql -U odoo -d postgres -c 'CREATE DATABASE ubitec OWNER odoo;'
cat backup/ubitec.dump | docker exec -i ubitec-dev-db pg_restore -U odoo -d ubitec --no-owner --role=odoo
# si se queda "Cargando": borrar assets rotos y reiniciar (ver ubitec/CONTABO_guia_completa.md)
```
→ http://localhost:8091 · usuarios en `memorias/ubitec/ACCESOS.md`

### EVENTRIVER — Node.js
```bash
cd eventriver && npm install && npx prisma generate && npm run dev
```
→ http://localhost:3000 · el `.env` viene en el repo · credenciales en `memorias/eventriver/ACCESOS.md`

### TRACCAR — ya está en PRODUCCIÓN (VPS Contabo), no se monta local
Ver `memorias/traccar/ACCESOS.md` y `memorias/ubitec/CONTABO_guia_completa.md`.

---

## 🌐 SERVIDORES EN PRODUCCIÓN (ya vivos, NO se montan)
| Servicio | Dónde | Accesos |
|----------|-------|---------|
| Traccar | VPS Contabo `194.238.29.167` | traccar/ACCESOS.md (SSH root / `mtyTRACCAR@120201#11.25#09`) |
| Odoo Ubitec prod/dev | Contabo `:8090` / `:8091` | ubitec/CONTABO_guia_completa.md |
| EventRiver | Vercel (eventriver-psi.vercel.app) | eventriver/ACCESOS.md |

⚠️ TRACCAR = solo lectura/seguridad, NUNCA tocar.

---

## 🔐 RESUMEN RÁPIDO DE CREDENCIALES (detalle en cada ACCESOS.md)
- **Contabo SSH:** root / `mtyTRACCAR@120201#11.25#09` — IP 194.238.29.167
- **Odoo Ubitec web:** superadmin / `super123` · tecnico@ubitec.mx / `oscar123`
- **Supabase EventRiver:** DB pass `2521260015xvfz` (proyecto nsdcurchbtbpzwbffaue)
- **Postgres Odoo (Contabo):** user odoo / `odoo_ubitec_pass`
- **Telegram bot GPS:** token en ubitec/telegram_notificaciones.md, grupo "Ubitec Servicios"

---

## 📋 ESTADO DE LOS PROYECTOS (al 31-jul-2026)
- **gps_service (Odoo):** Fase 1 (flujo), Fase 2 (fotos), Fase 2.5 (fotos por etapa), Telegram → TODO en rama `dev` (mergeado y probado en dev de Contabo).
- **Facturación CONTPAQi:** pendiente que el cliente dé la API de timbrado (CONTPAQi Timbra). Ver ubitec/facturacion_contpaqi_requisitos.md.
- **Pendiente Fase 3:** vistas móviles del técnico.
- Ver investigaciones recientes en otros/investigaciones_jul2026.md.
