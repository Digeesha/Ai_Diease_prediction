import pandas as pd
import joblib
import json
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.multioutput import MultiOutputRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score

# Load dataset
df = pd.read_csv('D:/Ai_Diease_prediction/data/Expanded_Dataset_With_Ranges.csv')

# Encode city
city_encoder = LabelEncoder()
df["City_Code"] = city_encoder.fit_transform(df["City"])
joblib.dump(city_encoder, 'D:/Ai_Diease_prediction/model/city_encoder_range_model.save')

# Feature columns
feature_cols = [
    "Temperature_Min", "Temperature_Max",
    "Humidity_Min", "Humidity_Max",
    "Month", "City_Code"
]

# Dynamically find disease columns
exclude_cols = feature_cols + ["City", "Country", "Year"]
disease_cols = [
    col for col in df.columns
    if col not in exclude_cols and not col.endswith(("_Symptoms", "_Advice")) and df[col].dtype != 'O'
]

# Save disease columns
with open('D:/Ai_Diease_prediction/model/disease_columns.json', 'w') as f:
    json.dump(disease_cols, f)

# Prepare input & output
X = df[feature_cols]
Y = df[disease_cols]

# Normalize features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
joblib.dump(scaler, 'D:/Ai_Diease_prediction/model/scaler_range_model.save')

# Train/test split
X_train, X_test, Y_train, Y_test = train_test_split(X_scaled, Y, test_size=0.2, random_state=42)

# ✅ Replace XGBRegressor with RandomForestRegressor
rf_base = RandomForestRegressor(n_estimators=200, max_depth=10, random_state=42)
model = MultiOutputRegressor(rf_base)

# Train model
model.fit(X_train, Y_train)

# Predict on test data
Y_pred = model.predict(X_test)

# Evaluate accuracy
mae = mean_absolute_error(Y_test, Y_pred)
r2 = r2_score(Y_test, Y_pred)

print("📊 Model Evaluation:")
print("🔹 Mean Absolute Error (MAE):", round(mae, 2))
print("🔹 R² Score:", round(r2, 4))

# Save trained model
joblib.dump(model, 'D:/Ai_Diease_prediction/model/disease_predictor_rf_model.save')

print("✅ RandomForestRegressor model training complete and saved.")
print("🦠 Diseases learned:", disease_cols)
