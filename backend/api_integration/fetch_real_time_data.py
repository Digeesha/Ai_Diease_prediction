import requests
from datetime import datetime

def get_real_time_disease_data():
    disease_api = "https://disease.sh/v3/covid-19/countries"
    weather_api = "https://api.openweathermap.org/data/2.5/weather?q={city}&appid=secret_key"

    response = requests.get(disease_api)

    if response.status_code == 200:
        data = response.json()
        updated_data = []

        for entry in data:
            country = entry["country"]
            date = datetime.utcnow().strftime('%Y-%m-%d')  # Get current UTC date

            # Placeholder city (API does not provide cities)
            city = "Unknown"  # You can update this with actual city data if available
            
            # Example: Add more diseases based on region if needed
            disease_name = "COVID-19"
            if country in ["India", "Pakistan", "Bangladesh"]:
                disease_name = "Dengue"

            # Collect disease data
            updated_data.append({
                "date": date,
                "country": country,
                "city": city,
                "disease": disease_name,
                "cases": entry["cases"],
                "deaths": entry["deaths"],
                "active": entry["active"],
            })

        return updated_data
    else:
        return {"error": "Unable to fetch disease data"}
