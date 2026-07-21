---
name: Dates MVP - catálogo flexible (servicios, productos, combos, sesiones)
description: Reglas de negocio del catálogo que cada empresa puede dar de alta en Dates MVP, con combos, sesiones por servicio y visibilidad por check
type: project
---

# Catálogo por empresa (Dates MVP)

Cada negocio puede dar de alta tres tipos de ítems en su catálogo:

## 1. Servicios
- Tienen **sesiones/variantes** con costo individual (ej: "Tinte — 1 sesión $500", "Tinte — paquete 3 sesiones $1200")
- Cada variante = su propio precio y posiblemente su propia duración
- Ejemplos: consulta médica, corte de pelo, limpieza dental, masaje

## 2. Productos
- Ítems físicos que el negocio vende (shampoo, cremas, cepillos, etc.)
- Precio fijo, sin sesiones
- En el futuro se enlazan con el módulo Punto de Venta

## 3. Combos
- Combinación de servicio(s) + producto(s) con precio especial
- Ej: "Corte + shampoo premium $350"

## Visibilidad en la landing (lo que ve el cliente)
Cada ítem tiene un **check `visible`** individual para mostrarse o no en la lista pública.
Además, el admin puede hacer **toggles masivos** en la sección del catálogo:
- ☑ Mostrar todos los productos
- ☑ Mostrar todos los servicios
- ☑ Mostrar todos los combos

El cliente en la landing verá la lista filtrada según estos checks. Los no visibles siguen existiendo en BD (para uso interno, reportes, POS futuro) pero no se muestran en la web pública.

## Imágenes
Cada ítem (servicio, producto, combo) tiene **una imagen propia** que se muestra en la card.

## IDs / folios
Cada ítem tiene un **ID/folio** que el cliente puede:
- Dejar que el sistema lo genere automáticamente (ej: SRV-0001, PRD-0001, CMB-0001)
- O definirlo manualmente con un formato propio (ej: "CLINICA-CONS-001")
Regla: el folio es único por empresa.

## Relación con tipos de empresa (del brief multi-tenant)
- **Barbería / estética**: servicios con sesiones (cortes, tratamientos), productos (shampoos, ceras), combos
- **Clínica / consultorio médico**: servicios (consultas, exámenes), productos opcionales, combos raros
- **Dentista**: servicios (limpiezas, ortodoncia con sesiones), productos (cepillos, enjuagues), combos
- Cada tipo de empresa mostrará por default los módulos/categorías relevantes, pero el admin puede ajustar

## Meta del usuario
Vender el SaaS **este fin de semana** a barberías, estéticas, consultorios médicos y dentistas. Por eso el alcance debe recortarse al MÍNIMO que permita: crear empresa, configurar branding, dar de alta catálogo (con los 3 tipos), y que la landing funcione para agendar.

**Why:** El usuario lo dictó el 8 abril 2026 y es requisito para poder ofrecer demos reales a los cuatro nichos.

**How to apply:** Al modelar el schema Prisma: crear modelos `Product`, `Combo`, `ServiceVariant` (o `ServiceSession`), con campo `visible` boolean en cada uno, `imageUrl`, `folio` único por business. Los endpoints y el panel admin deben respetar estos checks. La landing debe filtrar por `visible=true`.
