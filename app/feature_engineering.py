import pandas as pd

# Load Aggregated Dataset
df = pd.read_csv("data/trend_dataset.csv")

# Avoid division by zero
df["impressions"] = df["impressions"].replace(0, 1)
df["posts"] = df["posts"].replace(0, 1)

# Feature Engineering

# Total engagement
df["engagement"] = (
    df["likes"] +
    df["comments"] +
    df["shares"]
)

# Engagement per impression
df["engagement_rate"] = (
    df["engagement"] /
    df["impressions"]
)

# Virality
df["virality_score"] = (
    df["shares"] /
    df["impressions"]
)

# Average watch time per post
df["avg_watch_time"] = (
    df["watch_time"] /
    df["posts"]
)

# Average CTR
df["avg_ctr"] = (
    df["ctr"] /
    df["posts"]
)

# Average engagement velocity
df["avg_velocity"] = (
    df["engagement_velocity"] /
    df["posts"]
)

# Average sentiment
df["avg_sentiment"] = (
    df["sentiment"] /
    df["posts"]
)

# Sentiment strength
df["sentiment_strength"] = (
    df["avg_sentiment"].abs()
)

# Overall trend score
df["trend_score"] = (
      0.30 * df["engagement_rate"]
    + 0.25 * df["virality_score"]
    + 0.20 * df["avg_watch_time"]
    + 0.15 * df["avg_velocity"]
    + 0.10 * df["sentiment_strength"]
)

# Save
df.to_csv(
    "data/ml_dataset.csv",
    index=False
)

print("ML dataset created successfully.")
print(df.head())