# Copyright 2025 Dixmit
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).


from odoo import models
from odoo.osv.expression import OR
from odoo.tools.safe_eval import safe_eval


class ReportTemplateKpiItem(models.Model):
    _inherit = "report.template.kpi.item"

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

    def _get_kpi_value_account_balp(self, col, domain=None):
        account_domain = self._get_kpi_account_domain(col, date_format="balance")
        if domain:
            account_domain += domain
        values = self.env["account.move.line"]._read_group(
            account_domain,
            groupby=("account_id", "company_id"),
            aggregates=("balance:sum",),
        )
        return sum(val[2] for val in values), {
            f"{val[0].code} - {val[0].name} [{val[1].name}]": val[2] for val in values
        }

    def _get_kpi_value_account_bali(self, col, domain=None):
        account_domain = self._get_kpi_account_domain(col, date_format="initial")
        if domain:
            account_domain += domain
        values = self.env["account.move.line"]._read_group(
            account_domain,
            groupby=("account_id", "company_id"),
            aggregates=("balance:sum",),
        )
        return sum(val[2] for val in values), {
            f"{val[0].code} - {val[0].name} [{val[1].name}]": val[2] for val in values
        }

    def _get_kpi_value_account_bale(self, col, domain=None):
        account_domain = self._get_kpi_account_domain(col, date_format="ending")
        if domain:
            account_domain += domain
        values = self.env["account.move.line"]._read_group(
            account_domain,
            groupby=("account_id", "company_id"),
            aggregates=("balance:sum",),
        )
        return sum(val[2] for val in values), {
            f"{val[0].code} - {val[0].name} [{val[1].name}]": val[2] for val in values
        }

    def _get_kpi_value_account_crdp(self, col, domain=None):
        account_domain = self._get_kpi_account_domain(col, date_format="balance")
        if domain:
            account_domain += domain
        values = self.env["account.move.line"]._read_group(
            account_domain,
            groupby=("account_id", "company_id"),
            aggregates=("credit:sum",),
        )
        return sum(val[2] for val in values), {
            f"{val[0].code} - {val[0].name} [{val[1].name}]": val[2] for val in values
        }

    def _get_kpi_value_account_crdi(self, col, domain=None):
        account_domain = self._get_kpi_account_domain(col, date_format="initial")
        if domain:
            account_domain += domain
        values = self.env["account.move.line"]._read_group(
            account_domain,
            groupby=("account_id", "company_id"),
            aggregates=("credit:sum",),
        )
        return sum(val[2] for val in values), {
            f"{val[0].code} - {val[0].name} [{val[1].name}]": val[2] for val in values
        }

    def _get_kpi_value_account_crde(self, col, domain=None):
        account_domain = self._get_kpi_account_domain(col, date_format="ending")
        if domain:
            account_domain += domain
        values = self.env["account.move.line"]._read_group(
            account_domain,
            groupby=("account_id", "company_id"),
            aggregates=("credit:sum",),
        )
        return sum(val[2] for val in values), {
            f"{val[0].code} - {val[0].name} [{val[1].name}]": val[2] for val in values
        }

    def _get_kpi_value_account_debp(self, col, domain=None):
        account_domain = self._get_kpi_account_domain(col, date_format="balance")
        if domain:
            account_domain += domain
        values = self.env["account.move.line"]._read_group(
            account_domain,
            groupby=("account_id", "company_id"),
            aggregates=("debit:sum",),
        )
        return sum(val[2] for val in values), {
            f"{val[0].code} - {val[0].name} [{val[1].name}]": val[2] for val in values
        }

    def _get_kpi_value_account_debi(self, col, domain=None):
        account_domain = self._get_kpi_account_domain(col, date_format="initial")
        if domain:
            account_domain += domain
        values = self.env["account.move.line"]._read_group(
            account_domain,
            groupby=("account_id", "company_id"),
            aggregates=("debit:sum",),
        )
        return sum(val[2] for val in values), {
            f"{val[0].code} - {val[0].name} [{val[1].name}]": val[2] for val in values
        }

    def _get_kpi_value_account_debe(self, col, domain=None):
        account_domain = self._get_kpi_account_domain(col, date_format="ending")
        if domain:
            account_domain += domain
        values = self.env["account.move.line"]._read_group(
            account_domain,
            groupby=("account_id", "company_id"),
            aggregates=("debit:sum",),
        )
        return sum(val[2] for val in values), {
            f"{val[0].code} - {val[0].name} [{val[1].name}]": val[2] for val in values
        }
