import openpyxl

wb = openpyxl.load_workbook("Facebook_Post_Schedule.xlsx")
ws = wb.active

print("--- Excel Status Verification ---")
for r in range(1, 4):
    row_vals = [ws.cell(row=r, column=c).value for c in range(1, 8)]
    # safe print to handle console encoding
    safe_vals = []
    for val in row_vals:
        if val is None:
            safe_vals.append("")
        else:
            val_str = str(val)
            if len(val_str) > 30:
                val_str = val_str[:27] + "..."
            safe_vals.append(val_str.encode('ascii', errors='replace').decode('ascii'))
    print(f"Row {r}: {safe_vals}")
wb.close()
