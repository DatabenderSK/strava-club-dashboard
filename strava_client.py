"""Strava OAuth token refresh + club API calls."""
import requests
import config


class StravaAuthError(Exception):
    """Raised when Strava authentication fails."""


TOKEN_URL = "https://www.strava.com/oauth/token"
CLUB_ACTIVITIES_URL = "https://www.strava.com/api/v3/clubs/{club_id}/activities"
CLUB_MEMBERS_URL = "https://www.strava.com/api/v3/clubs/{club_id}/members"


def get_access_token() -> str:
    """Exchange refresh token for a fresh access token."""
    try:
        resp = requests.post(TOKEN_URL, data={
            "client_id": config.STRAVA_CLIENT_ID,
            "client_secret": config.STRAVA_CLIENT_SECRET,
            "refresh_token": config.STRAVA_REFRESH_TOKEN,
            "grant_type": "refresh_token",
        }, timeout=15)
    except requests.RequestException as e:
        raise StravaAuthError(f"Network error connecting to Strava: {e}")

    if resp.status_code == 400:
        raise StravaAuthError(
            "Strava returned 400 — refresh token is likely expired or invalid.\n"
            "Fix: run 'python3 setup_strava.py' to get a new token,\n"
            "then update STRAVA_REFRESH_TOKEN in GitHub Secrets."
        )
    if resp.status_code == 401:
        raise StravaAuthError(
            "Strava returned 401 — client ID or secret is incorrect.\n"
            "Check STRAVA_CLIENT_ID and STRAVA_CLIENT_SECRET."
        )
    if not resp.ok:
        raise StravaAuthError(f"Strava auth failed: {resp.status_code} {resp.text}")

    return resp.json()["access_token"]


def fetch_club_activities(access_token: str, after: int = None, per_page: int = 200) -> list:
    """
    Fetch club activities with pagination.
    after: Unix timestamp — only return activities newer than this time.
    """
    url = CLUB_ACTIVITIES_URL.format(club_id=config.STRAVA_CLUB_ID)
    headers = {"Authorization": f"Bearer {access_token}"}
    activities = []
    page = 1

    while True:
        params = {"per_page": per_page, "page": page}
        if after:
            params["after"] = after
        resp = requests.get(url, headers=headers, params=params, timeout=15)
        resp.raise_for_status()
        batch = resp.json()
        if not batch:
            break
        activities.extend(batch)
        if len(batch) < per_page:
            break
        page += 1

    return activities


def fetch_club_members(access_token: str) -> list:
    """Fetch club member list (firstname, lastname, id)."""
    url = CLUB_MEMBERS_URL.format(club_id=config.STRAVA_CLUB_ID)
    headers = {"Authorization": f"Bearer {access_token}"}
    members = []
    page = 1

    while True:
        resp = requests.get(url, headers=headers,
                            params={"per_page": 200, "page": page}, timeout=15)
        resp.raise_for_status()
        batch = resp.json()
        if not batch:
            break
        members.extend(batch)
        if len(batch) < 200:
            break
        page += 1

    return members
