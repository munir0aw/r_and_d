import frappe
from frappe import _


def execute(filters=None):
	columns = get_columns()
	data = get_data(filters)
	return columns, data


def get_columns():
	return [
		{
			"fieldname": "experiment_id",
			"label": _("Experiment ID"),
			"fieldtype": "Link",
			"options": "R and D Experiment",
			"width": 150
		},
		{
			"fieldname": "linked_project",
			"label": _("Project"),
			"fieldtype": "Link",
			"options": "R and D Project",
			"width": 180
		},
		{
			"fieldname": "linked_sample",
			"label": _("Sample"),
			"fieldtype": "Link",
			"options": "R and D Sample",
			"width": 150
		},
		{
			"fieldname": "method",
			"label": _("Test Method"),
			"fieldtype": "Link",
			"options": "R and D Test Method",
			"width": 150
		},
		{
			"fieldname": "status",
			"label": _("Status"),
			"fieldtype": "Data",
			"width": 100
		},
		{
			"fieldname": "date_started",
			"label": _("Started"),
			"fieldtype": "Datetime",
			"width": 150
		},
		{
			"fieldname": "date_completed",
			"label": _("Completed"),
			"fieldtype": "Datetime",
			"width": 150
		},
		{
			"fieldname": "parameter",
			"label": _("Parameter"),
			"fieldtype": "Link",
			"options": "R and D Parameter",
			"width": 150
		},
		{
			"fieldname": "value",
			"label": _("Value"),
			"fieldtype": "Data",
			"width": 100
		},
		{
			"fieldname": "unit",
			"label": _("Unit"),
			"fieldtype": "Data",
			"width": 80
		}
	]


def get_data(filters):
	conditions = get_conditions(filters)

	data = frappe.db.sql("""
		SELECT
			e.name as experiment_id,
			e.linked_project,
			e.linked_sample,
			e.method,
			e.status,
			e.date_started,
			e.date_completed,
			rd.parameter,
			rd.value,
			rd.unit
		FROM
			`tabR and D Experiment` e
		LEFT JOIN
			`tabR and D Result Detail` rd ON rd.parent = e.name
		WHERE
			e.docstatus < 2
			{conditions}
		ORDER BY
			e.date_started DESC
	""".format(conditions=conditions), filters, as_dict=1)

	return data


def get_conditions(filters):
	conditions = ""

	if filters.get("linked_project"):
		conditions += " AND e.linked_project = %(linked_project)s"

	if filters.get("linked_sample"):
		conditions += " AND e.linked_sample = %(linked_sample)s"

	if filters.get("method"):
		conditions += " AND e.method = %(method)s"

	if filters.get("status"):
		conditions += " AND e.status = %(status)s"

	if filters.get("from_date"):
		conditions += " AND e.date_started >= %(from_date)s"

	if filters.get("to_date"):
		conditions += " AND e.date_started <= %(to_date)s"

	return conditions
