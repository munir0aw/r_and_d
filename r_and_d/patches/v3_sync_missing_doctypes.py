import frappe

def execute():
	"""
	Sync missing DocTypes that weren't loaded after app rename.
	This forces Frappe to reload specific DocTypes from the file system.
	"""
	missing_doctypes = [
		"R and D Experiment Step Material",
		"R and D Lab Material",
		"R and D Lab Material Category",
		"R and D Material Type"
	]

	for doctype_name in missing_doctypes:
		try:
			# Force reload from JSON
			frappe.reload_doc("R and D", "doctype", frappe.scrub(doctype_name), force=True)
			print(f"✅ Synced: {doctype_name}")
		except Exception as e:
			print(f"⚠️  Failed to sync {doctype_name}: {str(e)}")

	frappe.db.commit()
	print("🎯 Missing DocTypes sync complete!")
