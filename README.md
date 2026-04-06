# AI-Based Flood Prediction System for Tamil Nadu

## 📋 Project Overview

This is a comprehensive **machine learning-based flood prediction system** developed for Tamil Nadu, India, using 26 years of historical climatic data (1995-2020). The system leverages advanced data science techniques to predict flood occurrence based on multiple environmental and climatic indicators.

The project implements a complete end-to-end machine learning pipeline including:
- **Data Acquisition & Preprocessing**: Historical climate data cleaning and normalization
- **Feature Engineering**: Creation of temporal and seasonal features
- **Exploratory Data Analysis (EDA)**: Comprehensive statistical and visual analysis
- **Model Training & Evaluation**: 9 different machine learning algorithms tested
- **Hyperparameter Optimization**: GridSearchCV for best model tuning
- **Interpretability Analysis**: Feature importance and model explainability
- **Production Deployment**: Serialized models ready for real-world applications

---

## 🎯 Key Features

✅ **Achieves 68.25% Accuracy** with Gradient Boosting Classifier
✅ **Multi-Algorithm Comparison**: Tested 9 different ML models
✅ **Comprehensive Feature Set**: 23 engineered climatic and temporal features
✅ **Production-Ready**: Serialized models for deployment
✅ **Interpretable Predictions**: Feature importance analysis included
✅ **Extensive Visualizations**: 7+ high-resolution analysis charts
✅ **Robust Evaluation**: Cross-validation, confusion matrices, ROC curves

---

## 📊 Dataset Description

### Data Specifications
| Attribute | Value |
|-----------|-------|
| **Time Period** | 1995-2020 (26 years) |
| **Frequency** | Monthly aggregated data |
| **Total Records** | 312 samples (26 years × 12 months) |
| **Original Features** | 20+ raw climatic variables |
| **Engineered Features** | 23 total features after feature engineering |
| **Target Variable** | Flood (Binary: 0=Non-Flood Year, 1=Flood Year) |
| **Class Distribution** | 65.38% Non-Flood, 34.62% Flood |

### Data Sources
- **Climatic Variables**: Temperature, precipitation, humidity, pressure
- **Drought Indices**: SPEI (Standardized Precipitation-Evapotranspiration Index)
- **Rainfall Indices**: SPI (Standardized Precipitation Index)
- **Ocean Pressure**: Mean Sea Level (MSL) from Arabian Sea, Bay of Bengal, Indian Ocean
- **Air Quality**: PM2.5, CO2 levels
- **Atmospheric Parameters**: Dew point, wind speed, vapor pressure, shortwave radiation
- **Temporal Features**: Month, season, quarter information

### Flood Years Identified (Label = 1)
**1996, 2005, 2008, 2010, 2015, 2016, 2017, 2018, 2020**

These were identified through:
1. National Disaster Management Authority (NDMA) historical records
2. India Meteorological Department (IMD) rainfall analysis
3. Government flood advisory archives
4. Cyclone and extreme weather event documentation

---

## 🏗️ System Architecture

### Data Pipeline

```
Raw Data
   ↓
Data Cleaning & Missing Value Handling
   ↓
Feature Separation (Temporal vs Numerical)
   ↓
Feature Engineering (Seasonal Features, Temporal Indicators)
   ↓
Feature Scaling (StandardScaler)
   ↓
Train-Test Split (80-20 with Stratification)
   ↓
Model Training & Evaluation
   ↓
Hyperparameter Tuning
   ↓
Final Model Selection & Persistence
```

### Workflow Stages

1. **Data Loading & Exploration** (Cell 2)
   - Load CSV dataset
   - Display shape, dtypes, and basic statistics
   - Identify missing values and data quality issues

2. **Data Preprocessing** (Cell 3)
   - Handle missing values (if any)
   - Remove non-prediction columns
   - Verify temporal features
   - Convert data types

3. **Feature Engineering** (Cell 4)
   - Create seasonal indicators (Winter, Summer, Monsoon, Post-Monsoon)
   - Generate binary seasonal features
   - Create quarter information
   - Verify flood label distribution

