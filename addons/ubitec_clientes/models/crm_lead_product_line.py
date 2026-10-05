# -*- coding: utf-8 -*-
from odoo import api, fields, models


class CrmLeadProductLine(models.Model):
    _name = "crm.lead.product.line"
    _description = "Producto en una oportunidad de Ubitec"

    lead_id = fields.Many2one("crm.lead", required=True, ondelete="cascade")
    product_id = fields.Many2one("product.product", string="Producto", required=True)
    quantity = fields.Float(string="Cantidad", default=1.0, required=True)
    price_unit = fields.Float(string="Precio unitario")
    subtotal = fields.Float(string="Subtotal", compute="_compute_subtotal", store=True)

    @api.depends("quantity", "price_unit")
    def _compute_subtotal(self):
        for line in self:
            line.subtotal = line.quantity * line.price_unit

    @api.onchange("product_id")
    def _onchange_product_id(self):
        for line in self:
            if line.product_id:
                line.price_unit = line.product_id.list_price
