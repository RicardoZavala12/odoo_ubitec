---
name: vps-traccar-credenciales-y-acceso-contabo
description: "Credenciales rescatadas del VPS de Traccar (194.238.29.167 Contabo), estado de acceso SSH y cómo recuperarlo"
metadata: 
  node_type: memory
  type: reference
  originSessionId: eb02eef8-ae7b-4cdf-9888-8040b31f6d06
  modified: 2026-07-20T18:46:31.271Z
---

## VPS Traccar — Contabo (194.238.29.167 = vmi2462265.contaboserver.net)

**Customer ID Contabo:** 13727344 · Panel: https://my.contabo.com · Email cuenta: carlockventas@gmail.com

### Credenciales rescatadas
- **SSH root:** `mtyTRACCAR@120201#11.25#09` ✅ VERIFICADA 20-jul-2026 (conecta OK). Estaba en la USB: `KINGSTON/screenshots/media/tonrk/memory/sesion-seguridad-y-local-feb2026.md`. Conexión: `sshpass -p 'mtyTRACCAR@120201#11.25#09' ssh -o PreferredAuthentications=password -o PubkeyAuthentication=no root@194.238.29.167` (puerto 22 estándar).
- **PostgreSQL `traccaruser`:** `Ftrk@Pg2026!Xm9vL`
- **PostgreSQL `postgres` (superuser):** `Ftrk@PgRoot2026!Qw7`
- **pgAdmin (Docker):** email carlockventas@gmail.com, pass anterior `tinta4204` (no accesible desde internet por firewall)
- **Traccar Admin web:** email traccarjuan@gmail.com, pass "la que tú tenías" (no la tocamos)
- **VNC Contabo:** pass `AvRt0406` (IP:puerto VNC 209.145.54.193:63113) — entra SIN pasar por SSH.

### Estado verificado (20-jul-2026) — ACCESO RECUPERADO ✅
Entré por SSH con la contraseña de arriba. Todo corriendo:
- Docker: `Controldetrafico` (Traccar), `whatsapp` (:2900), `postgresql_postgresql_database_1` (:5432), `postgresql_pgadmin_1` (:9999) — todos UP.
- Traccar web local (8082) → HTTP 200.
- ufw activo + fail2ban bloqueando bots SSH. La IP del usuario NO está bloqueada (por eso entró). Disco 13% usado, sano.
- NOTA: el server se había reiniciado (uptime ~44 min) — por eso los primeros pings/puertos daban cerrado; ya normal.
- Contraseñas que FALLARON (no usar): `FullgpsYKtl0qJj01m0A16dkav4pAv`, `jezsE2-jiqbuf-wopqyn`, y las 3 llaves locales.

### Otras notas de la USB (KINGSTON/screenshots/media/tonrk/)
Ahí está TODO el contexto perdido del Traccar: `memory/` (7 .md incl. manual-completo-fulltrack.md, vps-emergencia-seguridad-respaldo.md), `vps-backup/` (código + GUIA-SOLUCION-COMPLETA.md), `traccar/`, `traccar-web/`. Traccar local: BD `traccar_mty`, user `ricky_dev`/`1202`, puerto Teltonika 5027.

**Why:** El usuario perdió acceso SSH al VPS de Traccar y necesita recuperarlo. Regla suya: en prod solo lectura/seguridad, nunca cambios sin consultar.
**How to apply:** No hacer cambios en prod sin confirmar. Ver [[MEMORY]] regla VPS.