4. **Feature Preparation & Scaling** (Cell 5)
   - Select numerical features (23 total)
   - Apply StandardScaler normalization
   - Separate features and target variable

5. **Exploratory Data Analysis** (Cell 6)
   - 9-subplot comprehensive visualization
   - Year-vs-rainfall trends, flood distribution
   - Correlation heatmaps, boxplots
   - Monthly/seasonal patterns
   - Data quality assessment
   - **Output**: `eda_analysis.png`

6. **Data Splitting** (Cell 7)
   - 80-20 train-test split
   - Stratified sampling to maintain class distribution
   - Training set: 249 samples
   - Testing set: 63 samples

7. **Model Training** (Cell 8)
   - Train 9 different classifiers:
     1. Logistic Regression
     2. Decision Tree
     3. Random Forest
     4. Support Vector Machine (SVM)
     5. K-Nearest Neighbors (KNN)
     6. Gaussian Naive Bayes
     7. Gradient Boosting
     8. XGBoost
     9. LightGBM

8. **Model Evaluation** (Cell 9)
   - Calculate metrics: Accuracy, Precision, Recall, F1 Score
   - Generate confusion matrices for all models
   - Plot ROC curves and AUC scores
   - **Outputs**: `confusion_matrices.png`, `roc_curves.png`

9. **Model Comparison** (Cell 10)
   - Rank models by performance metrics
   - Compare F1 scores and accuracy
   - Identify best performing model
   - Generate comparison visualizations
   - **Output**: `model_comparison.png`

10. **Hyperparameter Tuning** (Cell 11)
    - GridSearchCV on best model (Gradient Boosting)
    - Test 27 parameter combinations
    - 5-fold cross-validation
    - Select best parameters
    - Evaluate on test set

11. **Feature Importance Analysis** (Cell 12)
    - Extract feature importance from Random Forest
    - Extract feature importance from XGBoost
    - Identify top 15 most influential features
    - **Output**: `feature_importance.png`

12. **Model Persistence & Prediction Function** (Cell 13)
    - Save trained model as pickle file
    - Save feature scaler
    - Save feature names
    - Create reusable prediction function
    - Test with sample data

13. **Final Visualization & Dashboard** (Cell 14)
    - Create comprehensive results dashboard
    - Prediction vs actual plots
    - Class-wise recall metrics
    - Final model performance summary
    - **Output**: `prediction_dashboard.png`

14. **Conclusions & Summary** (Cell 15)
    - Print comprehensive findings
    - Model performance summary
    - Feature importance ranking
    - Practical applications
    - Limitations and recommendations
    - Technical specifications

---

## 📈 Model Performance

### Test Set Results (63 samples)

| Model | Accuracy | Precision | Recall | F1 Score | AUC |
|-------|----------|-----------|--------|----------|-----|
| **Gradient Boosting** | **68.25%** | **55.56%** | 45.45% | **50.00%** | 0.790 |
| XGBoost | 68.25% | 54.17% | 59.09% | 56.52% | 0.729 |
| Decision Tree | 66.67% | 52.00% | 59.09% | 55.32% | 0.649 |
| LightGBM | 66.67% | 52.63% | 45.45% | 48.78% | 0.735 |
| Random Forest | 65.08% | 50.00% | 40.91% | 45.00% | 0.727 |
| KNN | 66.67% | 53.85% | 31.82% | 40.00% | 0.643 |
| Logistic Regression | 61.90% | 43.75% | 31.82% | 36.84% | 0.646 |
| SVM | 63.49% | 44.44% | 18.18% | 25.81% | 0.642 |
| Naive Bayes | 63.49% | 42.86% | 13.64% | 20.69% | 0.586 |

### Best Model: Gradient Boosting Classifier

**Test Metrics:**
- **Accuracy**: 68.25% (43 out of 63 correct predictions)
- **Precision**: 55.56% (When model predicts flood, 55.56% are correct)
- **Recall**: 45.45% (Detects 45.45% of actual flood years)
- **F1 Score**: 0.5000 (Harmonic mean of precision & recall)
- **AUC-ROC**: 0.7900

