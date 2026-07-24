---
name: ubitec-gps-notificaciones-telegram
description: "Bot de Telegram que notifica al crear servicios GPS; token, chat_id, cómo funciona y configurar"
metadata: 
  node_type: memory
  type: project
  originSessionId: eb02eef8-ae7b-4cdf-9888-8040b31f6d06
  modified: 2026-07-24T18:39:30.076Z
---

## Notificaciones Telegram al crear servicio GPS (24-jul-2026)

Al crear un `gps.service`, el módulo envía un mensaje a un grupo de Telegram.

### Bot y grupo
- **Bot:** `@ubitec_servicios_bot` (creado con @BotFather).
- **Token:** `8855890832:AAHlwO9e4dCIGkbia08gSepsLbCnoV0cRNM`
- **Grupo:** "Ubitec Servicios" · **chat_id:** `-5552473247`
- ⚠️ IMPORTANTE: se desactivó el **modo privacidad** del bot en BotFather (`/setprivacy` → Disable) para que el bot pudiera detectar el grupo y sacar el chat_id. Para obtener el chat_id: mandar un mensaje en el grupo y `curl https://api.telegram.org/bot<TOKEN>/getUpdates`.

### Implementación (rama feature/telegram-notif, desde dev)
- `models/gps_service.py`: `create()` llama `_notify_telegram_created()`. Helper `_send_telegram(text)` hace POST a la API de Telegram (usa `requests`, timeout 10s, falla silenciosa para no romper la creación). Token/chat leídos de `ir.config_parameter` (`gps_service.telegram_token`, `gps_service.telegram_chat_id`).
- `data/telegram_config.xml`: guarda token y chat_id como parámetros de sistema (noupdate=1, editables desde Ajustes→Técnico→Parámetros del sistema).
- Mensaje: folio, cliente, unidad, técnico, ubicación, fecha programada.
- Probado en local: crear servicio → llega mensaje al grupo. ✅

### Para cambiar token/chat sin tocar código
Ajustes → Técnico (modo dev) → Parámetros del sistema → editar `gps_service.telegram_token` / `gps_service.telegram_chat_id`.

### Pendiente / ideas
- Notificar en más eventos (aceptado, iniciado, finalizado, validado) — el usuario aún no lo pidió, se dejó "solo al crear" por ahora.
- Falta merge feature/telegram-notif → dev → main/prod, y pull en Contabo.

Relacionado: [[project_ubitec_gps_service]], [[DESPLIEGUE_contabo_dev_prod]].
