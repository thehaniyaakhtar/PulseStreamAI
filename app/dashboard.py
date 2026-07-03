import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
from streamlit_autorefresh import st_autorefresh

# =====================================================
# Page Configuration
# =====================================================

st.set_page_config(
    page_title="Social Trend Forecasting Engine",
    page_icon="📈",
    layout="wide"
)

st_autorefresh(interval=5000, key="refresh")

# =====================================================
# Custom Styling
# =====================================================

st.markdown("""
<style>

.block-container{
    padding-top:2rem;
    padding-bottom:2rem;
}

div[data-testid="metric-container"]{
    background:#FFFFFF;
    border-radius:12px;
    padding:15px;
    border:1px solid #DDDDDD;
    box-shadow:0 2px 8px rgba(0,0,0,.08);
}

h1,h2,h3{
    color:#1F4E79;
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# Load Data
# =====================================================

DATA = Path("data")


@st.cache_data(ttl=5)
def load_data():

    trend = pd.read_csv(DATA / "trend_dataset.csv")
    forecast = pd.read_csv(DATA/ "forecast.csv")
    insights = pd.read_csv(DATA / "insights.csv")

    trend["timestamp"] = pd.to_datetime(trend["timestamp"])
    forecast["ds"] = pd.to_datetime(forecast["ds"])

    return trend, forecast, insights


try:

    trend_df, forecast_df, insights_df = load_data()

except Exception as e:

    st.error("Unable to load project data.")
    st.exception(e)
    st.stop()

# =====================================================
# Sidebar
# =====================================================

st.sidebar.title("⚙ Filters")

hashtags = sorted(trend_df["hashtag"].unique())

selected_hashtag = st.sidebar.selectbox(
    "Hashtag",
    hashtags
)

show_anomalies = st.sidebar.checkbox(
    "Only show anomalies",
    False
)

# =====================================================
# Filter Data
# =====================================================

trend_filtered = trend_df[
    trend_df["hashtag"] == selected_hashtag
]

forecast_filtered = forecast_df[
    forecast_df["hashtag"] == selected_hashtag
]

if show_anomalies:

    insights_filtered = insights_df[
        insights_df["is_anomaly"] == True
    ]

else:

    insights_filtered = insights_df.copy()

# =====================================================
# Header
# =====================================================

st.title("📈 Social Trend Forecasting Engine")

st.caption(
    "Real-time monitoring, forecasting and anomaly detection for social media trends."
)

st.divider()

# =====================================================
# KPI Cards
# =====================================================

top = insights_df.sort_values(
    "trend_rank_score",
    ascending=False
).iloc[0]

total_posts = int(trend_df["posts"].sum())

total_impressions = int(trend_df["impressions"].sum())

active_anomalies = int(
    insights_df["is_anomaly"].sum()
)

c1, c2, c3, c4 = st.columns(4)

with c1:

    st.metric(
        "🔥 Top Trend",
        top["hashtag"]
    )

with c2:

    st.metric(
        "📈 Forecast",
        round(top["yhat"], 1)
    )

with c3:

    st.metric(
        "⭐ Trend Score",
        round(top["trend_rank_score"], 3)
    )

with c4:

    st.metric(
        "🚨 Active Anomalies",
        active_anomalies
    )

c5, c6 = st.columns(2)

with c5:

    st.metric(
        "📝 Total Posts",
        total_posts
    )

with c6:

    st.metric(
        "👀 Total Impressions",
        total_impressions
    )

st.divider()

# =====================================================
# Historical Activity
# =====================================================

left, right = st.columns(2)

with left:

    st.subheader("Historical Posts")

    history_fig = px.line(
        trend_filtered,
        x="timestamp",
        y="posts",
        markers=True
    )

    history_fig.update_layout(
        xaxis_title="Time",
        yaxis_title="Posts",
        height=420
    )

    st.plotly_chart(
        history_fig,
        use_container_width=True
    )

with right:
    st.subheader("Engagement Breakdown")
    latest = trend_filtered.iloc[-1]
    engagement = pd.DataFrame({

        "Metric":[
            "Likes",
            "Comments",
            "Shares"
        ],

        "Value":[
            latest["likes"],
            latest["comments"],
            latest["shares"]
        ]

    })

    engagement_fig = px.bar(
        engagement,
        x="Metric",
        y="Value",
        text="Value"
    )

    engagement_fig.update_layout(
        showlegend=False,
        height=420
    )
    
    st.plotly_chart(
        engagement_fig,
        use_container_width=True
    )
st.divider()

# =====================================================
# Forecast
# =====================================================
st.subheader("Forecast")
forecast_fig = go.Figure()
forecast_fig.add_trace(
    go.Scatter(
        x=forecast_filtered["ds"],
        y=forecast_filtered["yhat"],
        mode="lines",
        name="Forecast"
    )
)

forecast_fig.add_trace(
    go.Scatter(
        x=forecast_filtered["ds"],
        y=forecast_filtered["yhat_upper"],
        line=dict(width=0),
        showlegend=False
    )
)

forecast_fig.add_trace(
    go.Scatter(
        x=forecast_filtered["ds"],
        y=forecast_filtered["yhat_lower"],
        fill="tonexty",
        line=dict(width=0),
        name="Confidence Interval"
    )
)

forecast_fig.update_layout(
    height=500,
    xaxis_title="Time",
    yaxis_title="Predicted Posts"
)

st.plotly_chart(
    forecast_fig,
    use_container_width=True
)

st.divider()

# =====================================================
# Top Trending Hashtags + Anomaly Alerts
# =====================================================

left, right = st.columns([2, 1])
with left:
    st.subheader("🏆 Top Trending Hashtags")

    leaderboard = insights_df[
        [
            "rank",
            "hashtag",
            "trend_rank_score",
            "yhat",
            "direction"
        ]
    ].copy()

    leaderboard.columns = [
        "Rank",
        "Hashtag",
        "Trend Score",
        "Forecast",
        "Direction"
    ]

    st.dataframe(
        leaderboard,
        use_container_width=True,
        hide_index=True
    )

with right:
    st.subheader("🚨 Anomaly Alerts")
    anomalies = insights_df[
        insights_df["is_anomaly"] == True
    ]
    if anomalies.empty:
        st.success("No anomalies detected.")

    else:
        st.error(f"{len(anomalies)} anomaly(s) detected.")
        st.dataframe(
            anomalies[
                [
                    "hashtag",
                    "forecast_error",
                    "trend_rank_score"
                ]
            ],
            use_container_width=True,
            hide_index=True
        )

st.divider()

# =====================================================
# Trend Score Comparison
# =====================================================

st.subheader("📊 Trend Scores")

trend_fig = px.bar(
    insights_df.sort_values(
        "trend_rank_score",
        ascending=False
    ),

    x="hashtag",
    y="trend_rank_score",
    text="trend_rank_score",
    color="trend_rank_score",
    color_continuous_scale="Blues"
)

trend_fig.update_layout(
    height=450,
    xaxis_title="Hashtag",
    yaxis_title="Trend Score",
    coloraxis_showscale=False
)

st.plotly_chart(
    trend_fig,
    use_container_width=True
)
st.divider()

# =====================================================
# Latest Incoming Posts
# =====================================================

st.subheader("📰 Recent Incoming Posts")
recent_posts = (
    trend_df
    .sort_values("timestamp", ascending=False)
    .head(10)
)

for _, row in recent_posts.iterrows():
    with st.container(border=True):
        c1, c2 = st.columns([3, 1])
        with c1:
            st.markdown(f"### {row['hashtag']}")
            st.caption(row["timestamp"])
        with c2:
            st.metric(
                "Posts",
                int(row["posts"])
            )
            
        c3, c4, c5 = st.columns(3)
        c3.metric("👍 Likes", int(row["likes"]))
        c4.metric("💬 Comments", int(row["comments"]))
        c5.metric("🔁 Shares", int(row["shares"]))
        if "impressions" in row:
            st.caption(
                f"👀 Impressions: {int(row['impressions'])}"
            )
st.divider()

# =====================================================
# Dataset Preview
# =====================================================

with st.expander("📂 View Aggregated Dataset"):
    st.dataframe(
        trend_df.sort_values(
            "timestamp",
            ascending=False
        ),
        use_container_width=True
    )

st.divider()

# =====================================================
# Footer
# =====================================================

st.markdown(
"""
---
### About

This dashboard demonstrates an end-to-end social media analytics pipeline built with:

- Redis Streams
- Python
- Pandas
- Prophet Forecasting
- Feature Engineering
- Trend Ranking
- Anomaly Detection
- Streamlit
- Plotly

The dashboard refreshes automatically every 5 seconds to visualize newly processed streaming data.
"""
)