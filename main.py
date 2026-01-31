import os
import json
import requests
from datetime import datetime
from urllib.parse import quote
import tempfile

import gspread
from dotenv import load_dotenv, find_dotenv
from google.oauth2.service_account import Credentials

# ======================
# CONFIGURATION
# ======================

# Load environment variables from .env (local development)
load_dotenv(find_dotenv())

# API keys and credentials
OWM_API_KEY = os.getenv("OPENWEATHER_API_KEY")
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")
GOOGLE_CREDS_JSON = os.getenv("GOOGLE_CREDENTIALS_JSON")  # GitHub Actions secret
GOOGLE_CREDENTIALS = os.getenv("GOOGLE_CREDENTIALS")      # local file

# ======================
# RUN TYPE DETECTION
# ======================
# Determine if the script is running locally (manual) or via GitHub Actions (scheduled)
if "GITHUB_ACTIONS" in os.environ:
    RUN_TYPE = os.getenv("RUN_TYPE", "Scheduled")
else:
    RUN_TYPE = "Manual"

# ======================
# WEATHER SETTINGS
# ======================

# Location and units
CITY = "New York"
COUNTRY_CODE = "US"
UNITS = "metric"

# Alert thresholds
PRECIP_THRESHOLD = 0.5
WIND_THRESHOLD = 10
ALERT_KEYWORDS = ["tornado", "hurricane", "blizzard", "snow", "storm", "thunder", "rain"]

# Severe weather conditions
SEVERE_WEATHERS = [
    "tornado", "hurricane", "blizzard", "thunderstorm",
    "extreme heat", "heat", "cold", "frost"
]

ALERTED_FILE = "alerted.txt"  # Stores timestamps of already sent alerts

# Mapping weather conditions to icons
WEATHER_ICONS = {
    "clear sky": "☀️", "few clouds": "🌤️", "scattered clouds": "⛅",
    "broken clouds": "🌥️", "overcast clouds": "☁️", "light rain": "🌦️",
    "moderate rain": "🌧️", "heavy intensity rain": "🌧️", "thunderstorm": "⛈️",
    "snow": "❄️", "light snow": "🌨️", "mist": "🌫️", "fog": "🌫️",
    "haze": "🌫️", "dust": "🌪️", "sand": "🌪️", "volcanic ash": "🌋",
    "squalls": "💨", "tornado": "🌪️", "tropical storm": "🌀", "hurricane": "🌀",
    "extreme heat": "🔥", "heat": "🔥", "cold": "❄️", "frost": "❄️",
}

# Advisory messages for different conditions
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
    """Constructs the OpenWeatherMap API URL for the forecast."""
    return f"https://api.openweathermap.org/data/2.5/forecast?q={quote(CITY)},{COUNTRY_CODE}&appid={OWM_API_KEY}&units={UNITS}"

def get_forecast():
    """Fetches the latest weather forecast data from OpenWeatherMap API."""
    try:
        response = requests.get(build_forecast_url(), timeout=10)
        response.raise_for_status()
        return response.json()["list"][0]  # return first forecast entry
    except requests.RequestException as e:
        raise RuntimeError(f"Forecast API request failed: {e}")

def should_send_alert(conditions, precip, wind):
    """Determines if an alert should be sent based on weather conditions and thresholds."""
    conditions_lower = [c.lower() for c in conditions]
    return (
        any(keyword in cond for cond in conditions_lower for keyword in ALERT_KEYWORDS)
        or precip >= PRECIP_THRESHOLD
        or wind >= WIND_THRESHOLD
    )

def get_severe_condition(conditions):
    """Returns the first severe weather condition detected from the forecast."""
    conditions_lower = [c.lower() for c in conditions]
    for severe in SEVERE_WEATHERS:
        for cond in conditions_lower:
            if severe in cond:
                return severe
    return None

