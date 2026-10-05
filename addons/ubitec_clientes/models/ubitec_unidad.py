# -*- coding: utf-8 -*-
from odoo import api, fields, models
from odoo.exceptions import UserError


class UbitecUnidad(models.Model):
    _name = "ubitec.unidad"
    _description = "Unidad / Equipo GPS de un cliente Ubitec"
    _rec_name = "imei"

    partner_id = fields.Many2one(
        "res.partner", string="Cliente", ondelete="cascade", index=True
    )
    imei = fields.Char(string="IMEI", index=True)
    folio = fields.Char(string="Folio", index=True)
    numero_serie = fields.Char(string="Número de serie")
    marca = fields.Char(string="Marca / Modelo")
    unidad = fields.Char(
        string="Unidad / Vehículo",
        help="Vehículo donde está instalado el GPS (ej. Freightliner blanco).",
    )
    plataforma = fields.Char(string="Plataforma")
    sim = fields.Char(string="SIM / Línea")
    icc = fields.Char(string="ICC")
    fecha_activacion = fields.Date(string="Fecha de activación")
    esquema = fields.Selection(
        selection=[
            ("venta", "Venta"),
            ("comodato", "Comodato"),
            ("migracion", "Migración"),
            ("otro", "Otro"),
        ],
        string="Esquema",
    )
    costo = fields.Float(string="Costo")
    forma_pago = fields.Char(string="Forma de pago")
    fecha_llegada = fields.Date(string="Fecha de llegada")
    fecha_instalacion = fields.Date(string="Fecha de instalación")
    estado = fields.Selection(
        selection=[
            ("stock", "En stock"),
            ("instalado", "Instalado"),
            ("baja", "Dado de baja"),
        ],
        string="Estado",
        default="instalado",
    )
    notas = fields.Text(string="Notas")

    # ── Suscripcion / cobro recurrente (punto 3 del alcance) ──
    contract_line_ids = fields.One2many(
        "contract.line", "ubitec_unidad_id", string="Suscripciones"
    )
    contract_line_count = fields.Integer(
        string="Nº suscripciones", compute="_compute_contract_line_count"
    )

    # ── Historial de movimientos (punto 4 del alcance) ──
    movimiento_ids = fields.One2many(
        "ubitec.unidad.movimiento", "unidad_id", string="Movimientos"
    )

    @api.depends("contract_line_ids")
    def _compute_contract_line_count(self):
        for unidad in self:
            unidad.contract_line_count = len(unidad.contract_line_ids)

    @api.model
    def _tipo_movimiento(self, estado_anterior, estado_nuevo):
        if estado_anterior == "baja" and estado_nuevo != "baja":
            return "reactivado"
        return {
            "stock": "entrada",
            "instalado": "instalado",
            "baja": "baja",
        }.get(estado_nuevo, "entrada")

    @api.model_create_multi
    def create(self, vals_list):
        unidades = super().create(vals_list)
        estado_label = dict(self._fields["estado"].selection)
        for unidad in unidades:
            self.env["ubitec.unidad.movimiento"].create({
                "unidad_id": unidad.id,
                "tipo": self._tipo_movimiento(False, unidad.estado),
                "estado_nuevo": estado_label.get(unidad.estado, unidad.estado),
                "partner_id": unidad.partner_id.id,
                "nota": "Alta del equipo",
            })
        return unidades

    def write(self, vals):
        estado_label = dict(self._fields["estado"].selection)
        antes = {
            unidad.id: (unidad.estado, unidad.partner_id)
            for unidad in self
        } if ("estado" in vals or "partner_id" in vals) else {}

        res = super().write(vals)

        for unidad in self:
            estado_antes, partner_antes = antes.get(unidad.id, (None, None))
            if "estado" in vals and vals["estado"] != estado_antes:
                self.env["ubitec.unidad.movimiento"].create({
                    "unidad_id": unidad.id,
                    "tipo": self._tipo_movimiento(estado_antes, vals["estado"]),
                    "estado_anterior": estado_label.get(estado_antes, estado_antes),
                    "estado_nuevo": estado_label.get(vals["estado"], vals["estado"]),
                    "partner_id": unidad.partner_id.id,
                })
            elif "partner_id" in vals and partner_antes is not None and vals["partner_id"] != partner_antes.id:
                self.env["ubitec.unidad.movimiento"].create({
                    "unidad_id": unidad.id,
                    "tipo": "reasignado",
                    "partner_id": vals["partner_id"],
                    "nota": "Antes: %s" % (partner_antes.name or "(sin cliente)"),
                })
        return res

    def _crear_suscripcion(self, rule_type):
        self.ensure_one()
        if not self.partner_id:
            raise UserError("Este equipo no tiene cliente asignado, asígnalo primero.")
        producto = self.env.ref("ubitec_clientes.product_monitoreo_gps", raise_if_not_found=False)
        if not producto:
            raise UserError("No se encontró el producto 'Monitoreo GPS' en el catálogo.")
        precio = (
            self.partner_id.ubitec_anualidad
            if rule_type == "yearly"
            else self.partner_id.ubitec_mensualidad
        )
        contract = self.env["contract.contract"].create({
            "name": "Monitoreo - %s - %s" % (self.partner_id.name, self.imei or self.folio or self.id),
            "partner_id": self.partner_id.id,
            "contract_type": "sale",
            "contract_line_ids": [(0, 0, {
                "product_id": producto.id,
                "name": producto.name,
                "quantity": 1,
                "automatic_price": False,
                "specific_price": precio,
                "recurring_rule_type": rule_type,
                "recurring_interval": 1,
                "recurring_invoicing_type": "pre-paid",
                "date_start": fields.Date.context_today(self),
                "ubitec_unidad_id": self.id,
            })],
        })
        return contract

    def _abrir_contrato(self, contract):
        return {
            "type": "ir.actions.act_window",
            "res_model": "contract.contract",
            "view_mode": "form",
            "res_id": contract.id,
            "target": "current",
        }

    def action_crear_plan_mensual(self):
        return self._abrir_contrato(self._crear_suscripcion("monthly"))

    def action_crear_plan_anual(self):
        return self._abrir_contrato(self._crear_suscripcion("yearly"))

    def action_ver_suscripcion(self):
        self.ensure_one()
        contratos = self.contract_line_ids.mapped("contract_id")
        if len(contratos) == 1:
            return self._abrir_contrato(contratos)
        return {
            "type": "ir.actions.act_window",
            "res_model": "contract.contract",
            "view_mode": "list,form",
            "domain": [("id", "in", contratos.ids)],
            "target": "current",
        }
