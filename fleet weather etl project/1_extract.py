
import requests
import pandas as pd
import random
import os
from datetime import datetime

# Create raw_data folder if it doesn't exist
os.makedirs("raw_data", exist_ok=True)

# 1. Cities with Latitude & Longitude
cities = {
    "Chennai": (13.0827, 80.2707),
    "Bengaluru": (12.9716, 77.5946),
    "Mumbai": (19.0760, 72.8777),
    "Pune": (18.5204, 73.8567),
    "Delhi": (28.7041, 77.1025)
}

weather_records = []
today_str = datetime.now().strftime("%Y-%m-%d")

print("Fetching live weather from Open-Meteo API...")

for city, (lat, lon) in cities.items():

    # Correct Open-Meteo API URL
    url = "https://api.open-meteo.com/v1/forecast"

    params = {
        "latitude": lat,
        "longitude": lon,
        "current": "temperature_2m,wind_speed_10m,weather_code"
    }

    try:
        response = requests.get(url, params=params, timeout=15)
        response.raise_for_status()

        data = response.json()
        current = data["current"]

        # Map WMO weather codes to simple labels
        code = current["weather_code"]

        if code <= 3:
            condition = "Clear"
        elif 51 <= code <= 67 or 80 <= code <= 82:
            condition = "Rain"
        else:
            condition = "Cloudy"

        weather_records.append({
            "city": city,
            "date": today_str,
            "temperature_c": current["temperature_2m"],
            "windspeed_kmh": current["wind_speed_10m"],
            "weather_condition": condition
        })

        print(f"{city}: Weather fetched successfully!")

    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather for {city}: {e}")

    except (KeyError, ValueError) as e:
        print(f"Invalid weather response for {city}: {e}")

# Save weather data
df_weather = pd.DataFrame(weather_records)

if not df_weather.empty:
    df_weather.to_csv("raw_data/weather_logs.csv", index=False)
    print("Saved raw_data/weather_logs.csv!")
else:
    print("No weather data collected.")

# 2. Generate 5,000 Simulated Heavy Fleet Trip Logs
print("Generating 5,000 simulated fleet trip logs...")

fleet_records = []
city_names = list(cities.keys())

for i in range(1, 5001):

    city = random.choice(city_names)
    distance = round(random.uniform(25.0, 300.0), 2)
    load_tons = round(random.uniform(10.0, 60.0), 1)

    # Realistic fuel formula: heavier load = more fuel
    fuel = round(
        (distance / 3.2) +
        (load_tons * 0.4) +
        random.uniform(-3, 5), 2
    )

    # Inject ~2% dirty data (nulls & negative values)
    if random.random() < 0.01:
        fuel = None
    elif random.random() < 0.01:
        fuel = -15.0

    fleet_records.append({
        "trip_id": f"TRP_{10000 + i}",
        "vehicle_id": f"CAT_777_{random.randint(1, 50):02d}",
        "city": city,
        "date": today_str,
        "distance_km": distance,
        "load_tons": load_tons,
        "fuel_liters": fuel
    })

df_fleet = pd.DataFrame(fleet_records)

df_fleet.to_csv("raw_data/fleet_trips.csv", index=False)

print("Saved raw_data/fleet_trips.csv!")

print("\nAll data generation tasks completed successfully!")
print("Weather records:", len(df_weather))
print("Fleet trip records:", len(df_fleet))
