---
name: eventriver-setup-base-de-datos-local
description: "Cómo correr EventRiver con Postgres local mientras Supabase está pausado; usuarios admin, conexión, fix sessionStorage"
metadata: 
  node_type: memory
  type: project
  originSessionId: eb02eef8-ae7b-4cdf-9888-8040b31f6d06
---

## EventRiver — Base de datos (Supabase NUEVO + fallback local)

### Supabase NUEVO (activo desde 5-jun-2026) — `nsdcurchbtbpzwbffaue`
El Supabase viejo (`cvedgiouqobdceyvzfvo`) se pausó (free tier). Se creó uno NUEVO:
- **Project ref:** `nsdcurchbtbpzwbffaue`
- **DB password:** `2521260015xvfz`
- **Pooler host:** `aws-1-us-east-1.pooler.supabase.com` (detectado probando regiones; la conexión directa `db.xxx.supabase.co` solo va por IPv6 y la red local no la tiene).
- **LOCAL (.env):** `postgresql://postgres.nsdcurchbtbpzwbffaue:2521260015xvfz@aws-1-us-east-1.pooler.supabase.com:5432/postgres` (session pooler 5432).
- **VERCEL (producción):** mismo pero puerto `6543` + `?pgbouncer=true` (transaction pooler).
- Migraciones aplicadas (`prisma migrate deploy`) + seed corrido. RSVP y login admin verificados OK contra Supabase.

### Fallback Postgres local (si Supabase falla)
BD `eventriver_local` en Postgres 17 local, dueño `ricky_dev` (pass `1202`; el superuser `odoo` pass `1202` le dio CREATEDB). URL: `postgresql://ricky_dev:1202@localhost:5432/eventriver_local`.

### Conexión local
- BD: `eventriver_local` en el Postgres 17 local (puerto 5432), dueño `ricky_dev`.
- `.env`: `DATABASE_URL="postgresql://ricky_dev:1202@localhost:5432/eventriver_local"`
- `ricky_dev` (pass `1202`) NO tenía CREATEDB; se lo dio el rol `odoo` (superuser, pass también `1202`). La BD se creó con `CREATE DATABASE eventriver_local OWNER ricky_dev`.
- Tablas creadas con `npx prisma migrate deploy` (3 migraciones: init, add_event_slug, add_admin_users).

### Usuarios admin (creados con `npx tsx prisma/seed.ts`, pass común `eventriver2026`)
- `admin` → `__all__` (super admin, ve todos)
- `adminxv` → brisa-briana-xv
- `adminbby` → matias-babyshower
- `adminbri` → **briseidy-xv** (XV de Briseidy Nicol, agregado en seed.ts)

### Cómo correr
`cd /home/dev2salogaash/Documentos/cloude/eventriver && npm run dev` → http://localhost:3000 (o 3001 si 3000 ocupado por Traccar). Login admin en /admin.

### Fix aplicado
`src/app/admin/invitados/[slug]/page.tsx`: bug original — llamaba `sessionStorage.getItem("admin_slug")` en el cuerpo del componente (crashea en SSR con "sessionStorage is not defined", HTTP 500). Se movió a estado `isSuper` poblado en el `useEffect`.

### Nueva invitación creada: briseidy-xv
XV de Briseidy Nicol Maldonado Olvera, papás Verónica Olvera y Rubén Maldonado, 1 agosto 2026 7PM, Centro Social Norma Eventos Guadalupe NL, dress formal. Tema NUEVO `rosa-palo` (creado en globals.css + types.ts + page.tsx preview). Sin fotos (`photos: []` → sección galería oculta). Reveal.tsx mejorado con zoom-in sutil (scale 0.96→1) para animación de scroll más dinámica.

**Why:** El usuario quería probar todo el sistema local sin esperar a Supabase.
**How to apply:** Cuando reconecte Supabase, solo cambiar `DATABASE_URL` en `.env` (local = session pooler 5432; Vercel = transaction pooler 6543 + pgbouncer) y re-correr migraciones + seed en esa BD. Ver [[project_eventriver_contexto]].
