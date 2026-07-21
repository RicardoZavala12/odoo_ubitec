---
name: project-eventriver-supabase-pausa
description: EventRiver — la BD Supabase se pausa sola (tier gratis) y rompe el panel de invitados; cómo revivirla
metadata: 
  node_type: memory
  type: project
  originSessionId: d1dbe37a-2752-4c49-a198-a723ba878825
---

**Problema recurrente:** El proyecto Supabase de EventRiver (`eventriver`, ref `nsdcurchbtbpzwbffaue`, región us-east-1, cuenta `ricardozavala12` / org DEVOLONAPP) se **pausa automáticamente** tras ~1 semana de inactividad (Supabase free tier).

**Síntoma:** La invitación pública se ve OK (usa `demo-events.ts`, no BD), pero el **panel de admin de invitados** (`/admin/invitados/<slug>`) sale vacío o falla. La API `/api/guests` devuelve HTTP 500 con `FATAL: (ENOTFOUND) tenant/user postgres.nsdcurchbtbpzwbffaue not found` = BD pausada.

**Solución rápida:** Entrar a supabase.com/dashboard → proyecto `eventriver` → botón **"Resume project"** (NO "Upgrade to Pro"). Revive en ~2-5 min y el panel vuelve solo (data intacta). Se puede resumir dentro de los 90 días de pausado; después solo se baja backup.

**Verificar tras revivir:** `curl "https://eventriver-psi.vercel.app/api/guests?event=<slug>"` debe dar 200 con lista de invitados. Ej. briseidy-xv tenía 16 invitados / 31 personas (14-jul-2026), NO se perdieron.

**Prevención pendiente (no configurado aún):** un cron/ping cada 3 días a la BD para que Supabase no la pause; o Supabase Pro ($25/mes); o migrar la BD al servidor Hetzner. El usuario aún no eligió.

**OJO:** hay OTRO proyecto Supabase pausado llamado `devolonapp` (ref `tufetlrmvrnjqsksrcqr`) pausado +90 días (desde jun-2024) que YA NO se puede resumir — ese NO es el de eventriver, no confundir. Relacionado con [[project_eventriver_contexto]] y [[project_eventriver_local_db]].
