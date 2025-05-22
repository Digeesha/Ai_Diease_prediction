import React, { useState } from 'react';
import axios from 'axios';

function PredictDisease() {
  // 👇 Predefined city-country pairs
  const cityCountryMap = {
    'Mumbai': 'IN',
    'London': 'UK',
    'New York': 'US'
  };

  const [city, setCity] = useState('Mumbai');
  const [country, setCountry] = useState(cityCountryMap['Mumbai']);
  const [month, setMonth] = useState(new Date().getMonth() + 1);
  const [year, setYear] = useState(new Date().getFullYear());
  const [prediction, setPrediction] = useState(null);
  const [weather, setWeather] = useState(null);
  const [loading, setLoading] = useState(false);

  const currentYear = new Date().getFullYear();
  const availableYears = [currentYear, currentYear + 1];

  const fetchWeatherAndPredict = async () => {
    try {
      setLoading(true);
      setPrediction(null);
      setWeather(null);

      const res = await axios.post('http://127.0.0.1:5000/predict', {
        city,
        country,
        month,
        year
      });

      setWeather(res.data.weather);
      setPrediction(res.data.predictions);
    } catch (error) {
      console.error('Error:', error);

      // ✅ Improved error handling
      const message = error.response?.data?.error || '❌ Something went wrong. Try again.';
      alert(message);
    } finally {
      setLoading(false);
    }
  };

  const monthOptions = Array.from({ length: 12 }, (_, i) => {
    const date = new Date(0, i);
    return { value: i + 1, name: date.toLocaleString('default', { month: 'long' }) };
  });

  const handleCityChange = (e) => {
    const selectedCity = e.target.value;
    setCity(selectedCity);
    setCountry(cityCountryMap[selectedCity]);
  };

  return (
    <div style={{ padding: '2rem' }}>
      <h2>🌡️ AI Disease Predictor (with Smart Weather Mode)</h2>

      <select value={city} onChange={handleCityChange} style={{ marginRight: '1rem' }}>
        {Object.keys(cityCountryMap).map((cityName) => (
          <option key={cityName} value={cityName}>{cityName}</option>
        ))}
      </select>

      <input
        type="text"
        placeholder="Country"
        value={country}
        readOnly
        style={{ marginRight: '1rem', backgroundColor: '#f0f0f0' }}
      />

      <select value={month} onChange={(e) => setMonth(Number(e.target.value))} style={{ marginRight: '1rem' }}>
        {monthOptions.map(({ value, name }) => (
          <option key={value} value={value}>{name}</option>
        ))}
      </select>

      <select value={year} onChange={(e) => setYear(parseInt(e.target.value))}>
        {availableYears.map((y) => (
          <option key={y} value={y}>{y}</option>
        ))}
      </select>

      <button onClick={fetchWeatherAndPredict} style={{ marginTop: '1rem', marginLeft: '1rem' }}>
        {loading ? 'Loading...' : 'Predict'}
      </button>

      {weather && (
        <div style={{ marginTop: '2rem', background: '#f1f8ff', padding: '1rem', borderRadius: '8px' }}>
          <h3>🌍 Weather for Prediction — {monthOptions[month - 1].name}</h3>
          <p><b>Temperature:</b> {weather.temp_min}–{weather.temp_max} °C</p>
          <p><b>Humidity:</b> {weather.humidity_min}–{weather.humidity_max} %</p>
        </div>
      )}

      {prediction && (
        <div style={{ marginTop: '2rem' }}>
          <h3>🧠 Predicted Diseases for {monthOptions[month - 1].name} {year}</h3>
          <p>📊 Based on weather in {city}, {country.toUpperCase()}</p>
          <ul>
            {prediction.map((disease, index) => (
              <li key={index} style={{ marginBottom: '1rem' }}>
                <strong>{disease.name}</strong><br />
                <b>Symptoms:</b> {disease.symptoms}<br />
                <b>Advice:</b> {disease.advice}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

export default PredictDisease;
