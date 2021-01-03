"""
Generic functions for displaying things in Jupyter Notebooks
"""

from blaseball_mike.models import Base, Player, Team
import pandas
from beakerx import ThreeColorHeatmapHighlighter, HighlightStyle, EasyForm
from ipywidgets import *

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

def player_gen_UI(form_name, tag_name):
    """
    Generate a UI Form for modifying replacement player stars
    :param form_name: Name of form
    :param tag_name: Tag of jupyter notebook cell to update
    :return: beakerx EasyForm
    """
    batting = FloatSlider(value=NEW_PLAYER["batting"], min=0.0, max=5.0, description="Batting Stars:")
    pitching = FloatSlider(value=NEW_PLAYER["pitching"], min=0.0, max=5.0, description="Pitching Stars:")
    baserunning = FloatSlider(value=NEW_PLAYER["baserunning"],min=0.0, max=5.0, description="Baserunning Stars:")
    defense = FloatSlider(value=NEW_PLAYER["defense"],min=0.0, max=5.0, description="Defense Stars:")

    form = EasyForm(form_name)
    form.addWidget("batting", batting)
    form.addWidget("pitching", pitching)
    form.addWidget("baserunning", baserunning)
    form.addWidget("defense", defense)
    form.addButton("Update", tag=tag_name)
    return form


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

def set_heatmap(table, maxVal=None):
    """
    Add a heatmap to a beakerx TableDisplay
    :param table: input TableDisplay
    :param maxVal: highest expected value
    :return:
    """
    goodColor = "#74d8b4"
    midColor = "#ffdac1"
    badColor = "#ff4857"

    for column in table.chart.columnNames:
        if column.lower() in ("patheticism", "tragicness"):
            maxC = badColor
            minC = goodColor
        else:
            maxC = goodColor
            minC = badColor

        if maxVal:
            midVal = maxVal/2
        else:
            midVal = None

        table.addCellHighlighter(ThreeColorHeatmapHighlighter(column, style=HighlightStyle.SINGLE_COLUMN, minVal=0, midVal=midVal, maxVal=maxVal, maxColor=maxC, midColor=midColor, minColor=minC))
    return table


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