---
name: contabo-gu-a-completa-credenciales-ssh-deploy
description: "TODO sobre el VPS Contabo — cómo conectarse por SSH, credenciales, generar llaves, Deploy Key GitHub, levantar Odoo dev/prod"
metadata: 
  node_type: memory
  type: reference
  originSessionId: eb02eef8-ae7b-4cdf-9888-8040b31f6d06
  modified: 2026-07-21T20:16:10.794Z
---

# 🖥️ CONTABO — Guía completa del servidor

VPS que aloja **Traccar (producción)** + **Odoo Ubitec (dev/prod)**.
⚠️ **TRACCAR NO SE TOCA** — solo lectura/seguridad. Contenedor `Controldetrafico`, puerto 8082.

---

## 1. DATOS DEL SERVIDOR
| Dato | Valor |
|------|-------|
| Proveedor | Contabo |
| IP | `194.238.29.167` (= vmi2462265.contaboserver.net) |
| Customer ID | 13727344 |
| Panel | https://my.contabo.com · email `carlockventas@gmail.com` (pass del panel: usar "Forgot password") |
| OS | Ubuntu 24.04 LTS |
| Specs | 4 cores AMD EPYC, 3.8 GB RAM + **4 GB swap**, 387 GB disco |
| VNC (entra sin SSH) | `209.145.54.193:63113` · pass `AvRt0406` |

---

## 2. CONECTARSE POR SSH
- **Usuario:** `root`
- **Contraseña:** `mtyTRACCAR@120201#11.25#09`
- **Puerto:** 22

### Desde una PC con SSH normal:
```bash
ssh root@194.238.29.167
# pega la contraseña cuando la pida
```

### Con sshpass (sin que pida la contraseña interactiva):
```bash
sudo apt install sshpass    # si no está
sshpass -p 'mtyTRACCAR@120201#11.25#09' ssh -o PreferredAuthentications=password -o PubkeyAuthentication=no root@194.238.29.167
```

> ⚠️ **fail2ban** está activo: muchas conexiones seguidas → timeout temporal ("banner exchange timed out"). Esperar ~20s y reintentar. La IP del usuario NO se bloquea.

---

## 3. CREDENCIALES DENTRO DEL SERVIDOR
### PostgreSQL de Traccar (Docker, puerto 5432)
- `traccaruser` / `Ftrk@Pg2026!Xm9vL`
- `postgres` (superuser) / `Ftrk@PgRoot2026!Qw7`

### Odoo Ubitec (contenedores separados de Traccar)
- **PROD** (`ubitec-prod-*`): web `:8090`, db `:5440`. **DEV** (`ubitec-dev-*`): web `:8091`, db `:5441`.
- Postgres de Odoo: user `odoo` / pass `odoo_ubitec_pass` · BD `ubitec`
- Contraseña maestra Odoo (crear/borrar BD): `ubitec_admin_2026`
- Usuarios web Odoo: `superadmin`/`super123` (admin), `tecnico@ubitec.mx`/`oscar123` (técnico Oscar). Ver [[ACCESOS]].

### Traccar admin (web :8082)
- email `traccarjuan@gmail.com` · pass la que tenía el usuario (hasheada).

### pgAdmin (Docker :9999)
- `carlockventas@gmail.com` / `tinta4204` (no accesible desde internet por firewall).

---

## 4. GENERAR LLAVE SSH (en una PC nueva, para acceder a GitHub)
```bash
# generar
ssh-keygen -t ed25519 -C "mi-pc" -f ~/.ssh/github_ricardo -N ""
# ver la pública para pegarla en GitHub
cat ~/.ssh/github_ricardo.pub
# agregar en https://github.com/settings/keys
# configurar host
cat >> ~/.ssh/config <<'EOF'
Host github-ricardo
    HostName github.com
    User git
    IdentityFile ~/.ssh/github_ricardo
    IdentitiesOnly yes
EOF
ssh -T git@github-ricardo   # "Hi RicardoZavala12!"
```

---

## 5. DEPLOY KEY (cómo Contabo accede al repo privado de GitHub)
Contabo tiene su propia llave `/root/.ssh/ubitec_deploy` (solo-lectura), agregada en
GitHub → repo odoo_ubitec → Settings → Deploy keys ("Contabo (solo lectura)").
El `/root/.ssh/config` del VPS mapea github.com → esa llave.
Para regenerarla si se pierde:
```bash
ssh-keygen -t ed25519 -C 'ubitec-contabo-deploy' -f /root/.ssh/ubitec_deploy -N '' -q
cat /root/.ssh/ubitec_deploy.pub   # agregar en GitHub Deploy keys
```

---

## 6. LEVANTAR / OPERAR ODOO EN CONTABO
Proyecto en `/root/odoo_ubitec/` (es git, rama dev trackea origin/dev).
```bash
cd /root/odoo_ubitec

# traer últimos cambios de GitHub
git pull

# levantar DEV (apaga prod, prende dev :8091)
bash scripts/up-dev.sh

# levantar PROD (apaga dev, prende prod :8090)
bash scripts/up-prod.sh

# promover dev -> prod ("PR")
bash scripts/promote.sh

# actualizar el módulo tras cambios de código
docker exec ubitec-dev-odoo odoo -d ubitec -u gps_service --stop-after-init --no-http
docker restart ubitec-dev-odoo
```
⚠️ Contabo tiene `docker-compose` **v1.29** (con guion). Los scripts ya lo usan con `-p`.
⚠️ NUNCA levantar dev y prod juntos (comparten RAM con Traccar).

### Fix "se queda Cargando" o muestra gestor de BD
El dump no trae filestore. En `config/odoo.conf` debe estar `db_name = ubitec` y `list_db = False`.
Para el cargando infinito: borrar assets rotos y reiniciar:
```bash
docker exec ubitec-prod-db psql -U odoo -d ubitec -c "DELETE FROM ir_attachment WHERE res_model='ir.ui.view' AND name LIKE 'web.assets%' OR url LIKE '/web/assets/%';"
docker restart ubitec-prod-odoo
```

---

## 7. VERIFICAR QUE TRACCAR SIGUE VIVO (hacer siempre tras tocar algo)
```bash
curl -s -o /dev/null -w 'Traccar: HTTP %{http_code}\n' http://localhost:8082   # debe dar 200
docker ps --format '{{.Names}}' | grep Controldetrafico                        # debe aparecer
```

---

## 8. DOMINIO (pendiente, para futuro)
El server ya tiene Apache + certbot + HTTPS (dominios fulltrack.com.mx). Para poner
`odoo.ubitec.mx` o `odoo.fulltrack.com.mx`: crear registro A → 194.238.29.167, luego
VirtualHost Apache + certbot. `ubitec.mx` lo controla el cliente (GoDaddy);
`fulltrack.com.mx` lo controla el usuario (controldns.mx, login.fulltrack ya apunta al server).

Relacionado: [[ACCESOS]], [[DESPLIEGUE_contabo_dev_prod]], [[traccar/ACCESOS]].
