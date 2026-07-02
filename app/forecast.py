import pandas as pd
from prophet import Prophet

# Load ML Dataset
df = pd.read_csv("ml_dataset.csv")
df["timestamp"] = pd.to_datetime(df["timestamp"])

# store forecasts from every hashtag
all_forecasts = []

# Train one Prophet model per #
for hashtag in df["hastag"].unique():
    print(f"Training model for {hashtag}: ")
    
    hashtag_df = (
        df[df["hastag"] == hashtag]
        [["timestamp", "trend_score"]].rename(
            columns={
                "timestamp": "ds",
                "trend_score": "y" # y: value to forecast
                # Prophet does not understand cols names timestamp/ likes, 
            }
        )
    )
    
    # Prophet limitations: small datasets
    # skip # with too few observations
    if len(hashtag_df) < 10:
        print(f"Skipping {hashtag} (not enough data)")
        continue
    
    model = Prophet()
    
    model.fit(hashtag_df)
    
    # for production window of 60 seconds
    future = model.make_future_dataframe(
        periods = 30,
        freq = "min"
    )
    
    forecast = model.predict(future)
    
    forecast["hashtag"] = hashtag
    
    all_forecasts.append(
        forecast[
            [
                "hashtag",
                "ds"
                "yhat",
                "yhat_lower",
                "yhat_upper"
            ]
        ]
    )

forecast_df = pd.concat(
    all_forecasts,
    index = True
)

forecast_df.to_csv(
    "forecast.csv",
    index = False
)

print("\nForecasting complete")
print(forecast_df.head())