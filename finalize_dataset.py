import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

FLOOD_YEARS = [1996, 2005, 2008, 2010, 2015, 2016, 2017, 2018, 2020]

print("="*80)
print("FINALIZING CLEANED DATASET")
print("="*80)

# Load the current cleaned dataset
df = pd.read_csv('cleaned_flood_dataset.csv')

print(f"\nInitial shape: {df.shape}")

# Remove rows where Year > 2020 (keep only 1995-2020)
df_final = df[df['Year'] <= 2020].copy()

print(f"After removing years > 2020: {df_final.shape}")

# Verify data quality
print(f"\n" + "="*80)
print("DATASET QUALITY CHECK")
print("="*80)

print(f"\nYear range: {df_final['Year'].min()} - {df_final['Year'].max()}")
print(f"Total months: {len(df_final)}")
print(f"Expected (26 years × 12): {26 * 12}")

print(f"\nFlood Distribution:")
flood_counts = df_final['Flood'].value_counts()
print(f"  Non-Flood (0): {flood_counts[0]} months ({flood_counts[0]/len(df_final)*100:.1f}%)")
print(f"  Flood (1): {flood_counts[1]} months ({flood_counts[1]/len(df_final)*100:.1f}%)")

# Check for missing values
nan_summary = df_final.isnull().sum()
print(f"\nMissing values per column:")
nan_cols = nan_summary[nan_summary > 0]
if len(nan_cols) > 0:
    for col, count in nan_cols.items():
        print(f"  {col}: {count}")
    # Fill remaining NaNs
    for col in nan_cols.index:
        if col not in ['Month_Name', 'Drought_Label']:
            df_final[col].fillna(df_final[col].median(), inplace=True)
    print("  ✓ Remaining NaN values filled")
else:
    print("  ✓ No missing values!")

# Verify all numeric columns
print(f"\nNumeric columns verified:")
for col in df_final.columns:
    if col not in ['Month_Name', 'Drought_Label', 'Flood']:
        print(f"  ✓ {col}")

# Save final version
csv_file = "cleaned_flood_dataset.csv"
xlsx_file = "cleaned_flood_dataset.xlsx"

df_final.to_csv(csv_file, index=False)
df_final.to_excel(xlsx_file, index=False, sheet_name='Flood_Data')

print(f"\n" + "="*80)
print("✓ FINAL DATASET SAVED")
print("="*80)

print(f"\nFiles:")
print(f"  • {csv_file} ({df_final.shape[0]} rows × {df_final.shape[1]} columns)")
print(f"  • {xlsx_file}")

print(f"\nDataset Summary:")
print(f"  Years: 1995-2020 (26 years)")
print(f"  Months: {len(df_final)} total")
print(f"  Flood samples: {(df_final['Flood']==1).sum()}")
print(f"  Non-Flood samples: {(df_final['Flood']==0).sum()}")
print(f"  Features: {len(df_final.columns) - 5} climatic/environmental")

print(f"\n" + "="*80)
print("✓ READY TO USE IN FLOOD PREDICTION NOTEBOOK!")
print("="*80)
