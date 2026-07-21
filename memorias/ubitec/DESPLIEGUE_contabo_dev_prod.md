---
name: ubitec-despliegue-contabo-dev-prod-reglas
description: "Cómo está desplegado Odoo Ubitec en Contabo con entornos dev/prod separados, scripts, reglas críticas y troubleshooting"
metadata: 
  node_type: memory
  type: project
  originSessionId: eb02eef8-ae7b-4cdf-9888-8040b31f6d06
  modified: 2026-07-21T16:26:06.563Z
---

# 🚀 Despliegue Odoo Ubitec en Contabo (dev + prod)

Migrado desde Hetzner (204.168.157.138, que se cayó/daba problemas) al VPS Contabo `194.238.29.167` — el MISMO server de Traccar. Fecha: 20-jul-2026.

## ⚠️⚠️ REGLA DE ORO: TRACCAR NO SE TOCA
Traccar (contenedor `Controldetrafico`, puerto 8082) corre en el mismo VPS. NUNCA tocarlo. Todo lo de Odoo usa contenedores `ubitec-*`, puertos y volúmenes SEPARADOS. Verificar `curl localhost:8082` da HTTP 200 antes y después de cualquier operación. SSH root del VPS: ver [[ACCESOS]] y [[traccar/ACCESOS]] (pass `mtyTRACCAR@120201#11.25#09`).

## Arquitectura: 2 stacks Docker, SOLO UNO PRENDIDO A LA VEZ
Comparten 3.8GB RAM con Traccar (por eso nunca los dos juntos). Hay swap 4GB de colchón (creado en el VPS, permanente en /etc/fstab, swappiness=10).

| | PROD | DEV |
|---|---|---|
| compose | docker-compose.prod.yml | docker-compose.dev.yml |
| contenedores | ubitec-prod-odoo, ubitec-prod-db | ubitec-dev-odoo, ubitec-dev-db |
| puerto web | 8090 | 8091 |
| puerto db | 5440 | 5441 |
| project name | -p ubitec-prod | -p ubitec-dev |
| rama git | main | dev |

- **URL PROD:** http://194.238.29.167:8090 · **URL DEV:** http://194.238.29.167:8091
- Proyecto en Contabo: `/root/odoo_ubitec/` (addons, config, composes, scripts, ubitec.dump).
- ⚠️ Contabo tiene `docker-compose` **v1.29** (con guion), NO el plugin `docker compose`. Composes en formato `version: "3.3"`, project name con `-p`. NO usar campo `name:` top-level (v1 lo rechaza).

## Scripts (en /root/odoo_ubitec/scripts/, cada uno apaga el otro stack → nunca corren juntos)
- `bash scripts/up-dev.sh` → apaga prod, prende dev (:8091), checkout dev.
- `bash scripts/up-prod.sh` → apaga dev, prende prod (:8090), checkout main.
- `bash scripts/promote.sh` → "PR a prod": merge dev→main, apaga dev, prende prod, actualiza gps_service.

## Flujo de trabajo (lo que pidió el usuario)
Trabajar en DEV (:8091) → validar → `promote.sh` para pasar cambios a PROD (:8090). Nunca dev y prod prendidos juntos (recursos + Traccar).

## Restaurar BD en un stack (dev o prod)
Cada stack tiene su BD separada (volúmenes distintos). Para clonar datos de prod a dev, restaurar el dump:
```
docker stop ubitec-dev-odoo   # liberar conexiones
docker exec ubitec-dev-db psql -U odoo -d postgres -c 'DROP DATABASE IF EXISTS ubitec;'
docker exec ubitec-dev-db psql -U odoo -d postgres -c 'CREATE DATABASE ubitec OWNER odoo;'
cat /root/odoo_ubitec/ubitec.dump | docker exec -i ubitec-dev-db pg_restore -U odoo -d ubitec --no-owner --role=odoo
docker start ubitec-dev-odoo
```
OJO: restaurar SOBRE una BD que ya tiene datos deja todo inconsistente (errores + conteos raros). SIEMPRE DROP + CREATE limpio antes.

