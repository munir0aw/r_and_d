import frappe
from frappe import _


def execute(filters=None):
	columns = get_columns()
	data = get_data(filters)
	return columns, data


def get_columns():
	return [
		{
			"fieldname": "project_name",
			"label": _("Project Name"),
			"fieldtype": "Link",
			"options": "R and D Project",
			"width": 200
		},
		{
			"fieldname": "project_type",
			"label": _("Type"),
			"fieldtype": "Data",
			"width": 120
		},
		{
			"fieldname": "status",
			"label": _("Status"),
			"fieldtype": "Data",
			"width": 120
		},
		{
			"fieldname": "principal_investigator",
			"label": _("Principal Investigator"),
			"fieldtype": "Link",
			"options": "User",
			"width": 180
		},
		{
			"fieldname": "start_date",
			"label": _("Start Date"),
			"fieldtype": "Date",
			"width": 100
		},
		{
			"fieldname": "end_date",
			"label": _("End Date"),
			"fieldtype": "Date",
			"width": 100
		},
		{
			"fieldname": "sample_count",
			"label": _("Samples"),
			"fieldtype": "Int",
			"width": 80
		},
		{
			"fieldname": "experiment_count",
			"label": _("Experiments"),
			"fieldtype": "Int",
			"width": 100
		},
		{
			"fieldname": "report_count",
			"label": _("Reports"),
			"fieldtype": "Int",
			"width": 80
		}
	]


def get_data(filters):
	conditions = get_conditions(filters)

	data = frappe.db.sql("""
		SELECT
			p.name as project_name,
			p.project_type,
			p.status,
			p.principal_investigator,
			p.start_date,
			p.end_date,
			(SELECT COUNT(*) FROM `tabR and D Sample` WHERE linked_project = p.name) as sample_count,
			(SELECT COUNT(*) FROM `tabR and D Experiment` WHERE linked_project = p.name) as experiment_count,
			(SELECT COUNT(*) FROM `tabR and D Report` WHERE linked_project = p.name) as report_count
		FROM
			`tabR and D Project` p
		WHERE
			p.docstatus < 2
			{conditions}
		ORDER BY
			p.start_date DESC
	""".format(conditions=conditions), filters, as_dict=1)

	return data


def get_conditions(filters):
	conditions = ""

	if filters.get("project_type"):
		conditions += " AND p.project_type = %(project_type)s"

	if filters.get("status"):
		conditions += " AND p.status = %(status)s"

	if filters.get("principal_investigator"):
		conditions += " AND p.principal_investigator = %(principal_investigator)s"

	if filters.get("from_date"):
		conditions += " AND p.start_date >= %(from_date)s"

	if filters.get("to_date"):
		conditions += " AND p.start_date <= %(to_date)s"

	return conditions
