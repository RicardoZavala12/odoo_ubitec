---
name: Dates MVP - Ajustes de branding SOLO editables por super admin
description: Regla de negocio crítica para Dates MVP — el branding (colores, imágenes, video, redes, ajustes visuales) solo lo puede cambiar el super admin, no el admin del negocio
type: project
---

# Regla: quién puede editar qué en el panel

En Dates MVP los ajustes visuales/branding de cada empresa **SOLO los puede modificar el SUPER ADMIN**, NO el admin/owner del propio negocio.

## Qué es "solo super admin"
- Colores (primaryColor, secondaryColor)
- Logo
- Imágenes de fondo (hero, whyUs, cta, aboutUs)
- Video de AboutUs
- Redes sociales (IG, FB, TikTok, WhatsApp)
- Datos generales del business (nombre, tipo, slug, dirección, email, teléfono)
- Toggles de visibilidad masiva (showServices/Products/Combos)

## Qué SÍ puede hacer el admin de la empresa
- Gestionar su catálogo (servicios, productos, combos, variantes) — CRUD
- Gestionar especialistas, cabinas, clientes, citas
- Marcar visibilidad individual de ítems del catálogo
- Ver ventas del día (cuando esté implementado)

## Implicaciones técnicas
- Los endpoints `PATCH /api/superadmin/businesses/:id` y `POST /api/superadmin/businesses` ya son restringidos a super_admin ✅
- El endpoint legacy `PUT /api/business` (businessController.update) actualmente permite que el owner edite su propio business — **debe restringirse** para que no acepte campos de branding, O el panel admin debe ocultar la sección de ajustes
- La sección "Ajustes" del branding debe vivir DENTRO del panel del super admin (`/superadmin`), no en `/admin/ajustes`
- Flujo: super admin → abre card de empresa → botón "Ajustes" → modal/página con tabs Branding/Redes/General
- El admin normal del negocio NO ve ningún link de "Ajustes" en su sidebar

## Razón de negocio
El usuario quiere vender el SaaS como servicio administrado: él (super admin) configura el branding de cada cliente, y el cliente solo se preocupa por operar su negocio (citas, catálogo, ventas). Es un modelo de SaaS gestionado, no self-service de branding.

**Why:** El usuario lo aclaró el 8 abril 2026: "recuerda que esos cambios solo los hara el super admin". Quiere control centralizado del look & feel de todas las empresas que vende.

**How to apply:** Cualquier UI o endpoint de edición de branding/business debe estar bajo `requireSuperAdmin`. El admin normal NO ve "Ajustes" en sidebar, NO puede cambiar colores/imágenes/redes. Si en el futuro se quiere permitir self-service, será opt-in por empresa.