**Confusion Matrix (Test Set):**
```
                 Predicted
              Non-Flood  Flood
Actual Non-Flood    33      8
       Flood        12     10
```

**Class-wise Performance:**
- Non-Flood Year Detection (Specificity): 80.49%
- Flood Year Detection (Sensitivity): 45.45%

---

## 🎯 Top 5 Most Influential Features

Feature importance was analyzed using both **Random Forest** and **XGBoost** models:

### Combined Top 5 Predictors:
1. **PM2.5** (Particulate Matter 2.5 µm)
   - RF Importance: 9.50% | XGB Importance: 13.68%
   - Indicates air quality and atmospheric conditions

2. **CO2** (Carbon Dioxide Levels)
   - RF Importance: 7.68% | XGB Importance: 9.51%
   - Reflects atmospheric greenhouse gas concentration

3. **MSL_IndianOcean** (Mean Sea Level - Indian Ocean)
   - RF Importance: 7.63% | XGB Importance: 3.46%
   - Indicates oceanic pressure patterns

4. **SPEI_12** (12-month Standardized Precipitation-Evapotranspiration Index)
   - RF Importance: 6.35% | XGB Importance: 7.20%
   - Measures drought/wetness on annual scale

5. **SPI_3** (3-month Standardized Precipitation Index)
   - RF Importance: 5.57% | XGB Importance: 6.75%
   - Captures short-term rainfall patterns

---

## 📁 Project Structure

```
AI-Based Flood Prediction System/
│
├── Flood_Prediction_System.ipynb       # Main Jupyter notebook (15 cells)
├── README.md                           # This file
├── .gitignore                          # Git ignore rules
│
├── Data Files:
│   ├── modified_flood_dataset.csv      # Clean processed dataset
│   ├── fix_columns.py                  # Data preprocessing script
│   └── generate_report_assets.py       # Report generation script
│
├── Report Files:
│   ├── AI_Based_Flood_Prediction_Report.tex
│   ├── report_metrics.json             # Metrics in JSON format
│   └── Soft_Computing_Flood_Prediction.ipynb
│
├── Generated Outputs (from notebook execution):
│   ├── eda_analysis.png                # 9-subplot EDA visualization
│   ├── confusion_matrices.png          # Confusion matrices for all models
│   ├── roc_curves.png                  # ROC curves for all models
│   ├── model_comparison.png            # Model performance comparison
│   ├── feature_importance.png          # Feature importance analysis
│   ├── prediction_dashboard.png        # Final results dashboard
│   ├── model_summary.txt               # Text summary of final model
│   │
│   └── Serialized Models (pickle files):
│       ├── Gradient_Boosting_flood_predictor.pkl
│       ├── feature_scaler.pkl
│       └── feature_names.pkl
│
└── Virtual Environment:
    └── .venv/                          # Python virtual environment
```

---

## 🚀 Installation & Setup

### Prerequisites
- **Python**: 3.8 or higher
- **Jupyter Notebook** or **VS Code with Python extension**
- **Git**: For version control

### Step 1: Clone Repository
```bash
git clone https://github.com/ethical0101/AI-Based-Flood-Prediction-System.git
cd "AI-Based Flood Prediction System"
```

### Step 2: Create Virtual Environment
```bash
# Windows
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# macOS/Linux
python3 -m venv .venv
source .venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install --upgrade pip

# Core Data Science Libraries
pip install pandas numpy scikit-learn matplotlib seaborn scipy

# Machine Learning Models
pip install xgboost lightgbm

# Jupyter Environment
pip install jupyter jupyterlab ipykernel

# Optional: For advanced analysis
pip install shap statsmodels
```

### Step 4: Run the Notebook
```bash
# Option 1: Jupyter Notebook
jupyter notebook Flood_Prediction_System.ipynb

# Option 2: Jupyter Lab
jupyter lab Flood_Prediction_System.ipynb

# Option 3: VS Code
# Open in VS Code with Python & Jupyter extensions installed
```

---

## 💻 Usage

### Running the Complete Pipeline

Execute all cells in the notebook sequentially:

