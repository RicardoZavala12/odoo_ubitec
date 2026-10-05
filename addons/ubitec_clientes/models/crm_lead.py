# -*- coding: utf-8 -*-
import base64

from odoo import api, fields, models


class CrmLead(models.Model):
    _inherit = "crm.lead"

    product_line_ids = fields.One2many(
        "crm.lead.product.line", "lead_id", string="Productos"
    )
    amount_total = fields.Float(
        string="Total productos", compute="_compute_amount_total", store=True
    )

    @api.depends("product_line_ids.subtotal")
    def _compute_amount_total(self):
        for lead in self:
            lead.amount_total = sum(lead.product_line_ids.mapped("subtotal"))

    @api.onchange("product_line_ids", "amount_total")
    def _onchange_product_line_ids(self):
        for lead in self:
            lead.expected_revenue = lead.amount_total
            if lead.product_line_ids:
                lead.name = ", ".join(
                    lead.product_line_ids.mapped("product_id.name")
                )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get("name") and vals.get("product_line_ids"):
                vals["name"] = "Nueva oportunidad"
        leads = super().create(vals_list)
        leads._sync_from_products()
        return leads

    def write(self, vals):
        res = super().write(vals)
        if "product_line_ids" in vals:
            self._sync_from_products()
        return res

    def _sync_from_products(self):
        for lead in self:
            if not lead.product_line_ids:
                continue
            if not lead.name or lead.name == "Nueva oportunidad":
                lead.name = ", ".join(lead.product_line_ids.mapped("product_id.name"))
            if lead.expected_revenue != lead.amount_total:
                lead.expected_revenue = lead.amount_total

    is_quote_sent_stage = fields.Boolean(compute="_compute_is_quote_sent_stage")
    is_won_stage = fields.Boolean(compute="_compute_is_won_stage")

    @api.depends("stage_id")
    def _compute_is_quote_sent_stage(self):
        stage = self.env.ref("crm.stage_lead3", raise_if_not_found=False)
        for lead in self:
            lead.is_quote_sent_stage = bool(stage) and lead.stage_id.id == stage.id

    @api.depends("stage_id")
    def _compute_is_won_stage(self):
        stage = self.env.ref("crm.stage_lead4", raise_if_not_found=False)
        for lead in self:
            lead.is_won_stage = bool(stage) and lead.stage_id.id == stage.id

    def _attach_report_and_open_composer(self, report_xmlid, filename):
        self.ensure_one()
        report = self.env.ref(report_xmlid)
        pdf_content, _ = report._render_qweb_pdf(report_xmlid, self.ids)
        attachment = self.env["ir.attachment"].create({
            "name": filename,
            "type": "binary",
            "datas": base64.b64encode(pdf_content),
            "res_model": "crm.lead",
            "res_id": self.id,
            "mimetype": "application/pdf",
        })
        compose_form = self.env.ref("mail.email_compose_message_wizard_form")
        ctx = {
            "default_model": "crm.lead",
            "default_res_ids": self.ids,
            "default_composition_mode": "comment",
            "default_partner_ids": self.partner_id.ids,
            "default_attachment_ids": [(4, attachment.id)],
        }
        return {
            "name": "Enviar correo",
            "type": "ir.actions.act_window",
            "view_mode": "form",
            "res_model": "mail.compose.message",
            "views": [(compose_form.id, "form")],
            "view_id": compose_form.id,
            "target": "new",
            "context": ctx,
        }

    def action_send_quote_email(self):
        return self._attach_report_and_open_composer(
            "ubitec_clientes.action_report_crm_quote", "Cotizacion.pdf"
        )

    def action_send_welcome_email(self):
        return self._attach_report_and_open_composer(
            "ubitec_clientes.action_report_crm_welcome", "Bienvenida.pdf"
        )
