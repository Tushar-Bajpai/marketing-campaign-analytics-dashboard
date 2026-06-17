# Marketing Campaign Dashboard

A Streamlit-based analytics dashboard for exploring marketing campaign performance across channels, countries, devices, and audience segments. The app provides KPI cards, interactive charts, and a filter-driven layout to help review revenue, spend, clicks, conversions, ROI, and related trends in one place.

## Project Overview

This project is designed to make campaign analysis easier by presenting the most important business metrics in a clean dashboard interface. It is useful for quick performance checks, comparative analysis, and filtering campaign data into smaller, more meaningful views.

## Key Features

- Clean and responsive Streamlit UI
- Filter sidebar with dropdown-based selections
- KPI summary cards for fast performance review
- Interactive Plotly charts for channel, device, segment, and country analysis
- Filtered data table for row-level inspection
- Robust data loading from Excel or CSV sources

## Tech Stack

- Python
- Streamlit
- Pandas
- Plotly

## Folder Structure

```text
Marketing-Campaign-Dashboard/
├── app.py
├── Readme.md
├── requirements.txt
├── data/
│   ├── campaign_data.csv
│   └── marketing_campaign.xlsx
└── screenshots/
```

## Data Files

The application looks for campaign data in the `data/` folder.

- `data/marketing_campaign.xlsx` is the primary dataset used by the dashboard.
- `data/campaign_data.csv` is included as an alternate data source.

If you replace the dataset, keep the column names consistent with the app logic so the filters and charts continue to work correctly.

## Required Columns

The dashboard expects the following columns to be present in the dataset:

- `channel`
- `country`
- `device`
- `segment`
- `impressions`
- `clicks`
- `conversion`
- `spend_usd`
- `revenue_usd`
- `roi`

## Installation

1. Clone or open the project folder in VS Code.
2. Create and activate a Python virtual environment.
3. Install the dependencies.

```bash
pip install -r requirements.txt
```

## Run the App

Start the dashboard with Streamlit:

```bash
streamlit run app.py
```

After the app opens, use the sidebar dropdowns to filter by:

- Channel
- Country
- Device
- Segment

## How to Use

1. Open the dashboard in your browser.
2. Select values from the filter dropdowns in the sidebar.
3. Review the KPI cards at the top for the main performance snapshot.
4. Move through the tabs to compare channel mix, audience trends, and table-level data.
5. Use the filtered dataset table to inspect the underlying records.

## Dashboard Sections

- **Hero section**: Introduces the dashboard and sets the business context.
- **At a glance**: Shows the top summary metrics.
- **Overview tab**: Displays revenue and spend distribution.
- **Channel mix tab**: Focuses on conversion and ROI comparisons.
- **Audience tab**: Highlights device and segment performance.
- **Data tab**: Shows the filtered dataset behind the charts.

## Notes

- The app is built with a focus on readability and fast filtering.
- Charts and cards are styled directly in the app for a more polished presentation.
- The data source is loaded dynamically, so the dashboard can work with the workbook or CSV file in the `data/` folder.

## Future Improvements

- Add more advanced time-based analysis if date fields become available.
- Include downloadable chart exports and filtered data exports.
- Add richer comparison views across campaigns and segments.
- Improve KPI storytelling with more context-aware insights.

## Status

There are still changes need to be made in this analytics project.
