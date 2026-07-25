import React, { useState } from 'react';
import axios from 'axios';

function PredictDisease({ onPredictTriggered }) {
  const [countryOptions, setCountryOptions] = useState([]);
  const [countryCityMap, setCountryCityMap] = useState({});
  const [country, setCountry] = useState('');
  const [cityOptions, setCityOptions] = useState([]);
  const [city, setCity] = useState('');
  const [month, setMonth] = useState(new Date().getMonth() + 1);
  const [year, setYear] = useState(new Date().getFullYear());
  const [prediction, setPrediction] = useState(null);
  const [weather, setWeather] = useState(null);
  const [loading, setLoading] = useState(false);

  const currentYear = new Date().getFullYear();
  const availableYears = [currentYear, currentYear + 1];

  React.useEffect(() => {
    const fetchCities = async () => {
      try {
        const res = await axios.get('http://127.0.0.1:5000/cities', {
          params: { month },
        });
        const records = res.data?.cities || [];
        const map = records.reduce((acc, item) => {
          if (!acc[item.country]) {
            acc[item.country] = [];
          }
          if (!acc[item.country].includes(item.city)) {
            acc[item.country].push(item.city);
          }
          return acc;
        }, {});
        const countries = Object.keys(map).sort((a, b) => a.localeCompare(b));
        countries.forEach((countryName) => {
          map[countryName].sort((a, b) => a.localeCompare(b));
        });

        setCountryCityMap(map);
        setCountryOptions(countries);
      } catch (error) {
        console.error('Error loading cities:', error);
        setCountryOptions([]);
        setCountryCityMap({});
        setCountry('');
        setCityOptions([]);
        setCity('');
      }
    };

    fetchCities();
    // Re-fetch cities when month changes so dropdown shows available data.
  }, [month]);

  React.useEffect(() => {
    if (countryOptions.length === 0) {
      setCountry('');
      setCityOptions([]);
      setCity('');
      return;
    }

    const nextCountry = countryCityMap[country] ? country : countryOptions[0];
    if (nextCountry !== country) {
      setCountry(nextCountry);
      return;
    }

    const nextCities = countryCityMap[country] || [];
    setCityOptions(nextCities);
    setCity((prevCity) => (nextCities.includes(prevCity) ? prevCity : (nextCities[0] || '')));
  }, [country, countryOptions, countryCityMap]);

  const fetchWeatherAndPredict = async () => {
    if (onPredictTriggered) {
      onPredictTriggered();
    }

    if (!city || !country) {
      alert('No city data available for this month.');
      return;
    }

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
      const message = error.response?.data?.error || 'Something went wrong. Try again.';
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
    setCity(e.target.value);
  };

  const handleCountryChange = (e) => {
    setCountry(e.target.value);
  };

  return (
    <section className="predictor-card">
      <div className="predictor-title-row">
        <h2>Disease Predictor</h2>
        <span className="smart-badge">Smart Weather Mode</span>
      </div>

      <div className="controls-grid">
        <label>
          Country
          <select value={country} onChange={handleCountryChange} disabled={countryOptions.length === 0}>
            {countryOptions.map((countryName) => (
              <option key={countryName} value={countryName}>
                {countryName}
              </option>
            ))}
          </select>
        </label>

        <label>
          City
          <select value={city} onChange={handleCityChange} disabled={cityOptions.length === 0}>
            {cityOptions.map((cityName) => (
              <option key={cityName} value={cityName}>
                {cityName}
              </option>
            ))}
          </select>
        </label>

        <label>
          Month
          <select value={month} onChange={(e) => setMonth(Number(e.target.value))}>
            {monthOptions.map(({ value, name }) => (
              <option key={value} value={value}>
                {name}
              </option>
            ))}
          </select>
        </label>

        <label>
          Year
          <select value={year} onChange={(e) => setYear(parseInt(e.target.value, 10))}>
            {availableYears.map((y) => (
              <option key={y} value={y}>
                {y}
              </option>
            ))}
          </select>
        </label>

        <button className="predict-button" onClick={fetchWeatherAndPredict}>
          {loading ? 'Predicting...' : 'Predict Diseases'}
        </button>
      </div>
      {cityOptions.length === 0 && (
        <p className="result-subtitle">No city data available for the selected month.</p>
      )}

      {weather && (
        <section className="result-card weather-card">
          <h3>Weather Snapshot ({monthOptions[month - 1].name})</h3>
          <div className="weather-grid">
            <p>
              <span>Temperature</span>
              {` ${weather.temp_min} to ${weather.temp_max} \u00b0C`}
            </p>
            <p>
              <span>Humidity</span>
              {` ${weather.humidity_min} to ${weather.humidity_max} %`}
            </p>
          </div>
        </section>
      )}

      {prediction && (
        <section className="result-card prediction-card">
          <h3>
            Top Predictions for {monthOptions[month - 1].name} {year}
          </h3>
          <p className="result-subtitle">
            Based on weather signals for {city}, {country.toUpperCase()}
          </p>
          <div className="prediction-list">
            {prediction.map((disease, index) => (
              <article key={index} className="prediction-item">
                <div className="prediction-head">
                  <strong>{disease.name}</strong>
                  <span className="score-pill">Score: {disease.score}</span>
                </div>
                <p>
                  <span>Symptoms:</span> {disease.symptoms}
                </p>
                <p>
                  <span>Advice:</span> {disease.advice}
                </p>
              </article>
            ))}
          </div>
        </section>
      )}
    </section>
  );
}

export default PredictDisease;
