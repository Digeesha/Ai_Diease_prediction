import React from 'react';
import PredictDisease from './PredictDisease';
import './App.css';

function App() {
  const [showSecondImage, setShowSecondImage] = React.useState(false);

  return (
    <div className="app-shell">
      <main className="app-container">
        <header className="hero">
          <p className="hero-kicker">AI Health Intelligence</p>
          <h1>Disease Forecast Dashboard</h1>
          <p className="hero-subtitle">
            Predict likely diseases from city-level climate signals and get actionable
            health guidance.
          </p>
        </header>
        <section className="dashboard-layout">
          <div className="dashboard-main">
            <PredictDisease onPredictTriggered={() => setShowSecondImage(true)} />
          </div>
          <aside className="health-side-panel">
            <h3>Health + Weather Insights</h3>
            <p>
              Keep climate-aware disease forecasting in view while selecting city, month, and
              year.
            </p>
            <div className="poster-frame">
              <img
                src="/season-health-theme.png"
                alt="Seasonal weather and health illustration"
                className="poster-image"
              />
            </div>
            {showSecondImage && (
              <div className="poster-frame poster-frame-secondary">
                <img
                  src="/health-weather-panel.png"
                  alt="Outdoor weather and health activity"
                  className="poster-image"
                />
              </div>
            )}
          </aside>
        </section>
      </main>
    </div>
  );
}

export default App;
