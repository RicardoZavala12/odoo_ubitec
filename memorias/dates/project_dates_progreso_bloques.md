---
name: Dates MVP - progreso por bloques (fin de semana abril 2026)
description: Estado de avance del plan recortado de Dates MVP dividido en bloques para llegar al fin de semana con un demo vendible
type: project
---

# Progreso del sprint fin de semana (iniciado 8 abril 2026)

Plan recortado para ofrecer el SaaS a barberías, estéticas, consultorios médicos, dentistas y spas.

## ✅ Bloque 1 — Schema + super admin backend (TERMINADO)
- Prisma migrado con nuevos modelos: `ServiceVariant`, `Product`, `Combo`, `ComboItem`, `Sale`, `SaleItem`
- Nuevos enums: `UserRole.super_admin`, `BusinessType` con `spa`, `clinica_estetica`, `clinica_medica`, `dentista`, `estetica`; `CatalogItemType`, `SaleItemType`, `PaymentMethod`
- `Business` ganó: `facebookUrl`, `tiktokUrl`, `whatsappUrl`, `videoUrl`, `showServices/Products/Combos`
- `Service/Product/Combo` tienen `folio` único por business, `imageUrl`, `visible`
- Folios de servicios existentes backfilleados SRV-0001..SRV-0004 por business
- Middleware `requireSuperAdmin` y `requireRole(...)` en src/middleware/auth.js
- Script `npm run reset-super-pass [email] [password]` (scripts/resetSuperAdmin.js)
- Super admin creado: `super@demo.com` / `super123` (businessId=null)
- Endpoints CRUD en `/api/superadmin/businesses` (GET, POST, PATCH, DELETE) con delete en cascada manual
- businessController actualizado con los campos nuevos vía pickFields
- Probado end-to-end con curl: login, list, create (spa), 403 a non-super, delete

## ✅ Bloque 2 — Panel Super Admin frontend (TERMINADO)
- src/api/superadmin.js con los 4 métodos
- src/pages/SuperAdmin.jsx: header morado/índigo, grid de cards con logo/nombre/slug/tipo/contadores, modal "Nueva empresa" con 13 tipos incluidos spa/dentista/clinica_estetica
- Guard SuperAdminRoute en App.jsx, ruta /superadmin
- ProtectedRoute del /admin ahora redirige a /superadmin si el user es super_admin
- Login.jsx redirige según role tras login
- Botón "Ver landing" lleva a /<slug>; botón eliminar con confirm
- LIMITACIÓN: super admin NO puede entrar al panel admin de otras empresas (se pospuso impersonación para después)

## ✅ Bloque 3 — Catálogo en panel admin (TERMINADO)
Sección nueva /admin/catalogo con 3 tabs: Servicios / Productos / Combos.
- CRUD visual para cada uno (imagen, folio auto-generado editable, check visible, precio)
- En Servicios: sub-formulario de variantes/sesiones con precio
- Toggles masivos arriba: showServices/Products/Combos (del Business)
- Backend: falta crear endpoints CRUD /api/products, /api/combos, /api/service-variants

## ✅ Bloque 4 — Ajustes branding (TERMINADO — solo super admin)
Sección /superadmin/business/:id con 4 tabs (General, Branding, Redes, Visibilidad). Todo editable solo por super_admin. businessController.update bloqueado para admins normales (solo phone/email/address/schedule).

## ✅ Bloque 4.5 — Registro de Ventas del día (TERMINADO)
/admin/ventas con stats, desglose por método de pago, auto-creación de venta al marcar cita como completed vía salesController.createSaleFromAppointment.

## ✅ Bloque 5 — Landing dinámica (TERMINADO)
businessController.getBySlug incluye services/products/combos filtrados por visible + toggles masivos. ServicesGrid reescrito con tabs Servicios/Productos/Combos, variantes visibles, productos con botón "Pedir por WhatsApp" (wa.me/<whatsappUrl>). AboutUs video dinámico desde business.videoUrl con fallback /videobarber.mp4. InstagramFeed con íconos FB/TikTok/WhatsApp dinámicos. Landing tiene botón flotante WhatsApp. Modal "Personalizar" de landing ELIMINADO (ahora solo se edita desde /superadmin). Clínica San Rafael preservada sin romper Instagram/imágenes/video.

## ⏳ Bloque 6 — Hardening (viejo, no aplicado aún)
## ⏳ Bloque 6 — Hardening seguridad (al final)
- Rate limiting login
- Validación inputs con zod/joi
- CORS prod, no stack traces, confirmar que no hay raw SQL

**Why:** El usuario quiere vender demo este fin de semana.
**How to apply:** Al retomar, continuar desde el bloque marcado EN PROGRESO. Cada bloque se termina y se prueba antes de pasar al siguiente.