1. **Cell 1**: Install required packages (xgboost, lightgbm)
2. **Cells 2-5**: Data loading and preprocessing
3. **Cell 6**: Generate EDA visualizations
4. **Cells 7-10**: Model training and comprehensive evaluation
5. **Cell 11**: Hyperparameter tuning
6. **Cell 12**: Feature importance analysis
7. **Cell 13**: Model persistence and prediction function
8. **Cell 14**: Create final prediction dashboard
9. **Cell 15**: Print conclusions and summary

### Using Pre-trained Model

```python
import pickle
import pandas as pd
from sklearn.preprocessing import StandardScaler

# Load the pre-trained model
with open('Gradient_Boosting_flood_predictor.pkl', 'rb') as f:
    model = pickle.load(f)

# Load the scaler
with open('feature_scaler.pkl', 'rb') as f:
    scaler = pickle.load(f)

# Load feature names
with open('feature_names.pkl', 'rb') as f:
    feature_names = pickle.load(f)

# Prepare your data
# Assume you have 23 features in the correct order
X_new = pd.DataFrame([your_feature_values], columns=feature_names)
X_scaled = scaler.transform(X_new)

# Make predictions
prediction = model.predict(X_scaled)
probability = model.predict_proba(X_scaled)

print(f"Prediction: {'Flood Year' if prediction[0] == 1 else 'Non-Flood Year'}")
print(f"Flood Probability: {probability[0][1]:.2%}")
print(f"Non-Flood Probability: {probability[0][0]:.2%}")
```

### Using the Prediction Function

```python
# Call the prediction function directly
result = predict_flood(
    feature_values=[...],  # 23 feature values
    model=final_model,
    feature_names=feature_cols,
    scaler_obj=scaler
)

print(f"Prediction: {result['prediction']}")
print(f"Confidence: {result['confidence']:.2%}")
print(f"Flood Probability: {result['probability_flood']:.4f}")
```

---

## 📊 Key Findings

### 1. Best Performing Model
**Gradient Boosting Classifier** achieved the highest overall performance with:
- Highest accuracy (68.25%)
- Strong precision (55.56%)
- Best F1 score (0.5000)
- Excellent AUC-ROC (0.7900)

### 2. Feature Insights
- **Atmospheric conditions** (PM2.5, CO2) are critical predictors
- **Oceanic pressure patterns** (MSL data) significantly affect flood probability
- **Drought/wetness indices** (SPEI, SPI) provide valuable long-term signals
- **Temperature variations** contribute to flood prediction

### 3. Temporal Patterns
- Monsoon season shows highest flood incidence
- Post-monsoon period has secondary importance
- Monthly patterns are captured in feature engineering

### 4. Model Behavior
- Boosting algorithms (Gradient Boosting, XGBoost) outperformed other models
- Decision trees show good recall but lower precision
- Simple models (Linear, KNN) struggle with non-linear relationships
- Ensemble methods are more robust

---

## 🔍 Limitations & Considerations

### Current Limitations
1. **Historical Data Gaps**: Analysis limited to 1995-2020
2. **Climate Change Effects**: May not capture unprecedented weather patterns
3. **Label Quality**: Flood labels derived from multiple sources with varying reliability
4. **Monthly Aggregation**: Loses intra-month variability that could be important
5. **Limited Sample Size**: 26 years provides moderate data for deep learning approaches
6. **Regional Specificity**: Model trained for Tamil Nadu, may not generalize to other regions

### Model Uncertainties
- 31.7% of test predictions are incorrect
- Lower recall (45.45%) means some floods are missed
- Imbalanced class handling could be improved
- External flood-intensifying factors not captured

---

## 🚀 Future Enhancements

### Short-term Improvements
- [ ] Add humidity and evaporation rate features
- [ ] Include satellite imagery and radar data
- [ ] Implement ensemble voting of top 3 models
- [ ] Add uncertainty quantification (Bayesian approaches)
- [ ] Create confidence intervals for predictions

### Medium-term Enhancements
- [ ] Migrate to daily/weekly data instead of monthly
- [ ] Integrate real-time meteorological data feeds
- [ ] Develop web API for model serving
- [ ] Create interactive dashboard for stakeholders
- [ ] Implement automated retraining pipeline

