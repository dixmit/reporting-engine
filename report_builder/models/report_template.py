# Copyright 2025 Dixmit
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ReportTemplate(models.Model):
    _name = "report.template"
    _description = "Template"

    name = fields.Char(required=True)
    source = fields.Selection(
        [("account", "Account")],
        required=True,
        default="account",
    )
    kpi_ids = fields.One2many(
        "report.template.kpi",
        "template_id",
    )
    style_id = fields.Many2one("report.style")
