# ⚡ Weather Alert Bot

**Developer:** Bryant James Mingoy  
**Test Project:** Weather Alert Bot  

---

## 1️⃣ __Project Overview__

This Python bot monitors New York City weather and performs the following tasks:

- 🌤 Fetch real-time weather from OpenWeatherMap API (free tier)  
- 📊 Log hourly or on-demand forecasts to Google Sheets  
- 📢 Send Slack alerts for snow or storm conditions  

**Purpose:** Showcase Python automation, logging, and alerting skills.

---

## 2️⃣ __Repository Structure__

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

**Google Sheet:**  
[View Weather Alert Data Sheet](https://docs.google.com/spreadsheets/d/1oS-NxBStujxZwpABxfBMpu_DWZ4Nj653yx6v0W52qV0/edit?gid=0)

> ⚠️ Anyone with this link can view the sheet. Contact the project owner if you need edit access.

**Columns:**

1. 📝 Log – Internal ID / timestamp  
2. 📅 Forecasted Time – Date & time of forecast  
3. 🌡 Temp (°C) – Temperature  
4. ⛅ Conditions – Weather description (Clear, Snow, etc.)  
5. 🌬 Wind (m/s) – Wind speed  
6. ❄ Precip (%) – Chance of precipitation  
7. 🔄 Run Type – Scheduled vs Manual  

**Features:**

- Conditional formatting highlights severe weather  
- Clean layout for quick scanning  
- Supports hourly and manual runs  

---

## 4️⃣ __Slack Alerts__

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

## 5️⃣ __Setup Instructions__

**Step 1 – Clone the Repository**
```bash
git clone https://github.com/<USERNAME>/<REPO>.git
cd weather-alert-bot
```

**Step 2 – Create & Activate Virtual Environment**
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

**Step 3 – Install Dependencies**
```bash
pip install -r requirements.txt
```

**Step 4 – Configure API Keys**

1. Copy `.env.example` → `.env`  
2. Add your API keys:

```
OPENWEATHER_API_KEY=your_key_here
GOOGLE_SHEETS_KEY=your_key_here
SLACK_WEBHOOK_URL=your_url_here
```

> 🔒 `.env` must not be committed. `.env.example` is safe to include.

---

## 6️⃣ __Running the Bot__

```bash
python main.py
```

- Fetches weather data  
- Logs to Google Sheets  
- Sends Slack alerts if thresholds are met  

> ⏰ Hourly automation possible with Python `schedule` or GitHub Actions.

---

## 7️⃣ __Dependencies__

- requests>=2.31.0  
- gspread>=6.2.1  
- google-auth>=2.23.0  
- google-auth-oauthlib>=1.1.0  
- google-auth-httplib2>=0.1.0  
- python-dotenv>=1.0.0  
- pytz>=2025.2  
- schedule>=1.2.0  

---

## 8️⃣ __GitHub Secrets Setup__

To run the workflow securely, configure GitHub Secrets:

1. Go to **Settings → Secrets and variables → Actions → New repository secret**  
2. Add the following:

    | Secret Name             | Description                                 |
    |-------------------------|---------------------------------------------|
    | OPENWEATHER_API_KEY      | OpenWeatherMap API key                      |
    | GOOGLE_SHEETS_KEY        | Google Sheets API service account key      |
    | SLACK_WEBHOOK_URL        | Slack webhook URL for alerts                |

3. Test the workflow by going to **Actions → Weather Alert Bot → Run workflow**  

    - Google Sheets should receive new logs  
    - Slack should receive alerts if weather threshold is met  

---

## 9️⃣ __Project Summary__

- ✅ Google Sheets logging implemented and formatted  
- ✅ Slack alerts configured and logic verified  
- ✅ Dependencies installed and verified  
- ✅ GitHub Actions workflow set up  
- ✅ API keys managed via `.env` locally and GitHub Secrets  
- ✅ Project ready for local execution and portfolio showcase
