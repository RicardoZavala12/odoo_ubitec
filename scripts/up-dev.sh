#!/usr/bin/env bash
# Enciende DEV y apaga PROD. Nunca corren los dos juntos. NO toca Traccar.
set -e
cd "$(dirname "$0")/.."

echo "==> Apagando PROD (si estaba prendido)..."
docker-compose -p ubitec-prod -f docker-compose.prod.yml down 2>/dev/null || true

echo "==> Encendiendo DEV..."
git checkout dev 2>/dev/null || echo "(sin git o ya en dev)"
docker-compose -p ubitec-dev -f docker-compose.dev.yml up -d

echo "==> DEV arriba en http://$(hostname -I | awk '{print $1}'):8091 (PROD dormido). Traccar intacto."
