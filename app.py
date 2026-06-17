from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


st.set_page_config(
    page_title="Marketing Campaign Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)


def load_data() -> pd.DataFrame:
    base_path = Path(__file__).resolve().parent / "data"
    candidates = [
        base_path / "marketing_campaign.xlsx",
        base_path / "campaign_data.csv",
    ]

    for candidate in candidates:
        if candidate.exists() and candidate.stat().st_size > 0:
            if candidate.suffix.lower() == ".xlsx":
                return pd.read_excel(candidate)
            return pd.read_csv(candidate)

    raise FileNotFoundError("No campaign dataset found in the data folder.")


@st.cache_data
def get_data() -> pd.DataFrame:
    df = load_data().copy()
    df.columns = [column.strip() for column in df.columns]
    return df


def format_currency(value: float) -> str:
    return f"${value:,.0f}"


def add_chart_style(fig):
    fig.update_layout(
        template="plotly_white",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=0, r=0, t=40, b=0),
        font=dict(family="Inter, sans-serif", color="#183153"),
        title_font=dict(size=18),
        hovermode="x unified",
    )
    fig.update_xaxes(showgrid=False, title=None)
    fig.update_yaxes(gridcolor="rgba(24, 49, 83, 0.08)", title=None)
    return fig


st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

        :root {
            --bg: #f4f8fb;
            --surface: rgba(255, 255, 255, 0.88);
            --surface-strong: #ffffff;
            --text: #17324d;
            --muted: #5d738d;
            --accent: #0f766e;
            --accent-2: #0b5cab;
            --border: rgba(15, 118, 110, 0.14);
            --shadow: 0 18px 55px rgba(15, 23, 42, 0.10);
        }

        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
        }

        .stApp {
            background:
                radial-gradient(circle at top left, rgba(15, 118, 110, 0.10), transparent 28%),
                radial-gradient(circle at top right, rgba(11, 92, 171, 0.10), transparent 26%),
                linear-gradient(180deg, #eef5f8 0%, #f7fbfd 35%, #f4f8fb 100%);
            color: var(--text);
        }

        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }

        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, rgba(255,255,255,0.95), rgba(241,248,250,0.94));
            border-right: 1px solid rgba(15, 23, 42, 0.06);
        }

        .hero {
            background: linear-gradient(135deg, rgba(15, 118, 110, 0.98), rgba(11, 92, 171, 0.96));
            color: white;
            border-radius: 28px;
            padding: 2rem 2rem 1.75rem;
            box-shadow: var(--shadow);
            position: relative;
            overflow: hidden;
        }

        .hero::after {
            content: "";
            position: absolute;
            inset: 0;
            background: radial-gradient(circle at top right, rgba(255,255,255,0.20), transparent 28%);
            pointer-events: none;
        }

        .eyebrow {
            font-size: 0.82rem;
            letter-spacing: 0.18em;
            text-transform: uppercase;
            opacity: 0.85;
            margin-bottom: 0.75rem;
        }

        .hero h1 {
            font-size: 2.25rem;
            margin: 0 0 0.5rem;
            line-height: 1.08;
        }

        .hero p {
            margin: 0;
            max-width: 64ch;
            opacity: 0.9;
            font-size: 1rem;
            line-height: 1.6;
        }

        .metric-card {
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 22px;
            padding: 1rem 1.1rem;
            box-shadow: 0 8px 30px rgba(15, 23, 42, 0.05);
            backdrop-filter: blur(12px);
        }

        .metric-label {
            color: var(--muted);
            font-size: 0.84rem;
            margin-bottom: 0.4rem;
        }

        .metric-value {
            font-size: 1.65rem;
            font-weight: 800;
            color: var(--text);
            line-height: 1;
        }

        .metric-subtext {
            margin-top: 0.45rem;
            color: var(--muted);
            font-size: 0.84rem;
        }

        .section-card {
            background: var(--surface-strong);
            border: 1px solid rgba(15, 23, 42, 0.06);
            border-radius: 24px;
            padding: 1.25rem;
            box-shadow: 0 10px 35px rgba(15, 23, 42, 0.05);
        }

        .stDataFrame, .stDataFrame [data-testid="stTable"] {
            border-radius: 18px;
            overflow: hidden;
        }

        .stTabs [data-baseweb="tab-list"] {
            gap: 0.5rem;
        }

        .stTabs [data-baseweb="tab"] {
            border-radius: 999px;
            padding: 0.6rem 1rem;
            background: rgba(255,255,255,0.62);
            border: 1px solid rgba(15, 118, 110, 0.10);
        }

        .stTabs [aria-selected="true"] {
            background: linear-gradient(135deg, rgba(15, 118, 110, 0.16), rgba(11, 92, 171, 0.14));
        }

        .stMetric {
            background: transparent;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


df = get_data()

required_columns = {
    "channel",
    "country",
    "device",
    "segment",
    "impressions",
    "clicks",
    "conversion",
    "spend_usd",
    "revenue_usd",
    "roi",
}

missing_columns = required_columns - set(df.columns)
if missing_columns:
    st.error(f"The dataset is missing required columns: {', '.join(sorted(missing_columns))}")
    st.stop()


st.markdown(
    """
    <div class="hero">
        <div class="eyebrow">Marketing Campaign Performance</div>
        <h1>Smarter visibility into revenue, spend, and conversion quality.</h1>
        <p>
            Explore campaign performance with a cleaner layout, stronger hierarchy, and faster filtering.
            The dashboard highlights the metrics that matter first, then lets you drill into channel, country,
            device, and audience patterns.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)


with st.sidebar:
    st.markdown("## Filters")
    st.caption("Narrow the dashboard before you compare channels or audiences.")

    selected_channels = st.multiselect(
        "Channel",
        options=sorted(df["channel"].dropna().unique().tolist()),
        default=sorted(df["channel"].dropna().unique().tolist()),
    )

    selected_countries = st.multiselect(
        "Country",
        options=sorted(df["country"].dropna().unique().tolist()),
        default=sorted(df["country"].dropna().unique().tolist()),
    )

    selected_devices = st.multiselect(
        "Device",
        options=sorted(df["device"].dropna().unique().tolist()),
        default=sorted(df["device"].dropna().unique().tolist()),
    )

    selected_segments = st.multiselect(
        "Segment",
        options=sorted(df["segment"].dropna().unique().tolist()),
        default=sorted(df["segment"].dropna().unique().tolist()),
    )


filtered_df = df.copy()
if selected_channels:
    filtered_df = filtered_df[filtered_df["channel"].isin(selected_channels)]
if selected_countries:
    filtered_df = filtered_df[filtered_df["country"].isin(selected_countries)]
if selected_devices:
    filtered_df = filtered_df[filtered_df["device"].isin(selected_devices)]
if selected_segments:
    filtered_df = filtered_df[filtered_df["segment"].isin(selected_segments)]


if filtered_df.empty:
    st.warning("No data matches the current filters. Clear one or more filters to continue.")
    st.stop()


total_revenue = filtered_df["revenue_usd"].sum()
total_spend = filtered_df["spend_usd"].sum()
total_clicks = filtered_df["clicks"].sum()
total_impressions = filtered_df["impressions"].sum()
total_conversions = filtered_df["conversion"].sum()
ctr = (total_clicks / total_impressions * 100) if total_impressions else 0
conversion_rate = (total_conversions / total_clicks * 100) if total_clicks else 0
avg_roi = filtered_df["roi"].mean()
revenue_per_conversion = (total_revenue / total_conversions) if total_conversions else 0


st.markdown("### At a glance")

metric_cols = st.columns(4)
metric_blocks = [
    ("Revenue", format_currency(total_revenue), f"Spend: {format_currency(total_spend)}"),
    ("Spend", format_currency(total_spend), f"Revenue / Spend ratio: {(total_revenue / total_spend):.2f}" if total_spend else "No spend recorded"),
    ("CTR", f"{ctr:.2f}%", f"Clicks: {int(total_clicks):,}"),
    ("Conversions", f"{int(total_conversions):,}", f"Conversion rate: {conversion_rate:.2f}%"),
]

for column, (label, value, note) in zip(metric_cols, metric_blocks):
    with column:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">{label}</div>
                <div class="metric-value">{value}</div>
                <div class="metric-subtext">{note}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


metric_cols_2 = st.columns(4)
second_metric_blocks = [
    ("Average ROI", f"{avg_roi:.2f}", f"Revenue / conversion: {format_currency(revenue_per_conversion)}" if revenue_per_conversion else "No conversions recorded"),
    ("Impressions", f"{int(total_impressions):,}", f"Filtered rows: {len(filtered_df):,}"),
    ("Countries", f"{filtered_df['country'].nunique():,}", "Distinct market coverage"),
    ("Campaigns", f"{filtered_df['campaign_id'].nunique():,}", "Unique active campaigns"),
]

for column, (label, value, note) in zip(metric_cols_2, second_metric_blocks):
    with column:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">{label}</div>
                <div class="metric-value">{value}</div>
                <div class="metric-subtext">{note}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


overview_tab, channel_tab, audience_tab, data_tab = st.tabs(
    ["Overview", "Channel mix", "Audience", "Data"]
)


with overview_tab:
    left_col, right_col = st.columns([1.25, 1])

    with left_col:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown("#### Revenue by channel")
        revenue_channel = (
            filtered_df.groupby("channel", as_index=False)["revenue_usd"].sum().sort_values("revenue_usd", ascending=False)
        )
        fig = px.bar(
            revenue_channel,
            x="channel",
            y="revenue_usd",
            color="revenue_usd",
            color_continuous_scale=["#ccefe9", "#0f766e"],
            text_auto=".2s",
        )
        fig.update_traces(marker_line_width=0, textposition="outside")
        st.plotly_chart(add_chart_style(fig), use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with right_col:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown("#### Spend distribution")
        spend_channel = (
            filtered_df.groupby("channel", as_index=False)["spend_usd"].sum().sort_values("spend_usd", ascending=False)
        )
        fig2 = px.pie(
            spend_channel,
            names="channel",
            values="spend_usd",
            hole=0.58,
            color_discrete_sequence=["#0f766e", "#0b5cab", "#14b8a6", "#22c55e", "#38bdf8"],
        )
        fig2.update_traces(textinfo="percent+label", sort=False, marker=dict(line=dict(color="white", width=2)))
        st.plotly_chart(add_chart_style(fig2), use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)


with channel_tab:
    left_col, right_col = st.columns(2)

    with left_col:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown("#### Conversions by channel")
        conv_channel = (
            filtered_df.groupby("channel", as_index=False)["conversion"].sum().sort_values("conversion", ascending=False)
        )
        fig3 = px.bar(
            conv_channel,
            x="channel",
            y="conversion",
            color="conversion",
            color_continuous_scale=["#d9f2ef", "#0f766e"],
            text_auto=True,
        )
        fig3.update_traces(marker_line_width=0, textposition="outside")
        st.plotly_chart(add_chart_style(fig3), use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with right_col:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown("#### ROI by country")
        roi_country = (
            filtered_df.groupby("country", as_index=False)["roi"].mean().sort_values("roi", ascending=False)
        )
        fig4 = px.bar(
            roi_country,
            x="country",
            y="roi",
            color="roi",
            color_continuous_scale=["#dbeafe", "#0b5cab"],
            text_auto=".2f",
        )
        fig4.update_traces(marker_line_width=0, textposition="outside")
        st.plotly_chart(add_chart_style(fig4), use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)


with audience_tab:
    left_col, right_col = st.columns(2)

    with left_col:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown("#### Revenue by device")
        device_revenue = (
            filtered_df.groupby("device", as_index=False)["revenue_usd"].sum().sort_values("revenue_usd", ascending=False)
        )
        fig5 = px.bar(
            device_revenue,
            x="device",
            y="revenue_usd",
            color="revenue_usd",
            color_continuous_scale=["#d7fbf5", "#0f766e"],
            text_auto=".2s",
        )
        fig5.update_traces(marker_line_width=0, textposition="outside")
        st.plotly_chart(add_chart_style(fig5), use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with right_col:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown("#### Segment performance")
        segment_summary = (
            filtered_df.groupby("segment", as_index=False)[["revenue_usd", "conversion", "spend_usd"]]
            .sum()
            .sort_values("revenue_usd", ascending=False)
        )
        fig6 = px.bar(
            segment_summary,
            x="segment",
            y="revenue_usd",
            color="conversion",
            color_continuous_scale=["#e0f2fe", "#0b5cab"],
            text_auto=".2s",
        )
        fig6.update_traces(marker_line_width=0, textposition="outside")
        st.plotly_chart(add_chart_style(fig6), use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)


with data_tab:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown("#### Filtered dataset")
    st.caption("Preview the rows behind the charts. Use the filters in the sidebar to focus on a specific market or channel mix.")
    st.dataframe(
        filtered_df.sort_values(["revenue_usd", "roi"], ascending=[False, False]),
        use_container_width=True,
        height=420,
    )
    st.markdown("</div>", unsafe_allow_html=True)
