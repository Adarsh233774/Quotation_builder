import openpyxl
import json
import sys
import os

def inspect_excel(filepath):
    if not os.path.exists(filepath):
        print(f"Error: File {filepath} does not exist.")
        return

    try:
        wb = openpyxl.load_workbook(filepath, data_only=False)
        wb_data = openpyxl.load_workbook(filepath, data_only=True)
    except Exception as e:
        print(f"Failed to load workbook: {e}")
        return

    output = {
        "file": filepath,
        "sheets": wb.sheetnames,
        "sheet_data": {}
    }

    for sheet_name in wb.sheetnames:
        sheet = wb[sheet_name]
        sheet_d = wb_data[sheet_name]
        
        sheet_info = {
            "max_row": sheet.max_row,
            "max_column": sheet.max_column,
            "merged_cells": [str(cr) for cr in sheet.merged_cells.ranges],
            "sample_rows": []
        }
        
        # Read first 50 rows to understand the structure
        for row_idx in range(1, min(sheet.max_row + 1, 100)):
            row_data = []
            for col_idx in range(1, min(sheet.max_column + 1, 30)):
                cell = sheet.cell(row=row_idx, column=col_idx)
                cell_d = sheet_d.cell(row=row_idx, column=col_idx)
                
                val = cell.value
                val_d = cell_d.value
                
                if val is not None:
                    cell_info = {
                        "cell": cell.coordinate,
                        "value": val,
                        "data_value": val_d,
                        "type": type(val).__name__
                    }
                    if hasattr(cell, 'number_format') and cell.number_format:
                         cell_info["format"] = cell.number_format
                    row_data.append(cell_info)
            if row_data:
                sheet_info["sample_rows"].append({"row": row_idx, "data": row_data})
                
        output["sheet_data"][sheet_name] = sheet_info

    with open("excel_analysis.json", "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, default=str)

    print("Analysis saved to excel_analysis.json")

if __name__ == "__main__":
    inspect_excel(r"D:\MY\Dad Work\Common Temp.xlsx")
