# Multivariate Parameter Relationship Analysis

Dataset: `cleaned_flood_dataset.csv`

## What Was Compared
- Pairwise correlations between all numeric parameters
- Direct relation of each parameter with Flood label
- Multivariate comparison (pairplot) of top flood-related parameters
- Flood vs Non-Flood distributions for strongest parameters

## Top Positive Correlations with Flood
| Feature | Correlation with Flood |
|---|---:|
| Year | 0.4042 |
| CO2 | 0.3010 |
| MSL_BayOfBengal | 0.2459 |
| SPI_12 | 0.2271 |
| MSL_IndianOcean | 0.2208 |
| SPEI_12 | 0.1335 |

## Top Negative Correlations with Flood
| Feature | Correlation with Flood |
|---|---:|
| Min_Temp | -0.0090 |
| Shortwave_Radiation | -0.0349 |
| Cloud_Amount | -0.0377 |
| Wind_Speed | -0.0464 |
| SPEI_6 | -0.0504 |
| PM2_5 | -0.1069 |

## Strong Inter-Parameter Correlations (|r| >= 0.70)
| Parameter A | Parameter B | Correlation |
|---|---|---:|
| Cloud_Amount | Shortwave_Radiation | 0.9859 |
| Cloud_Amount | Dew_Point | -0.8506 |
| Precipitation | Vapour_Pressure | 0.8151 |
| Dew_Point | Shortwave_Radiation | -0.7829 |

## Generated Visual Files
- `parameter_correlation_heatmap.png`
- `flood_top_parameter_relations.png`
- `multivariate_pairplot_top_parameters.png`
- `flood_vs_nonflood_multivariate_boxplot.png`

## Interpretation Note
Correlation indicates statistical association, not guaranteed causation. Parameters should be interpreted with domain context (rainfall systems, seasonal cycles, pressure systems).