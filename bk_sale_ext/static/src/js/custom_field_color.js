/** @odoo-module **/

import { registry } from "@web/core/registry";
import { FloatField, floatField } from "@web/views/fields/float/float_field";
import { onMounted } from "@odoo/owl";

export class ColorValueWidget extends FloatField {
    setup() {
        super.setup();
        console.log("Setup started...");
        onMounted(this._onMounted.bind(this)); // Привязываем контекст
    }

    async _onMounted() {
        console.log("_onMounted called");
        this._setColor();
    }

    _setColor() {
        console.log("_setColor called");
        console.log("this called", this);
        const value = this.value;
        if (value < 10) {
            this.inputRef.el.style.backgroundColor = 'green';
        } else if (value > 10) {
            this.inputRef.el.style.backgroundColor = 'red';
        } else if (value === 0.0) {
            this.inputRef.el.style.backgroundColor = '';
        }
    }
}

ColorValueWidget.supportedTypes = ["float"];

const colorValueWidgetField = {
    ...floatField,
    component: ColorValueWidget,
};

registry.category("fields").add("color_widget", colorValueWidgetField);
