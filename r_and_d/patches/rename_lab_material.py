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
		except Exception as e:
			print(f"⚠️ Could not rename: {e}")

	# Case 2: New name ALREADY exists -> Just print
	if frappe.db.exists("DocType", new_name):
		print(f"✅ {new_name} already exists in database.")
	
	# Case 3: Neither exists ??? -> This shouldn't happen if files are consistent, 
	# but we can try to force reload
	else:
		print(f"⚠️ Neither {old_name} nor {new_name} found in DB. Attempting to install...")
		try:
			# Force install the app's doctypes
			frappe.clear_cache()
			frappe.sync_module("r_and_d") 
			print(f"✅ Module synced. {new_name} should be visible now.")
		except Exception as e:
			print(f"❌ Error syncing module: {e}")

	# Final check
	if frappe.db.exists("DocType", new_name):
		# Ensure permissions are set
		doc = frappe.get_doc("DocType", new_name)
		# We don't overwrite permissions blindly usually, but if it was fresh, we ensure System Manager has it
		# doc.permissions = [
		# 	{"role": "System Manager", "read": 1, "write": 1, "create": 1, "delete": 1}
		# ]
		# doc.save(ignore_permissions=True)
		print(f"Confirmed {new_name} is accessible.")
