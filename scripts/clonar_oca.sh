#!/bin/bash
# Re-clona los repos OCA (rama 18.0) que el proyecto necesita.
# Se ejecuta una vez tras clonar este repo, dentro de addons/.
set -e
cd "$(dirname "$0")/../addons"
echo "Clonando repos OCA (rama 18.0)..."
[ -d oca_web ]           || git clone --depth 1 -b 18.0 https://github.com/OCA/web.git oca_web
[ -d oca_contract ]      || git clone --depth 1 -b 18.0 https://github.com/OCA/contract.git oca_contract
[ -d oca_field_service ] || git clone --depth 1 -b 18.0 https://github.com/OCA/field-service.git oca_field_service
[ -d oca_helpdesk ]      || git clone --depth 1 -b 18.0 https://github.com/OCA/helpdesk.git oca_helpdesk
echo "OCA clonados. Ya puedes levantar con: docker compose up -d"
