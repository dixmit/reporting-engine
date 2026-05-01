# Copyright 2025 Dixmit
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from collections import defaultdict

from odoo import fields, models
from odoo.osv.expression import OR
from odoo.tools.safe_eval import safe_eval


class ReportTemplateKpiItem(models.Model):
    _name = "report.template.kpi.item"
    _description = "Report Template Kpi Item"  # TODO

    kind = fields.Selection(
        [("query", "Query"), ("kpi", "KPI")],
        default="query",
    )
    parent_kpi_id = fields.Many2one(
        "report.template.kpi",
        ondelete="cascade",
        required=True,
    )
    kpi_id = fields.Many2one(
        "report.template.kpi",
        ondelete="cascade",
        domain="[('template_id', '=', template_id), ('id', '!=', parent_kpi_id)]",
    )
    query_kind_id = fields.Many2one(
        "report.template.kpi.query.kind",
        domain="[('source', '=', source)]",
    )
    code = fields.Char()
    source = fields.Selection(related="parent_kpi_id.template_id.source", store=True)
    domain = fields.Char(help="Domain to filter the records for this KPI item. ")
    template_id = fields.Many2one(
        related="parent_kpi_id.template_id",
    )
    positive = fields.Boolean(
        help="If checked, the KPI item will be considered positive. "
        "If not checked, it will be considered negative.",
        default=True,
    )

    def _get_kpi_data(self, cols, kpi_data):
        """
        Process the KPI item and return the data for the KPI.
        This method should be overridden in subclasses if needed.
        """
        value = defaultdict(lambda: {"total": 0, "values": defaultdict(lambda: 0)})
        for item in self:
            item._get_kpi_value(cols, kpi_data, value)
        return value

    def _get_kpi_value(self, cols, kpi_data, value):
        """
        Get the value for the KPI item.
        This method should be overridden in subclasses if needed.
        """
        for col in cols:
            multiplier = 1 if self.positive else -1
            values = {}
            if self.kind == "query":
                kpi_value, values = getattr(
                    self, f"_get_kpi_value_{self.source}_{self.query_kind_id.code}"
                )(col)
            elif self.kind == "kpi":
                kpi_value = kpi_data.get(self.kpi_id.id, {}).get(col["id"], 0)["total"]
                values = (
                    kpi_data.get(self.kpi_id.id, {})
                    .get(col["id"], {})
                    .get("values", {})
                )
            for val in values:
                value[col["id"]]["values"][val] += multiplier * values[val]
            value[col["id"]]["total"] += multiplier * kpi_value

    def _get_kpi_account_domain(self, col, date_format="balance"):
        domain = []
        if self.domain:
            domain += safe_eval(self.domain)
        if self.code:
            domain += OR(
                [
                    [("account_id.code", "=ilike", code.strip())]
                    for code in self.code.split(",")
                ]
            )
        if date_format == "balance":
            domain += [
                ("date", ">=", col["date_from"]),
                ("date", "<=", col["date_to"]),
            ]
        elif date_format == "initial":
            domain += [
                ("date", "<", col["date_from"]),
            ]
        elif date_format == "ending":
            domain += [
                ("date", "<=", col["date_to"]),
            ]
        return domain

    def _get_kpi_value_account_balp(self, col):
        domain = self._get_kpi_account_domain(col, date_format="balance")
        values = self.env["account.move.line"]._read_group(
            domain, groupby=("account_id", "company_id"), aggregates=("balance:sum",)
        )
        return sum(val[2] for val in values), {
            f"{val[0].code} - {val[0].name} [{val[1].name}]": val[2] for val in values
        }

    def _get_kpi_value_account_bali(self, col):
        domain = self._get_kpi_account_domain(col, date_format="initial")
        values = self.env["account.move.line"]._read_group(
            domain, groupby=("account_id", "company_id"), aggregates=("balance:sum",)
        )
        return sum(val[2] for val in values), {
            f"{val[0].code} - {val[0].name} [{val[1].name}]": val[2] for val in values
        }

    def _get_kpi_value_account_bale(self, col):
        domain = self._get_kpi_account_domain(col, date_format="ending")
        values = self.env["account.move.line"]._read_group(
            domain, groupby=("account_id", "company_id"), aggregates=("balance:sum",)
        )
        return sum(val[2] for val in values), {
            f"{val[0].code} - {val[0].name} [{val[1].name}]": val[2] for val in values
        }

    def _get_kpi_value_account_crdp(self, col):
        domain = self._get_kpi_account_domain(col, date_format="balance")
        values = self.env["account.move.line"]._read_group(
            domain, groupby=("account_id", "company_id"), aggregates=("credit:sum",)
        )
        return sum(val[2] for val in values), {
            f"{val[0].code} - {val[0].name} [{val[1].name}]": val[2] for val in values
        }

    def _get_kpi_value_account_crdi(self, col):
        domain = self._get_kpi_account_domain(col, date_format="initial")
        values = self.env["account.move.line"]._read_group(
            domain, groupby=("account_id", "company_id"), aggregates=("credit:sum",)
        )
        return sum(val[2] for val in values), {
            f"{val[0].code} - {val[0].name} [{val[1].name}]": val[2] for val in values
        }

    def _get_kpi_value_account_crde(self, col):
        domain = self._get_kpi_account_domain(col, date_format="ending")
        values = self.env["account.move.line"]._read_group(
            domain, groupby=("account_id", "company_id"), aggregates=("credit:sum",)
        )
        return sum(val[2] for val in values), {
            f"{val[0].code} - {val[0].name} [{val[1].name}]": val[2] for val in values
        }

    def _get_kpi_value_account_debp(self, col):
        domain = self._get_kpi_account_domain(col, date_format="balance")
        values = self.env["account.move.line"]._read_group(
            domain, groupby=("account_id", "company_id"), aggregates=("debit:sum",)
        )
        return sum(val[2] for val in values), {
            f"{val[0].code} - {val[0].name} [{val[1].name}]": val[2] for val in values
        }

    def _get_kpi_value_account_debi(self, col):
        domain = self._get_kpi_account_domain(col, date_format="initial")
        values = self.env["account.move.line"]._read_group(
            domain, groupby=("account_id", "company_id"), aggregates=("debit:sum",)
        )
        return sum(val[2] for val in values), {
            f"{val[0].code} - {val[0].name} [{val[1].name}]": val[2] for val in values
        }

    def _get_kpi_value_account_debe(self, col):
        domain = self._get_kpi_account_domain(col, date_format="ending")
        values = self.env["account.move.line"]._read_group(
            domain, groupby=("account_id", "company_id"), aggregates=("debit:sum",)
        )
        return sum(val[2] for val in values), {
            f"{val[0].code} - {val[0].name} [{val[1].name}]": val[2] for val in values
        }
