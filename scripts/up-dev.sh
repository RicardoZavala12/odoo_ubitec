#!/usr/bin/env bash
# Enciende DEV y apaga PROD. Nunca corren los dos juntos.
# NO toca Traccar (sus contenedores no se llaman ubitec-*).
set -e
cd "$(dirname "$0")/.."

echo "==> Apagando PROD (si estaba prendido)..."
docker compose -f docker-compose.prod.yml down 2>/dev/null || true

echo "==> Encendiendo DEV..."
git checkout dev 2>/dev/null || echo "(ya en dev o sin git)"
docker compose -f docker-compose.dev.yml up -d

echo "==> DEV arriba en http://\$(hostname -I | awk '{print \$1}'):8091"
echo "    (PROD dormido). Traccar intacto."
