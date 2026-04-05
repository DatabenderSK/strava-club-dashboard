"""Central configuration loaded from .env file."""
import os
from dotenv import load_dotenv

load_dotenv()

# Required — Strava API
STRAVA_CLIENT_ID = os.environ["STRAVA_CLIENT_ID"]
STRAVA_CLIENT_SECRET = os.environ["STRAVA_CLIENT_SECRET"]
STRAVA_REFRESH_TOKEN = os.environ["STRAVA_REFRESH_TOKEN"]
STRAVA_CLUB_ID = os.getenv("STRAVA_CLUB_ID", "")

# Optional — Dashboard customization
CLUB_NAME = os.getenv("CLUB_NAME", "My Cycling Club")
WEATHER_LAT = os.getenv("WEATHER_LAT", "40.71")
WEATHER_LON = os.getenv("WEATHER_LON", "-74.01")
TIMEZONE = os.getenv("TIMEZONE", "America/New_York")
