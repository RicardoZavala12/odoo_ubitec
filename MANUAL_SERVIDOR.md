# MANUAL DEL SERVIDOR — Odoo UBITEC (Hetzner)

Manual de operación: cómo conectarse al servidor, levantar/parar Odoo,
restaurar la BD, y la estructura del proyecto.

---

## 1. DATOS DEL SERVIDOR

| Dato | Valor |
|------|-------|
| Proveedor | Hetzner Cloud (proyecto `ubitec`) |
| Servidor | `ubitec-odoo` (CX23, 4 GB RAM, 40 GB SSD) |
| Ubicación | Helsinki |
| **IP pública** | **204.168.157.138** |
| Usuario SSH | `root` |
| Llave SSH (privada) | `~/.ssh/ubitec_hetzner` (en la PC de desarrollo) |
| **URL Odoo** | **http://204.168.157.138:8090** |
| Costo | ~€4-5/mes (lo paga el cliente vía contrato) |

### Credenciales Odoo
| Rol | Usuario | Contraseña |
|-----|---------|------------|
| Administrador | `admin.ubitec@ubitec.mx` | `Ubitec.Admin#2026` |
| Comercial | `ventas@ubitec.mx` | `Ubitec.Ventas#2026` |
| Técnico | `tecnico@ubitec.mx` | `Ubitec.Tecnico#2026` |
| Soporte | `soporte@ubitec.mx` | `Ubitec.Soporte#2026` |

> Contraseña maestra de Odoo (crear/borrar BD): `ubitec_admin_2026` (en config/odoo.conf)
> BD Postgres: base `ubitec`, user `odoo`, pass `odoo_ubitec_pass`

---

## 2. CÓMO CONECTARSE AL SERVIDOR (SSH)

Desde la PC de desarrollo (que tiene la llave):

```bash
ssh -i ~/.ssh/ubitec_hetzner root@204.168.157.138
```

Si te conectas desde OTRA PC, primero necesitas copiar la llave privada
`~/.ssh/ubitec_hetzner` a esa PC (o generar una nueva y agregarla en el panel de Hetzner).

Una vez dentro, el proyecto vive en:
```bash
cd /root/odoo_ubitec
```

---

## 3. ESTRUCTURA DEL PROYECTO

```
/root/odoo_ubitec/                  (en el servidor; mismo repo que en GitHub)
├── docker-compose.yml              # define los 2 contenedores (odoo + postgres)
├── config/
│   └── odoo.conf                   # config de Odoo (dbfilter, addons_path, passwords)
├── addons/                         # módulos
│   ├── ubitec_clientes/            # MÓDULO CUSTOM (clientes, equipos, sims, pagos, servicios)
│   ├── oca_contract/               # OCA: suscripciones/contratos
│   ├── oca_field_service/          # OCA: field service
│   ├── oca_helpdesk/               # OCA: helpdesk
│   └── oca_web/                    # OCA: web_responsive (menú con iconos)
├── backup/
│   └── ubitec.dump                 # respaldo de la BD (pg_dump)
├── data_origen/                    # Excels originales de UBITEC
├── scripts/
│   └── clonar_oca.sh               # re-clona los módulos OCA
├── README.md                       # descripción y cómo está desarrollado
├── HANDOFF.md                      # guía para retomar en otra PC
├── MANUAL_SERVIDOR.md              # este archivo
└── DEPLOY_HETZNER.md               # guía de despliegue en Hetzner

Contenedores Docker:
- ubitec-odoo   → Odoo 18 (puerto 8090 host → 8069 contenedor)
- ubitec-db     → PostgreSQL 17 (puerto 5440 host → 5432 contenedor)
Volúmenes: ubitec_odoo_data (filestore), ubitec_db_data (base de datos)
```

---

## 4. LEVANTAR / PARAR / REINICIAR ODOO

Siempre dentro de `/root/odoo_ubitec`:

