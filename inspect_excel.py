import pandas as pd
import numpy as np

file_name = "kullback category and weights xlx.xlsx"

# Read without header to see raw structure
raw = pd.read_excel(file_name, sheet_name='kullback category and weights', header=None)

print("="*80)
print("RAW EXCEL FILE INSPECTION")
print("="*80)

print(f"\nRaw shape: {raw.shape}")
print(f"\nFirst 20 rows and first 12 columns:")
print(raw.iloc[:20, :12])

print(f"\n\nData types of first 12 columns:")
for i in range(12):
    print(f"  Column {i}: {raw[i].dtype}")

print(f"\n\nSample values from different columns:")
for col_idx in [0, 1, 2, 3, 4]:
    print(f"\nColumn {col_idx} (first 10 non-null values):")
    non_null = raw[col_idx].dropna()
    print(non_null.head(10).tolist())

# Try to identify which columns have numeric data
print(f"\n\n" + "="*80)
print("NUMERIC COLUMN DETECTION")
print("="*80)

numeric_col_ratio = {}
for col_idx in range(raw.shape[1]):
    col_data = raw[col_idx]
    # Try numeric conversion
    numeric_count = 0
    for val in col_data:
        try:
            float(val)
            numeric_count += 1
        except:
            pass
    ratio = numeric_count / len(col_data)
    numeric_col_ratio[col_idx] = ratio

# Show columns with >50% numeric values
reliable_numeric_cols = [col for col, ratio in numeric_col_ratio.items() if ratio > 0.5]
print(f"\nColumns with >50% numeric values: {reliable_numeric_cols}")
print(f"\nNumeric ratio for each column:")
for col_idx, ratio in sorted(numeric_col_ratio.items(), key=lambda x: x[1], reverse=True)[:15]:
    print(f"  Column {col_idx}: {ratio*100:.1f}%")
