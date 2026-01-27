import os
import json
import requests
from datetime import datetime
from urllib.parse import quote

import gspread
from dotenv import load_dotenv
from google.oauth2.service_account import Credentials

# ======================
# CONFIGURATION
# ======================

# Load local .env if exists (for local runs)
load_dotenv()

# API keys and credentials
OWM_API_KEY = os.getenv("OPENWEATHER_API_KEY")
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")
GOOGLE_CREDENTIALS_JSON = os.getenv("GOOGLE_CREDENTIALS_JSON")  # GitHub secret

# Weather location and units
CITY = "New York"
COUNTRY_CODE = "US"
UNITS = "metric"

# Alert thresholds
PRECIP_THRESHOLD = 0.5  # 50% chance
WIND_THRESHOLD = 10     # 10 m/s wind
ALERT_KEYWORDS = ["tornado", "hurricane", "blizzard", "snow", "storm", "thunder", "rain"]

# Severe weather order for prioritization
SEVERE_WEATHERS = [
    "tornado", "hurricane", "blizzard", "thunderstorm",
    "extreme heat", "heat", "cold", "frost"
]

# File to track alerts already sent locally
ALERTED_FILE = "alerted.txt"

# ======================
# WEATHER ICONS & ADVISORIES
# ======================

WEATHER_ICONS = {
    "clear sky": "☀️", "few clouds": "🌤️", "scattered clouds": "⛅",
    "broken clouds": "🌥️", "overcast clouds": "☁️", "light rain": "🌦️",
    "moderate rain": "🌧️", "heavy intensity rain": "🌧️", "thunderstorm": "⛈️",
    "snow": "❄️", "light snow": "🌨️", "mist": "🌫️", "fog": "🌫️",
    "haze": "🌫️", "dust": "🌪️", "sand": "🌪️", "volcanic ash": "🌋",
    "squalls": "💨", "tornado": "🌪️", "tropical storm": "🌀", "hurricane": "🌀",
    "extreme heat": "🔥", "heat": "🔥", "cold": "❄️", "frost": "❄️",
}

ADVISORY_MAP = {
    "snow": "Please drive carefully; roads may be slippery.",
    "blizzard": "Avoid traveling; visibility may be very low.",
    "sleet": "Use caution; surfaces may be icy.",
    "freezing rain": "Ice may form on roads; move cautiously.",
    "thunderstorm": "Stay indoors until the storm passes.",
    "lightning": "Avoid open spaces; unplug electronics.",
    "heavy rain": "Flooding may occur in low areas.",
    "rain": "Drive cautiously; use headlights.",
    "fog": "Visibility reduced; drive slowly.",
    "mist": "Drive with care.",
    "haze": "Air quality poor; limit outdoor activity.",
    "smoke": "Reduce prolonged outdoor exposure.",
    "dust": "Protect yourself outdoors.",
    "sand": "Limit outdoor activity.",
    "wind": "Secure loose items outside.",
    "strong wind": "High-profile vehicles exercise caution.",
    "gale": "Travel may be hazardous.",
    "tornado": "Seek shelter immediately.",
    "hurricane": "Follow local emergency guidance.",
    "extreme heat": "Stay hydrated and limit outdoor activities.",
    "heat": "Drink water regularly; take breaks in shade.",
    "cold": "Dress warmly; avoid prolonged exposure.",
    "frost": "Surfaces may be icy; be cautious.",
}

# ======================
# HELPER FUNCTIONS
# ======================

def build_forecast_url():
    return f"https://api.openweathermap.org/data/2.5/forecast?q={quote(CITY)},{COUNTRY_CODE}&appid={OWM_API_KEY}&units={UNITS}"

def get_forecast():
    try:
        response = requests.get(build_forecast_url(), timeout=10)
        response.raise_for_status()
        return response.json()["list"][0]
    except requests.RequestException as e:
        raise RuntimeError(f"Forecast API request failed: {e}")

def should_send_alert(conditions, precip, wind):
    conditions_lower = [c.lower() for c in conditions]
    return (
        any(keyword in cond for cond in conditions_lower for keyword in ALERT_KEYWORDS)
        or precip >= PRECIP_THRESHOLD
        or wind >= WIND_THRESHOLD
    )

