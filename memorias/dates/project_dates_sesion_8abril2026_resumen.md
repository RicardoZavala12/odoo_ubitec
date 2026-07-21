---
name: Dates MVP - sesión 8 abril 2026 - resumen completo y cómo probar
description: Lo que se hizo en la sesión del 8 abril 2026 en Dates MVP (bloques 1-5), credenciales, URLs, y cómo probar cada bloque paso a paso
type: project
---

# Sesión 8 abril 2026 — Dates MVP multi-tenant sprint fin de semana

## Estado general
| Bloque | Nombre | Estado |
|---|---|---|
| 1 | Schema multi-tenant + super admin backend | ✅ |
| 2 | Panel Super Admin frontend | ✅ |
| 3 | Catálogo en panel admin | ✅ |
| 4 | Ajustes branding (solo super admin) | ✅ |
| 4.5 | Registro de Ventas del día | ✅ |
| 5 | Landing dinámica + WhatsApp | ✅ |
| 6 | Hardening de seguridad | ⏳ pendiente |

## Credenciales y usuarios en BD
- Super admin: `super@demo.com` / `super123` (businessId=null, role=super_admin)
- Clínica San Rafael → `admin@demo.com` (Dr. Ricardo García, owner) — pass tentativa `admin123`
- Barbería Don Juan → `juan@barber.com` (Juan Barbero, owner)
- Ricardo Flores (empresa de prueba) → `desarrollo2@vinegarden.mx`
- Para cambiar pass super admin: `cd dates-back && npm run reset-super-pass nuevo@email.com nuevaPass`
- No hay script de reset para admins de empresa aún — si el admin123 no jala hay que crear uno.

## URLs
- Frontend dev: http://localhost:3001 (Vite; el 3000 estaba ocupado)
- Backend: http://localhost:4000
- Landing clínica: http://localhost:3001/clinica-san-rafael
- Landing barbería: http://localhost:3001/barberia-don-juan
- Login: http://localhost:3001/login
- Panel super admin: http://localhost:3001/superadmin
- Ajustes de un negocio (solo super admin): http://localhost:3001/superadmin/business/:id
- Panel admin normal: http://localhost:3001/admin

## Bloque 1 — Schema + backend super admin
- Prisma migración `bloque1_multitenant_catalogo_ventas` aplicada
- Modelos nuevos: `ServiceVariant`, `Product`, `Combo`, `ComboItem`, `Sale`, `SaleItem`
- Enums: `UserRole.super_admin`, `BusinessType` con spa/clinica_estetica/clinica_medica/dentista/estetica, `CatalogItemType`, `SaleItemType`, `PaymentMethod`
- `Business` gana: facebookUrl, tiktokUrl, whatsappUrl, videoUrl, showServices/Products/Combos
- `Service/Product/Combo`: folio único por business, imageUrl, visible
- Folios backfilleados SRV-0001..SRV-0004 por business con WITH numbered + ROW_NUMBER
- Middleware `requireSuperAdmin` y `requireRole(...)` en `src/middleware/auth.js`
- Script `scripts/resetSuperAdmin.js`, npm script `reset-super-pass`
- Endpoints CRUD `/api/superadmin/businesses` (GET list, GET :id, POST, PATCH, DELETE) con delete en cascada transaccional
- Helper `src/utils/folio.js` con `nextFolio(type, businessId)`
- **Probar**: `psql -c "\dt"` ver tablas nuevas; `SELECT folio, name FROM services;`; `SELECT email, role FROM users WHERE role='super_admin';`

## Bloque 2 — Panel Super Admin (frontend)
- `src/api/superadmin.js` con listBusinesses, getBusiness, createBusiness, updateBusiness, deleteBusiness, uploadImage, uploadVideo
- `src/pages/SuperAdmin.jsx`: header morado/índigo, grid de cards con logo/nombre/slug/tipo/contadores users/services/appointments, modal "Nueva empresa" con 13 tipos
- Guard `SuperAdminRoute` en `App.jsx`; `ProtectedRoute` de /admin redirige a /superadmin si user es super_admin
- `Login.jsx` redirige según role tras login
- Botones en card: "Ajustes" (primario cyan), ExternalLink (ver landing), Trash2 (eliminar con confirm)
- **Probar**: login con super@demo.com/super123 → debe redirigir auto a /superadmin; click "Nueva empresa" → crear un spa/dentista; verificar que /admin con super admin redirige a /superadmin

