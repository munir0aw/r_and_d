import frappe
from frappe.model.rename_doc import rename_doc

def execute():
	"""
	Final Restoration Fix:
	Now that directory structure is correct, force reload the DocTypes.
	"""
	print("🚀 STARTING FINAL RESTORATION PATCH 🚀")
	
	try:
		# Reload all missing DocTypes
		doc_types = [
			"r_and_d_lab_material", 
			"r_and_d_material_type", 
			"r_and_d_lab_material_category"
		]
		
		for dt in doc_types:
			print(f"Reloading {dt}...")
			frappe.reload_doc("r_and_d", "doctype", dt)
			
		print("✅ All DocTypes successfully reloaded!")
		
	except Exception as e:
		print(f"❌ Error during reload: {e}")
