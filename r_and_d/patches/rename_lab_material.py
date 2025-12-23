import frappe
from frappe.model.rename_doc import rename_doc

def execute():
	"""
	Fix Lab Material:
	1. Rename 'Lab Material' to 'R and D Lab Material' if it exists.
	2. If 'Lab Material' does not exist, check if 'R and D Lab Material' exists.
	3. Reload the doc to ensure it's registered.
	"""
	
	old_name = "Lab Material"
	new_name = "R and D Lab Material"

	# Case 1: Old name exists in DB -> Rename it
	if frappe.db.exists("DocType", old_name):
		print(f"Renaming {old_name} to {new_name}...")
		try:
			rename_doc("DocType", old_name, new_name, force=True, merge=False)
			frappe.db.commit()
			print(f"✅ Renamed {old_name} back to {new_name}")
			return # We are done
		except Exception as e:
			print(f"⚠️ Could not rename: {e}")

	# Case 2: New name ALREADY exists -> Check permissions
	if frappe.db.exists("DocType", new_name):
		print(f"✅ {new_name} already exists in database.")
	
	# Case 3: Neither exists -> Force reload
	else:
		print(f"⚠️ Neither {old_name} nor {new_name} found in DB. Forcing reload...")
		try:
			# Correct way to reload a specific DocType [module, type, name]
			frappe.reload_doc("r_and_d", "doctype", "r_and_d_lab_material")
			frappe.reload_doc("r_and_d", "doctype", "r_and_d_material_type")
			frappe.reload_doc("r_and_d", "doctype", "r_and_d_lab_material_category")
			print(f"✅ Force reloaded {new_name}")
		except Exception as e:
			print(f"❌ Error reloading DocType: {e}")
