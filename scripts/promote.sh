#!/usr/bin/env bash
# PROMOVER dev -> prod ("PR a producción"). NO toca Traccar.
set -e
cd "$(dirname "$0")/.."

echo "==> 1. Merge dev -> main..."
git checkout main && git merge dev --no-edit

echo "==> 2. Apagando DEV..."
docker-compose -p ubitec-dev -f docker-compose.dev.yml down 2>/dev/null || true

echo "==> 3. Encendiendo PROD..."
docker-compose -p ubitec-prod -f docker-compose.prod.yml up -d

echo "==> 4. Esperando a que Odoo PROD levante..."
until docker exec ubitec-prod-odoo curl -s -o /dev/null http://localhost:8069/web/login 2>/dev/null; do sleep 3; done

echo "==> 5. Actualizando módulos custom en PROD..."
docker exec ubitec-prod-odoo odoo -d ubitec -u gps_service --stop-after-init --no-http 2>&1 | tail -3
docker restart ubitec-prod-odoo

echo "==> PROMOCIÓN COMPLETA. PROD en :8090. DEV dormido. Traccar intacto."
