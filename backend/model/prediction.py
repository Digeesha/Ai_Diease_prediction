import requests
import os

# Function to fetch weather data from OpenWeather API
def get_weather(city, country):
    api_key = "93785eaa7f9e442d868cc80ac924648b"  # Replace with your actual API key
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city},{country}&appid={api_key}"
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Weather data not found"}

# Function to fetch real-time disease outbreaksimport requests
def get_disease_outbreaks(city, country):
      
    url = "https://data.cdc.gov/resource/mr8w-325u.json"
    response = requests.get(url)

    try:
        data = response.json()
        disease_names = set()

        for entry in data:
            if "state" in entry and "condition" in entry:
                if city.lower() in entry["state"].lower() or country.lower() in entry["state"].lower():
                    disease_names.add(entry["condition"])

        return list(disease_names) if disease_names else ["No active outbreaks"]

    except Exception as e:
        print("❌ CDC API error:", str(e))
        return ["No data available"]


# Function to fetch symptoms & advice from SymCat API


def get_symptoms_and_advice(disease_name):
    """Fetch symptoms and advice dynamically for a disease."""
    try:
        # Using SymCat API to get symptoms (replace with a valid API)
        url = f"https://api.symcat.com/v1/conditions/{disease_name.lower().replace(' ', '-')}"
        response = requests.get(url)

        if response.status_code == 200:
            disease_info = response.json()
            symptoms = disease_info.get("symptoms", ["No symptoms available"])
            advice = disease_info.get("treatment", "No specific advice available")
        else:
            symptoms = ["No symptoms available"]
            advice = "No specific advice available"

    except Exception as e:
        print("❌ Error fetching symptoms:", str(e))
        symptoms = ["No symptoms available"]
        advice = "No specific advice available"

    return symptoms, advice

# Function to combine weather, disease, symptoms, and advice
def get_weather_and_disease_prediction(city, country):
    weather_data = get_weather(city, country)
    disease_data = get_disease_outbreaks(city, country)

    if "error" in weather_data:
        return {"error": "Weather data unavailable"}

    temp = weather_data["main"]["temp"] - 273.15  # Convert Kelvin to Celsius
    humidity = weather_data["main"]["humidity"]
    condition = weather_data["weather"][0]["main"]

    # ✅ If disease data is found, show the first disease (or all in a list)
    if len(disease_data) > 0:
        disease = ", ".join(disease_data)  # Combine multiple diseases
    else:
        disease = "No active outbreaks"

    return {
        "city": city,
        "country": country,
        "temperature": round(temp, 2),
        "humidity": humidity,
        "weather_condition": condition,
        "predicted_disease": disease,
        "symptoms": ["Data unavailable"],  # You can integrate symptom API later
        "advice": "Follow local health guidelines."
    }
