# Copyright (c) 2025, Your Company and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import getdate, nowdate


class ExperimentStepMaterial(Document):
	def validate(self):
		# Validate expiry date if material is selected
		if self.material and self.expiry_date:
			if getdate(self.expiry_date) < getdate(nowdate()):
				frappe.msgprint(
					f"Warning: Material has expired on {self.expiry_date}",
					indicator="orange",
					alert=True
				)

		# Validate stock availability if material and quantity are set
		if self.material and self.quantity_used:
			material_doc = frappe.get_doc("R and D Lab Material", self.material)
			if material_doc.current_stock < self.quantity_used:
				frappe.throw(
					f"Insufficient stock for {material_doc.material_name}. "
					f"Available: {material_doc.current_stock} {self.unit_of_measurement or ''}, "
					f"Required: {self.quantity_used}"
				)
