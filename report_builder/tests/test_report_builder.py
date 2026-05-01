# Copyright 2026 Dixmit
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo_test_helper import FakeModelLoader

from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase


class TestReportBuilder(TransactionCase):
    def setUp(self):
        super().setUp()
        self.loader = FakeModelLoader(self.env, self.__module__)
        self.loader.backup_registry()
        from .fake_models import (
            ReportingDummyModel,
            ReportTemplateKpiItem,
            ReportTemplateKpiQueryKind,
        )

        self.loader.update_registry(
            (
                ReportingDummyModel,
                ReportTemplateKpiQueryKind,
                ReportTemplateKpiItem,
            )
        )
        self.addCleanup(self.loader.restore_registry)
        self.style = self.env["report.style"].create(
            {"name": "Style", "font_size": "medium", "font_size_inherit": False}
        )
        self.style_01 = self.env["report.style"].create(
            {
                "name": "Style 01",
            }
        )
        self.style_02 = self.env["report.style"].create(
            {"name": "Style 02", "font_size": "small", "font_size_inherit": False}
        )
        for i in range(31):
            self.env["reporting.dummy.model"].create(
                {"name": f"{i}", "value": i, "date": f"2023-01-{(i%31)+1}"}
            )
        self.report = self.env["report.template"].create(
            {
                "name": "Test Report",
                "source": "dummy",
                "style_id": self.style.id,
            }
        )
        self.report_kpi = {}
        self.query_kind = self.env["report.template.kpi.query.kind"].create(
            {
                "name": "Dummy Query",
                "code": "dummy",
                "source": "dummy",
            }
        )
        for i in range(1, 10):
            kpi = self.env["report.template.kpi"].create(
                {
                    "name": f"KPI {i}",
                    "template_id": self.report.id,
                    "item_ids": [
                        (
                            0,
                            0,
                            {
                                "kind": "query",
                                "source": "dummy",
                                "query_kind_id": self.query_kind.id,
                                "code": f"{i}%",
                            },
                        ),
                    ],
                    "style_id": self.style_01.id if i % 2 == 0 else self.style_02.id,
                }
            )
            self.report_kpi[i] = kpi

    def test_report(self):
        report = self.env["report.instance"].create(
            {
                "name": "Test Report Instance",
                "template_id": self.report.id,
                "column_ids": [
                    (
                        0,
                        0,
                        {
                            "name": "Column 1",
                            "date_from": "2023-01-01",
                            "date_to": "2023-01-10",
                            "mode": "date",
                        },
                    ),
                    (
                        0,
                        0,
                        {
                            "name": "Column 2",
                            "date_from": "2023-01-11",
                            "date_to": "2023-01-31",
                            "mode": "date",
                        },
                    ),
                ],
            }
        )
        column_1 = report.column_ids[0]
        column_2 = report.column_ids[1]
        data = report.process_information("2023-01-31")
        self.assertEqual(
            data[self.report_kpi[1].id][column_1.id]["total"],
            1,
        )
        self.assertEqual(
            data[self.report_kpi[1].id][column_2.id]["total"],
            145,
        )
        self.assertEqual(
            data[self.report_kpi[2].id][column_1.id]["total"],
            2,
        )
        self.assertEqual(
            data[self.report_kpi[2].id][column_2.id]["total"],
            245,
        )
        self.assertEqual(
            data[self.report_kpi[3].id][column_1.id]["total"],
            3,
        )
        self.assertEqual(
            data[self.report_kpi[3].id][column_2.id]["total"],
            30,
        )
        self.assertEqual(
            data[self.report_kpi[4].id][column_1.id]["total"],
            4,
        )
        self.assertEqual(
            data[self.report_kpi[4].id][column_2.id]["total"],
            0,
        )
        self.assertEqual(
            data[self.report_kpi[5].id][column_1.id]["total"],
            5,
        )
        self.assertEqual(
            data[self.report_kpi[5].id][column_2.id]["total"],
            0,
        )
        self.assertEqual(
            data[self.report_kpi[6].id][column_1.id]["total"],
            6,
        )
        self.assertEqual(
            data[self.report_kpi[6].id][column_2.id]["total"],
            0,
        )
        self.assertEqual(
            data[self.report_kpi[7].id][column_1.id]["total"],
            7,
        )
        self.assertEqual(
            data[self.report_kpi[7].id][column_2.id]["total"],
            0,
        )
        self.assertEqual(
            data[self.report_kpi[8].id][column_1.id]["total"],
            8,
        )
        self.assertEqual(
            data[self.report_kpi[8].id][column_2.id]["total"],
            0,
        )
        self.assertEqual(
            data[self.report_kpi[9].id][column_1.id]["total"],
            9,
        )
        self.assertEqual(
            data[self.report_kpi[9].id][column_2.id]["total"],
            0,
        )

    def test_style(self):
        report = self.env["report.instance"].create(
            {
                "name": "Test Report Instance",
                "template_id": self.report.id,
            }
        )
        style_data = report.data
        for i in range(0, 9):
            if i % 2 == 0:
                self.assertEqual(
                    style_data["rows"][i]["parameters"]["font-size"], "small"
                )
                self.assertRegex(style_data["rows"][i]["style"], r"font-size: small")
            else:
                self.assertEqual(
                    style_data["rows"][i]["parameters"]["font-size"], "medium"
                )
                self.assertRegex(style_data["rows"][i]["style"], r"font-size: medium")

    def test_report_kpi(self):
        report = self.env["report.template"].create(
            {
                "name": "Test Report",
                "source": "dummy",
            }
        )
        report_kpi = self.env["report.template.kpi"].create(
            {
                "name": "KPI",
                "template_id": report.id,
                "item_ids": [
                    (
                        0,
                        0,
                        {
                            "kind": "query",
                            "source": "dummy",
                            "query_kind_id": self.query_kind.id,
                            "code": "%",
                        },
                    ),
                ],
            }
        )
        report_kpi_2 = self.env["report.template.kpi"].create(
            {
                "name": "KPI 2",
                "template_id": report.id,
                "item_ids": [
                    (
                        0,
                        0,
                        {
                            "kind": "kpi",
                            "kpi_id": report_kpi.id,
                        },
                    ),
                ],
            }
        )
        instance = self.env["report.instance"].create(
            {
                "name": "Test Report Instance",
                "template_id": report.id,
                "column_ids": [
                    (
                        0,
                        0,
                        {
                            "name": "Column 1",
                            "date_from": "2023-01-01",
                            "date_to": "2023-01-31",
                            "mode": "date",
                        },
                    ),
                ],
            }
        )
        data = instance.process_information("2023-01-31")
        self.assertEqual(465, data[report_kpi.id][instance.column_ids[0].id]["total"])
        self.assertEqual(465, data[report_kpi_2.id][instance.column_ids[0].id]["total"])

    def test_report_error(self):
        report = self.env["report.template"].create(
            {
                "name": "Test Report",
                "source": "dummy",
            }
        )
        report_kpi = self.env["report.template.kpi"].create(
            {
                "name": "KPI",
                "template_id": report.id,
                "item_ids": [
                    (
                        0,
                        0,
                        {
                            "kind": "query",
                            "source": "dummy",
                            "query_kind_id": self.query_kind.id,
                            "code": "%",
                        },
                    ),
                ],
            }
        )
        report_kpi_2 = self.env["report.template.kpi"].create(
            {
                "name": "KPI 2",
                "template_id": report.id,
                "item_ids": [
                    (
                        0,
                        0,
                        {
                            "kind": "kpi",
                            "kpi_id": report_kpi.id,
                        },
                    ),
                ],
            }
        )
        report_kpi.item_ids.write(
            {
                "kind": "kpi",
                "kpi_id": report_kpi_2.id,
            }
        )

        instance = self.env["report.instance"].create(
            {
                "name": "Test Report Instance",
                "template_id": report.id,
            }
        )
        with self.assertRaises(ValidationError):
            instance.process_information("2023-01-31")

    def test_mis_formula(self):
        self.assertEqual(self.report_kpi[1].code, "kpi_1")
        self.assertEqual(self.report_kpi[1].mis_builder_formula, "dummy[1%]")
