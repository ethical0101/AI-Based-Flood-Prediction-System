import pandas as pd
import numpy as np

# Load the Excel file
file_name = "kullback category and weights xlx.xlsx"
xls = pd.ExcelFile(file_name)

print("="*80)
print("EXCEL FILE STRUCTURE ANALYSIS")
print("="*80)
print(f"\nSheet names: {xls.sheet_names}\n")

# Analyze each sheet
for sheet in xls.sheet_names:
    df = pd.read_excel(file_name, sheet_name=sheet)
    print(f"\n{'='*80}")
    print(f"Sheet: '{sheet}'")
    print(f"{'='*80}")
    print(f"Shape: {df.shape} (Rows: {df.shape[0]}, Columns: {df.shape[1]})")
    print(f"\nFirst 5 rows:")
    print(df.head())
    print(f"\nColumns: {df.columns.tolist()}")
    print(f"\nData types:\n{df.dtypes}\n")
    print(f"Missing values: {df.isnull().sum().sum()}")