def get_severe_condition(conditions):
    conditions_lower = [c.lower() for c in conditions]
    for severe in SEVERE_WEATHERS:
        for cond in conditions_lower:
            if severe in cond:
                return severe
    return None

def get_advisory(conditions):
    severe = get_severe_condition(conditions)
    if severe:
        return ADVISORY_MAP.get(severe, "")
    for cond in conditions:
        for key, tip in ADVISORY_MAP.items():
            if key in cond.lower():
                return tip
    return ""

def get_google_credentials():
    if GOOGLE_CREDENTIALS_JSON:
        creds_dict = json.loads(GOOGLE_CREDENTIALS_JSON)
        return Credentials.from_service_account_info(creds_dict, scopes=[
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive",
        ])
    else:
        return Credentials.from_service_account_file("credentials.json", scopes=[
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive",
        ])

def log_to_google_sheets(row):
    try:
        creds = get_google_credentials()
        client = gspread.authorize(creds)
        sheet = client.open("WeatherBotLogs").sheet1
        sheet.append_row(row)
    except Exception as e:
        print(f"Google Sheets logging failed: {e}")

def send_slack_alert(message):
    try:
        resp = requests.post(SLACK_WEBHOOK_URL, json={"text": message}, timeout=5)
        if resp.status_code != 200:
            print(f"Slack alert failed: {resp.text}")
    except requests.RequestException as e:
        print(f"Slack alert request failed: {e}")

def load_alerted_timestamps():
    try:
        with open(ALERTED_FILE, "r") as f:
            return set(line.strip() for line in f)
    except FileNotFoundError:
        return set()

def save_alerted_timestamp(forecast_time):
    with open(ALERTED_FILE, "a") as f:
        f.write(f"{forecast_time}\n")

# ======================
# MAIN
# ======================

def main():
    try:
        forecast = get_forecast()
    except RuntimeError as e:
        print(e)
        return

    logged_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    forecast_time = forecast["dt_txt"]

    temp_c = forecast["main"]["temp"]
    temp_f = round(temp_c * 9 / 5 + 32, 1)
    conditions = [w["description"] for w in forecast["weather"]]
    icons = [WEATHER_ICONS.get(c.lower(), "🌡️") for c in conditions]
    wind_speed = forecast["wind"]["speed"]
    precip_prob = round(float(forecast.get("pop", 0)), 2)
    precip_percent = int(precip_prob * 100)

    # Log to Google Sheets
    log_to_google_sheets([
        logged_at,
        forecast_time,
        temp_c,
        " / ".join(f"{icon} {desc.title()}" for icon, desc in zip(icons, conditions)),
        wind_speed,
        precip_prob
    ])

    # Alert logic
    if should_send_alert(conditions, precip_prob, wind_speed):
        alerted = load_alerted_timestamps()
        if forecast_time in alerted:
            return

        advisory = get_advisory(conditions)
        friendly_date = datetime.strptime(forecast_time, "%Y-%m-%d %H:%M:%S").strftime("%A, %d %B %Y at %I:%M %p")

        if any("snow" in c.lower() for c in conditions):
            precip_phrase = "chance of snow"
        elif any("rain" in c.lower() or "drizzle" in c.lower() for c in conditions):
            precip_phrase = "chance of rain"
        else:
            precip_phrase = "chance of precipitation"

        severe_condition = get_severe_condition(conditions)
        icon = WEATHER_ICONS.get(severe_condition, icons[0])

        message = (
            f":warning: {icon} NYC Weather Alert {icon} :warning:\n"
            f"{', '.join(desc.title() for desc in conditions)} expected on {friendly_date} at {temp_f}°F.\n"
            f"Wind: {wind_speed:.0f} m/s | {precip_phrase}: {precip_percent}%.\n"
        )
        if advisory:
            message += f"Safety Reminder: {advisory}"

        send_slack_alert(message)
        save_alerted_timestamp(forecast_time)

if __name__ == "__main__":
    main()
