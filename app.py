

# Prject Name: # Scotland vs UK: Airport Passenger Recovery Analysis (2019–2023)

# Step 1: Import required libraries.
import streamlit as st         # Streamlit – create interactive dashboard UI
import pandas as pd           # Pandas – load and manage data tables
import plotly.express as px   # Plotly – create interactive charts and graphs



st.set_page_config(
    page_title="Scotland vs UK: Airport Passenger Recovery (2019–2023)",
    page_icon="✈️",
    layout="wide"
)

st.title("✈️ Scotland vs UK: Airport Passenger Recovery (2019–2023)")
st.caption("Built with UK Civil Aviation Authority passenger data")

@st.cache_data
def load_data():
    df = pd.read_csv("uk_airport_passengers_2019_2023.csv")
    return df

df = load_data()

# Sidebar filters
st.sidebar.header("Filters")

years = sorted(df["Year"].unique())
year_range = st.sidebar.select_slider(
    "Select Year Range",
    options=years,
    value=(min(years), max(years))
)

airports = sorted(df["Airport"].unique())
default_airports = ["EDINBURGH", "GLASGOW", "HEATHROW", "MANCHESTER"]
default_airports = [a for a in default_airports if a in airports]

selected_airports = st.sidebar.multiselect(
    "Select Airports",
    options=airports,
    default=default_airports
)

# Apply filters
df_filtered = df[
    (df["Year"] >= year_range[0]) &
    (df["Year"] <= year_range[1]) &
    (df["Airport"].isin(selected_airports))
]

# KPIs
col1, col2 = st.columns(2)

latest_year = df_filtered["Year"].max()
baseline_year = 2019

latest_total = df_filtered[df_filtered["Year"] == latest_year]["Total_Passengers"].sum()
baseline_total = df[df["Year"] == baseline_year]["Total_Passengers"].sum()

recovery = (latest_total / baseline_total * 100) if baseline_total > 0 else 0

with col1:
    st.metric(f"Total Passengers in {latest_year}", f"{latest_total:,.0f}")

with col2:
    st.metric("Recovery vs 2019", f"{recovery:.1f}%")

st.markdown("---")

# Charts
tab1, tab2 = st.tabs(["📊 Yearly Trend", "📈 Airport Comparison"])

with tab1:
    yearly = (
        df_filtered
        .groupby("Year", as_index=False)["Total_Passengers"]
        .sum()
    )
    fig_year = px.bar(
        yearly,
        x="Year",
        y="Total_Passengers",
        title="Total Passengers by Year (Filtered)",
        text_auto=True
    )
    fig_year.update_layout(xaxis=dict(dtick=1))
    st.plotly_chart(fig_year, use_container_width=True)

with tab2:
    fig_trend = px.line(
        df_filtered.sort_values(["Airport", "Year"]),
        x="Year",
        y="Total_Passengers",
        color="Airport",
        markers=True,
        title="Passenger Trends by Airport"
    )
    fig_trend.update_layout(xaxis=dict(dtick=1))
    st.plotly_chart(fig_trend, use_container_width=True)


