---
name: eventriver-accesos-vault
description: "Todas las credenciales de EventRiver (invitaciones producción) — Supabase, Vercel, admins"
metadata: 
  node_type: memory
  type: reference
  originSessionId: eb02eef8-ae7b-4cdf-9888-8040b31f6d06
  modified: 2026-07-20T18:50:59.662Z
---

# 🔐 ACCESOS — EventRiver (invitaciones digitales, PRODUCCIÓN)

**Ruta local del proyecto:** `/home/dev2salogaash/Documentos/cloude/eventriver/`
**Stack:** Next.js 16 + TypeScript + Tailwind 4 + Prisma 6 + Supabase Postgres + Vercel

## URLs producción
- Home: https://eventriver-psi.vercel.app
- Admin: https://eventriver-psi.vercel.app/admin
- Ej. invitación: /invitacion/briseidy-xv , /invitacion/brisa-briana-xv , /invitacion/matias-babyshower

## Supabase (BD) — proyecto ACTIVO
- **Ref:** `nsdcurchbtbpzwbffaue` · región us-east-1 · cuenta `ricardozavala12` / org DEVOLONAPP
- **DB password:** `2521260015xvfz`
- **Pooler host:** `aws-1-us-east-1.pooler.supabase.com`
- **URL LOCAL (.env, session pooler 5432):**
  `postgresql://postgres.nsdcurchbtbpzwbffaue:2521260015xvfz@aws-1-us-east-1.pooler.supabase.com:5432/postgres`
- **URL VERCEL (transaction pooler 6543):**
  `postgresql://postgres.nsdcurchbtbpzwbffaue:2521260015xvfz@aws-1-us-east-1.pooler.supabase.com:6543/postgres?pgbouncer=true`
- ⚠️ Free tier: se PAUSA sola tras ~1 semana sin uso → panel admin falla con "tenant not found". Revivir: dashboard → Resume project (data intacta, 90 días). Ver [[project_eventriver_supabase_pausa]].

### Supabase VIEJO (pausado, ya no se usa)
- Ref `cvedgiouqobdceyvzfvo`, email `rikyesc1202011@gmail.com`, DB pass `MOLOTOV12fz@1202`. Se pausó; se migró al nuevo.
- OJO: otro proyecto `devolonapp` (ref `tufetlrmvrnjqsksrcqr`) pausado +90 días, YA NO resumible. No confundir.

## Vercel (hosting)
- Usuario `ricardozavala12` · team `team_VvdwiLzuUSqHG9YGUCmz0tVC` · dominio eventriver-psi.vercel.app
- Deploy: `cd eventriver && vercel deploy --prod`
- El código se recuperó del deployment (no había GitHub). **Pendiente: git init + push.**

## Usuarios admin del panel (en BD, bcrypt)
- `superadmin` / `superadmin2026` → todos los eventos
- `adminxv` / `eventriver2026` → gemelas XV
- `adminbby` / `eventriver2026` → baby shower Matías
- `adminbri` / `eventriver2026` → briseidy-xv
- (nuevos admins: `npx tsx prisma/seed.ts`, pass común `eventriver2026`)

## Fallback Postgres LOCAL (si Supabase pausado)
- BD `eventriver_local` en Postgres 17 local, dueño `ricky_dev` / pass `1202`.
  `postgresql://ricky_dev:1202@localhost:5432/eventriver_local` (el superuser `odoo`/`1202` le dio CREATEDB).
- Correr: `cd eventriver && npm run dev` → localhost:3000 (o 3001 si Traccar ocupa 3000).
