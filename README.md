# AI Disease Prediction

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Node.js](https://img.shields.io/badge/Node.js-18%2B-green)

A full-stack application to predict potential disease outbreaks based on climate and health data using machine learning.

---

## 🚀 Table of Contents

* [📖 Project Overview](#-project-overview)
* [✨ Features](#-features)
* [🧩 Architecture](#-architecture)
* [📂 Directory Structure](#-directory-structure)
* [⚙️ Prerequisites](#-prerequisites)
* [💻 Installation](#-installation)

  * [Backend](#backend)
  * [Model Training](#model-training)
  * [Frontend](#frontend)
* [🚦 Usage](#-usage)

  * [API Endpoints](#api-endpoints)
  * [Sample Requests](#-sample-requests)
* [🤝 Contributing](#-contributing)
* [📄 License](#-license)
* [✉️ Contact](#-contact)

---

## 📖 Project Overview

This project leverages historical climate and epidemiological datasets to train a machine learning model that forecasts the likelihood of various diseases in a given city and month. A Flask-based backend serves prediction requests and integrates real-time disease data from public APIs, while a React frontend provides an intuitive dashboard for users.

---

## ✨ Features

* **Disease Forecasting**
  Top-3 disease predictions with confidence scores.
* **Climatic Factors**
  Incorporates temperature and humidity trends.
* **Real-Time Data**
  Fetches live disease statistics via third-party APIs.
* **Interactive UI**
  React-based dashboard to input parameters and view results.

---

## 🧩 Architecture

1. **Data Layer**
   Combines health incidence data with global climate records.
2. **Modeling Pipeline**
   Data preprocessing, feature engineering, and Random Forest training.
3. **API Layer**
   Flask application exposing a `/predict` endpoint.
4. **Client Layer**
   React app consuming the API to display predictions.

---

## 📂 Directory Structure

```
├── backend/
│   ├── api_integration/       # Real-time data fetch scripts
│   ├── model/                 # Training & prediction scripts, serialized models
│   ├── app.py                 # Flask server
│   ├── requirements.txt       # Python dependencies
│   └── train_model.py         # End-to-end training pipeline
├── data/                      # Raw and merged datasets
├── frontend/                  # React application
│   ├── public/index.html
│   └── src/                   # React components and entrypoints
├── model/                     # (Optional) auxiliary model artifacts
└── README.md                  # Project documentation
```

---

## ⚙️ Prerequisites

* **Python** ≥ 3.10
* **Node.js** ≥ 18
* **Git**

---

## 💻 Installation

### Backend

1. Clone the repo and `cd` into `backend/`:

   ```bash
   git clone https://github.com/Digeesha/Ai_Diease_prediction.git
   cd Ai_Diease_prediction/backend
   ```
2. Create & activate a virtual environment:

   ```bash
   python3 -m venv venv
   # macOS/Linux
   source venv/bin/activate
   # Windows
   venv\Scripts\activate
   ```
3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```
4. Configure environment variables:

   * `OPENWEATHER_API_KEY`: Your OpenWeatherMap API key
   * (Optional) `DISEASE_API_URL`: Override the default disease API endpoint

### Model Training

1. Place raw datasets in `data/`:

   * `Expanded_Dataset_With_Ranges.csv`
   * Relevant climate CSVs
2. Merge & preprocess:

   ```bash
   python backend/model/merge_datasets.py
   ```
3. Train the model:

   ```bash
   python backend/model/train_model.py
   ```
4. Trained artifacts will be saved under `backend/model/`.

### Frontend

1. `cd frontend/`
2. Install dependencies:

   ```bash
   npm install
   ```
3. Run the development server:

   ```bash
   npm start
   ```

   Open [http://localhost:3000](http://localhost:3000).

---

## 🚦 Usage

### API Endpoints

* **POST** `/predict`
  **Description:** Returns top-3 disease predictions for a given city, country, and month.
  **Request Body:**

  ```json
  {
    "city": "London",
    "country": "UK",
    "month": 7,
    "year": 2025   // Optional, defaults to current year
  }
  ```

  **Response:**

  ```json
  {
    "weather": {
      "temp_min": 15.2,
      "temp_max": 23.5,
      "humidity_min": 55.0,
      "humidity_max": 80.1
    },
    "predictions": [
      { "name": "Influenza", "score": 0.78, "symptoms": "Fever, cough", "advice": "Get vaccinated" },
      { "name": "Dengue",    "score": 0.15, "symptoms": "Headache, rash", "advice": "Avoid mosquito bites" },
      { "name": "COVID-19",  "score": 0.07, "symptoms": "Loss of taste", "advice": "Wear a mask" }
    ]
  }
  ```

### Sample Requests

```bash
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{"city":"Delhi","country":"IN","month":8}'
```

---

## 🤝 Contributing

1. Fork the repo.
2. Create a branch:

   ```bash
   git checkout -b feature/YourFeature
   ```
3. Commit your changes:

   ```bash
   git commit -m "Add your feature"
   ```
4. Push & open a Pull Request.

---

## 📄 License

This project is licensed under the **MIT License**. See [LICENSE](LICENSE) for details.

---

## ✉️ Contact

For questions or feedback, reach out to **Digi** at [digeesha@example.com](mailto:digeesha@example.com).
