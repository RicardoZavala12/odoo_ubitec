---
name: ubitec-facturaci-n-cfdi-con-contpaqi-requisitos
description: Análisis de integrar timbrado CFDI en Odoo vía CONTPAQi Timbra API; qué pedir al cliente antes de codear
metadata: 
  node_type: memory
  type: project
  originSessionId: eb02eef8-ae7b-4cdf-9888-8040b31f6d06
  modified: 2026-07-24T18:53:51.625Z
---

## Facturación CFDI en Odoo Ubitec vía CONTPAQi (24-jul-2026)

### Contexto
El usuario ofreció al cliente ~150 timbres/mes. El cliente Ubitec YA tiene licencia CONTPAQi
y ya integra CONTPAQi con sus clientes (lo sugirió una chica de ahí). La duda era si se puede
meter en Odoo → **SÍ se puede**, vía la **CONTPAQi Timbra API** (REST en la nube).

### Hallazgos técnicos (verificados por web, jul-2026)
- Odoo del usuario es **Community** (no Enterprise). El módulo oficial `l10n_mx_edi` es de Enterprise → NO lo tiene.
- CONTPAQi **es un PAC** autorizado por el SAT.
- **CONTPAQi Timbra** = API REST en la nube (JSON) para timbrar CFDI desde cualquier sistema externo. Portal: `developers.contpaqinube.com`. Funciona desde Python (=Odoo).
- Flujo: Odoo genera XML CFDI → llama Timbra API → CONTPAQi timbra (sella con SAT) → regresa CFDI timbrado → Odoo lo guarda.
- Métodos de la API: request asíncrono de timbrado (reserva y da URL) → subir el XML → consultar estatus + TFD.
- Requiere cuenta CONTPAQi Nube + suscripción a la API de Timbrado en el developer portal.

### Requisitos que confirmar/pedir al CLIENTE antes de codear
1. RFC de Ubitec dado de alta y datos fiscales (régimen, dirección fiscal).
2. **CSD del SAT** (Certificado de Sello Digital): archivos `.cer` + `.key` + su contraseña. Sin esto NO se timbra a su nombre. (Si ya facturan, ya los tienen.)
3. **API de Timbrado activa** en su cuenta CONTPAQi Nube (CONTPAQi Timbra suscrita).
4. **Credenciales de la API** del developer portal (usuario/API key/tokens).
5. Confirmar cuántos timbres incluye su plan (para los 150/mes).
6. Documentación técnica de la API que les den (endpoints exactos, auth).

### Alternativas (por si CONTPAQi no da la API fácil)
- Módulo OCA `l10n_mx_cfdi` (gratis) + PAC común (Finkok, Facturama, SW Sapien) — mejor documentados para Odoo Community. CONTPAQi es más popular como programa standalone que como PAC-para-integrar.

### Estado
Solo análisis. Pendiente: que el cliente responda los requisitos → luego armar plan del módulo Odoo (embebido, como gps_service) que consuma la Timbra API. NO se ha codeado nada.

Relacionado: [[project_ubitec_gps_service]], [[DESPLIEGUE_contabo_dev_prod]].
