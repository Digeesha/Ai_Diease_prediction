# AI Disease Prediction Project

## Project Overview

This project is a full-stack AI application that predicts likely diseases for a selected location and time period using climate-related inputs. It combines a machine learning backend (Flask + scikit-learn) with a React frontend dashboard.

Users select a country, city, month, and year. The system then analyzes weather-linked patterns from the training dataset and returns the top predicted diseases along with symptoms and safety advice.

## Problem Statement

Many diseases are influenced by environmental factors such as temperature and humidity. This project aims to provide an early warning style prediction system that uses climate signals to forecast potential health risks for a city.

## Objectives

- Build a user-friendly web interface for disease risk forecasting.
- Train a machine learning model on weather and disease data.
- Predict multiple disease risks at once.
- Display understandable outputs (scores, symptoms, and advice).

## System Architecture

### 1) Frontend (React)

- Built with React and Axios.
- Main screen allows selecting:
  - Country
  - City
  - Month
  - Year
- Calls backend APIs:
  - `GET /cities` to populate location options.
  - `POST /predict` to request disease predictions.
- Displays:
  - Weather snapshot (temperature/humidity ranges)
  - Top 3 predicted diseases
  - Symptoms and advice

### 2) Backend (Flask)

- Provides REST APIs in `backend/app.py`.
- Loads dataset and trained model artifacts at startup.
- Validates request input (month range, past date checks, city availability).
- Preprocesses feature input with saved scaler and city encoder.
- Runs prediction and returns ranked disease results.

### 3) Machine Learning Pipeline

- Implemented in `backend/train_model.py`.
- Uses:
  - `LabelEncoder` for city encoding
  - `StandardScaler` for feature normalization
  - `MultiOutputRegressor(RandomForestRegressor)` for multi-disease prediction
- Saves trained artifacts:
  - model file
  - scaler
  - city encoder
  - disease column mapping

### 4) Data Validation

- `backend/validate_dataset.py` checks:
  - required columns
  - valid month range (1-12)
  - temperature/humidity range consistency
  - disease/symptom/advice schema consistency
  - missing values and duplicates

## Input Features and Prediction Output

### Input Features

- Temperature_Min
- Temperature_Max
- Humidity_Min
- Humidity_Max
- Month
- City_Code (encoded city)

### Output

- Predicted scores for multiple diseases
- Top 3 diseases with highest scores
- For each predicted disease:
  - name
  - symptoms
  - advice
  - score

## Technologies Used

- Python
- Flask
- scikit-learn
- pandas
- joblib
- React
- Axios

## Key Strengths of the Project

- End-to-end implementation from training to deployment-ready UI.
- Multi-output disease prediction model.
- Practical and interpretable results for users.
- Clean separation of frontend, backend, and model logic.
- Input and dataset validation for better reliability.

## Future Improvements

- Use real-time weather APIs to combine historical + live weather.
- Expand dataset coverage (more cities/regions and disease categories).
- Add model explainability (feature importance per prediction).
- Introduce confidence intervals and uncertainty reporting.
- Deploy as a cloud-hosted web service.

## Conclusion

This project demonstrates how AI and climate data can be integrated into a usable health forecasting tool. It shows practical application of machine learning, full-stack development, and API-based architecture to address a real-world public health problem.
