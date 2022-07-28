## TEAM DISPLAY

from blaseball_mike.models import League

def league_teams():
    """
    Get list of all league teams
    """
    return League.load().teams
