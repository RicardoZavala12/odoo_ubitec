---
name: Dates MVP - sesión 9 abril 2026
description: Cambios del 9 abril 2026 — Google Maps URL, botón Agendar, rutas /admin/:slug/, colores extra, animaciones scroll, QR real + escáner + checkin
type: project
---

# Sesión 9 abril 2026

## Cambios realizados

### 1. Google Maps → campo URL simple
- Nuevo campo `googleMapsUrl` en Business (schema + BD)
- Reemplaza la lógica de lat/lng → el super admin pega una URL de Google Maps
- BusinessSettings tab General: campo "URL de Google Maps"
- AboutUs: usa googleMapsUrl si existe, fallback a address
- Quitada la dependencia de getBusinessType en AboutUs

### 2. WhatsApp flotante → Botón "Agendar" flotante
- Botón verde de WhatsApp COMENTADO (no borrado) en Landing.jsx
- Reemplazado por botón flotante "Agendar" con ícono de calendario, color del negocio
- Lleva a `/booking/:slug`

### 3. Panel admin por slug `/admin/:slug/`
- Rutas cambiadas de `/admin` a `/admin/:slug` 
- AdminRedirect en `/admin` detecta el slug del user y redirige a `/admin/:slug`
- Login.jsx redirige a `/admin/:slug` tras login
- AdminSidebar: links dinámicos usando base `/admin/${business.slug}`
- Logout navega a /login
- Ejemplo: `localhost:3000/admin/clinica-san-rafael/`

### 4. Colores de divs/texto personalizables
- Nuevos campos en Business: `bgColor`, `textColor`, `cardBgColor`, `buttonTextColor`
- Valores default: #ffffff, #111827, #ffffff, #ffffff
- Agregados al superAdminController allowed fields
- BusinessSettings tab Branding: 6 color pickers (primario, secundario, fondo página, texto, fondo cards, texto botones)
- Preview en vivo actualizado con todos los colores

### 5. Animaciones scroll reveal en landing
- Hook `useScrollReveal()` y `useStaggerReveal()` en `src/utils/useScrollReveal.js`
- CSS en index.css: `.scroll-reveal`, `.stagger-item`, `.scroll-reveal-left`, `.scroll-reveal-right`
- Aplicado en: ServicesGrid (título + cards stagger), WhyUs (título + cards stagger), CTASection (contenido), AboutUs (texto desde izquierda)
- No se instaló framer-motion — todo nativo con IntersectionObserver + CSS transitions

### 6. QR real + escáner + flujo de checkin
- Nuevo estado `in_progress` en AppointmentStatus enum
- Endpoint público `POST /api/appointments/code/:bookingCode/checkin` con body `{action: 'confirm'|'start'|'complete'}`
- Transiciones validadas: pending→confirmed, confirmed→in_progress, in_progress→completed
- Auto-crea venta al completar (idempotente)
- Protección contra doble acción
- `BookingQR.jsx` ahora genera QR con URL real: `dominio/cita/:bookingCode`
- Nueva página `CitaCheckin.jsx` en `/cita/:bookingCode`: header con branding del negocio, badge de estado con color, info de cita, botones de acción según estado
- Nueva página `Scanner.jsx` en `/admin/:slug/scanner`: abre cámara con html5-qrcode, escanea QR y redirige a la vista de cita
- Link "Escáner QR" en AdminSidebar con ícono ScanLine
- Librerías instaladas: `qrcode.react` (ya estaba), `html5-qrcode`

### Fix de conexión BD
- DATABASE_URL cambiada de `172.17.0.1` a `localhost` (pg_hba dejó de aceptar la IP del bridge Docker)

## Archivos creados/modificados
- Backend: schema.prisma, .env, appointmentController.js (checkin), appointments routes, superAdminController.js
- Frontend: CitaCheckin.jsx (nuevo), Scanner.jsx (nuevo), useScrollReveal.js (nuevo), index.css, Landing.jsx, App.jsx, Login.jsx, AdminSidebar.jsx, BusinessSettings.jsx, ServicesGrid.jsx, WhyUs.jsx, CTASection.jsx, AboutUs.jsx, BookingQR.jsx

## Pruebas OK
- Flujo QR: pending→confirmed→in_progress→completed con auto-venta ✅
- Doble acción rechazada ✅
- Panel /admin/:slug redirige correctamente ✅
