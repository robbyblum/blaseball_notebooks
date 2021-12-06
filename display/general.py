"""
Generic functions for displaying things in Jupyter Notebooks
"""

from blaseball_mike.models import Base, Player, Team, Stadium, Modification
import pandas
import matplotlib

# The average stats of a rerolled player
NEW_PLAYER = {"batting": 2, "pitching": 1.5, "baserunning": 2.5, "defense": 2.5}


class HTMLWrapper():
    """For some reason IPython's HTML wrapper is busted, make our own"""
    def __init__(self, html_string):
        self.html = html_string

    def _repr_html_(self):
        return self.html


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


def has_mods(values, mods, mod_type="permanent"):
    """
    Filter a list of Players/Teams/Stadiums that have certain Modifications

    :param values: Player, Team, Stadium, or list/dictionary of Players/Teams/Stadiums
    :param mods: Modification, String ID of Modification, or list or Modifications/Strings
    :param mod_type: type of mod to check against (permanent, seasonal, weekly, game, item)
    :return: list of filtered objects
    """

    if not isinstance(values, (Player, Team, list, dict)):
        return

    if isinstance(values, (Player, Team, Stadium)):
        values = [values]
    elif isinstance(values, dict):
        values = list(values.values())

    fields = None
    if isinstance(values[0], Stadium):
        fields = "_mods_ids"
    elif mod_type.lower() == "permanent":
        fields = "_perm_attr_ids"
    elif mod_type.lower() == "seasonal":
        fields = "_seas_attr_ids"
    elif mod_type.lower() == "weekly":
        fields = "_week_attr_ids"
    elif mod_type.lower() == "game":
        fields = "_game_attr_ids"
    elif mod_type.lower() == "item" and isinstance(values[0], Player):
        fields = "_item_attr_ids"

    if fields is None:
        raise ValueError(f"Invalid mod_type \"{mod_type}\" for object \"{type(values[0])}\"")

    if isinstance(mods, (str, Modification)):
        mods = [mods]

    if isinstance(mods[0], Modification):
        mods = [x.id for x in mods]

    return [x for x in values if any(mod in mods for mod in getattr(x, fields, list()))]


def set_heatmap(table, maxVal=None, colormap="RdYlGn"):
    """
    Add a heatmap to a pandas DataFrame
    :param table: input TableDisplay
    :param maxVal: highest expected value
    :param: colormap: string matching a [matplotlib colormap](https://matplotlib.org/tutorials/colors/colormaps.html)
    :return: output TableDisplay
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


def god_text(html_str, index):
    style_extra = ""
    style_font = "font-family: 'Lora', 'Courier New', monospace, serif;font-weight: 700"
    if index == -1:   # EMERGENCY ALERT
        style_extra = "font-style:italic;color:#000"
    elif index == 0:    # PEANUT
        style_extra = "color:red"
    elif index == 1:  # SQUID
        style_extra = "color:#5988ff;text-shadow:0 0 20px #5988ff"
    elif index == 2:  # COIN
        style_extra = "color:#ffbe00"
    elif index == 3:  # READER
        style_extra = "color:#a16dc3;text-shadow:0 0 10px #a16dc3"
    elif index == 4:  # Microphone
        style_font = "font-family:'Open Sans','Helvetica Neue',sans-serif;font-weight:400"
        style_extra = "color:#000"
    elif index == 5:  # Lootcrates
        style_extra = "font-style:italic;color:#626262"
    elif index == 6:  # Namerifeht
        style_extra = "color:#ea5b23;-webkit-transform:scaleX(-1);transform:scaleX(-1)"

    return HTMLWrapper(f'<div style="text-align:center;{style_font};{style_extra}">{html_str}</div>')
