import pandas as pd
from prophet import Prophet

# Load ML Dataset
df = pd.read_csv("ml_dataset.csv")
# Converting timestamp col from string to datetime format
df["timestamp"] = pd.to_datetime(df["timestamp"])

# store forecasts from every hashtag

# stores forecast df for each hashtag
all_forecasts = []

# Train one Prophet model per #
for hashtag in df["hastag"].unique():
    print(f"Training model for {hashtag}: ")
    
    hashtag_df = (
        # Select rows belonging to #
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
    # skip # with too few observations (> 10 obs)
    if len(hashtag_df) < 10:
        print(f"Skipping {hashtag} (not enough data)")
        continue
    
    model = Prophet()
    model.fit(hashtag_df)
    
    # for production window of 60 seconds
    # generate timestamps for prediction
    future = model.make_future_dataframe(
        periods = 30, # forecast 30 future time steps
        freq = "min"  # 1 min intervals
    )
    # thus for production system receiving data every minute, prediction for next 30 mins
    # predicts value for both historical timestamp + future timestamp
    forecast = model.predict(future)
    
    # add hashtag so we know forecast belongs to it
    forecast["hashtag"] = hashtag
    
    # save only useful columns
    all_forecasts.append(
        forecast[
            [
                "hashtag",
                "ds"
                "yhat",         # predicted trend score
                "yhat_lower",   # lower confidence intervel
                "yhat_upper"    # upper confidence interval
            ]
        ]
    )

forecast_df = pd.concat(
    all_forecasts,
    index = True
)
# merge all # forecasts to one df

forecast_df.to_csv(
    "forecast.csv",
    index = False
)
# export the final forecast df to a csv file

print("\nForecasting complete")
print(forecast_df.head())