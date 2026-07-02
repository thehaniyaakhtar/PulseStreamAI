import pandas as pd
df = pd.read_csv("trend_dataset.csv")

# Convert timestamp to datetime
df["timestamp"] = pd.to_datetime(df["timestamp"])

# Sort data chronologicaly
df = df.sort_values(["hashtag", "timestamp"])
print(df.head())

# Time Features
df["hour"] = df["timestamp"].dt.hour
df["minute"] = df["timestamp"].dt.minute
df["day_of_week"] = df["timestamp"].dt.day_of_week

# Lag Features: what happened in the previous window?
df["likes_lag_1"] = (
    df.groupby("hashtag")["likes"]
        .shift(1)
)

df["posts_lag_1"] = (
    df.groupby("hashtag")["posts"]
        .shift(1)
)

# Rolling average: avg the last three
df["likes_ma_3"] = (
    df.groupby("hashtag")["likes"]
        .rolling(3)
        .mean()
        .reset_index(level = 0, drop = True)
)

# Growth Rate
df["growth_rate"] = (
    df.groupby("hashtag")["likes"]
        .pct_change()
)

# Engagement Rate
df["engagement_rate"] = (
    df["likes"] + 
    df["comments"] + 
    df["shares"] 
) / df["posts"]

# Trend Score: how "hot" is a #
df["trend_score"] = (
    0.5 * df["likes"] + 
    0.3 * df["comments"] + 
    0.2 * df["shares"]
)

# Handle misssing values created by rolling and lagging features
df = df.fillna(0)

# Export 
df.to_csv("ml_dataset.csv", index = False)
print(df.head())
print("\nML dataset created successfully")