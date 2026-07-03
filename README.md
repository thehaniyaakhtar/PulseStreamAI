# PulseStream AI: Real-Time Social Media Trend Intelligence Platform

## Overview
A platform that simulates social media activity, processes streaming events using Redis Streams, performs feature engineering, forecasts future trend scores using Prophet, and visualizes insights through an interactive Streamlit dashboard.

The project demonstrates an end-to-end data engineering and machine learning workflow, covering synthetic data generation, stream processing, window-based aggregation, predictive analytics, and business intelligence visualization.

---

## Features

* Real-time social media post simulation
* Redis Streams-based event ingestion
* Sliding window trend aggregation
* Automatic dataset generation
* Feature engineering pipeline
* Trend score forecasting using Prophet
* Interactive Streamlit dashboard
* Exportable datasets for further analysis

---

## Tech Stack

### Languages

* Python

### Streaming & Storage

* Redis Streams
* Docker

### Data Processing

* Pandas
* NumPy

### Machine Learning

* Prophet

### Dashboard

* Streamlit
* Plotly

### Fake Data Generation

* Faker

---

## Project Structure

```text
trend-engine/
│
├── app/
│   ├── producer.py
│   ├── consumer.py
│   ├── window_aggregator.py
│   ├── feature_engineering.py
│   ├── forecast.py
│   └── dashboard.py
│
├── data/
│   ├── trend_dataset.csv
│   ├── ml_dataset.csv
│   └── forecast.csv
│
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

## Architecture

```text
Synthetic Social Posts
          │
          ▼
     Producer
          │
          ▼
    Redis Streams
          │
          ▼
      Consumer
          │
          ▼
 Window Aggregator
          │
          ▼
 trend_dataset.csv
          │
          ▼
 Feature Engineering
          │
          ▼
  ml_dataset.csv
          │
          ▼
 Prophet Forecasting
          │
          ▼
   forecast.csv
          │
          ▼
 Streamlit Dashboard
```

---

## Simulated Post Features

Each generated post contains realistic metadata including:

* User ID
* User type
* Country
* Follower count
* Verification status
* Caption
* Hashtag
* Media type
* Likes
* Comments
* Shares
* Impressions
* Average watch time
* Click-through rate
* Sentiment score
* Engagement velocity
* Timestamp

---

## Feature Engineering

Additional analytical features include:

* Engagement rate
* Virality score
* Interaction rate
* Trend score
* Rolling averages
* Window-based aggregations

---

## Forecasting

The forecasting pipeline trains a separate Prophet model for every hashtag and predicts future trend scores, enabling comparison between historical and projected popularity.

---

## Dashboard

The Streamlit dashboard includes:

* Executive KPI cards
* Live hashtag leaderboard
* Trend score analysis
* Forecast visualizations
* Engagement metrics
* Geographic distribution
* Media type analysis
* Sentiment overview
* Interactive filtering

---

## Running the Project

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd trend-engine
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Windows

```bash
venv\Scripts\activate
```

Linux / macOS

```bash
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Start Redis

Using Docker:

```bash
docker compose up -d
```

If Redis is already running:

```bash
docker ps
```

### 5. Start the producer

```bash
python app/producer.py
```

### 6. Start the consumer

```bash
python app/consumer.py
```

### 7. Generate the ML dataset

```bash
python app/feature_engineering.py
```

### 8. Train forecasting models

```bash
python app/forecast.py
```

### 9. Launch the dashboard

```bash
streamlit run app/dashboard.py
```

---

## License

This project is intended for educational and portfolio purposes.
