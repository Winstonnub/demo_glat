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


if __name__ == "__main__":
    app.run(debug=True)