## Bloque 3 — Catálogo en panel admin
- Backend: `productController.js`, `comboController.js` con CRUD + tenant check; `serviceController.js` extendido con folio/imageUrl/visible + CRUD de variantes en `/api/services/:id/variants`
- Rutas nuevas: `/api/products`, `/api/combos`, `/api/services/:id/variants`
- Todos usan `nextFolio` si no se pasa folio; validan pertenencia al business del user
- `productController` y `comboController` rechazan con P2002 (folio duplicado)
- `comboController.update` usa replace-all items en transacción
- Frontend: `src/api/admin.js` extendido con products/combos/variants + uploadImage; `src/pages/admin/Catalogo.jsx` con 3 tabs (Servicios/Productos/Combos), 3 toggles masivos arriba que patchean el business, modales por tipo, ImageField con upload
- Link "Catálogo" en `AdminSidebar.jsx` con ícono Package
- **Probar**: login admin@demo.com/admin123 → sidebar Catálogo → crear servicio con variantes ("3 sesiones", 3, 500), producto con imagen, combo con items; probar toggles masivos e íconos visible

## Bloque 4 — Ajustes branding (solo super admin)
- Backend: `upload.js` nuevo endpoint `POST /api/upload/video` (mp4/webm/mov hasta 50MB); `superAdminController.js` GET+PATCH `/businesses/:id` acepta TODOS los campos (slug, lat/lng, schedule, branding, redes, video, toggles); validación slug único al cambiar
- **Bloqueo crítico**: `businessController.update` del admin normal SOLO acepta phone/email/address/schedule. Branding está bloqueado para admins de empresa.
- Frontend: `src/pages/BusinessSettings.jsx` con 4 tabs (General/Branding/Redes/Visibilidad):
  - General: nombre, tipo, slug, descripción, tel, email, dirección, aboutUs, lat/lng, editor horarios por día con check cerrado/abierto
  - Branding: ColorField con input color + hex sincronizado, preview de botones en vivo, logo, 4 imágenes (hero/whyUs/cta/aboutUs), video con MediaField (preview reproducible)
  - Redes: IG, FB, TikTok, WhatsApp (con helper de formato "5218112345678")
  - Visibilidad: 3 toggles iOS-style para showServices/Products/Combos
- Header sticky con Guardar deshabilitado si no dirty; mensaje "✓ Guardado"
- **Probar**: login super admin → click "Ajustes" en card → cambiar colores y ver preview; subir imágenes; subir video .mp4; pon WhatsApp 5218112345678; toggles; Guardar → "✓ Guardado"
- **Probar restricción**: login admin@demo.com → sidebar NO muestra "Ajustes"; PUT /api/business con primaryColor NO se aplica

## Bloque 4.5 — Registro de Ventas del día
- Backend: `src/controllers/salesController.js` con list(date) que incluye totales agregados (total, byMethod, byType, count), create manual transaccional (resuelve nombres/precios server-side), update método de pago, addItem/removeItem con recálculo atómico del total, remove
- Helper `createSaleFromAppointment(tx, appointmentId)` idempotente (no duplica si ya existe) exportado
- `appointmentController.updateStatus` ahora transaccional: al pasar a `completed` auto-crea la venta con el servicio. Devuelve `{appointment, sale}`
- Rutas `/api/sales` con GET/POST/PATCH/DELETE + /:id/items
- Frontend: `src/api/admin.js` + 6 métodos; `src/pages/admin/Ventas.jsx` con selector de fecha, 4 stat cards (Total día, Transacciones, Servicios$, Productos+Combos$), desglose por método de pago (efectivo/tarjeta/transferencia/otro), lista de ventas con badge verde "Desde cita" o gris "Manual", select inline de método de pago, modal Nueva Venta con ItemPicker + carrito + total live, modal Editar para agregar ítems
- Link "Ventas del día" en sidebar con ícono Receipt
- **Probar**: login admin → sidebar Ventas del día → "Nueva venta" → elegir ítems del catálogo, método de pago, registrar; probar auto-create marcando cita como completed en Appointment Hub y volviendo a Ventas; cambiar fecha para ver días anteriores

