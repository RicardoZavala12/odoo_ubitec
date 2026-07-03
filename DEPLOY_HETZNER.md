# Desplegar Odoo UBITEC en Hetzner (VPS ~$5/mes)

Guía para poner el Odoo en línea de forma estable y permanente.
Resultado: `http://<IP-DEL-SERVIDOR>:8090` (luego con dominio y HTTPS).

---

## FASE 1 — Crear cuenta y servidor (navegador, ~15 min)

1. Entra a **https://www.hetzner.com/cloud** → "Sign Up".
2. Crea cuenta (correo + contraseña). Verifica tu correo.
3. Te pedirá método de pago (tarjeta o PayPal) y quizá verificación de identidad
   (Hetzner a veces pide una foto de ID la primera vez — es normal, anti-fraude).
4. Ya dentro → **"New Project"** → nombre: `ubitec` → Create.
5. Dentro del proyecto → **"Add Server"**:
   - **Location**: Ashburn (EE.UU.) o Hillsboro — los más cercanos a México.
   - **Image**: **Ubuntu 24.04**
   - **Type**: pestaña **Shared vCPU** → **CX22** (2 vCPU, 4 GB RAM, 40 GB) ~€4.59/mes.
     (Si quieres más holgura: CX32 con 8 GB.)
   - **Networking**: deja IPv4 pública activada (viene por defecto).
   - **SSH key**: click "Add SSH key" → pega tu llave pública (ver Fase 2).
   - **Name**: `ubitec-odoo`.
   - **Create & Buy now**.
6. En ~30 seg el servidor está listo. Copia la **IP pública** que aparece.

## FASE 2 — Llave SSH (antes de crear el server, o desde tu PC)

En tu PC (Linux), genera una llave si no tienes:
```bash
ssh-keygen -t ed25519 -C "ubitec-hetzner" -f ~/.ssh/ubitec_hetzner
# Enter, Enter (sin passphrase para simplificar)
cat ~/.ssh/ubitec_hetzner.pub   # <- copia TODO esto y pégalo en Hetzner (Add SSH key)
```

## FASE 3 — Conectarse e instalar Docker (SSH, ~10 min)

```bash
ssh -i ~/.ssh/ubitec_hetzner root@<IP-DEL-SERVIDOR>

# Dentro del servidor:
apt update && apt install -y docker.io docker-compose-v2 git
systemctl enable --now docker
```

## FASE 4 — Subir el proyecto y levantarlo

```bash
# Clonar el repo (necesita acceso a RicardoZavala12/odoo_ubitec)
git clone https://github.com/RicardoZavala12/odoo_ubitec.git
cd odoo_ubitec

# Reclonar los módulos OCA
bash scripts/clonar_oca.sh

# Levantar
docker compose up -d      # espera 2-3 min la primera vez

# Restaurar la base de datos con toda la data
docker exec ubitec-db createdb -U odoo ubitec 2>/dev/null
docker exec -i ubitec-db pg_restore -U odoo -d ubitec --clean --if-exists < backup/ubitec.dump
docker restart ubitec-odoo
```

## FASE 5 — Abrir el puerto y que el cliente entre

Hetzner por defecto NO tiene firewall (abierto). Si activaste uno, abre el 8090.
Comparte: **http://<IP-DEL-SERVIDOR>:8090**
Login: `admin.ubitec@ubitec.mx` / `Ubitec.Admin#2026`

## FASE 6 (opcional) — Dominio bonito + HTTPS

1. Compra un dominio (Namecheap/Cloudflare ~$200 MXN/año), ej. `ubitec.com`.
2. En el DNS del dominio, crea un registro **A** apuntando a la IP de Hetzner.
3. Para HTTPS (candado): instalar Nginx + Certbot, o usar Cloudflare (proxy gratis).

---

## COSTOS (los paga el cliente vía contrato)
- Servidor Hetzner CX22: ~€4.59/mes (~$85 MXN)
- Dominio .com: ~$200 MXN/año (opcional)
- Contrato Ubitec cubre "alojamiento $9,000/año" → margen de sobra.

## SEGURIDAD antes de mostrar al cliente
- Cambiar contraseñas de los 4 usuarios y el admin_passwd de config/odoo.conf.
- Data confidencial (LFPDPPP): mantener accesos privados.
