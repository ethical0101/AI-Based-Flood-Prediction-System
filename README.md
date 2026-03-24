# AI-Based-Flood-Prediction-System

AI-based flood prediction project for Tamil Nadu climate data using machine learning and soft computing methods.

## Project Summary
- Region: Tamil Nadu, India
- Time range: 1995-2020
- Records: 312 monthly samples
- Core task: Multi-class classification
  - 0: Normal
  - 1: Drought
  - 2: Flood

## Methods Used
- Logistic Regression
- Random Forest
- Support Vector Machine (SVM)
- Artificial Neural Network (TensorFlow/Keras)
- Fuzzy Logic inference model

## Dataset Files
- `modified_flood_dataset.csv` (primary modeling dataset)
- `kullback category and weights xlx.xlsx` (raw source/derived dataset file)

## Main Notebook
- `Soft_Computing_Flood_Prediction.ipynb`

## How to Run
1. Create and activate a Python environment.
2. Install dependencies:
   - `pandas`, `numpy`, `matplotlib`, `seaborn`, `scikit-learn`, `tensorflow`, `scikit-fuzzy`, `openpyxl`
3. Open and run all cells in the notebook.

## Key Outputs
- Model evaluation metrics (accuracy, precision, recall, F1-score)
- Confusion matrix and comparison visualizations
- Predicted flood-year analysis for Tamil Nadu

## Notes
This repository focuses on core reproducible code and dataset artifacts. Auto-generated report artifacts and helper files are excluded via `.gitignore`.