## 🐛 FIX CRÍTICO: "se queda Cargando" / muestra el gestor de BD
El dump NO trae el filestore (los archivos físicos de attachments/assets). Al restaurar en otro server, los bundles de assets (JS/CSS) apuntan a archivos que no existen → páginas se quedan "Cargando" para siempre, y a veces sale el "Gestionar bases de datos" en vez del login. Solución (2 partes):
1. **Login/gestor BD:** en `config/odoo.conf` agregar `db_name = ubitec` y `list_db = False` (el dbfilter solo no basta al entrar por IP). Reiniciar odoo.
2. **Cargando infinito:** borrar los assets rotos para que Odoo los regenere:
   `docker exec <db> psql -U odoo -d ubitec -c "DELETE FROM ir_attachment WHERE res_model='ir.ui.view' AND name LIKE 'web.assets%' OR url LIKE '/web/assets/%';"` + reiniciar odoo. La primera carga de cada módulo tarda (recompila ese asset), luego instantáneo.

## Git en Contabo (deploy con pull) — configurado 21-jul-2026
- Repo GitHub: `RicardoZavala12/odoo_ubitec` (PRIVADO, cuenta PERSONAL del usuario, NO la del trabajo dev2-sg).
- **Cuentas GitHub del usuario en su PC:** `~/.ssh/github_ricardo` → RicardoZavala12 (personal, la del repo); `~/.ssh/id_ed25519` → RoyDevVi; `gh` CLI logueado como dev2-sg (trabajo, NO tiene acceso al repo personal).
  - Para pushear desde la PC: remote del proyecto local usa SSH `git@github-ricardo:RicardoZavala12/odoo_ubitec.git` (host `github-ricardo` en ~/.ssh/config → llave github_ricardo). NO usar HTTPS (pide user/pass).
- **Contabo accede al repo privado con DEPLOY KEY:** llave `/root/.ssh/ubitec_deploy` (generada en el VPS), su pública agregada en GitHub → Settings → Deploy keys ("Contabo (solo lectura)"). ~/.ssh/config del VPS mapea github.com → esa llave. Autentica como `RicardoZavala12/odoo_ubitec`.
- **Repo en Contabo:** `/root/odoo_ubitec/` es git init + remote origin (SSH) + rama dev trackeando origin/dev. El `ubitec.dump` NO está en git (se preserva aparte).
- **FLUJO para traer cambios a Contabo:** en la PC `git push origin dev` → en Contabo `cd /root/odoo_ubitec && git fetch && git checkout dev && git pull` → `bash scripts/up-dev.sh` + `docker exec ubitec-dev-odoo odoo -d ubitec -u gps_service --stop-after-init --no-http` + restart. (La primera vez hubo choque rsync-vs-git; se resolvió con `git checkout -f -b dev origin/dev`).

## Gotcha SSH
fail2ban activo: muchas conexiones SSH seguidas pueden dar timeout temporal ("banner exchange timed out"). Reintentar con pausa de ~20s.

## Estado 20-jul-2026
- PROD (:8090): datos completos (1099 unidades, 410 clientes, gps_service installed), login OK (superadmin/super123), módulo GPS abre bien. Actualmente DORMIDO (se apagó al levantar dev).
- DEV (:8091): CORRIENDO con datos clonados de prod (410 clientes, 433 partners, gps_service). Login OK. Restaurado limpio (DROP+CREATE, 0 errores).
- Regla aprendida: al restaurar dev, SIEMPRE parar odoo + DROP DATABASE + CREATE antes del pg_restore (si no, queda inconsistente: pasó con 41 partners / 9 clientes por restaurar sobre BD con datos).
- Pendiente: cancelar Hetzner cuando el usuario confirme.

Relacionado: [[ACCESOS]], [[project_ubitec_gps_service]], [[traccar/ACCESOS]].
