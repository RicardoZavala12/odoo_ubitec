/** @odoo-module **/

import { registry } from "@web/core/registry";

// Oculta el icono de gota (Preferencias del Menu Aplicaciones, de
// web_responsive) de la barra superior: no aporta nada al negocio y
// confunde a los usuarios.
registry.category("systray").remove("AppMenuTheme");
