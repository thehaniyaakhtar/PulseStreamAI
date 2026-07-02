import pandas as pd

# Load data
forecast_df = pd.read_csv("forecast.csv")
ml_df = pd.read_csv("ml_dataset.csv")

forecast_df["ds"] = pd.to_datetime(forecast_df["ds"])
ml_df["timestamp"] = pd.to_datetime(ml_df["timestamp"])

# keep only future forecasts
latest_time = ml_df["timestamp"].max()

future_forecasts = forecast_df[
    forecast_df["ds"] > latest_time
]

# latest observed metrics
latest_metrics = (
    ml_df
        .sort_values("timestamp")
        .groupby("hashtag")
        .tail(1)
)

# frst forecast for each #
next_prediction = (
    future_forecasts
        .groupby("hashtag")
        .first()
        .reset_index()
)

# Merge everything
results = next_prediction.merge(
    latest_metrics,
    on = "hashtag"
)

# Anomaly Detection
results["forecast_error"] = (
    results["posts"] - 
    results["yhat"]
)

results["is_anomaly"] = (
    results["forecast_error"].abs()
    >
    (0.30 * results["yhat"])
)

# Trend Ranking
results["trend_rank_score"] = (
    0.40 * results["yhat"] +
    0.30 * results["likes"] +
    0.20 * results["comments"] +
    0.10 * results["shares"]
)

results = results.sort_values(
    "trend_rank_score",
    ascending=False
)

# Export
results.to_csv(
    "insights.csv",
    index=False
)

print(results[
    [
        "hashtag",
        "trend_rank_score",
        "is_anomaly"
    ]
])