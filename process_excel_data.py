import pandas as pd
import numpy as np
from openpyxl import load_workbook
import warnings
warnings.filterwarnings('ignore')

# Define flood years
FLOOD_YEARS = [1996, 2005, 2008, 2010, 2015, 2016, 2017, 2018, 2020]

print("="*80)
print("CLEANING AND TRANSFORMING EXCEL DATASET")
print("="*80)

# Load the Excel file
file_name = "kullback category and weights xlx.xlsx"
df = pd.read_excel(file_name, sheet_name='kullback category and weights')

print(f"\nOriginal Dataset Shape: {df.shape}")
print(f"Columns: {len(df.columns)}")

# Step 1: Clean column names and handle the Unnamed columns
print("\n" + "="*80)
print("STEP 1: Clean Column Names and Remove Duplicate Data")
print("="*80)

# Keep only non-Unnamed columns (actual feature values)
unnamed_cols = [col for col in df.columns if 'Unnamed' in col]
df_clean = df.drop(columns=unnamed_cols).copy()

print(f"\nCleaned to {len(df_clean.columns)} main feature columns")
print(f"New shape: {df_clean.shape}\n")
print(f"Feature columns kept: {df_clean.columns.tolist()}\n")
print(df_clean.head())

# Step 2: Extract Year and Month from the 'Months' column
print("\n" + "="*80)
print("STEP 2: Extract Year and Month Information")
print("="*80)

# The 'Months' column contains info like "Jan", "Feb", etc.
# We need to infer the year from row position (assuming monthly sequence from 1995-2020)
months_in_year = 12
start_year = 1995

# Calculate year for each row
years = []
months = []
month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

