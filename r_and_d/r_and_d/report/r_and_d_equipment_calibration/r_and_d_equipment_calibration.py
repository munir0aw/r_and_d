import frappe
from frappe import _
from frappe.utils import getdate, today


def execute(filters=None):
	columns = get_columns()
	data = get_data(filters)
	return columns, data


def get_columns():
	return [
		{
			"fieldname": "equipment_name",
			"label": _("Equipment Name"),
			"fieldtype": "Link",
			"options": "R and D Equipment",
			"width": 200
		},
		{
			"fieldname": "model_number",
			"label": _("Model"),
			"fieldtype": "Data",
			"width": 120
		},
		{
			"fieldname": "serial_no",
			"label": _("Serial No"),
			"fieldtype": "Data",
			"width": 120
		},
		{
			"fieldname": "location",
			"label": _("Location"),
			"fieldtype": "Data",
			"width": 120
		},
		{
			"fieldname": "status",
			"label": _("Status"),
			"fieldtype": "Data",
			"width": 100
		},
		{
			"fieldname": "last_calibration",
			"label": _("Last Calibration"),
			"fieldtype": "Date",
			"width": 120
		},
		{
			"fieldname": "calibration_due",
			"label": _("Calibration Due"),
			"fieldtype": "Date",
			"width": 120
		},
		{
			"fieldname": "days_until_due",
			"label": _("Days Until Due"),
			"fieldtype": "Int",
			"width": 100
		},
		{
			"fieldname": "last_result",
			"label": _("Last Result"),
			"fieldtype": "Data",
			"width": 100
		},
		{
			"fieldname": "calibration_status",
			"label": _("Cal. Status"),
			"fieldtype": "Data",
			"width": 120
		}
	]


def get_data(filters):
	conditions = get_conditions(filters)

	data = frappe.db.sql("""
		SELECT
			e.name as equipment_name,
			e.model_number,
			e.serial_no,
			e.location,
			e.status,
			(SELECT MAX(date) FROM `tabR and D Calibration Log` WHERE parent = e.name) as last_calibration,
			e.calibration_due,
			(SELECT result FROM `tabR and D Calibration Log`
			 WHERE parent = e.name
			 ORDER BY date DESC LIMIT 1) as last_result
		FROM
			`tabR and D Equipment` e
		WHERE
			e.docstatus < 2
			{conditions}
		ORDER BY
			e.calibration_due ASC
	""".format(conditions=conditions), filters, as_dict=1)

	# Calculate days until due and calibration status
	today_date = getdate(today())
	for row in data:
		if row.calibration_due:
			due_date = getdate(row.calibration_due)
			days_diff = (due_date - today_date).days
			row.days_until_due = days_diff

			if days_diff < 0:
				row.calibration_status = "Overdue"
			elif days_diff <= 30:
				row.calibration_status = "Due Soon"
			else:
				row.calibration_status = "Current"
		else:
			row.days_until_due = None
			row.calibration_status = "Not Scheduled"

	return data


def get_conditions(filters):
	conditions = ""

	if filters.get("equipment_name"):
		conditions += " AND e.name = %(equipment_name)s"

	if filters.get("status"):
		conditions += " AND e.status = %(status)s"

	if filters.get("location"):
		conditions += " AND e.location = %(location)s"

	return conditions
