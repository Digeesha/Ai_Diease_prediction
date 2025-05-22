import pandas as pd

# Load the datasets
climate_health_df = pd.read_csv("D:/Ai_Diease_prediction/data/final_climate_health_dataset.csv")
temperature_df = pd.read_csv("D:/Ai_Diease_prediction/data/GlobalTemperatures.csv")

# ✅ No need to process "dt" column, since "year" and "month" already exist in the dataset

# Select only required columns from temperature dataset
temperature_df = temperature_df[["year", "month", "LandAverageTemperature", 
                                 "LandMaxTemperature", "LandMinTemperature"]]

# ✅ Merge datasets on year and month
merged_df = pd.merge(climate_health_df, temperature_df, on=["year", "month"], how="left")

# Drop unnecessary columns and rename for consistency
merged_df = merged_df[["year", "month", "mean_temp_C", "humidity_mean_percent", 
                       "wind_speed_mean_mps", "LandAverageTemperature", 
                       "LandMaxTemperature", "LandMinTemperature", "CLASSI_FIN"]]

merged_df.rename(columns={
    "mean_temp_C": "local_avg_temp_C",
    "humidity_mean_percent": "local_avg_humidity",
    "wind_speed_mean_mps": "local_avg_wind_speed",
    "CLASSI_FIN": "disease_class"
}, inplace=True)

# ✅ Remove rows with missing disease classification
merged_df = merged_df.dropna(subset=["disease_class"])

# ✅ Save merged dataset
merged_df.to_csv("D:/Ai_Diease_prediction/data/merged_climate_health_dataset.csv", index=False)

print("✅ Merged dataset saved as merged_climate_health_dataset.csv")
