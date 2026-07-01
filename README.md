# Odoo 18 — UBITEC (Rastreo Satelital)

Implementación de Odoo 18 Community para UBITEC: gestión de clientes, equipos GPS,
SIMs, servicios, cobranza y soporte.

> ⚠️ **CONFIDENCIAL** — Este repo contiene datos reales de clientes de UBITEC (RFC,
> teléfonos, correos). Mantener el repositorio **privado**. Uso sujeto a la LFPDPPP.

## Estructura

- `addons/ubitec_clientes/` — Módulo a la medida (clientes, equipos GPS, SIMs, pagos, servicios).
- `addons/oca_*/` — Módulos OCA de terceros (NO versionados, ver abajo).
- `config/odoo.conf` — Configuración de Odoo.
- `docker-compose.yml` — Stack: Odoo 18 + Postgres 17. Puertos 8090 (web) / 5440 (db).
- `backup/ubitec.dump` — Respaldo de la base de datos (pg_dump formato custom).
- `data_origen/` — Excels originales de UBITEC de donde se importó la data.
- `scripts/clonar_oca.sh` — Re-clona los módulos OCA.

## Módulos instalados

Núcleo Odoo: CRM, Ventas, Inventario, Proyecto, HR, Asistencias, Ausencias, Gastos, Flota.
OCA: `contract` (suscripciones), `fieldservice`, `helpdesk_mgmt`, `web_responsive`.
Custom: `ubitec_clientes`.

## Levantar el proyecto desde cero

```bash
# 1. Clonar los módulos OCA de terceros
bash scripts/clonar_oca.sh

# 2. Levantar contenedores
docker compose up -d

# 3. Restaurar la base de datos (opcional, si quieres la data)
docker exec -i ubitec-db pg_restore -U odoo -d ubitec --clean < backup/ubitec.dump

# 4. Abrir
#    http://localhost:8090
```

## Data cargada (real, de los Excels de UBITEC)

- 409 clientes (128 con RFC, 56 con cartera vencida)
- 1,099 equipos GPS por IMEI (241 ligados a cliente)
- 307 SIMs (Telcel/Claro)
- 3,307 servicios (historial/agenda)
- 42 productos (lista de precios)
- 14 empleados · 29 tickets de soporte
