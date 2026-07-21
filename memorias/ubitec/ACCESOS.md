---
name: ubitec-accesos-vault
description: "Credenciales del Odoo de Ubitec (usuarios, BD Postgres, Docker) y del módulo gps_service"
metadata: 
  node_type: memory
  type: reference
  originSessionId: eb02eef8-ae7b-4cdf-9888-8040b31f6d06
  modified: 2026-07-20T20:15:39.350Z
---

# 🔐 ACCESOS — Ubitec (Odoo 18, rastreo satelital)

**Ruta proyecto local:** `/home/dev2salogaash/Imágenes/screenshots/odoo_ubitec/` (Docker, dev local)
**Web local:** http://localhost:8090 · **Ramas git:** `dev` (trabajo) y `main` (prod)

## 🚀 PRODUCCIÓN — migrado a Contabo (20-jul-2026)
El Hetzner (204.168.157.138) se cayó/dio problemas → se migró Odoo Ubitec al VPS de Contabo (194.238.29.167, el mismo de Traccar). ⚠️ TRACCAR NO SE TOCA — usa contenedores/puertos aparte, verificado intacto en toda la migración.
- **Odoo PROD:** `http://194.238.29.167:8090` (mismos usuarios: superadmin/super123, tecnico@ubitec.mx/tecnico123).
- **Proyecto en Contabo:** `/root/odoo_ubitec/` (SSH root, ver [[traccar/ACCESOS]] pass `mtyTRACCAR@120201#11.25#09`).
- **2 stacks Docker, NUNCA juntos** (comparten 3.8GB RAM con Traccar; hay swap 4GB de colchón):
  - PROD: `docker-compose.prod.yml` → contenedores `ubitec-prod-*`, puertos 8090/5440.
  - DEV: `docker-compose.dev.yml` → `ubitec-dev-*`, puertos 8091/5441.
  - Contabo tiene `docker-compose` v1.29 (con guion), NO el plugin. Composes en formato version:"3.3", nombre con `-p ubitec-prod`.
- **Scripts** en `scripts/`: `up-dev.sh` (prende dev, apaga prod), `up-prod.sh` (viceversa), `promote.sh` (merge dev→main + prende prod + actualiza gps_service). Cada uno hace `down` del otro → nunca corren los dos.
- **Flujo:** trabajar en dev (:8091) → `promote.sh` para pasar a prod (:8090).
- BD restaurada del dump local (1099 unidades, 410 clientes, gps_service installed). Dump en `/root/odoo_ubitec/ubitec.dump`.
- Firewall Contabo: puerto 8090 abierto (regla agregada, sin tocar Traccar).
- OJO fail2ban: muchas conexiones SSH seguidas pueden dar timeout temporal — reintentar con pausa.

## Docker / infra
- Contenedores: `ubitec-odoo` (web, host 8090 → 8069), `ubitec-db` (Postgres 17, host **5440** → 5432)
- **Postgres:** user `odoo` / pass `odoo_ubitec_pass` · BD `ubitec`
- `dbfilter = ^ubitec$` · addons: `/mnt/extra-addons` + OCA (oca_field_service, oca_contract, oca_helpdesk, oca_web)

## Usuarios Odoo (contraseñas reseteadas por Claude 17-jul-2026)
- **`superadmin` / `super123`** → TODOS los permisos (clon del admin del sistema). Creado a pedido del usuario, para quien él designe.
- `admin` (id 2) / `admin123` → admin del sistema.
- `admin.ubitec@ubitec.mx` (id 6) → el admin real del cliente (Administrador Ubitec). Se le dieron permisos GPS.
- `tecnico@ubitec.mx` / `tecnico123` → Oscar (técnico).
- `ventas@ubitec.mx` → Jose Luis Oliva (comercial). Con grupo GPS.
- `soporte@ubitec.mx` → Magali (soporte/oficina).

## Comandos útiles
- Instalar módulo: `docker exec ubitec-odoo odoo -d ubitec -i gps_service --stop-after-init --no-http` + `docker restart ubitec-odoo`
- Actualizar: `-u gps_service` en vez de `-i`
- Shell: `docker exec -i ubitec-odoo odoo shell -d ubitec --no-http`
- Acción directa del módulo GPS: `http://localhost:8090/odoo/action-708`

## Módulo gps_service (ver [[project_ubitec_gps_service]])
Fase 1 (flujo de estados) y Fase 2 (6 fotos evidencia obligatorias) COMPLETAS y probadas. Pendiente Fase 3 (vistas móviles).

## Regla del usuario
JAMÁS inventar/inyectar datos demo o falsos en las BD de Ubitec. Solo datos reales de sus archivos. Ver [[feedback_ubitec_jamas_inventar_data]].
