import frappe

def update_item_uoms(doc, method=None):
    """Update Dimensions, Area, PCS Factor, Box Factor and UOMs on Item Save"""

    pcs_factor = 0
    box_factor = 0

    # --- Auto-fill Dimensions from Length & Width ---
    if doc.custom_length and doc.custom_width:
        doc.custom_dimensions = f"{int(doc.custom_length)}x{int(doc.custom_width)}"

        # --- Area ---
        doc.custom_area = round((doc.custom_length * doc.custom_width) / 1_000_000, 3)
    else:
        doc.custom_area = 0

    # --- PCS Factor ---
    if doc.custom_length and doc.custom_width:
        pcs_factor = (doc.custom_length * doc.custom_width) / 1_000_000
        doc.custom_pcs_factor = round(pcs_factor, 3)
    else:
        doc.custom_pcs_factor = 0

    # --- Box Factor ---
    if pcs_factor and doc.custom_pcs_in_box:
        box_factor = pcs_factor * doc.custom_pcs_in_box
        doc.custom_box_factor = round(box_factor, 3)
    else:
        doc.custom_box_factor = 0

    # --- Reset UOMs table ---
    doc.set("uoms", [])
    doc.append("uoms", {"uom": "M2", "conversion_factor": 1})

    if pcs_factor:
        doc.append("uoms", {"uom": "PCS", "conversion_factor": pcs_factor})

    if box_factor:
        doc.append("uoms", {"uom": "BOX", "conversion_factor": box_factor})
