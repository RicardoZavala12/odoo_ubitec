---
name: feedback-ubitec-jamas-inventar-data
description: REGLA ABSOLUTA — nunca inventar/inyectar datos demo o falsos en Odoo Ubitec ni en ningún proyecto del usuario
metadata: 
  node_type: memory
  type: feedback
  originSessionId: d1dbe37a-2752-4c49-a198-a723ba878825
---

NUNCA inventar ni inyectar datos falsos/demo en las bases de datos del usuario. Solo importar/usar datos que existan realmente en sus archivos fuente (Excel, Drive, plataforma).

**Why:** En el proyecto Odoo Ubitec metí un "cliente demo completo" con equipos, pagos y servicios inventados para mostrar las pestañas llenas. El usuario lo rechazó tajantemente ("JAMAS EN TU VIDA INVENTES DATA"). Inventar registros contamina datos reales del cliente y rompe la confianza.

**How to apply:** Si una pestaña/vista está vacía, está vacía — se muestra así o se explica por qué no hay datos en la fuente. Para validar UI usar datos reales existentes, nunca fabricados. Si no existe la liga/dato en el Excel (ej. relación IMEI↔cliente), decirlo con honestidad y pedir la fuente real, NO rellenar con ejemplos. Relacionado con [[feedback-dates-confirmar-antes]].
