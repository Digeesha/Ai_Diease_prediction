import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib

# Load merged dataset
df = pd.read_csv("D:/Ai_Diease_prediction/data/merged_climate_health_dataset.csv")

# Select features (climate data) and target (disease classification)
X = df[["local_avg_temp_C", "local_avg_humidity", "local_avg_wind_speed", 
        "LandAverageTemperature", "LandMaxTemperature", "LandMinTemperature"]]
y = df["disease_class"]

# Handle missing values (fill with mean)
X = X.fillna(X.mean())

# Split data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train Random Forest Model
rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)

# Save trained model
joblib.dump(rf_model, "disease_prediction_model.pkl")

# Model accuracy on test data
accuracy = rf_model.score(X_test, y_test)
print(f"✅ AI Model Trained with Accuracy: {accuracy:.2f}")