def get_advisory(conditions):
    """Retrieves the advisory message based on detected severe weather."""
    severe = get_severe_condition(conditions)
    if severe:
        return ADVISORY_MAP.get(severe, "")
    for cond in conditions:
        for key, tip in ADVISORY_MAP.items():
            if key in cond.lower():
                return tip
    return ""

def get_gspread_client():
    """Authenticates and returns a Google Sheets client."""
    if GOOGLE_CREDS_JSON:
        # Use JSON from GitHub secret
        creds_dict = json.loads(GOOGLE_CREDS_JSON)
        tmp_file = tempfile.NamedTemporaryFile(mode="w+", delete=False, suffix=".json")
        json.dump(creds_dict, tmp_file)
        tmp_file.flush()
        creds = Credentials.from_service_account_file(tmp_file.name, scopes=[
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive",
        ])
    else:
        # Use local credentials file
        creds = Credentials.from_service_account_file(GOOGLE_CREDENTIALS, scopes=[
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive",
        ])
    return gspread.authorize(creds)

def log_to_google_sheets(row):
    """Appends a row of weather data to the Google Sheet."""
    try:
        client = get_gspread_client()
        sheet = client.open("WeatherBotLogs").sheet1
        sheet.append_row(row)
    except Exception as e:
        print(f"Google Sheets logging failed: {e}")

def send_slack_alert(message):
    """Sends a formatted alert message to Slack via webhook."""
    try:
        resp = requests.post(SLACK_WEBHOOK_URL, json={"text": message}, timeout=5)
        if resp.status_code != 200:
            print(f"Slack alert failed: {resp.text}")
    except requests.RequestException as e:
        print(f"Slack alert request failed: {e}")

def load_alerted_timestamps():
    """Loads timestamps of previously sent alerts to prevent duplicates."""
    try:
        with open(ALERTED_FILE, "r") as f:
            return set(line.strip() for line in f)
    except FileNotFoundError:
        return set()

def save_alerted_timestamp(forecast_time):
    """Records a timestamp of a sent alert."""
    with open(ALERTED_FILE, "a") as f:
        f.write(f"{forecast_time}\n")

# ======================
# MAIN FUNCTION
# ======================

def main():
    """Main workflow: fetch forecast, log to Google Sheets, and send Slack alerts if needed."""
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

    # Log weather data to Google Sheets
    log_to_google_sheets([
        logged_at,
        forecast_time,
        temp_c,
        " / ".join(f"{icon} {desc.title()}" for icon, desc in zip(icons, conditions)),
        wind_speed,
        precip_prob,
        RUN_TYPE
    ])

    # Check if alert should be sent
    if should_send_alert(conditions, precip_prob, wind_speed):
        alerted = load_alerted_timestamps()
        if forecast_time in alerted:
            return  # Skip if alert already sent

        advisory = get_advisory(conditions)
        friendly_date = datetime.strptime(forecast_time, "%Y-%m-%d %H:%M:%S").strftime("%A, %d %B %Y at %I:%M %p")

        # Determine precipitation phrase
        if any("snow" in c.lower() for c in conditions):
            precip_phrase = "chance of snow"
        elif any("rain" in c.lower() or "drizzle" in c.lower() for c in conditions):
            precip_phrase = "chance of rain"
        else:
            precip_phrase = "chance of precipitation"

        severe_condition = get_severe_condition(conditions)
        icon = WEATHER_ICONS.get(severe_condition, icons[0])

        # Build alert message
        message = (
            f":warning: {icon} NYC Weather Alert {icon} :warning:\n"
            f"{', '.join(desc.title() for desc in conditions)} expected on {friendly_date} at {temp_f}°F.\n"
            f"Wind: {wind_speed:.0f} m/s | {precip_phrase}: {precip_percent}%.\n"
        )
        if advisory:
            message += f"Safety Reminder: {advisory}"

        # Send Slack alert and save timestamp
        send_slack_alert(message)
        save_alerted_timestamp(forecast_time)

if __name__ == "__main__":
    main()