## Bloque 5 — Landing dinámica
- Backend `businessController.getBySlug` incluye services/products/combos filtrados por visible + variantes; respeta toggles masivos (showServices/Products/Combos=false → array vacío)
- `ServicesGrid.jsx` reescrito con tabs Servicios/Productos/Combos (solo si hay contenido en cada uno), ServiceCard con chips de variantes, ProductCard con botón verde "Pedir por WhatsApp" (wa.me/<número>?text=Hola! Me interesa el producto "X"...), ComboCard con lista de ítems y precio de paquete
- `AboutUs.jsx` video dinámico `business.videoUrl` con fallback `/videobarber.mp4`, `key={videoUrl}` para re-render
- `InstagramFeed.jsx` íconos FB/TikTok/WhatsApp dinámicos (solo aparecen si están configurados)
- `Landing.jsx`: ELIMINADO el modal flotante de "Personalizar" y el botón Settings. Botón flotante verde de WhatsApp abajo-derecha si `whatsappUrl` configurado. Archivo pasó de 292 → 124 líneas
- **Clínica San Rafael preservada**: verificado con curl que hero/cta/instagram/services siguen cargando; video usa fallback porque no tiene videoUrl aún
- **Probar**: abrir /clinica-san-rafael como visitante sin login → verificar que imagen hero, video AboutUs, Instagram posts, parallax CTA siguen funcionando; ya NO aparece botón "Personalizar"; si configuras WhatsApp en Ajustes aparece botón verde flotante; crear producto en catálogo de barbería → landing muestra tab Productos con botón WhatsApp

## Archivos clave creados/modificados
### Backend
- prisma/schema.prisma
- prisma/migrations/20260408013500_bloque1_multitenant_catalogo_ventas/migration.sql (con backfill SQL de folios)
- src/middleware/auth.js (requireSuperAdmin)
- src/controllers/superAdminController.js (nuevo)
- src/controllers/businessController.js (getBySlug extendido, update bloqueado)
- src/controllers/serviceController.js (variantes + folio + visible)
- src/controllers/productController.js (nuevo)
- src/controllers/comboController.js (nuevo)
- src/controllers/salesController.js (nuevo)
- src/controllers/appointmentController.js (updateStatus auto-crea sale)
- src/routes/superAdmin.js, products.js, combos.js, sales.js (nuevos)
- src/routes/upload.js (+ endpoint /video)
- src/utils/folio.js (nuevo)
- scripts/resetSuperAdmin.js (nuevo)

### Frontend
- src/api/superadmin.js (nuevo)
- src/api/admin.js (extendido con catalog, sales, upload)
- src/pages/SuperAdmin.jsx (nuevo)
- src/pages/BusinessSettings.jsx (nuevo)
- src/pages/admin/Catalogo.jsx (nuevo)
- src/pages/admin/Ventas.jsx (nuevo)
- src/pages/Landing.jsx (simplificado: 292→124 líneas)
- src/components/landing/ServicesGrid.jsx (reescrito con tabs)
- src/components/landing/AboutUs.jsx (video dinámico)
- src/components/landing/InstagramFeed.jsx (redes dinámicas)
- src/components/layout/AdminSidebar.jsx (links Catálogo + Ventas)
- src/App.jsx (rutas /superadmin, /superadmin/business/:id, /admin/catalogo, /admin/ventas)
- src/pages/Login.jsx (redirect según rol)

**Why:** El usuario arrancó este sprint el 8 abril 2026 para vender demo del SaaS multi-tenant este fin de semana a barberías, estéticas, consultorios médicos, dentistas y spas.

**How to apply:** Si se retoma el trabajo, el siguiente paso es Bloque 6 (hardening: rate limit login, zod/joi validación, CORS prod, no stack traces, verificar no raw SQL). Antes de codear consultar al usuario el plan (regla de feedback_dates_confirmar_antes.md).
