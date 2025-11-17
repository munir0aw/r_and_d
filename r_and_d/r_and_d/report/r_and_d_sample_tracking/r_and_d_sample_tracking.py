import frappe
from frappe import _
from frappe.utils import getdate, date_diff, today


def execute(filters=None):
	columns = get_columns()
	data = get_data(filters)
	return columns, data


def get_columns():
	return [
		{
			"fieldname": "sample_id",
			"label": _("Sample ID"),
			"fieldtype": "Link",
			"options": "R and D Sample",
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
			"fieldname": "sample_type",
			"label": _("Sample Type"),
			"fieldtype": "Data",
			"width": 150
		},
		{
			"fieldname": "source",
			"label": _("Source"),
			"fieldtype": "Data",
			"width": 150
		},
		{
			"fieldname": "received_date",
			"label": _("Received Date"),
			"fieldtype": "Date",
			"width": 120
		},
		{
			"fieldname": "days_in_lab",
			"label": _("Days in Lab"),
			"fieldtype": "Int",
			"width": 100
		},
		{
			"fieldname": "status",
			"label": _("Status"),
			"fieldtype": "Data",
			"width": 120
		},
		{
			"fieldname": "custody",
			"label": _("Custody"),
			"fieldtype": "Link",
			"options": "User",
			"width": 150
		},
		{
			"fieldname": "experiment_count",
			"label": _("Experiments"),
			"fieldtype": "Int",
			"width": 100
		}
	]


def get_data(filters):
	conditions = get_conditions(filters)

	data = frappe.db.sql("""
		SELECT
			s.name as sample_id,
			s.linked_project,
			s.sample_type,
			s.source,
			s.received_date,
			s.status,
			s.custody,
			(SELECT COUNT(*) FROM `tabR and D Experiment` WHERE linked_sample = s.name) as experiment_count
		FROM
			`tabR and D Sample` s
		WHERE
			s.docstatus < 2
			{conditions}
		ORDER BY
			s.received_date DESC
	""".format(conditions=conditions), filters, as_dict=1)

	# Calculate days in lab
	today_date = getdate(today())
	for row in data:
		if row.received_date:
			received = getdate(row.received_date)
			row.days_in_lab = date_diff(today_date, received)
		else:
			row.days_in_lab = None

	return data


def get_conditions(filters):
	conditions = ""

	if filters.get("linked_project"):
		conditions += " AND s.linked_project = %(linked_project)s"

	if filters.get("sample_type"):
		conditions += " AND s.sample_type = %(sample_type)s"

	if filters.get("status"):
		conditions += " AND s.status = %(status)s"

	if filters.get("custody"):
		conditions += " AND s.custody = %(custody)s"

	if filters.get("from_date"):
		conditions += " AND s.received_date >= %(from_date)s"

	if filters.get("to_date"):
		conditions += " AND s.received_date <= %(to_date)s"

	return conditions
