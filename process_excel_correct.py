import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

# Define flood years
FLOOD_YEARS = [1996, 2005, 2008, 2010, 2015, 2016, 2017, 2018, 2020]

print("="*80)
print("CORRECTED EXCEL DATA PROCESSING")
print("="*80)

file_name = "kullback category and weights xlx.xlsx"
df = pd.read_excel(file_name, sheet_name='kullback category and weights')

print(f"\nOriginal shape: {df.shape}")
print(f"Columns: {df.columns.tolist()}")

# The pattern is: [Text_Col, Numeric_Col, Text_Col, Numeric_Col, ...]
# We want only the Numeric columns (odd indices: 1, 3, 5, ...)
numeric_col_indices = [i for i in range(len(df.columns)) if i > 0 and i % 2 == 1]
print(f"\nNumeric column indices: {numeric_col_indices}")

# Also keep the first column (Months)
df_clean = df.iloc[:, [0] + numeric_col_indices].copy()

print(f"After extracting numeric columns: {df_clean.shape}")

# Rename columns properly
feature_names = [
    'Months',
    'Max_Temp',
    'Mean_Temp',
    'Min_Temp',
    'Vapour_Pressure',
    'Wind_Speed',
    'Precipitation',
    'Shortwave_Radiation',
    'Dew_Point',
    'Cloud_Amount',
    'CO2',
    'PM2_5',
    'MSL_BayOfBengal',
    'MSL_ArabianSea',
    'MSL_IndianOcean',
    'SPI_3',
    'SPI_6',
    'SPI_12',
    'SPEI_3',
    'SPEI_6',
    'SPEI_12',
    'Drought_Label'
]

df_clean.columns = feature_names
print(f"\nColumns renamed: {df_clean.columns.tolist()}")

# Extract Year and Month
print(f"\n" + "="*80)
print("Extracting Year and Month Information")
print("="*80)

months_in_year = 12
start_year = 1995

years = []
months = []

for idx in range(len(df_clean)):
    year = start_year + (idx // months_in_year)
    month = (idx % months_in_year) + 1
    years.append(year)
    months.append(month)

df_clean['Year'] = years
df_clean['Month'] = months
df_clean.rename(columns={'Months': 'Month_Name'}, inplace=True)

print(f"✓ Year range: {min(years)} to {max(years)}")
print(f"✓ Total months: {len(years)} ({len(years)/12} years)")

# Create Flood label
df_clean['Flood'] = df_clean['Year'].apply(lambda x: 1 if x in FLOOD_YEARS else 0)

# Convert numeric columns properly
print(f"\n" + "="*80)
print("Converting to Numeric Data Types")
print("="*80)

numeric_cols = df_clean.columns.difference(['Month_Name', 'Year', 'Month', 'Flood', 'Drought_Label'])
for col in numeric_cols:
    df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce')

nan_total = df_clean[numeric_cols].isnull().sum().sum()
print(f"Total missing values in features: {nan_total}")

# Fill missing values
if nan_total > 0:
    print(f"\nFilling missing values with column medians:")
    for col in numeric_cols:
        nan_count = df_clean[col].isnull().sum()
        if nan_count > 0:
            median_val = df_clean[col].median()
            df_clean[col].fillna(median_val, inplace=True)
            print(f"  {col}: filled {nan_count} NaN with {median_val:.6f}")

# Reorder columns
important_cols = ['Year', 'Month', 'Month_Name', 'Flood', 'Drought_Label']
other_cols = [col for col in numeric_cols]
df_final = df_clean[important_cols + other_cols].copy()

print(f"\n" + "="*80)
print("FINAL DATASET SUMMARY")
print("="*80)

print(f"\nShape: {df_final.shape}")
print(f"Columns: {len(df_final.columns)}")
print(f"Year range: {df_final['Year'].min()} - {df_final['Year'].max()}")

print(f"\nFlood Distribution:")
flood_dist = df_final['Flood'].value_counts()
print(f"  Non-Flood (0): {flood_dist[0]} months ({flood_dist[0]/len(df_final)*100:.1f}%)")
print(f"  Flood (1): {flood_dist[1]} months ({flood_dist[1]/len(df_final)*100:.1f}%)")

nan_after = df_final.isnull().sum().sum()
print(f"\nMissing values: {nan_after}")
print(f"Data quality: {'✓ Complete' if nan_after == 0 else '⚠ Has missing values'}")

# Save files
csv_file = "cleaned_flood_dataset.csv"
xlsx_file = "cleaned_flood_dataset.xlsx"

df_final.to_csv(csv_file, index=False)
df_final.to_excel(xlsx_file, index=False, sheet_name='Flood_Data')

print(f"\n" + "="*80)
print("FILES SAVED")
print("="*80)
print(f"✓ {csv_file}")
print(f"✓ {xlsx_file}")

print(f"\nSample Data (First 15 rows):")
print("-" * 80)
print(df_final[['Year', 'Month', 'Month_Name', 'Flood', 'Precipitation', 'Max_Temp', 'Min_Temp']].head(15).to_string())

print(f"\n" + "="*80)
print("✓ DATA PROCESSING COMPLETE - READY FOR MODEL TRAINING!")
print("="*80)