```bash
cd /root/odoo_ubitec

# LEVANTAR (arrancar todo)
docker compose up -d

# PARAR (apagar, sin borrar datos)
docker compose down

# REINICIAR solo Odoo (tras cambiar código o si se traba)
docker restart ubitec-odoo

# VER si están corriendo
docker ps

# VER LOGS de Odoo en vivo (Ctrl+C para salir)
docker logs -f ubitec-odoo
```

---

## 5. ACTUALIZAR EL CÓDIGO (cuando cambie el módulo custom)

```bash
cd /root/odoo_ubitec
git pull                                    # trae los últimos cambios del repo

# actualizar el módulo custom en Odoo
docker exec ubitec-odoo odoo -d ubitec -u ubitec_clientes --stop-after-init \
  --db_host=db --db_port=5432 --db_user=odoo --db_password=odoo_ubitec_pass
docker restart ubitec-odoo
```

---

## 6. RESPALDAR Y RESTAURAR LA BASE DE DATOS

```bash
cd /root/odoo_ubitec

# HACER UN NUEVO RESPALDO
docker exec ubitec-db pg_dump -U odoo -d ubitec -F c -f /tmp/ubitec.dump
docker cp ubitec-db:/tmp/ubitec.dump backup/ubitec.dump

# RESTAURAR desde el respaldo
docker exec -i ubitec-db pg_restore -U odoo -d ubitec --clean --if-exists < backup/ubitec.dump
docker restart ubitec-odoo
```

> ⚠️ Tras restaurar, si Odoo muestra "Your logo / Gestionar bases de datos" en vez
> del login, es que quedaron assets viejos. Se arregla limpiándolos:
> ```bash
> docker exec ubitec-db psql -U odoo -d ubitec -c \
>   "DELETE FROM ir_attachment WHERE res_model='ir.ui.view' OR url LIKE '/web/assets/%';"
> docker restart ubitec-odoo
> ```

---

## 7. CONSULTAR LA BASE DE DATOS DIRECTO

```bash
# entrar a psql
docker exec -it ubitec-db psql -U odoo -d ubitec

# o una consulta rápida
docker exec ubitec-db psql -U odoo -d ubitec -c \
  "SELECT count(*) FROM res_partner WHERE ubitec_es_cliente=true;"
```

---

## 8. LEVANTAR TODO DESDE CERO (servidor nuevo)

Si algún día montas en otro servidor:

```bash
# 1. instalar docker + git
apt update && apt install -y docker.io docker-compose-v2 git
systemctl enable --now docker

# 2. clonar el repo (privado, necesita token/acceso a RicardoZavala12/odoo_ubitec)
git clone https://github.com/RicardoZavala12/odoo_ubitec.git
cd odoo_ubitec

# 3. reclonar OCA + levantar
bash scripts/clonar_oca.sh
docker compose up -d

# 4. restaurar BD
docker exec ubitec-db createdb -U odoo ubitec
docker exec -i ubitec-db pg_restore -U odoo -d ubitec --clean --if-exists < backup/ubitec.dump
docker restart ubitec-odoo

# 5. abrir http://<IP>:8090
```

---

## 9. PENDIENTES / MEJORAS RECOMENDADAS

- [ ] Dominio bonito (ej. ubitec.com) apuntando a 204.168.157.138
- [ ] HTTPS (candado) con Nginx + Certbot o Cloudflare
- [ ] Cambiar contraseñas de los 4 usuarios y admin_passwd antes de entregar
- [ ] Respaldos automáticos (cron diario del pg_dump)
- [ ] Firewall: dejar solo puertos 22 (SSH), 8090 (Odoo), 80/443 (si HTTPS)

---

## 10. SEGURIDAD

- Data confidencial de clientes (RFC, teléfonos) → sujeta a LFPDPPP.
- El repo con la BD y Excels debe permanecer PRIVADO.
- No compartir la llave SSH privada ni el token de GitHub.
