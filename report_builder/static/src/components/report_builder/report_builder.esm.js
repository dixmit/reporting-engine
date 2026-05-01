import {Component, onWillStart, onWillUnmount, useState} from "@odoo/owl";
import {parseDate, serializeDate} from "@web/core/l10n/dates";
import {DateTimeInput} from "@web/core/datetime/datetime_input";
import {SearchBar} from "@web/search/search_bar/search_bar";
import {formatMonetary} from "@web/views/fields/formatters";
import {registry} from "@web/core/registry";
import {useService} from "@web/core/utils/hooks";

export class ReportBuilderValue extends Component {
    get formattedValue() {
        const {value, currency_id} = this.props;
        if (value && value.total) {
            return formatMonetary(value.total, {currencyId: currency_id[0]});
        }
        return "";
    }
}
ReportBuilderValue.template = "report_builder.ReportBuilderValue";
ReportBuilderValue.props = {
    value: {type: Object},
    currency_id: {type: Object, optional: true},
};

export class ReportBuilder extends Component {
    setup() {
        super.setup();
        this.state = useState({date: false, data: {}});
        this.orm = useService("orm");
        this.bus_service = useService("bus_service");
        this.action_service = useService("action");
        onWillStart(this.onWillStart);
        onWillUnmount(() => {
            this.bus_service.deleteChannel("report_builder");
        });
    }
    onWillStart() {
        this.state.pivot_date = parseDate(this.props.record.data.data.date);
        this.updateData();
    }
    async updateData() {
        const data = await this.orm.call(
            this.props.record.model.config.resModel,
            "process_information",
            [this.props.record.resIds, serializeDate(this.state.pivot_date)]
        );
        this.state.data = data;
    }
    onPivotDateChanged(pivot_date) {
        this.state.pivot_date = pivot_date;
        this.updateData();
    }
    refresh() {
        this.updateData();
    }
    printPdf() {
        // TODO: implement the method to print the report in PDF format
    }
    printXlsx() {
        // TODO: implement the method to print the report in XLSX format
    }
    async displaySettings() {
        this.action_service.doAction(
            await this.orm.call(
                this.props.record.model.config.resModel,
                "get_display_settings_action",
                [this.props.record.resIds[0]]
            )
        );
        // TODO: implement the method to display the report settings
    }
}

ReportBuilder.components = {SearchBar, DateTimeInput, ReportBuilderValue};
ReportBuilder.template = "report_builder.ReportBuilder";

export const reportBuilder = {
    component: ReportBuilder,
    fieldDependencies: [
        {name: "name", type: "char"},
        {name: "data", type: "json"},
        {name: "currency_id", type: "many2one", relation: "res.currency"},
        {name: "show_search_bar", type: "boolean"},
        {name: "show_settings", type: "boolean"},
        {name: "show_pivot_date", type: "boolean"},
    ],
};

registry.category("fields").add("report_builder", reportBuilder);
