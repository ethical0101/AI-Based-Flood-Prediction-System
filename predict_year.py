import argparse
from pathlib import Path

import joblib
import numpy as np
import pandas as pd


COLUMN_MAPPING = {
    "Cloud Amount": "Cloud_Amount",
    "Average of Mean Dew point": "Dew_Point",
    "Mean sea level Arabian sea": "MSL_ArabianSea",
    "Mean Sea level Bay ofBengal": "MSL_BayOfBengal",
    "Mea sea level Indian ocean": "MSL_IndianOcean",
    "Average of Max temp": "Max_Temp",
    "Average of mean": "Mean_Temp",
    "Average of Min": "Min_Temp",
    "PM2.5": "PM2_5",
    "Average of precitation": "Precipitation",
    "Average of shortwave radiation": "Shortwave_Radiation",
    "Average of Vapour Pressure": "Vapour_Pressure",
    "Average of wind speed": "Wind_Speed",
}


MONSOON_MONTHS = {6, 7, 8, 9}
POST_MONSOON_MONTHS = {10, 11, 12}
SUMMER_MONTHS = {3, 4, 5}


def normalize_month_series(df: pd.DataFrame) -> pd.Series:
    if "Month" in df.columns:
        month = pd.to_numeric(df["Month"], errors="coerce")
    elif "Months" in df.columns:
        month = pd.to_numeric(df["Months"], errors="coerce")
    else:
        raise ValueError("Input data must contain either 'Month' or 'Months' column.")

    if month.isna().any():
        raise ValueError("Month column has non-numeric or missing values.")

    # Normalize non-standard month coding into 1..12.
    return ((month.astype(int) - 1) % 12) + 1


def harmonize_schema(year_df: pd.DataFrame) -> pd.DataFrame:
    out = year_df.rename(columns=COLUMN_MAPPING).copy()

    month_normalized = normalize_month_series(out)
    out["Month_Normalized"] = month_normalized
    out["Is_Monsoon"] = month_normalized.isin(MONSOON_MONTHS).astype(int)
    out["Is_PostMonsoon"] = month_normalized.isin(POST_MONSOON_MONTHS).astype(int)
    out["Is_Summer"] = month_normalized.isin(SUMMER_MONTHS).astype(int)

    return out


def predict_year(
    year: int,
    input_csv: Path,
    model_path: Path,
    scaler_path: Path,
    feature_names_path: Path,
    output_csv: Path,
) -> pd.DataFrame:
    df = pd.read_csv(input_csv)

    if "Year" not in df.columns:
        raise ValueError("Input CSV must contain 'Year' column.")

    year_df = df[df["Year"] == year].copy()
    if year_df.empty:
        available_years = sorted(df["Year"].dropna().astype(int).unique().tolist())
        raise ValueError(
            f"No rows found for year {year}. Available years: {available_years}"
        )

    year_df = harmonize_schema(year_df)

    model = joblib.load(model_path)
    scaler = joblib.load(scaler_path)
    feature_names = joblib.load(feature_names_path)

    missing_features = [c for c in feature_names if c not in year_df.columns]
    if missing_features:
        raise ValueError(
            "Input data does not have all required model features. Missing: "
            + ", ".join(missing_features)
        )

    X = year_df[feature_names].astype(float)
    X_scaled = scaler.transform(X)

    predicted_label = model.predict(X_scaled).astype(int)
    if hasattr(model, "predict_proba"):
        flood_probability = model.predict_proba(X_scaled)[:, 1]
    else:
        flood_probability = predicted_label.astype(float)

    result = pd.DataFrame(
        {
            "Year": year_df["Year"].astype(int),
            "Month_Raw": year_df["Month"] if "Month" in year_df.columns else year_df["Months"],
            "Month_Normalized": year_df["Month_Normalized"].astype(int),
            "Predicted_Flood_Label": predicted_label,
            "Flood_Probability": np.round(flood_probability, 4),
        }
    )
    result["Predicted_Class"] = result["Predicted_Flood_Label"].map(
        {0: "Non-Flood", 1: "Flood"}
    )

    result.to_csv(output_csv, index=False)
    return result


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Predict flood class for any year using saved flood model artifacts."
    )
    parser.add_argument("--year", type=int, required=True, help="Target year to predict")
    parser.add_argument(
        "--input-csv",
        type=Path,
        default=Path("modified_flood_dataset.csv"),
        help="Path to source CSV containing feature rows",
    )
    parser.add_argument(
        "--model",
        type=Path,
        default=Path("Gradient_Boosting_flood_predictor.pkl"),
        help="Path to trained model artifact",
    )
    parser.add_argument(
        "--scaler",
        type=Path,
        default=Path("feature_scaler.pkl"),
        help="Path to scaler artifact",
    )
    parser.add_argument(
        "--feature-names",
        type=Path,
        default=Path("feature_names.pkl"),
        help="Path to feature names artifact",
    )
    parser.add_argument(
        "--output-csv",
        type=Path,
        default=None,
        help="Output predictions CSV path (default: predictions_<year>.csv)",
    )

    args = parser.parse_args()
    output_csv = args.output_csv or Path(f"predictions_{args.year}.csv")

    try:
        result = predict_year(
            year=args.year,
            input_csv=args.input_csv,
            model_path=args.model,
            scaler_path=args.scaler,
            feature_names_path=args.feature_names,
            output_csv=output_csv,
        )
    except ValueError as exc:
        print(f"Prediction failed: {exc}")
        raise SystemExit(1)

    flood_count = int((result["Predicted_Flood_Label"] == 1).sum())
    total = len(result)
    avg_prob = float(result["Flood_Probability"].mean())

    print(f"Prediction complete for year {args.year}")
    print(f"Rows scored: {total}")
    print(f"Flood predictions: {flood_count}/{total}")
    print(f"Average flood probability: {avg_prob:.4f}")
    print(f"Saved: {output_csv}")


if __name__ == "__main__":
    main()
