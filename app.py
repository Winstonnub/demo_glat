import os

import requests
from dotenv import load_dotenv
from flask import Flask, jsonify, render_template

load_dotenv()

app = Flask(__name__)

API_KEY = os.getenv("OPENWEATHER_API_KEY")
CITY = "Toronto"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/weather")
def weather():
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {"q": CITY, "appid": API_KEY, "units": "metric"}
    response = requests.get(url, params=params, timeout=10)

    if response.status_code != 200:
        return jsonify({"error": "Failed to fetch weather data"}), 502

    data = response.json()
    return jsonify({
        "city": CITY,
        "temperature": data["main"]["temp"],
        "condition": data["weather"][0]["description"],
        "humidity": data["main"]["humidity"],
        "wind_speed": data["wind"]["speed"],
    })


@app.route("/api/forecast")
def forecast():
    url = "https://api.openweathermap.org/data/2.5/forecast"
    params = {"q": CITY, "appid": API_KEY, "units": "metric"}
    response = requests.get(url, params=params, timeout=10)

    if response.status_code != 200:
        return jsonify({"error": "Failed to fetch forecast data"}), 502

    data = response.json()
    daily = {}
    for entry in data["list"]:
        date = entry["dt_txt"].split(" ")[0]
        if date not in daily:
            daily[date] = {
                "date": date,
                "temp_high": entry["main"]["temp_max"],
                "temp_low": entry["main"]["temp_min"],
                "condition": entry["weather"][0]["description"],
                "humidity": entry["main"]["humidity"],
            }
        else:
            daily[date]["temp_high"] = max(daily[date]["temp_high"], entry["main"]["temp_max"])
            daily[date]["temp_low"] = min(daily[date]["temp_low"], entry["main"]["temp_min"])

    return jsonify({"city": CITY, "forecast": list(daily.values())})


@app.route("/api/hourly-forecast")
def hourly_forecast():
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": 43.65107,  # Toronto latitude
        "longitude": -79.347015,  # Toronto longitude
        "hourly": "temperature_2m",
        "forecast_days": 1,
        "timezone": "auto",
    }
    response = requests.get(url, params=params, timeout=10)

    if response.status_code != 200:
        return jsonify({"error": "Failed to fetch hourly forecast data"}), 502

    data = response.json()
    hourly = data.get("hourly") or {}
    times = hourly.get("time") or []
    temperatures = hourly.get("temperature_2m") or []

    if not times or not temperatures:
        return jsonify({"error": "Invalid hourly forecast data"}), 502

    entries = [
        {"time": time, "temperature": temp}
        for time, temp in zip(times, temperatures)
    ][:6]

    return jsonify({"city": CITY, "hours": entries})


if __name__ == "__main__":
    app.run(debug=True)
