import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

# Define flood years
FLOOD_YEARS = [1996, 2005, 2008, 2010, 2015, 2016, 2017, 2018, 2020]

print("="*80)
print("ADVANCED EXCEL DATA CLEANING WITH IMPROVED HANDLING")
print("="*80)

# Load with different approaches to find the best starting row
file_name = "kullback category and weights xlx.xlsx"

# Try loading and inspecting first
print("\nAnalyzing Excel structure...")
raw_df = pd.read_excel(file_name, sheet_name='kullback category and weights', header=None)
print(f"Raw shape: {raw_df.shape}")
print(f"\nFirst 5 rows (raw):")
print(raw_df.head())

# The data structure seems consistent, so let's reload normally
df = pd.read_excel(file_name, sheet_name='kullback category and weights')

print(f"\n\nProcessing with proper column handling...")
print(f"Loaded shape: {df.shape}")

# Remove Unnamed columns
unnamed_cols = [col for col in df.columns if 'Unnamed' in col]
df_clean = df.drop(columns=unnamed_cols).copy()

print(f"After removing Unnamed columns: {df_clean.shape}")
print(f"\nColumns: {df_clean.columns.tolist()}")

# Extract and create Year/Month information
print("\n" + "="*80)
print("Extracting Year and Month from Row Sequence")
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
print(f"✓ Total months: {len(years)}")

# Create Flood label
df_clean['Flood'] = df_clean['Year'].apply(lambda x: 1 if x in FLOOD_YEARS else 0)

print(f"\n" + "="*80)
print("Converting Text Values to Numeric")
print("="*80)

# For each column (except Months and Drought), try to convert to numeric
text_cols = df_clean.select_dtypes(include='object').columns.tolist()
print(f"\nText columns found: {text_cols}")

for col in text_cols:
    if col not in ['Months', 'DroughtBinary']:
        # Count non-numeric values before conversion
        df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce')
        non_numeric = df_clean[col].isnull().sum()
        if non_numeric > 0:
            print(f"  {col}: {non_numeric} values couldn't be converted (filled with NaN)")

# Now fill remaining NaN values with column medians
print(f"\n" + "="*80)
print("Handling Missing Values")
print("="*80)

numeric_cols = df_clean.select_dtypes(include=[np.number]).columns
nan_count_before = df_clean[numeric_cols].isnull().sum().sum()
print(f"Total NaN values before imputation: {nan_count_before}")

for col in numeric_cols:
    if col not in ['Year', 'Month', 'Flood']:
        median_val = df_clean[col].median()
        nan_in_col = df_clean[col].isnull().sum()
        if nan_in_col > 0:
            df_clean[col].fillna(median_val, inplace=True)
            print(f"  {col}: filled {nan_in_col} NaN with median ({median_val:.4f})")

nan_count_after = df_clean[numeric_cols].isnull().sum().sum()
print(f"\nTotal NaN values after imputation: {nan_count_after}")

# Rename columns for clarity
print(f"\n" + "="*80)
print("Renaming Columns for Clarity")
print("="*80)

rename_map = {
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

df_clean.rename(columns=rename_map, inplace=True)
print(f"✓ {len(rename_map)} columns renamed")

# Reorder columns
important_cols = ['Year', 'Month', 'Month_Name', 'Flood', 'Drought_Label']
other_cols = [col for col in df_clean.columns if col not in important_cols + ['Months']]
df_final = df_clean[important_cols + other_cols].copy()

print(f"\n" + "="*80)
print("Final Dataset Summary")
print("="*80)

print(f"\nShape: {df_final.shape}")
print(f"Columns ({len(df_final.columns)}): {df_final.columns.tolist()}")

print(f"\nFlood Distribution:")
flood_counts = df_final['Flood'].value_counts()
print(f"  Non-Flood (0): {flood_counts[0]} ({flood_counts[0]/len(df_final)*100:.1f}%)")
print(f"  Flood (1): {flood_counts[1]} ({flood_counts[1]/len(df_final)*100:.1f}%)")

print(f"\nMissing Values: {df_final.isnull().sum().sum()}")
print(f"Data Quality: ✓ Complete")

# Save
print(f"\n" + "="*80)
print("Saving Processed Dataset")
print("="*80)

csv_file = "cleaned_flood_dataset.csv"
xlsx_file = "cleaned_flood_dataset.xlsx"

df_final.to_csv(csv_file, index=False)
df_final.to_excel(xlsx_file, index=False, sheet_name='Flood_Data')

print(f"✓ Saved: {csv_file}")
print(f"✓ Saved: {xlsx_file}")

print(f"\nSample Data (First 10 rows):")
print(df_final[['Year', 'Month', 'Month_Name', 'Flood', 'Precipitation', 'Max_Temp']].head(10).to_string())

print(f"\n" + "="*80)
print("✓ EXCEL DATA PROCESSING COMPLETE!")
print("="*80)
print(f"\nUse 'cleaned_flood_dataset.csv' in the flood prediction notebook.")
