# Strava Club Dashboard

Free, open-source weekly statistics dashboard for any Strava cycling club. Auto-updates every hour via GitHub Actions, hosted free on GitHub Pages.

**Features:**
- Weekly leaderboard with 20+ metrics (distance, elevation, speed, time...)
- Awards: Distance King, Climbing King, Marathoner, Fastest, Mountain Goat...
- Fun stats: Virtual Cyclist, E-Biker, Break King
- Device stats across the club
- Outdoor/Indoor activity filter
- Week history archive with visual picker
- Local weather widget
- Fully responsive (mobile + desktop)
- No database needed — JSON file storage

**[Live Demo](https://kcmi.sk/strava/)** — see it in action for Klub cyklistov Michalovce (Slovak cycling club)

---

## Quick Start (5 minutes)

### 1. Create a Strava API Application

1. Go to [strava.com/settings/api](https://www.strava.com/settings/api)
2. Create a new application:
   - **Application Name:** anything (e.g. "My Club Dashboard")
   - **Category:** Club
   - **Website:** your GitHub Pages URL (or just `http://localhost`)
   - **Authorization Callback Domain:** `localhost`
3. Note your **Client ID** and **Client Secret**

### 2. Get Your Refresh Token

```bash
# Clone this repo
git clone https://github.com/DatabenderSK/strava-club-dashboard.git
cd strava-club-dashboard

# Install dependencies
pip install -r requirements.txt

# Run the setup wizard
python3 setup_strava.py
```

The wizard will:
1. Ask for your Client ID and Client Secret
2. Give you a URL to open in your browser
3. You authorize the app on Strava
4. Your browser redirects to `localhost` (page won't load — that's expected!)
5. Copy the full URL from your browser and paste it back
6. You get your `STRAVA_REFRESH_TOKEN`

### 3. Find Your Club ID

Open your Strava club page. The URL looks like:
```
https://www.strava.com/clubs/123456
                             ^^^^^^ this is your CLUB_ID
```

### 4. Configure

Copy the example config and fill in your values:

```bash
cp env.example .env
```

Edit `.env`:
```env
STRAVA_CLIENT_ID=your_id
STRAVA_CLIENT_SECRET=your_secret
STRAVA_REFRESH_TOKEN=your_token
STRAVA_CLUB_ID=123456
CLUB_NAME=My Cycling Club
WEATHER_LAT=48.75
WEATHER_LON=21.92
TIMEZONE=Europe/Bratislava
```

### 5. Generate Your Dashboard

```bash
python3 generate.py
```

Open `dashboard/index.html` in your browser. Done!

---

## Auto-Update with GitHub Actions + GitHub Pages (Free Hosting)

### Set Up Secrets

In your GitHub repo, go to **Settings → Secrets and variables → Actions** and add:

| Secret | Value |
|--------|-------|
| `STRAVA_CLIENT_ID` | Your Strava app Client ID |
| `STRAVA_CLIENT_SECRET` | Your Strava app Client Secret |
| `STRAVA_REFRESH_TOKEN` | Token from setup wizard |
| `STRAVA_CLUB_ID` | Your club ID number |
| `CLUB_NAME` | Your club name (optional) |
| `WEATHER_LAT` | Latitude for weather (optional) |
| `WEATHER_LON` | Longitude for weather (optional) |
| `TIMEZONE` | Your timezone (optional, default: America/New_York) |

### Enable GitHub Pages

1. Go to **Settings → Pages**
2. Source: **Deploy from a branch**
3. Branch: `main`, folder: `/dashboard`
4. Save

Your dashboard will be live at `https://yourusername.github.io/strava-club-dashboard/`

The GitHub Action runs every hour and auto-commits updated data.

---

## Customization

### Language / Localization

The dashboard is in English by default. To translate it to your language, you can simply ask an AI assistant:

> "Translate all UI text in `generate.py` to Czech/Slovak/German/Spanish/..."

All translatable strings are in one place inside the `TEMPLATE` variable in `generate.py` — the JavaScript constants `AWARDS`, `FUN`, `EMPTY_MSGS`, button labels, and section titles.

### Colors

The accent color is Strava orange (`#FC4C02`). Search and replace in the `TEMPLATE` CSS to change it.

### Weather Location

Find your coordinates at [latlong.net](https://www.latlong.net/) and set `WEATHER_LAT` / `WEATHER_LON` in `.env`. Weather data comes from [Open-Meteo](https://open-meteo.com/) (free, no API key needed).

---

## How It Works

```
Strava API
    ↓
strava_client.py      → OAuth token refresh + fetch activities/members
    ↓
report_generator.py   → Compute 20+ statistics, awards, leaderboard
    ↓
generate.py           → Inject data into HTML template
    ↓
dashboard/index.html  → Static file, open in any browser
dashboard/history/    → Weekly JSON snapshots (auto-archived)
```

**Key design decisions:**
- **No server needed** — generates a single static HTML file
- **No database** — weekly history stored as JSON files
- **E-bike fair play** — awards exclude e-bike rides (tracked separately)
- **Rate limit friendly** — uses ~4 API calls per run (Strava allows 1000/day)

---

## File Structure

```
├── generate.py           # Main script — generates the dashboard
├── strava_client.py      # Strava API client (OAuth + data fetch)
├── report_generator.py   # Statistics engine (all computations)
├── config.py             # Configuration from .env
├── setup_strava.py       # One-time OAuth setup wizard
├── requirements.txt      # Python dependencies
├── env.example           # Example .env file
├── dashboard/            # OUTPUT — generated files
│   ├── index.html        # The dashboard (don't edit manually!)
│   └── history/          # Weekly JSON snapshots
└── .github/workflows/
    └── update.yml        # Hourly auto-update via GitHub Actions
```

---

## Requirements

- Python 3.9+
- A Strava account that's a member of the club
- The club must be set to allow member activity visibility

---

## Troubleshooting

**"401 Unauthorized" from Strava**
→ Your refresh token may have expired. Run `python3 setup_strava.py` again.

**Empty dashboard (no activities)**
→ Check that your club has activities this week. The dashboard shows Monday–Sunday.

**Weather not showing**
→ Check your `WEATHER_LAT`/`WEATHER_LON` values. Weather is optional — the dashboard works without it.

**GitHub Actions not running**
→ Make sure all required secrets are set. Check the Actions tab for error logs.

---

## License

MIT — use it for your club, modify it, share it.

---

Built with data from [Strava API](https://developers.strava.com/) and weather from [Open-Meteo](https://open-meteo.com/).
