#!/usr/bin/env bash
# Enciende PROD y apaga DEV. Nunca corren los dos juntos. NO toca Traccar.
set -e
cd "$(dirname "$0")/.."

echo "==> Apagando DEV (si estaba prendido)..."
docker-compose -p ubitec-dev -f docker-compose.dev.yml down 2>/dev/null || true

echo "==> Encendiendo PROD (código de main)..."
git checkout main 2>/dev/null || echo "(sin git o ya en main)"
docker-compose -p ubitec-prod -f docker-compose.prod.yml up -d

echo "==> PROD arriba en http://$(hostname -I | awk '{print $1}'):8090 (DEV dormido). Traccar intacto."
