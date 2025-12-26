import frappe

def execute():
	"""
	This patch is intentionally empty.
	The DocTypes will be synced automatically by Frappe's sync_all() during migration.
	We just needed this patch to trigger a migration after adding the new DocTypes.
	"""
	print("✅ DocType sync will be handled by Frappe's automatic sync process")
	print("🎯 New DocTypes: R and D Experiment Step Material, Lab Material, Lab Material Category, Material Type")
