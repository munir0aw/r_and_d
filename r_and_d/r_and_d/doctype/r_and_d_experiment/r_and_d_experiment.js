// Copyright (c) 2025, Your Company and contributors
// For license information, please see license.txt

frappe.ui.form.on("R and D Experiment", {
	refresh(frm) {
		// Simple refresh, steps now include materials directly
	}
});

frappe.ui.form.on("Experiment Step Material", {
	steps_add(frm, cdt, cdn) {
		// Set default status for new rows
		let row = locals[cdt][cdn];
		if (!row.status) {
			frappe.model.set_value(cdt, cdn, 'status', 'Pending');
		}
	},

	material(frm, cdt, cdn) {
		// Auto-fetch material details when material is selected
		let row = locals[cdt][cdn];
		if (row.material) {
			frappe.db.get_doc('R and D Lab Material', row.material).then(doc => {
				frappe.model.set_value(cdt, cdn, 'unit_of_measurement', doc.unit_of_measurement);
				frappe.model.set_value(cdt, cdn, 'batch_number', doc.batch_number);
				frappe.model.set_value(cdt, cdn, 'expiry_date', doc.expiry_date);

				// Validate expiry
				if (doc.expiry_date) {
					let today = frappe.datetime.get_today();
					if (doc.expiry_date < today) {
						frappe.msgprint({
							title: __('Warning'),
							indicator: 'red',
							message: __('Material {0} has expired on {1}', [doc.material_name, doc.expiry_date])
						});
					}
				}

				// Show available stock
				if (doc.current_stock) {
					frappe.show_alert({
						message: __('Available Stock: {0} {1}', [doc.current_stock, doc.unit_of_measurement]),
						indicator: 'blue'
					}, 3);
				}
			});
		}
	}
});
