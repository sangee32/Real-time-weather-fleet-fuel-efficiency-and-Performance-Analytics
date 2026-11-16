import streamlit as st
import pandas as pd
st.title("Heavy Fleet Fuel & Weather Analytics")
df = pd.read_parquet("processed_data/fleet_weather_analytics.parquet")
col1, col2, col3 = st.columns(3)
col1.metric("Total Clean Trips", len(df))
col2.metric("Avg Efficiency (km/L)", round(df["km_per_liter"].mean(), 2))
col3.metric("Total Fuel Used (L)", f"{int(df['fuel_liters'].sum()):,}")

st.subheader("Average Fuel Efficiency by City")
city_chart = df.groupby("city")["km_per_liter"].mean()
st.bar_chart(city_chart)

st.subheader("Trips Flagged for Maintenance ('Poor - Needs Check')")
st.dataframe(df[df["efficiency_status"] == "Poor - Needs Check"].head(20))
