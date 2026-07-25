from pathlib import Path
import sys

import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent
DEFAULT_DATASET_PATH = BASE_DIR / "data" / "Expanded_Dataset_With_Ranges.csv"

REQUIRED_BASE_COLUMNS = [
    "City",
    "Country",
    "Month",
    "Year",
    "Temperature_Min",
    "Temperature_Max",
    "Humidity_Min",
    "Humidity_Max",
]


def get_disease_columns(df: pd.DataFrame) -> list[str]:
    feature_cols = {
        "City",
        "Country",
        "Month",
        "Year",
        "Temperature_Min",
        "Temperature_Max",
        "Humidity_Min",
        "Humidity_Max",
    }
    disease_cols = []
    for col in df.columns:
        if col in feature_cols:
            continue
        if col.endswith("_Symptoms") or col.endswith("_Advice"):
            continue
        if pd.api.types.is_numeric_dtype(df[col]):
            disease_cols.append(col)
    return disease_cols


def validate(path: Path | str) -> int:
    errors: list[str] = []
    warnings: list[str] = []
    path = Path(path)

    if not path.exists():
        print(f"[ERROR] Dataset file not found: {path}")
        return 1

    try:
        df = pd.read_csv(path)
    except Exception as exc:
        print(f"[ERROR] Failed to read CSV: {exc}")
        return 1

    # Required columns
    for col in REQUIRED_BASE_COLUMNS:
        if col not in df.columns:
            errors.append(f"Missing required column: {col}")

    if errors:
        print("Dataset validation FAILED")
        for err in errors:
            print(f"- {err}")
        return 1

    # Basic row checks
    if df.empty:
        errors.append("Dataset is empty")
    if df.duplicated().any():
        warnings.append(f"Duplicate rows found: {int(df.duplicated().sum())}")

    # Month range
    bad_month = ~df["Month"].between(1, 12)
    if bad_month.any():
        errors.append(f"Rows with invalid Month (must be 1-12): {int(bad_month.sum())}")

    # Weather ranges
    bad_temp_range = df["Temperature_Min"] > df["Temperature_Max"]
    if bad_temp_range.any():
        errors.append(
            f"Rows where Temperature_Min > Temperature_Max: {int(bad_temp_range.sum())}"
        )
    bad_humidity_range = df["Humidity_Min"] > df["Humidity_Max"]
    if bad_humidity_range.any():
        errors.append(
            f"Rows where Humidity_Min > Humidity_Max: {int(bad_humidity_range.sum())}"
        )

    # Missing values in core columns
    for col in REQUIRED_BASE_COLUMNS:
        missing = int(df[col].isna().sum())
        if missing > 0:
            errors.append(f"Missing values in {col}: {missing}")

    # Disease schema checks
    disease_cols = get_disease_columns(df)
    if not disease_cols:
        errors.append("No numeric disease columns found")
    else:
        for disease in disease_cols:
            symptoms_col = f"{disease}_Symptoms"
            advice_col = f"{disease}_Advice"
            if symptoms_col not in df.columns:
                errors.append(f"Missing symptoms column for disease '{disease}': {symptoms_col}")
            if advice_col not in df.columns:
                errors.append(f"Missing advice column for disease '{disease}': {advice_col}")

            null_disease = int(df[disease].isna().sum())
            if null_disease > 0:
                warnings.append(f"Missing numeric values in {disease}: {null_disease}")

            if symptoms_col in df.columns:
                null_symptoms = int(df[symptoms_col].isna().sum())
                if null_symptoms > 0:
                    warnings.append(f"Missing symptoms in {symptoms_col}: {null_symptoms}")
            if advice_col in df.columns:
                null_advice = int(df[advice_col].isna().sum())
                if null_advice > 0:
                    warnings.append(f"Missing advice in {advice_col}: {null_advice}")

    print(f"Checked dataset: {path}")
    print(f"Rows: {len(df)} | Columns: {len(df.columns)} | Diseases: {len(disease_cols)}")

    if warnings:
        print("\nWarnings:")
        for warning in warnings:
            print(f"- {warning}")

    if errors:
        print("\nDataset validation FAILED")
        for err in errors:
            print(f"- {err}")
        return 1

    print("\nDataset validation PASSED")
    return 0


def main() -> int:
    dataset_path = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else DEFAULT_DATASET_PATH
    return validate(dataset_path)


if __name__ == "__main__":
    raise SystemExit(main())
