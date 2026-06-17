import streamlit as st
import pandas as pd
import plotly.express as px


# Page Config
st.set_page_config(
    page_title="Marketing Campaign Dashboard",
    page_icon="📊",
    layout="wide"
)

# Dashboard Title
st.title("📊 Marketing Campaign Analytics Dashboard")

# Load Dataset
df = pd.read_excel("data/marketing_campaign.xlsx")
# Sidebar Filters
st.sidebar.header("Filters")

channel = st.sidebar.selectbox(
    "Select Channel",
    ["All"] + list(df["channel"].unique())
)

country = st.sidebar.selectbox(
    "Select Country",
    ["All"] + list(df["country"].unique())
)

# Apply Filters
filtered_df = df.copy()

if channel != "All":
    filtered_df = filtered_df[filtered_df["channel"] == channel]

if country != "All":
    filtered_df = filtered_df[filtered_df["country"] == country]

# Show Data Preview
st.subheader("Dataset Preview")
st.dataframe(filtered_df.head())



# Basic Metrics
total_revenue = filtered_df["revenue_usd"].sum()
total_spend = filtered_df["spend_usd"].sum()
total_clicks = filtered_df["clicks"].sum()
total_impressions = filtered_df["impressions"].sum()

ctr = (total_clicks / total_impressions) * 100

total_conversions = filtered_df["conversion"].sum()

conversion_rate = (
    total_conversions / total_clicks * 100
    if total_clicks > 0 else 0
)

avg_roi = filtered_df["roi"].mean()


# KPI Cards
col1, col2, col3, col4, col5, col6 = st.columns(6)

col1.metric("Revenue ($)", f"{total_revenue:,.2f}")
col2.metric("Spend ($)", f"{total_spend:,.2f}")
col3.metric("Clicks", f"{total_clicks:,}")
col4.metric("CTR (%)", f"{ctr:.2f}")
col5.metric("Conversions", f"{int(total_conversions):,}")
col6.metric("Avg ROI", f"{avg_roi:.2f}")

st.subheader("Revenue by Channel")

revenue_channel = (
    filtered_df.groupby("channel")["revenue_usd"]
    .sum()
    .reset_index()
)

fig = px.bar(
    revenue_channel,
    x="channel",
    y="revenue_usd",
    title="Revenue by Channel"
)

st.plotly_chart(fig, use_container_width=True)

st.subheader("Spend by Channel")

spend_channel = (
    filtered_df.groupby("channel")["spend_usd"]
    .sum()
    .reset_index()
)

fig2 = px.pie(
    spend_channel,
    names="channel",
    values="spend_usd",
    title="Spend Distribution"
)

st.plotly_chart(fig2, use_container_width=True)

st.subheader("Revenue by Device")

device_revenue = (
    filtered_df.groupby("device")["revenue_usd"]
    .sum()
    .reset_index()
)

fig3 = px.bar(
    device_revenue,
    x="device",
    y="revenue_usd",
    title="Revenue by Device"
)

st.plotly_chart(fig3, use_container_width=True)

#ROI BY country chart

st.subheader("ROI by Country")

roi_country = (
    filtered_df.groupby("country")["roi"]
    .mean()
    .reset_index()
    .sort_values("roi", ascending=False)
)

fig4 = px.bar(
    roi_country,
    x="country",
    y="roi",
    title="Average ROI by Country"
)

st.plotly_chart(fig4, use_container_width=True)

st.subheader("Conversions by Channel")

conv_channel = (
    filtered_df.groupby("channel")["conversion"]
    .sum()
    .reset_index()
)

fig5 = px.bar(
    conv_channel,
    x="channel",
    y="conversion",
    title="Conversions by Channel"
)

st.plotly_chart(fig5, use_container_width=True)

st.subheader("Filtered Dataset")

st.dataframe(filtered_df)
