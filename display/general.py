"""
Generic functions for displaying things in Jupyter Notebooks
"""

from blaseball_mike.models import Base, Player, Team
import pandas
from ipywidgets import *
import matplotlib

# The average stats of a rerolled player
NEW_PLAYER = {"batting": 2, "pitching": 1.5, "baserunning": 2.5, "defense": 2.5}

def _display_name(value):
    if isinstance(value, Player):
        print(value.name)
    elif isinstance(value, Team):
        print(value.full_name)

def display_name(values, pre="", post=""):
    if isinstance(values, list):
        print(pre)
        for x in values:
            _display_name(x)
        print(post)
    else:
        _display_name(pre, values, post)

def blaseball_to_pandas(values):
    """
    Convert Blaseball objects to Pandas Dataframes
    :param values: Blaseball-Mike object or list of Blaseball-Mike objects
    :return: pandas.DataFrame
    """
    if not values:
        return None

    if not isinstance(values, list):
        values = [values]

    if len(values) == 0:
        return None

    if isinstance(values[0], Base):
        return pandas.DataFrame([x.json() for x in values]).set_index("id")
    return None

def set_heatmap(table, maxVal=None, colormap="RdYlGn"):
    """
    Add a heatmap to a pandas DataFrame
    :param table: input TableDisplay
    :param maxVal: highest expected value
    :param: colormap: string matching a [matplotlib colormap](https://matplotlib.org/tutorials/colors/colormaps.html)
    :return:
    """

    table_style = table.style.background_gradient(colormap, vmin=0, vmax=maxVal, axis=None)

    # Handle inverted properties (patheticism/tragicness)
    reverse = matplotlib.cm.get_cmap(colormap).reversed()
    if 'Patheticism' in table:
        table_style = table_style.background_gradient(reverse, vmin=0, vmax=maxVal, subset='Patheticism', axis=None)
    if 'Tragicness' in table:
        table_style = table_style.background_gradient(reverse, vmin=0, vmax=maxVal, subset='Tragicness', axis=None)

    return table_style

# Various Helper Functions
def vibe_to_string(vibe):
    if vibe > 0.8:
        vibe_str = "▲▲▲ Most Excellent"
    elif vibe > 0.4:
        vibe_str = "▲▲ Excellent"
    elif vibe > 0.1:
        vibe_str = "▲ Quality"
    elif vibe > -0.1:
        vibe_str = "⬌ Neutral"
    elif vibe > -0.4:
        vibe_str = "▼ Less Than Ideal"
    elif vibe > -0.8:
        vibe_str = "▼▼ Far Less Than Ideal"
    else:
        vibe_str = "▼▼▼ Honestly Terrible"
    return vibe_str

def vibe_to_color(vibe):
    if vibe > 0.8:
        vibe_str = "#15d400"
    elif vibe > 0.4:
        vibe_str = "#5de04f"
    elif vibe > 0.1:
        vibe_str = "#8fdb88"
    elif vibe > -0.1:
        vibe_str = "#d1d1d1"
    elif vibe > -0.4:
        vibe_str = "#d97373"
    elif vibe > -0.8:
        vibe_str = "#de3c3c"
    else:
        vibe_str = "#e00000"
    return vibe_str

def stars_to_string(stars):
    star_str = "★" * int(stars)
    if stars % 1 != 0:
        star_str += "☆"
    return star_str

def parse_emoji(val):
    try:
        return chr(int(val, 16))
    except ValueError:
        return val

def get_game_by_team(games, team):
    if isinstance(games, dict):
        games = games.values()
    games = [x for x in games if x._away_team_id == team.id or x._home_team_id == team.id]
    if len(games) == 0:
        return None
    return games[0]