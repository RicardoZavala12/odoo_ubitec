# HANDOFF — Proyecto Odoo 18 UBITEC

> **Para Claude / cualquier dev que retome este proyecto en otra PC.**
> Aquí está TODO: cómo se configuró, credenciales, qué se hizo, qué falta.
> Data real de clientes → repo PRIVADO, sujeto a LFPDPPP. Nunca inventar datos.

---

## 1. QUÉ ES ESTE PROYECTO

Implementación de **Odoo 18 Community** (en Docker) para **UBITEC**, empresa de
rastreo satelital / telemetría (instala GPS, cobra monitoreo mensual). ERP/CRM que
centraliza clientes, equipos GPS, SIMs, servicios, cobranza y soporte.

Contrato: $40,000 MXN, 4 entregables. Fuera de alcance: app móvil, contabilidad
completa, licencia Enterprise, reportes avanzados custom. CFDI 4.0 está EN alcance
(150 timbres/mes) pero aún no configurado.

---

## 2. CÓMO LEVANTARLO EN OTRA PC (paso a paso)

Requisitos: Docker + Docker Compose + git.

```bash
# 1. Clonar este repo
git clone https://github.com/RicardoZavala12/odoo_ubitec.git
cd odoo_ubitec

# 2. Clonar los módulos OCA de terceros (NO vienen en el repo, ver .gitignore)
bash scripts/clonar_oca.sh

# 3. Levantar Odoo + Postgres
docker compose up -d          # espera ~1-2 min la primera vez (baja imagen odoo:18.0)

# 4. Restaurar la base de datos con TODA la data ya cargada
docker exec -i ubitec-db pg_restore -U odoo -d ubitec --clean --if-exists < backup/ubitec.dump
#    (si la BD 'ubitec' no existe aún, primero: docker exec ubitec-db createdb -U odoo ubitec)

# 5. Reiniciar odoo para que tome la BD restaurada
docker restart ubitec-odoo

# 6. Abrir en el navegador
#    http://localhost:8090
```

Si el menú de apps se ve raro tras restaurar: recargar con Ctrl+Shift+R.

---

## 3. ARQUITECTURA / CONFIGURACIÓN

- **Odoo**: imagen oficial `odoo:18.0` (Community) de Docker Hub.
- **Postgres**: `postgres:17`.
- **Puertos** (elegidos para NO chocar con otros proyectos en la misma PC):
  - Odoo web: **8090** (host) → 8069 (contenedor)
  - Postgres: **5440** (host) → 5432 (contenedor)
- **Contenedores**: `ubitec-odoo`, `ubitec-db`. Proyecto compose: `ubitec-local`.
- **Volúmenes**: `ubitec_odoo_data`, `ubitec_db_data` (datos propios, aislados).
- **BD**: `ubitec` | user `odoo` | pass `odoo_ubitec_pass`.
- **addons_path** (en config/odoo.conf): incluye el custom + cada repo OCA:
  `/mnt/extra-addons,/mnt/extra-addons/oca_contract,/mnt/extra-addons/oca_field_service,/mnt/extra-addons/oca_helpdesk,/mnt/extra-addons/oca_web`
- **dbfilter**: `^ubitec$` (solo ve su propia BD).

### Contraseña maestra de Odoo (crear/borrar/backup de BDs)
`ubitec_admin_2026`  (definida en config/odoo.conf → admin_passwd)

---

## 4. CREDENCIALES DE USUARIOS (http://localhost:8090)

| Rol | Usuario (login) | Contraseña |
|-----|-----------------|------------|
| Administrador | `admin.ubitec@ubitec.mx` | `Ubitec.Admin#2026` |
| Comercial/Ventas | `ventas@ubitec.mx` | `Ubitec.Ventas#2026` |
| Técnico/Field Service | `tecnico@ubitec.mx` | `Ubitec.Tecnico#2026` |
| Soporte/Oficina | `soporte@ubitec.mx` | `Ubitec.Soporte#2026` |

> El admin tiene acceso total (se le asignaron todos los grupos internos, sin
> portal/public para no romper el chat). Los otros 3 tienen permisos base — FALTA
> afinar permisos por rol (ver pendientes).

---

## 5. MÓDULOS

**Núcleo Odoo (Community):** CRM, Ventas (sale_management), Inventario (stock),
Proyecto, HR, Asistencias, Ausencias (hr_holidays), Gastos (hr_expense), Flota (fleet),
Contactos.

**OCA (de terceros, rama 18.0 — se reclonan con scripts/clonar_oca.sh):**
- `contract` 18.0.2.4.x → Suscripciones/cobro recurrente (reemplaza sale_subscription Enterprise)
- `fieldservice` 18.0.5.6.x → Field Service (reemplaza industry_fsm Enterprise)
- `helpdesk_mgmt` 18.0.1.17.x → Helpdesk (reemplaza helpdesk Enterprise)
- `web_responsive` 18.0.1.0.x → menú de apps con iconos + responsive

