from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import numpy as np
import joblib
from datetime import datetime
import math
import json
from pathlib import Path

app = Flask(__name__)
CORS(app)

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
MODEL_DIR = BASE_DIR / "model"

DATASET_PATH = DATA_DIR / "Expanded_Dataset_With_Ranges.csv"
DISEASE_COLUMNS_PATH = MODEL_DIR / "disease_columns.json"
MODEL_PATH = MODEL_DIR / "disease_predictor_rf_model.save"
SCALER_PATH = MODEL_DIR / "scaler_range_model.save"
CITY_ENCODER_PATH = MODEL_DIR / "city_encoder_range_model.save"

required_files = [
    DATASET_PATH,
    DISEASE_COLUMNS_PATH,
    MODEL_PATH,
    SCALER_PATH,
    CITY_ENCODER_PATH,
]
missing_files = [str(path) for path in required_files if not path.exists()]

if missing_files:
    raise FileNotFoundError(
        "Missing required project files. Train the model and ensure these files exist: "
        + ", ".join(missing_files)
    )

# Load data
df = pd.read_csv(DATASET_PATH)

# Load disease names
with open(DISEASE_COLUMNS_PATH, 'r') as f:
    diseases = json.load(f)

# Load trained model & preprocessing tools
model = joblib.load(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)
city_encoder = joblib.load(CITY_ENCODER_PATH)

@app.route('/cities', methods=['GET'])
def cities():
    try:
        month_arg = request.args.get('month')
        filtered_df = df

        if month_arg is not None:
            month = int(month_arg)
            if month < 1 or month > 12:
                return jsonify({"error": "month must be between 1 and 12"}), 400
            filtered_df = df[df['Month'] == month]

        if filtered_df.empty:
            return jsonify({"cities": []})

        # Keep one country per city for current UI mapping.
        city_records = (
            filtered_df[['City', 'Country']]
            .dropna()
            .drop_duplicates(subset=['Country', 'City'])
            .sort_values(by=['Country', 'City'])
        )
        payload = [
            {"city": row.City, "country": row.Country}
            for row in city_records.itertuples(index=False)
        ]
        return jsonify({"cities": payload})
    except ValueError:
        return jsonify({"error": "month must be an integer"}), 400
    except Exception as e:
        print("Exception in /cities:", str(e))
        return jsonify({"error": str(e)}), 500

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        city_input = str(data['city']).strip().lower()
        country_input = str(data['country']).strip().lower()
        month = int(data['month'])
        year = int(data.get('year', datetime.now().year))

        # ✅ Check for past dates (month-wise)
        now = datetime.now()
        request_date = datetime(year, month, 1)
        current_date = datetime(now.year, now.month, 1)

        if request_date < current_date:
            return jsonify({"error": "Predictions for past dates are not allowed."}), 400

        # ✅ Filter the dataset (case-insensitive)
        filtered = df[
             (df['City'].str.lower() == city_input) &
              (df['Country'].str.lower().str.contains(country_input)) &  # <— use contains here
             (df['Month'] == month)
         ]


        if filtered.empty:
            return jsonify({
                "error": f"No data found for {city_input.title()}, {country_input.upper()} in month {month}."
            }), 404

        # ✅ Encode city
        lower_cities = [str(c).lower() for c in city_encoder.classes_]
        if city_input not in lower_cities:
            return jsonify({"error": f"City '{city_input}' not recognized in trained model."}), 400

        city_actual = city_encoder.classes_[lower_cities.index(city_input)]
        city_code = city_encoder.transform([city_actual])[0]

        # ✅ Average weather input
        avg = filtered.mean(numeric_only=True).fillna(0)
        weather_features = [
            avg.get("Temperature_Min", 0),
            avg.get("Temperature_Max", 0),
            avg.get("Humidity_Min", 0),
            avg.get("Humidity_Max", 0),
            month,
            city_code
        ]

        input_vector = scaler.transform([weather_features])
        prediction = model.predict(input_vector)[0]

        # ✅ Top 3 diseases
        disease_predictions = list(zip(diseases, prediction))
        top_predicted = sorted(
            [(name, val) for name, val in disease_predictions if not math.isnan(val)],
            key=lambda x: x[1], reverse=True
        )[:3]

        ref = filtered.iloc[0]
        results = []
        for disease, score in top_predicted:
            results.append({
                "name": disease,
                "symptoms": ref.get(f"{disease}_Symptoms", "N/A"),
                "advice": ref.get(f"{disease}_Advice", f"Stay safe from {disease}."),
                "score": float(round(score, 3))
            })

        return jsonify({
            "weather": {
                "temp_min": round(avg.get("Temperature_Min", 0), 1),
                "temp_max": round(avg.get("Temperature_Max", 0), 1),
                "humidity_min": round(avg.get("Humidity_Min", 0), 1),
                "humidity_max": round(avg.get("Humidity_Max", 0), 1)
            },
            "predictions": results
        })

    except Exception as e:
        print("💥 Exception:", str(e))
        return jsonify({"error": str(e)}), 500

# ✅ FIXED: Correct app start point
if __name__ == '__main__':
    app.run(debug=True)
