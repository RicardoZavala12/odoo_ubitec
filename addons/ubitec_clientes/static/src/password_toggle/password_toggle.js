/** @odoo-module **/

import { registry } from "@web/core/registry";
import { CharField, charField } from "@web/views/fields/char/char_field";
import { useState } from "@odoo/owl";

// Campo de texto con botón de ojito para mostrar/ocultar la contraseña.
export class PasswordToggleField extends CharField {
    static template = "ubitec_clientes.PasswordToggleField";

    setup() {
        super.setup();
        this.state = useState({ visible: false });
    }

    toggleVisibility() {
        this.state.visible = !this.state.visible;
    }

    get inputType() {
        return this.state.visible ? "text" : "password";
    }
}

export const passwordToggleField = {
    ...charField,
    component: PasswordToggleField,
    displayName: "Contraseña (ver/ocultar)",
    supportedTypes: ["char"],
};

registry.category("fields").add("password_toggle", passwordToggleField);
