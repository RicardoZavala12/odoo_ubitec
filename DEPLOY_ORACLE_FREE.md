# Desplegar Odoo UBITEC gratis en Oracle Cloud (Always Free)

Guía para poner el Odoo en línea, gratis y permanente, para que el cliente lo vea.
Resultado: `http://<IP-PUBLICA>:8090`

---

## FASE 1 — Crear cuenta y VM en Oracle Cloud (navegador, ~30-40 min)

1. Entra a **https://www.oracle.com/cloud/free/** → "Start for free".
2. Regístrate (pide tarjeta para verificar — **NO cobran** en el tier Always Free).
   - En **Home Region** elige una con capacidad ARM: **Frankfurt**, **Madrid** o
     **Querétaro (México Central)** suelen tener cupo. (US East suele estar saturado.)
3. Ya dentro de la consola: menú ☰ → **Compute → Instances → Create Instance**.
4. Configura:
   - **Image**: Canonical **Ubuntu 24.04** (aarch64 / ARM).
   - **Shape**: click "Change Shape" → **Ampere (ARM)** → `VM.Standard.A1.Flex`
     → pon **2 OCPU / 12 GB RAM** (dentro del free). (Si deja 4/24, mejor.)
   - **SSH keys**: "Generate a key pair" → **descarga la llave privada** (la usarás).
   - Deja el resto por defecto → **Create**.
   - Si dice "Out of host capacity": reintenta en unos minutos o cambia de región.
5. Cuando esté "Running", copia la **Public IP address**.

## FASE 2 — Abrir el puerto 8090 (para que el cliente entre)

1. En la instancia → sección **Primary VNIC** → click en la **Subnet**.
2. Entra a la **Security List** por defecto → **Add Ingress Rules**:
   - Source CIDR: `0.0.0.0/0`
   - IP Protocol: **TCP**, Destination Port: **8090**
   - Add.

## FASE 3 — Conectarse e instalar Docker (SSH, ~15 min)

Desde tu PC (con la llave descargada):

```bash
chmod 600 ~/Descargas/tu-llave.key
ssh -i ~/Descargas/tu-llave.key ubuntu@<IP-PUBLICA>

# Ya dentro del servidor:
sudo apt update && sudo apt install -y docker.io docker-compose-v2 git
sudo usermod -aG docker ubuntu && newgrp docker

# Abrir el puerto en el firewall interno de Ubuntu (Oracle lo trae cerrado)
sudo iptables -I INPUT 6 -m state --state NEW -p tcp --dport 8090 -j ACCEPT
sudo netfilter-persistent save   # si pide instalar: sudo apt install -y iptables-persistent
```

## FASE 4 — Subir el proyecto y levantarlo (~15 min)

```bash
# Clonar el repo (necesitas el token/acceso de RicardoZavala12)
git clone https://github.com/RicardoZavala12/odoo_ubitec.git
cd odoo_ubitec

# Reclonar los OCA
bash scripts/clonar_oca.sh

# Levantar (baja imágenes ARM automáticamente)
docker compose up -d      # espera 2-3 min la primera vez

# Restaurar la base de datos con toda la data
docker exec ubitec-db createdb -U odoo ubitec 2>/dev/null
docker exec -i ubitec-db pg_restore -U odoo -d ubitec --clean --if-exists < backup/ubitec.dump

docker restart ubitec-odoo
```

## FASE 5 — Que el cliente entre

Comparte con el cliente: **http://<IP-PUBLICA>:8090**
Login admin: `admin.ubitec@ubitec.mx` / `Ubitec.Admin#2026`

---

## RECOMENDACIONES

- **Dominio bonito (opcional)**: un dominio gratis (ej. DuckDNS) apuntando a la IP →
  `http://ubitec.duckdns.org:8090` en vez de la IP.
- **HTTPS (opcional)**: si quieres candado, poner Nginx + Certbot o Cloudflare Tunnel.
- **Seguridad**: cambia las contraseñas de los usuarios antes de mostrar al cliente,
  y el `admin_passwd` de config/odoo.conf. La data es confidencial (LFPDPPP).
- **Costo**: $0 permanente mientras te quedes en la shape Always Free (Ampere A1).
