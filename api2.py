import requests_cache

CHRON_URL = "https://api2.sibr.dev/chronicler/v0"
API_URL = "https://api2.blaseball.com"

_SESSIONS_BY_EXPIRY = {}


def session(expiry=0):
    """Get a caching HTTP session"""
    if expiry not in _SESSIONS_BY_EXPIRY:
        _SESSIONS_BY_EXPIRY[expiry] = requests_cache.CachedSession(backend="memory", expire_after=expiry)
    return _SESSIONS_BY_EXPIRY[expiry]


def _api_get(url, expiry=60):
    x = session(expiry).get(url)
    x.raise_for_status()
    return x.json()


def get_sim():
    return _api_get(f"{API_URL}/sim", expiry=360)


def get_all_teams():
    return [x["data"] for x in _api_get(f"{CHRON_URL}/entities?kind=team", expiry=120)["items"]]


def get_team(team_id):
    x = [x for x in get_all_teams() if x["id"] == team_id]
    if len(x) > 0:
        return x[0]
    return {}


def get_all_players():
    return [x["data"] for x in _api_get(f"{CHRON_URL}/entities?kind=player", expiry=120)["items"]]


def get_player(player_id):
    x = [x for x in get_all_players() if x["id"] == player_id]
    if len(x) > 0:
        return x[0]
    return {}