> IMPORTANTE: Suscripciones, Field Service y Helpdesk nativos son de Odoo ENTERPRISE
> (de pago) y NO existen en Community. Por eso se usan los equivalentes OCA gratuitos.

**Custom: `addons/ubitec_clientes/`** — el módulo a la medida. Contiene:
- `res.partner` extendido: esquema (venta/comodato/migración/...), mensualidad,
  costos, estado (nuevo/activo/inactivo con cron a 30 días), registro de pago
  (día corte, próximo pago, estado_pago), adeudo/cartera, servicios adicionales,
  usuario/contraseña de plataforma (con widget password_toggle = botón ojito),
  RFC (campo vat nativo).
- `ubitec.unidad` — equipos GPS: imei, folio, numero_serie, marca, unidad(vehículo),
  cliente, sim, icc, esquema, estado (stock/instalado/baja), costo, fechas. Tiene su
  propio MENÚ "Equipos GPS" con lista/form/filtros para dar de alta equipos.
- `ubitec.sim` — SIMs Telcel/Claro: sim_card, linea, icc, imsi, plan, operador.
- `ubitec.servicio` — historial/agenda de servicios (instalación, revisión, etc.).
- `ubitec.pago` — historial de pagos por cliente.

---

## 6. DATA CARGADA (real, de los Excels en data_origen/)

| Dato | Cantidad | Fuente Excel |
|------|----------|--------------|
| Clientes | 409 (128 con RFC, 56 con cartera vencida $266K) | Alta Clientes + FACTURAS + Faltantes |
| Equipos GPS (IMEI) | 1,099 (241 ligados a cliente) | Stock Oficina + Bajas + Programación |
| SIMs | 307 | Activaciones SIM + Claro |
| Servicios | 3,307 (1,200 ligados) | Programación 2025/2026 |
| Productos | 42 | Lista de precios |
| Empleados | 14 | hoja Asistencia |
| Tickets soporte | 29 | Llamadas y Reportes |

**Cómo se importó:** scripts Python ejecutados dentro del contenedor odoo con
`odoo.registry(...)` + `openpyxl`. Los Excels originales están en `data_origen/`.
Match cliente↔equipo se hizo por IMEI + nombre normalizado (de la hoja Programación).

**REGLA ABSOLUTA:** JAMÁS inventar/inyectar datos demo. Solo data real de los Excels.
Si un dato no existe en la fuente, se deja vacío y se dice, no se rellena.

---

## 7. QUÉ FALTA (según el contrato) — pendientes

Avance ~65%. La DATA está cargada; falta CONFIGURAR comportamiento de módulos:

1. **Suscripciones** (contract) — crear planes de monitoreo (mensual $300, anual)
   y activar el cobro recurrente automático. Entregable grande casi sin tocar.
2. **Pasarela de pago** — integrar (Mercado Pago/Stripe). Está en alcance.
3. **CFDI 4.0** — facturación localización MX (150 timbres/mes). En alcance, sin config.
4. **CRM** — personalizar etapas del pipeline + dejar cotizaciones/órdenes de venta.
5. **Field Service** — convertir los 3,307 servicios de historial a órdenes FSM
   agendables (técnico + fecha + ubicación). Hoy están en ubitec.servicio.
6. **Helpdesk** — configurar etapas y flujo de tickets.
7. **Permisos por rol** — afinar qué ve cada uno de los 4 usuarios.
8. **Respaldos automáticos** para producción + **capacitación** al cliente.

Fuera de alcance (no hacer salvo cotización aparte): app móvil, migración masiva
histórica, contabilidad completa, licencia Enterprise, reportes avanzados custom.

---

## 8. COMANDOS ÚTILES

```bash
# Ver logs de odoo
docker logs -f ubitec-odoo

# Actualizar el módulo custom tras editar código
docker exec ubitec-odoo odoo -d ubitec -u ubitec_clientes --stop-after-init \
  --db_host=db --db_port=5432 --db_user=odoo --db_password=odoo_ubitec_pass
docker restart ubitec-odoo

# Nuevo dump de la BD
docker exec ubitec-db pg_dump -U odoo -d ubitec -F c -f /tmp/ubitec.dump
docker cp ubitec-db:/tmp/ubitec.dump backup/ubitec.dump

# Consultar la BD directo
docker exec ubitec-db psql -U odoo -d ubitec -c "SELECT count(*) FROM res_partner WHERE ubitec_es_cliente=true;"
```

---

## 9. NOTAS / DECISIONES TOMADAS

- Puertos 8090/5440 elegidos porque en la PC original había otros Odoo/Postgres
  (salo_gaash usa 8069/5433, wallet 5435). Cambiar si chocan en la nueva PC.
- El `odoo shell` por stdin no aplicaba commits en este entorno; por eso las cargas
  se hicieron con scripts python autónomos (odoo.registry + cr.commit()).
- web_responsive da el menú de iconos tipo el proyecto salo_gaash (que usa un módulo
  custom apps_grid; aquí se optó por el OCA estándar).
