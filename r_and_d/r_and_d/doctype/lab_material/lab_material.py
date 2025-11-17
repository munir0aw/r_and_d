# Copyright (c) 2025, Your Company and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class LabMaterial(Document):
	def validate(self):
		# Validate expiry date
		if self.expiry_date:
			from frappe.utils import getdate, nowdate
			if getdate(self.expiry_date) < getdate(nowdate()):
				frappe.msgprint(f"Warning: Material {self.material_name} has expired!", indicator="orange", alert=True)

		# Check minimum stock level
		if self.minimum_stock_level and self.current_stock:
			if self.current_stock < self.minimum_stock_level:
				frappe.msgprint(f"Stock level for {self.material_name} is below minimum!", indicator="red", alert=True)
