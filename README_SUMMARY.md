# ⚡ Weather Alert Bot

**Developer:** Bryant James Mingoy  

---

## 🌤 Overview 🌤

Python bot for monitoring NYC weather:

- 🌡 Fetches real-time weather from OpenWeatherMap API  
- 📊 Logs hourly or on-demand forecasts to Google Sheets  
- ⚠ Sends Slack alerts for snow or storm conditions  

---

## 📂 Repository Structure 📂

```
main.py
specifications.md
requirements.txt
.env.example
.gitignore
.github/workflows/main.yml
```

---

## 📝 Google Sheet Logging 📝

**Columns:** Log | Forecasted Time | Temp (°C) | Conditions | Wind (m/s) | Precip (%) | Run Type  

- 🎨 Conditional formatting highlights severe weather  
- ⏰ Supports hourly and manual runs  

---

## 📢 Slack Alerts 📢

**Example message:**

```
NYC Weather Alert
Light Snow expected on Tuesday, 27 January 2026 at 09:00 PM at 21.5°F.
Wind: 6 m/s | chance of snow: 20%.
Safety Reminder: Please drive carefully; roads may be slippery.
```

- ⚠ Alerts only for snow/storm thresholds  
- 🧪 Can test with simulated data  

---

## ⚡ Quick Start ⚡

1. **Clone repo**:  
```bash
git clone https://github.com/<USERNAME>/<REPO>.git
cd weather-alert-bot
```
2. **Create & activate virtual environment**  
3. **Install dependencies**:  
```bash
pip install -r requirements.txt
```  
4. **Configure API keys**: Copy `.env.example` → `.env` and add keys  
5. **Run bot**:  
```bash
python main.py
```  

> ⏰ Hourly automation possible with Python `schedule` or GitHub Actions

---

## ✅ Highlights ✅

- ✅ Google Sheets logging fully implemented  
- ✅ Slack alerts configured and tested  
- ✅ Dependencies installed and verified  
- ✅ GitHub Actions workflow set up  
- ✅ API keys managed securely via `.env` and GitHub Secrets  
- ✅ Portfolio-ready Python automation project
