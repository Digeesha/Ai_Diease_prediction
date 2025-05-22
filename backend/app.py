from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import numpy as np
import joblib
from datetime import datetime
import math
import json

app = Flask(__name__)
CORS(app)

# Load data
df = pd.read_csv('D:/Ai_Diease_prediction/data/Expanded_Dataset_With_Ranges.csv')

# Load disease names
with open('D:/Ai_Diease_prediction/model/disease_columns.json', 'r') as f:
    diseases = json.load(f)

# Load trained model & preprocessing tools
model = joblib.load('D:/Ai_Diease_prediction/model/disease_predictor_rf_model.save')
scaler = joblib.load('D:/Ai_Diease_prediction/model/scaler_range_model.save')
city_encoder = joblib.load('D:/Ai_Diease_prediction/model/city_encoder_range_model.save')

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
