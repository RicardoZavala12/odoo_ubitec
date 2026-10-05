# -*- coding: utf-8 -*-
from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    gps_telegram_enabled = fields.Boolean(
        string="Activar notificaciones por Telegram",
        config_parameter="gps_service.telegram_enabled",
    )
    gps_telegram_token = fields.Char(
        string="Token del bot",
        config_parameter="gps_service.telegram_token",
    )
    gps_telegram_chat_id = fields.Char(
        string="Chat ID",
        config_parameter="gps_service.telegram_chat_id",
    )
