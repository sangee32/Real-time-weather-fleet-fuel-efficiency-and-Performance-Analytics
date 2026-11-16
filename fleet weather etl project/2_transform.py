import pandas as pd
print("Starting ETL Transformation...")

# 1. Load raw CSV files
df_fleet = pd.read_csv("raw_data/fleet_trips.csv")
df_weather = pd.read_csv("raw_data/weather_logs.csv")

initial_count = len(df_fleet)

# 2. Data Quality Checks (Remove nulls and invalid negative/zero fuel values)
df_fleet = df_fleet.dropna(subset=["fuel_liters"])
df_fleet = df_fleet[df_fleet["fuel_liters"] > 0]
df_fleet["city"] = df_fleet["city"].str.strip().str.title()

cleaned_count = len(df_fleet)
print(f"Data Quality Check: Removed {initial_count - cleaned_count} corrupted records.")

# 3. Join Fleet Data with Weather Data
df_merged = pd.merge(df_fleet, df_weather, on=["city", "date"], how="inner")

# 4. Feature Engineering (Calculate Efficiency KPIs)
df_merged["km_per_liter"] = (df_merged["distance_km"] / df_merged["fuel_liters"]).round(2)

def classify_efficiency(kpl):
    if kpl < 1.8:
        return "Poor - Needs Check"
    elif kpl <= 2.6:
        return "Average"
    return "Optimal"

df_merged["efficiency_status"] = df_merged["km_per_liter"].apply(classify_efficiency)

# 5. Save to Parquet (Industry Standard Columnar Storage)
output_path = "processed_data/fleet_weather_analytics.parquet"
df_merged.to_parquet(output_path, index=False)
print(f"ETL Complete! Saved {len(df_merged)} clean rows to {output_path}")
