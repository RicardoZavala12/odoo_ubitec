---
name: EventRiver - Contexto completo del proyecto
description: Plataforma de invitaciones digitales premium - stack, credenciales, arquitectura, deploy, estado actual
type: project
originSessionId: 9174ba55-fbc0-4a7a-9c7a-cca81d42b59d
---
## EventRiver — Invitaciones digitales premium

**Ruta local:** `/home/dev2salogaash/Documentos/cloude/eventriver/`
**Manual completo:** `/home/dev2salogaash/Documentos/cloude/eventriver/MANUAL.md`

> ♻️ **Código recuperado 5-jun-2026** desde el deployment de producción de Vercel (no había GitHub). Vercel guardaba el source completo en `src/` del deployment `dpl_CaL8ZQEsKZrUV9xcyuqGTNrsjJq5`. Se bajó vía API de Vercel (`/v7/deployments/{id}/files/{uid}`, devuelve base64), 62 archivos, incluyendo imágenes reales y mp3. `npm install` + `npm run dev` arranca OK en localhost (Next 16.2.3 Turbopack); la BD Supabase sigue viva y renderiza datos reales. Cuenta Vercel: usuario `ricardozavala12`, team `team_VvdwiLzuUSqHG9YGUCmz0tVC`. **NO hay repo Git aún — falta hacer `git init` + push para evitar otra pérdida.**

### URLs producción
- Home: https://eventriver-psi.vercel.app
- XV Gemelas: https://eventriver-psi.vercel.app/invitacion/brisa-briana-xv
- Baby Shower Matías: https://eventriver-psi.vercel.app/invitacion/matias-babyshower
- Admin: https://eventriver-psi.vercel.app/admin

### Credenciales admin (en DB, bcrypt)
- `superadmin` / `superadmin2026` → ve todos los eventos
- `adminxv` / `eventriver2026` → solo gemelas XV
- `adminbby` / `eventriver2026` → solo baby shower

### Servicios
- **Vercel:** eventriver-psi.vercel.app (free tier, deploy con `vercel deploy --prod`)
- **Supabase:** project `cvedgiouqobdceyvzfvo`, email rikyesc1202011@gmail.com
- **DB password:** MOLOTOV12fz@1202
- **Pooler URL (producción):** `postgresql://postgres.cvedgiouqobdceyvzfvo:MOLOTOV12fz%401202@aws-1-us-west-2.pooler.supabase.com:6543/postgres?pgbouncer=true`
- **Direct URL (local):** `postgresql://postgres:MOLOTOV12fz%401202@db.cvedgiouqobdceyvzfvo.supabase.co:5432/postgres`

### Stack
Next.js 16 (App Router) + TypeScript + Tailwind 4 + Framer Motion + Prisma 6 + Supabase Postgres + Vercel

### Eventos activos
1. **brisa-briana-xv** — XV Años gemelas Brisa & Briana Mercado, mamá Erika, Platinum Eventos Guadalupe NL, 24 abril 2026, tema pastel-xv, música Photograph Ed Sheeran (minuto 1:10), parallax con fotos reales, lluvia de sobres
2. **matias-babyshower** — Baby Shower Matías Abdiel, papás Paco y Aide, Salón PETIT Iztapalapa CDMX, 9 mayo 2026, tema sunshine con sol animado CSS, música Here Comes The Sun Beatles, mesa de regalos Liverpool

### Funcionalidades clave
- RSVP con QR único por invitado (detecta duplicados)
- Descarga PNG de tarjeta con nombre + personas + QR (html2canvas)
- Panel admin por usuario (auth contra DB con bcrypt)
- Scanner QR con cámara del cel (html5-qrcode)
- Asignación de mesas (texto libre)
- Al escanear muestra nombre + personas + mesa
- Campo `active` en eventos para activar/desactivar invitaciones
- Invitados separados por evento (campo event_slug)
- 6 temas CSS: pastel-xv, midnight-gold, rose-cream, heaven-blue, candy-pop, sunshine

### Comandos frecuentes
- Deploy: `cd eventriver && vercel deploy --prod`
- Vaciar invitados: `PGPASSWORD='MOLOTOV12fz@1202' psql -h db.cvedgiouqobdceyvzfvo.supabase.co -U postgres -d postgres -c "DELETE FROM guests WHERE event_slug='slug';"`
- Crear admin: ver MANUAL.md sección "Cómo agregar un nuevo evento"

**Why:** Proyecto vendible de invitaciones digitales. El usuario cobra por invitación y lo administra desde el panel.
**How to apply:** Siempre consultar antes de modificar archivos. Nunca tocar invitaciones de otros clientes al editar una. Deploy siempre a Vercel después de cambios.
