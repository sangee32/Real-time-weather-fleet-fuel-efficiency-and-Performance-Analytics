import duckdb
parquet_file = "processed_data/fleet_weather_analytics.parquet"
print("\n--- QUERY 1: Fuel Efficiency by Weather Condition ---")
q1 = duckdb.sql(f"""
    SELECT 
        weather_condition,
        COUNT(*) AS total_trips,
        ROUND(AVG(temperature_c), 1) AS avg_temp_c,
        ROUND(AVG(km_per_liter), 2) AS avg_km_per_liter
    FROM '{parquet_file}'
    GROUP BY weather_condition
    ORDER BY avg_km_per_liter ASC
""")
print(q1)

print("\n--- QUERY 2: Top 2 Lowest-Efficiency Vehicles Per City (Window Function) ---")
q2 = duckdb.sql(f"""
    WITH RankedVehicles AS (
        SELECT 
            city,
            vehicle_id,
            ROUND(AVG(km_per_liter), 2) AS avg_efficiency,
            RANK() OVER (PARTITION BY city ORDER BY AVG(km_per_liter) ASC) AS efficiency_rank
        FROM '{parquet_file}'
        GROUP BY city, vehicle_id
    )
    SELECT * FROM RankedVehicles WHERE efficiency_rank <= 2
""")
print(q2)