for idx, row in enumerate(df_clean.iterrows()):
    year = start_year + (idx // months_in_year)
    month = (idx % months_in_year) + 1
    years.append(year)
    months.append(month)

df_clean['Year'] = years
df_clean['Month'] = months

print(f"✓ Year range: {min(years)} to {max(years)}")
print(f"✓ Data span: {len(years)} months ({max(years) - min(years) + 1} years)")
print(f"\nFirst 15 rows with Year and Month:")
print(df_clean[['Months', 'Year', 'Month']].head(15))

# Step 3: Create Flood Label
print("\n" + "="*80)
print("STEP 3: Create Flood Labels")
print("="*80)

df_clean['Flood'] = df_clean['Year'].apply(lambda x: 1 if x in FLOOD_YEARS else 0)

flood_counts = df_clean['Flood'].value_counts()
print(f"\nFlood Label Distribution:")
print(f"  Non-Flood Years (0): {flood_counts[0]} months")
print(f"  Flood Years (1): {flood_counts[1]} months")
print(f"  Flood Year List: {FLOOD_YEARS}")

# Step 4: Clean up column names
print("\n" + "="*80)
print("STEP 4: Standardize Column Names")
print("="*80)

# Rename columns to be more useful
rename_dict = {
    'Months': 'Month_Name',
    'Average of Max temp': 'Max_Temp',
    'Average of mean': 'Mean_Temp',
    'Average of Min': 'Min_Temp',
    'Average of Vapour Pressure': 'Vapour_Pressure',
    'Average of wind speed': 'Wind_Speed',
    'Average of precitation': 'Precipitation',
    'Average of shortwave radiation': 'Shortwave_Radiation',
    'Average of Mean Dew point': 'Dew_Point',
    'Cloud Amount': 'Cloud_Amount',
    'CO2': 'CO2',
    'PM2.5': 'PM2_5',
    'Mean Sea level Bay ofBengal': 'MSL_BayOfBengal',
    'Mean sea level Arabian sea': 'MSL_ArabianSea',
    'Mea sea level Indian ocean': 'MSL_IndianOcean',
    'SPI_3': 'SPI_3',
    'SPI_6': 'SPI_6',
    'SPI_12': 'SPI_12',
    'SPEI_3': 'SPEI_3',
    'SPEI_6': 'SPEI_6',
    'SPEI_12': 'SPEI_12',
    'DroughtBinary': 'Drought_Label'
}

df_clean.rename(columns=rename_dict, inplace=True)
print(f"Columns renamed: {len(rename_dict)} columns standardized")

# Step 5: Convert text columns to numeric
print("\n" + "="*80)
print("STEP 5: Convert Text Values to Numeric")
print("="*80)

numeric_cols = df_clean.columns.difference(['Month_Name', 'Year', 'Month', 'Flood', 'Drought_Label'])

for col in numeric_cols:
    # Replace text values with numeric where possible
    if df_clean[col].dtype == 'object':
        # Try to convert to numeric, coerce errors to NaN
        df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce')

print(f"\nConverted {len(numeric_cols)} columns to numeric")
print(f"\nData types after conversion:")
print(df_clean.dtypes)

# Step 6: Handle missing values
print("\n" + "="*80)
print("STEP 6: Handle Missing Values")
print("="*80)

missing_before = df_clean.isnull().sum().sum()
print(f"\nMissing values before imputation: {missing_before}")

# Fill missing values with median for each column
for col in numeric_cols:
    if df_clean[col].isnull().sum() > 0:
        median_val = df_clean[col].median()
        df_clean[col].fillna(median_val, inplace=True)
        print(f"  {col}: filled {df_clean[col].isnull().sum()} NaN with median")

missing_after = df_clean.isnull().sum().sum()
print(f"\nMissing values after imputation: {missing_after}")

# Step 7: Reorder columns for clarity
print("\n" + "="*80)
print("STEP 7: Organize Columns")
print("="*80)

# Put important columns first
important_cols = ['Year', 'Month', 'Month_Name', 'Flood', 'Drought_Label']
other_cols = [col for col in df_clean.columns if col not in important_cols]
df_final = df_clean[important_cols + other_cols]

print(f"Final dataset columns ({len(df_final.columns)}):")
for i, col in enumerate(df_final.columns, 1):
    print(f"  {i:2d}. {col}")

# Step 8: Save the processed dataset
print("\n" + "="*80)
print("STEP 8: Save Processed Dataset")
print("="*80)

# Save as CSV
csv_filename = "cleaned_flood_dataset.csv"
df_final.to_csv(csv_filename, index=False)
print(f"✓ Saved as CSV: {csv_filename}")

# Also save as Excel
excel_filename = "cleaned_flood_dataset.xlsx"
df_final.to_excel(excel_filename, index=False, sheet_name='Flood_Data')
print(f"✓ Saved as Excel: {excel_filename}")

# Print summary
print("\n" + "="*80)
print("FINAL DATASET SUMMARY")
print("="*80)
print(f"\nShape: {df_final.shape}")
print(f"Rows: {len(df_final)}")
print(f"Columns: {len(df_final.columns)}")
print(f"\nYear Range: {df_final['Year'].min()} to {df_final['Year'].max()}")
print(f"Total Months: {len(df_final)}")
print(f"Expected Months (26 years × 12): {26 * 12}")
print(f"\nTarget Variable Distribution:")
print(f"  Flood Years: {(df_final['Flood']==1).sum()} months ({(df_final['Flood']==1).sum()/len(df_final)*100:.1f}%)")
print(f"  Non-Flood Years: {(df_final['Flood']==0).sum()} months ({(df_final['Flood']==0).sum()/len(df_final)*100:.1f}%)")

print(f"\nFirst 10 rows of final dataset:")
print(df_final.head(10))

print(f"\nLast 10 rows of final dataset:")
print(df_final.tail(10))

print("\n" + "="*80)
print("✓ DATA PROCESSING COMPLETE!")
print("="*80)
print("\nYou can now use 'cleaned_flood_dataset.csv' in your flood prediction notebook.")
print("Update the notebook to load: df = pd.read_csv('cleaned_flood_dataset.csv')")