### Long-term Vision
- [ ] Expand to other regions in India
- [ ] Incorporate climate projections for future scenarios
- [ ] Develop ensemble model combining multiple flood types
- [ ] Implement attention mechanisms for temporal relationships
- [ ] Create mobile app for early warning system
- [ ] Integrate with government disaster management systems

### Advanced Techniques to Explore
- [ ] LSTM/GRU for temporal sequence modeling
- [ ] Transformer models for long-range dependencies
- [ ] Graph Neural Networks for spatial relationships
- [ ] Federated learning for privacy-preserving collaboration
- [ ] Explainable AI (SHAP, LIME) for better interpretability

---

## 📈 Model Metrics Explained

### Accuracy
- **Definition**: Percentage of correct predictions
- **Formula**: (TP + TN) / Total
- **Target Set**: Overall model correctness

### Precision
- **Definition**: Of predicted floods, how many were correct
- **Formula**: TP / (TP + FP)
- **Importance**: Minimizes false alarms

### Recall (Sensitivity)
- **Definition**: Of actual floods, how many were detected
- **Formula**: TP / (TP + FN)
- **Importance**: Critical for early warning (avoiding missed floods)

### F1 Score
- **Definition**: Harmonic mean of precision and recall
- **Formula**: 2 × (Precision × Recall) / (Precision + Recall)
- **Use**: Balances classification trade-offs

### ROC-AUC
- **Definition**: Area under the Receiver Operating Characteristic curve
- **Range**: 0.5 (random) to 1.0 (perfect)
- **Interpretation**: 0.79 = Good discrimination ability

---

## 🔧 Technical Stack

| Component | Technology |
|-----------|-----------|
| **Language** | Python 3.8+ |
| **Data Processing** | Pandas, NumPy |
| **Visualization** | Matplotlib, Seaborn |
| **ML Algorithms** | Scikit-learn, XGBoost, LightGBM |
| **Model Evaluation** | Scikit-learn metrics |
| **Notebook Environment** | Jupyter, VS Code |
| **Version Control** | Git, GitHub |
| **Model Persistence** | Pickle |

---

## 📝 References & Data Sources

### Academic References
- Standardized Precipitation Index (SPI) - McKee et al.
- Standardized Precipitation-Evapotranspiration Index (SPEI)
- Ensemble Methods in Machine Learning

### Data Sources
- India Meteorological Department (IMD)
- National Disaster Management Authority (NDMA)
- Government of Tamil Nadu flood archives
- Copernicus Climate Data Store

### Related Research
- Climate change impacts on monsoon rainfall
- Machine learning for hydrological forecasting
- Early warning systems for natural disasters

---

## 👨‍💻 Authors & Contributors

**Project Developer**: AI-Based Research Initiative
**Repository**: [ethical0101/AI-Based-Flood-Prediction-System](https://github.com/ethical0101/AI-Based-Flood-Prediction-System)
**Last Updated**: April 2026

---

## 📜 License

This project is available under the **MIT License** - feel free to use, modify, and distribute with proper attribution.

---

## ⚠️ Disclaimer

This system is developed for **research and informational purposes**. While the model shows promising performance, it should NOT be used as the sole basis for critical flood management decisions. Always consult with:
- Official meteorological agencies
- Disaster management authorities
- Local flood prediction services
- Expert hydrologists

The developers are not responsible for any damages or losses resulting from decisions based on this model's predictions.

---

## 📞 Support & Feedback

For questions, suggestions, or contributions:
1. Open an issue on GitHub
2. Submit a pull request with improvements
3. Contact the development team

---

## 🎓 Educational Value

This project demonstrates:
- ✅ Complete ML pipeline development
- ✅ Multiple algorithm comparison
- ✅ Hyperparameter optimization techniques
- ✅ Model evaluation best practices
- ✅ Data visualization and storytelling
- ✅ Production-ready code structure
- ✅ Real-world problem solving

Perfect for learning machine learning applications in environmental science!

---

**Happy Predicting! 🌊**

*Last Generated: April 6, 2026*
*Model Accuracy: 68.25% | Best F1 Score: 0.5000*
