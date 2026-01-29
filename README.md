# ⚡🌤 Weather Alert Bot

**Developer:** Bryant James Mingoy
**Project:** Weather Alert Bot  

---

## 🏷️ Badges

![Python](https://img.shields.io/badge/python-3.11-blue)  
![Workflow](https://github.com/<USERNAME>/<REPO>/actions/workflows/main.yml/badge.svg)  
![Slack](https://img.shields.io/badge/slack-alerts-green)  
![Google Sheets](https://img.shields.io/badge/google-sheets-ready-blue)  
![Status](https://img.shields.io/badge/status-ready-brightgreen)

---

## 📌 1️⃣ Project Overview

This Python bot monitors **New York City weather** and performs:  

- 🌤 **Fetch** real-time weather from **OpenWeatherMap API (free tier)**  
- 📊 **Log** hourly or on-demand forecasts to **Google Sheets**  
- 📢 **Alert** via Slack for snow or storm conditions  

**Purpose:** Showcase Python automation, logging, and alerting skills.

---

## 🗂 2️⃣ Repository Structure

```
weather-alert-bot/
├── main.py                 # Main Python script
├── specifications.md       # Project specifications
├── requirements.txt        # Dependencies
├── .env.example            # Template for API keys
├── .gitignore              # Ignore sensitive files
└── .github/
    └── workflows/          # GitHub Actions workflow
        └── main.yml
```

---

## 📊 3️⃣ Google Sheet Logging

**Columns:**  

1. **Log** – Internal ID / timestamp  
2. **Forecasted Time** – Date & time of forecast  
3. **Temp (°C)** – Temperature  
4. **Conditions** – Weather description (Clear, Snow, etc.)  
5. **Wind (m/s)** – Wind speed  
6. **Precip (%)** – Chance of precipitation  
7. **Run Type** – Scheduled vs Manual  

**Features:**  

- 🔹 Conditional formatting highlights severe weather  
- 🔹 Clean layout for quick scanning  
- 🔹 Supports hourly and manual runs  

---

## 🛎 4️⃣ Slack Alerts

**Example message:**

```
NYC Weather Alert
Light Snow expected on Tuesday, 27 January 2026 at 09:00 PM at 21.5°F.
Wind: 6 m/s | chance of snow: 20%.
Safety Reminder: Please drive carefully; roads may be slippery.
```

- Alerts triggered only when snow or storm thresholds are met  
- Can test with simulated weather data  

---

## 🏗 5️⃣ Setup Instructions

### 📥 Step 1 – Clone the Repository
```
git clone https://github.com/<USERNAME>/<REPO>.git
cd weather-alert-bot
```

### 🛠 Step 2 – Create & Activate Virtual Environment
```
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

### 📦 Step 3 – Install Dependencies
```
pip install -r requirements.txt
```

### 🔑 Step 4 – Configure API Keys
1. Copy `.env.example` → `.env`  
2. Add your actual API keys:
```
OPENWEATHER_API_KEY=your_key_here
GOOGLE_SHEETS_KEY=your_key_here
SLACK_WEBHOOK_URL=your_url_here
```

> ⚠️ `.env` **must not** be committed. `.env.example` is safe to include.

---

## ▶️ 6️⃣ Running the Bot

```
python main.py
```

- Fetches weather data  
- Logs to Google Sheets  
- Sends Slack alerts if thresholds are met  

> ⏰ Hourly automation possible with Python `schedule` or GitHub Actions.

---

## 📚 7️⃣ Dependencies

- `requests>=2.31.0` – API requests  
- `gspread>=6.2.1` – Google Sheets integration  
- `google-auth>=2.23.0` – Google API auth  
- `google-auth-oauthlib>=1.1.0` – OAuth2 support  
- `google-auth-httplib2>=0.1.0` – HTTP transport  
- `python-dotenv>=1.0.0` – Manage environment variables  
- `pytz>=2025.2` – Timezone support  
- `schedule>=1.2.0` – Optional scheduling library  

---

## 📝 8️⃣ Notes

- 🔒 Keep API keys in `.env`  
- 📄 `.env.example` provided as template  
- ✅ Dependencies verified in a clean virtual environment  

---

## 🔐 9️⃣ GitHub Secrets Setup

To run the workflow and keep your API keys secure, configure **GitHub Secrets**:  

### 1️⃣ Go to Your Repository Settings
1. Open your GitHub repo in a browser  
2. Click on **Settings** → **Secrets and variables** → **Actions** → **New repository secret**

### 2️⃣ Add the Following Secrets
| Secret Name             | Description                                 |
|-------------------------|---------------------------------------------|
| `OPENWEATHER_API_KEY`   | Your OpenWeatherMap API key                 |
| `GOOGLE_SHEETS_KEY`     | Google Sheets API service account key       |
| `SLACK_WEBHOOK_URL`     | Slack webhook URL for alerts                |

> ⚠️ Keep the **exact names** as above – the workflow references these names.

### 3️⃣ Test the Setup
1. Go to **Actions** → **Weather Alert Bot** workflow  
2. Click **Run workflow** → choose `main` branch → **Run workflow**  
3. Verify:
   - Google Sheets receives new logs  
   - Slack receives alerts (if weather threshold met)  

> Once this is set, your workflow will run **hourly** automatically and the **workflow badge** will reflect the run status.

---

## 🟢 10️⃣ Project Status

- ✅ Google Sheets logging implemented and visually formatted  
- ✅ Slack alerts configured and logic verified  
- ✅ Dependencies installed and verified in a virtual environment  
- ✅ GitHub Actions workflow set up for hourly automation  
- ✅ API keys securely managed via `.env` locally and GitHub Secrets  
- ✅ Project ready for local execution and portfolio showcase
