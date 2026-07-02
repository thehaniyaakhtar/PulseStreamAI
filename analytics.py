import pandas as pd
import numpy as np

# Load Data
ml_df = pd.read_csv("data/ml_dataset.csv")
forecast_df = pd.read_csv("data/forecast.csv")

ml_df["timestamp"] = pd.to_datetime(ml_df["timestamp"])
forecast_df["ds"] = pd.to_datetime(forecast_df["ds"])

# Get Latest Snapshot Per Hashtag
latest = (
    ml_df
    .sort_values("timestamp")
    .groupby("hashtag")
    .tail(1)
)

# Get First Future Forecast
latest_time = ml_df["timestamp"].max()

future = forecast_df[
    forecast_df["ds"] > latest_time
]

future = (
    future
    .sort_values("ds")
    .groupby("hashtag")
    .first()
    .reset_index()
)

# Merge
insights = latest.merge(
    future[
        [
            "hashtag",
            "yhat",
            "yhat_lower",
            "yhat_upper"
        ]
    ],
    on="hashtag",
    how="left"
)

# Fill Missing Forecasts
insights["yhat"] = insights["yhat"].fillna(0)
insights["yhat_lower"] = insights["yhat_lower"].fillna(0)
insights["yhat_upper"] = insights["yhat_upper"].fillna(0)

# Forecast Error
insights["forecast_error"] = (
    insights["posts"] -
    insights["yhat"]
)

# Anomaly Detection
insights["is_anomaly"] = (
    abs(insights["forecast_error"])
    >
    (0.30 * insights["yhat"])
)

# Normalize Features
features = [
    "engagement_rate",
    "virality_score",
    "avg_watch_time",
    "avg_velocity",
    "sentiment_strength",
    "yhat"
]

for feature in features:
    minimum = insights[feature].min()
    maximum = insights[feature].max()

    if maximum == minimum:
        insights[f"{feature}_norm"] = 0
    else:
        insights[f"{feature}_norm"] = (
            (insights[feature] - minimum)
            / (maximum - minimum)
        )

# Final Trend Score
insights["trend_rank_score"] = (
      0.35 * insights["yhat_norm"]
    + 0.25 * insights["engagement_rate_norm"]
    + 0.15 * insights["virality_score_norm"]
    + 0.10 * insights["avg_watch_time_norm"]
    + 0.10 * insights["avg_velocity_norm"]
    + 0.05 * insights["sentiment_strength_norm"]
)

# Trend Direction
conditions = [
    insights["forecast_error"] > 0,
    insights["forecast_error"] < 0
]

choices = [
    "Rising",
    "Falling"
]

insights["direction"] = np.select(
    conditions,
    choices,
    default="➡ Stable"
)

# Ranking
insights = insights.sort_values(
    "trend_rank_score",
    ascending=False
)

insights["rank"] = range(
    1,
    len(insights) + 1
)

# Round Numeric Columns
round_columns = [
    "engagement_rate",
    "virality_score",
    "avg_watch_time",
    "avg_velocity",
    "avg_sentiment",
    "trend_score",
    "trend_rank_score",
    "yhat",
    "forecast_error"
]

for column in round_columns:
    insights[column] = insights[column].round(3)

# Save
insights.to_csv(
    "data/insights.csv",
    index=False
)
print()

print("=" * 60)
print("Analytics Complete")
print("=" * 60)
print()

print(
    insights[
        [
            "rank",
            "hashtag",
            "trend_rank_score",
            "direction",
            "is_anomaly"
        ]
    ]
)

print()
print("Saved to data/insights.csv")