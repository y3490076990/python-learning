import requests
import argparse
parser = argparse.ArgumentParser(description="查天气")
parser.add_argument("city", help="beijing")
args = parser.parse_args()

url = "https://geocoding-api.open-meteo.com/v1/search"
resp = requests.get(url, params={"name": args.city, "count": 1, "language": "zh"})
data = resp.json()

if "results" not in data or not data["results"]:
      print(f"找不到城市: {args.city}")
      exit()

loc = data["results"][0]
lat = loc["latitude"]
lon = loc["longitude"]
name = loc["name"]

forecast_url = "https://api.open-meteo.com/v1/forecast"
params = {
      "latitude": lat, "longitude": lon,
      "daily": "temperature_2m_max,temperature_2m_min,weathercode",
      "timezone": "Asia/Shanghai"
  }
forecast = requests.get(forecast_url, params=params).json()
print(f"\n{name} 未来几天天气：\n")
dates = forecast["daily"]["time"]
max_temps = forecast["daily"]["temperature_2m_max"]
min_temps = forecast["daily"]["temperature_2m_min"]

for i in range(len(dates)):
      print(f"  {dates[i]}:  {min_temps[i]}°C ~ {max_temps[i]}°C")

print()