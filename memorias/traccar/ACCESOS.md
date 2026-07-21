---
name: traccar-accesos-vault
description: "Todas las credenciales y accesos del VPS Traccar (SSH, BD, paneles, VNC)"
metadata: 
  node_type: memory
  type: reference
  originSessionId: eb02eef8-ae7b-4cdf-9888-8040b31f6d06
  modified: 2026-07-20T18:50:26.126Z
---

# 🔐 ACCESOS — VPS Traccar (FullTrack GPS)

> ⚠️ PRODUCCIÓN. Regla del usuario: solo lectura/seguridad, NUNCA cambios sin consultar. NO ejecutar comandos GitHub.

## Servidor (Contabo)
- **IP:** 194.238.29.167 (= vmi2462265.contaboserver.net)
- **Customer ID Contabo:** 13727344
- **Panel Contabo:** https://my.contabo.com · email cuenta: `carlockventas@gmail.com` (pass del panel NO guardada — usar "Forgot password" al correo)
- **VNC:** IP:puerto `209.145.54.193:63113` · pass `AvRt0406` (entra SIN SSH)

## SSH ✅ VERIFICADO 20-jul-2026
- **Usuario:** `root`
- **Contraseña:** `mtyTRACCAR@120201#11.25#09`
- **Puerto:** 22 (estándar)
- **Comando:** `sshpass -p 'mtyTRACCAR@120201#11.25#09' ssh -o PreferredAuthentications=password -o PubkeyAuthentication=no root@194.238.29.167`
- ❌ NO usar (contraseñas viejas que fallan): `FullgpsYKtl0qJj01m0A16dkav4pAv`, `jezsE2-jiqbuf-wopqyn`, ni las llaves locales.

## PostgreSQL (en el VPS, Docker)
- **traccaruser:** `Ftrk@Pg2026!Xm9vL`
- **postgres (superuser):** `Ftrk@PgRoot2026!Qw7`
- Puerto 5432 (contenedor `postgresql_postgresql_database_1`)

## pgAdmin (Docker, puerto 9999)
- email `carlockventas@gmail.com` · pass anterior `tinta4204` (no accesible desde internet por firewall)

## Traccar Admin (web, puerto 8082)
- email `traccarjuan@gmail.com` · pass "la que tenía el usuario" (no la tocamos, hasheada en BD)

## Traccar LOCAL (dev, la compu del usuario)
- BD `traccar_mty`, user `ricky_dev` / pass `1202`, web puerto 8082, Teltonika puerto 5027.

## Seguridad
- ufw + fail2ban ACTIVOS (bloquean bots SSH tras 3 intentos). La IP del usuario NO se bloquea (confirmado).
- `masterchecker` BLOQUEADO (locked + nologin). IP atacante `199.33.71.66`.

## Backup / contexto completo
En la USB KINGSTON: `screenshots/media/tonrk/` → `memory/` (manual-completo-fulltrack.md, vps-emergencia-seguridad-respaldo.md, sesion-seguridad-y-local-feb2026.md), `vps-backup/` (código + guías), `traccar/`, `traccar-web/`.
