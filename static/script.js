document.addEventListener("DOMContentLoaded", () => {
  fetchWeather();
  fetchForecast();
});

async function fetchWeather() {
  try {
    const res = await fetch("/api/weather");
    if (!res.ok) throw new Error("Failed to fetch weather");
    const data = await res.json();

    document.getElementById("temp").textContent = `${Math.round(data.temperature)}°C`;
    document.getElementById("condition").textContent = data.condition;
    document.getElementById("humidity").textContent = `${data.humidity}%`;
    document.getElementById("wind").textContent = `${data.wind_speed} m/s`;

    document.getElementById("loading").classList.add("hidden");
    document.getElementById("weather-data").classList.remove("hidden");
  } catch (err) {
    document.getElementById("loading").classList.add("hidden");
    document.getElementById("error").textContent = "Could not load weather data.";
    document.getElementById("error").classList.remove("hidden");
  }
}

async function fetchForecast() {
  try {
    const res = await fetch("/api/forecast");
    if (!res.ok) throw new Error("Failed to fetch forecast");
    const data = await res.json();

    const container = document.getElementById("forecast-list");
    data.forecast.forEach((day) => {
      const div = document.createElement("div");
      div.className = "forecast-day";
      const date = new Date(day.date + "T00:00:00");
      const dayName = date.toLocaleDateString("en-US", { weekday: "short", month: "short", day: "numeric" });
      div.innerHTML = `
        <div class="date">${dayName}</div>
        <div class="temps">${Math.round(day.temp_high)}° <span class="low">${Math.round(day.temp_low)}°</span></div>
        <div class="desc">${day.condition}</div>
      `;
      container.appendChild(div);
    });

    document.getElementById("forecast-loading").classList.add("hidden");
    container.classList.remove("hidden");
  } catch (err) {
    document.getElementById("forecast-loading").classList.add("hidden");
    document.getElementById("forecast-error").textContent = "Could not load forecast data.";
    document.getElementById("forecast-error").classList.remove("hidden");
  }
}
