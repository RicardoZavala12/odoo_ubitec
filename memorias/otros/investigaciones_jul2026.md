---
name: investigaciones-julio-2026-openvts-selliocrm-contpaqi-sat
description: "Contexto de temas investigados a fin de julio 2026 - competencia GPS, CRMs, facturación, trámite SAT"
metadata: 
  node_type: memory
  type: reference
  originSessionId: eb02eef8-ae7b-4cdf-9888-8040b31f6d06
  modified: 2026-07-31T08:20:41.773Z
---

# Investigaciones / temas (fin julio 2026)

## 1. CONTPAQi — facturación CFDI para Odoo Ubitec
- El cliente Ubitec quiere facturar desde Odoo (~150 timbres/mes ofrecidos). Ver detalle completo en [[ubitec/facturacion_contpaqi_requisitos]] y [[ubitec/PREGUNTAS_CLIENTE_facturacion]].
- El cliente dio acceso al portal **CFDI Facturación en Línea +** (cfdi.com.mx, usuario `OIRL870504190` / pass `Oirl8705**` — CAMBIAR, pasó por chat). Ese portal es MANUAL, NO sirve para integrar Odoo.
- Lo que SÍ sirve: **CONTPAQi Timbra API** (portal `developers.contpaqinube.com`). Ahí están los productos **"Timbra v2"** y **"Timbra v3"** = Web API de Timbrado y Cancelación de CFDIs (REST/JSON). REQUIERE autorización del administrador de la cuenta CONTPAQi.
- **Pendiente:** el usuario debe entrar a developers.contpaqinube.com (Sign in / Sign up), suscribirse a "Timbra v3" → obtiene 2 llaves (Primary/Secondary) = lo que Odoo necesita. Si CONTPAQi complica → alternativa Finkok/Facturama.

## 2. OpenVTS (openvts.io) — competencia de GPS
- Plataforma de rastreo GPS auto-alojada. **Casi seguro es Traccar reempaquetado** (200+ protocolos = cifra de Traccar, PostgreSQL+Docker, misma filosofía).
- Precios: GRATIS hasta 50 vehículos (de por vida). Growth 51-300, Scale 301-2500, Enterprise ilimitado = licencia ÚNICA (precios no públicos).
- ⚠️ Solo instala en **Windows** por ahora (Linux/Docker "planeado"). Licencia NO libre/clara ("full source access" ≠ puedes revender). 0 reseñas en Capterra (producto nuevo).
- Veredicto: NO aporta técnicamente sobre el Traccar que el usuario ya tiene. Lo valioso es su ESTRATEGIA COMERCIAL (licencia única sin mensualidad, features premium: combustible/temperatura/rutas). El usuario mostró interés en instalarlo en una PC Windows para probar/comparar — pendiente si lo hace.
- El link que llegó (mautic.openvts.io/r/...) era solo un tracker de campaña de email (usan Mautic para marketing).

## 3. Mautic
- Herramienta open source de email marketing/automatización (como HubSpot gratis). Se auto-aloja. OpenVTS la usa para sus campañas. No es prioridad del usuario.

## 4. SellioCRM (selliocrm.com) — CRM nuevo
- CRM gratis EN LA NUBE (app.selliocrm.com). NO es open source, NO se auto-aloja, NO se baja el código.
- Personalización: solo "de usuario" (crear campos/objetos/pantallas sin código) — NO personalización profunda como Odoo (código, tu servidor, módulos custom).
- Tiene REST API + servidor MCP + asistente IA (IA de pago por uso).
- El usuario quería "personalizarlo como Odoo" → NO se puede a fondo. Recomendación: usar el **CRM que ya trae Odoo** (personalizable de verdad, en su servidor). Pendiente decisión del usuario.

## 5. SAT — duda personal del usuario (asalariado + servicios profesionales)
- Puede tener 2 regímenes a la vez (asalariado gobierno + servicios profesionales/honorarios).
- Estaba haciendo el trámite en SAT (aviso de actualización de actividades): marcó Asalariado 80% + Servicios profesionales (consultoría en computación) 20%.
- Duda "asimilado a salarios" vs "servicios profesionales": depende de si el gobierno le pide FACTURA (servicios prof.) o le da RECIBO (asimilado). Se le recomendó confirmar con contador. Era duda personal, no proyecto.
