import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

#Define flood years
FLOOD_YEARS = [1996, 2005, 2008, 2010, 2015, 2016, 2017, 2018, 2020]

print("="*80)
print("FINAL EXCEL DATA PROCESSING - CORRECT APPROACH")
print("="*80)

file_name = "kullback category and weights xlx.xlsx"

# Read raw with no headers
raw = pd.read_excel(file_name, sheet_name='kullback category and weights', header=None)

print(f"\nRaw shape: {raw.shape}")

# Row 0 is headers, row 1-316 is data (skip row 0)
df = raw.iloc[1:].reset_index(drop=True).copy()

print(f"Data shape (after removing header): {df.shape}")

# Extract only numeric columns: 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36, 38, 40
# Plus column 0 for months
numeric_cols = [2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36, 38, 40]
df_clean = df[[0] + numeric_cols].reset_index(drop=True).copy()

print(f"After selecting numeric & month columns: {df_clean.shape}")

# Rename columns
feature_names = [
    'Month_Name',
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
    'SPEI_12'
]

df_clean.columns = feature_names

print(f"Columns renamed")
print(f"Features: {df_clean.columns.tolist()}\n")

# Ensure all feature columns are numeric
print("="*80)
print("Converting to Numeric Types")
print("="*80)

for col in feature_names[1:]:  # Skip month_name
    df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce')

print(f"✓ All features converted to numeric\n")

# Extract Year and Month
print("="*80)
print("Extracting Year and Month")
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

print(f"✓ Year range: {min(years)} to {max(years)}")
print(f"✓ Total months: {len(years)}\n")

# Create Flood label
df_clean['Flood'] = df_clean['Year'].apply(lambda x: 1 if x in FLOOD_YEARS else 0)
df_clean['Drought_Label'] = 'No'  # Placeholder - could be extracted from original data

# Handle missing values
print("="*80)
print("Handling Missing Values")
print("="*80)

nan_before = df_clean[feature_names[1:]].isnull().sum().sum()
print(f"Total NaN values before: {nan_before}")

for col in feature_names[1:]:
    nan_count = df_clean[col].isnull().sum()
    if nan_count > 0:
        median_val = df_clean[col].median()
        df_clean[col].fillna(median_val, inplace=True)

nan_after = df_clean[feature_names[1:]].isnull().sum().sum()
print(f"Total NaN values after: {nan_after}")
print(f"✓ Missing values handled\n")

# Reorder columns
important_cols = ['Year', 'Month', 'Month_Name', 'Flood', 'Drought_Label']
feature_cols_sorted = sorted([col for col in feature_names if col != 'Month_Name'])
df_final = df_clean[important_cols + feature_cols_sorted].copy()

print("="*80)
print("FINAL DATASET SUMMARY")
print("="*80)

print(f"\nShape: {df_final.shape}")
print(f"Columns: {len(df_final.columns)}")
print(f"Year range: {df_final['Year'].min()} - {df_final['Year'].max()}")

print(f"\nFlood Distribution:")
flood_counts = df_final['Flood'].value_counts()
print(f"  Non-Flood (0): {flood_counts[0]} months ({flood_counts[0]/len(df_final)*100:.1f}%)")
print(f"  Flood (1): {flood_counts[1]} months ({flood_counts[1]/len(df_final)*100:.1f}%)")

print(f"\nFlood Years: {FLOOD_YEARS}")

nan_total = df_final.isnull().sum().sum()
print(f"Total missing values: {nan_total}")
print(f"Data quality: ✓ Complete" if nan_total == 0 else f"⚠ {nan_total} missing values")

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

print(f"\nSample Data (Rows 1-15):")
print("-" * 100)
sample_display = df_final[['Year', 'Month', 'Month_Name', 'Flood', 'Precipitation', 'Max_Temp', 'Mean_Temp', 'Min_Temp']].head(15)
for idx, row in sample_display.iterrows():
    print(f"  {row['Year']}/{row['Month']:2d} {row['Month_Name']:>5} Flood:{int(row['Flood'])} "
          f"Precip:{row['Precipitation']:>8.5f} MaxT:{row['Max_Temp']:>8.5f} "
          f"MeanT:{row['Mean_Temp']:>8.5f} MinT:{row['Min_Temp']:>8.5f}")

print(f"\nSample Data (Rows 300-316):")
print("-" * 100)
sample_display_end = df_final[['Year', 'Month', 'Month_Name', 'Flood', 'Precipitation', 'Max_Temp']].tail(17)
for idx, row in sample_display_end.iterrows():
    print(f"  {row['Year']}/{row['Month']:2d} {row['Month_Name']:>5} Flood:{int(row['Flood'])} "
          f"Precip:{row['Precipitation']:>8.5f} MaxT:{row['Max_Temp']:>8.5f}")

print(f"\n" + "="*80)
print("✓ DATA PROCESSING COMPLETE!")
print("="*80)
print(f"\nYour cleaned Excel-derived dataset is ready for the flood prediction notebook!")
print(f"Load with: df = pd.read_csv('cleaned_flood_dataset.csv')")
