---
name: ubitec-mensaje-para-el-cliente-sobre-facturaci-n-contpaqi
description: Documento listo para mandar al cliente/CONTPAQi pidiendo la API de timbrado correcta
metadata: 
  node_type: memory
  type: reference
  originSessionId: eb02eef8-ae7b-4cdf-9888-8040b31f6d06
  modified: 2026-07-24T19:27:39.129Z
---

# 📋 Requisitos para facturar (CFDI) desde Odoo con CONTPAQi

> Para mandar/confirmar con el cliente Ubitec y su contacto de CONTPAQi.

## ⚠️ ACLARACIÓN (lo que ya dieron NO es lo que se necesita)
El acceso compartido es de **"CONTPAQi CFDI Facturación en Línea +"** (portal cfdi.com.mx,
usuario OIRL870504190), que sirve para **facturar A MANO** en el navegador. Ese portal
**NO se puede integrar a Odoo**. Para conectar Odoo se necesita OTRO producto: la
**API de Timbrado (CONTPAQi Timbra)**.

## ✅ Lo que necesitamos confirmar / entregar

### 1. Datos fiscales de Ubitec
- [ ] RFC · Razón social · Régimen fiscal · Domicilio fiscal (CP)

### 2. CSD (Certificado de Sello Digital) — obligatorio para timbrar
- [ ] `.cer` + `.key` + contraseña del `.key` (los del SAT; si ya facturan, ya los tienen)

### 3. API de Timbrado de CONTPAQi (lo clave para integrar)
- [ ] ¿Tienen activa la **API de Timbrado (CONTPAQi Timbra)** en CONTPAQi Nube?
- [ ] Acceso al **portal de desarrolladores** (developers.contpaqinube.com)
- [ ] **Credenciales de la API** (usuario / API key / tokens)
- [ ] **Documentación técnica** (endpoints, auth, formato XML)

### 4. Timbres
- [ ] ¿Cuántos timbres incluye su plan? (se ofrecieron ~150/mes)
- [ ] ¿La API está incluida en la licencia o cuesta aparte?

## Mensaje sugerido para CONTPAQi
> "El acceso que me dieron es del **portal de facturación manual** (CFDI Facturación en
> Línea +). Para conectarlo con Odoo necesito la **API de Timbrado (CONTPAQi Timbra)**,
> que es un producto diferente. ¿La tienen activa o me pueden dar acceso al portal de
> desarrolladores de CONTPAQi con las credenciales de la API?"

## Alternativa (si CONTPAQi complica la API)
PAC con API sencilla para Odoo Community: **Finkok** o **Facturama**. Solo se necesitan
los CSD del cliente + comprar timbres.
