---
name: Dates MVP - visión multi-tenant y super admin (brief abril 2026)
description: Requerimientos grandes del usuario para convertir Dates MVP en SaaS multi-tenant con super admin, módulos por permisos y panel por negocio
type: project
---

# Brief completo (dictado por el usuario, 8 abril 2026)

El usuario quiere evolucionar Dates MVP a un SaaS multi-tenant vendible como demo. Objetivos:

## 1. Super Admin (rol global)
- Único que puede **crear nuevas empresas/negocios**
- Al crear: elegir **tipo de negocio** (clínica, barbería, dentista, spa, consultorio genérico…) vía select
- Cada tipo define lógica/terminología (clínica→consultorios, barbería→estaciones, dentista→consultorios, etc.)
- Super admin puede **habilitar/deshabilitar módulos por empresa** (sistema de permisos por módulo)
- Módulos previstos: Appointment Hub, Especialistas, Cabinas/Salas, Clientes, **futuro: Punto de Venta**
- Super admin crea también los **admins de cada empresa**
- Admin de empresa crea empleados, cabinas, consultorios, clientes

## 2. Panel por empresa (multi-tenant por URL)
- Cada negocio tiene su panel en `/admin/:slug/` (ej: `/admin/clinica-san-rafael/`)
- Login **configurable y personalizable por empresa** (logo, colores, fondo)
- El logo de la empresa debe mostrarse en su panel (lo verá el cliente/admin)
- Los módulos visibles dependen de los permisos asignados por el super admin

## 3. Configuración visual dinámica (desde panel admin, no desde landing)
Todo lo siguiente debe ser editable desde una sección **Ajustes** del panel de cada empresa:
- Imágenes de fondo (hero, whyUs, cta, aboutUs)
- **Video** de la sección Sobre Nosotros (actualmente hardcoded `/videobarber.mp4`)
- **Colores de botones** y de divs/cards (primario, secundario)
- Links de redes sociales: Instagram, Facebook, **WhatsApp** (falta agregar ícono de WhatsApp en el footer/navbar)
- Textos: hero, CTA, sobre nosotros — todo dinámico

## 4. Roles jerárquicos
- **Super Admin** (global): crea empresas, admins, gestiona módulos/permisos
- **Admin Empresa**: gestiona su propio negocio (empleados, cabinas, clientes, ajustes)
- **Empleado**: acceso limitado según permisos
- **Cliente**: agenda citas desde landing pública

## 5. Cómo entrar como super admin
El usuario preguntó cómo acceder. Propuesta (pendiente de confirmar): ruta oculta `/superadmin` o flag `role: SUPER_ADMIN` en tabla User, login normal detecta rol y redirige a panel global `/superadmin/businesses`.

## 6. Visión a futuro
- Punto de Venta como módulo opcional habilitable por empresa
- Meta inmediata: tener algo vendible como demo

**Why:** El usuario quiere empezar a vender el producto; necesita que sea multi-tenant de verdad, con personalización por cliente y control centralizado.

**How to apply:** Toda decisión de arquitectura en Dates MVP debe considerar multi-tenancy desde ya. Schema Prisma debe reflejar: User.role (SUPER_ADMIN|ADMIN|EMPLOYEE|CUSTOMER), Business.type, Business.enabledModules (JSON array), relación User↔Business. Landing y panel deben leer config desde BD, no hardcodear.
