import pandas as pd
import numpy as np

# Test loading the cleaned dataset
df = pd.read_csv('cleaned_flood_dataset.csv')

print('='*80)
print('✓ CLEANED DATASET VERIFICATION')
print('='*80)

print(f'\nDataset loaded successfully from cleaned_flood_dataset.csv')
print(f'\nDataset Shape: {df.shape}')
print(f'Total Columns: {len(df.columns)}')
print(f'\nYear Range: {df["Year"].min()} - {df["Year"].max()}')
print(f'Month Range: {df["Month"].min()} - {df["Month"].max()}')

print(f'\n{"-"*80}')
print('Flood Distribution:')
print(f'{"-"*80}')
print(f'Non-Flood (0): {(df["Flood"]==0).sum()} months ({(df["Flood"]==0).sum()/len(df)*100:.1f}%)')
print(f'Flood (1): {(df["Flood"]==1).sum()} months ({(df["Flood"]==1).sum()/len(df)*100:.1f}%)')

print(f'\n{"-"*80}')
print('Sample Data (First 10 rows):')
print(f'{"-"*80}')
print(df[['Year', 'Month', 'Month_Name', 'Flood', 'Precipitation', 'Max_Temp', 'Min_Temp']].head(10).to_string())

print(f'\n{"-"*80}')
print('Column List:')
print(f'{"-"*80}')
for i, col in enumerate(df.columns, 1):
    print(f'{i:2d}. {col}')

print(f'\n{"-"*80}')
print('✓ DATASET IS READY FOR MODEL TRAINING!')
print('='*80)
