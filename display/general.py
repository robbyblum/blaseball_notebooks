"""
Generic functions for displaying things in Jupyter Notebooks
"""

import pandas
import matplotlib

class HTMLWrapper():
    """For some reason IPython's HTML wrapper is busted, make our own"""
    def __init__(self, html_string):
        self.html = html_string

    def _repr_html_(self):
        return self.html


def set_heatmap(table, maxVal=None, colormap="RdYlGn"):
    """
    Add a heatmap to a pandas DataFrame
    :param table: input TableDisplay
    :param maxVal: highest expected value
    :param: colormap: string matching a [matplotlib colormap](https://matplotlib.org/tutorials/colors/colormaps.html)
    :return: output TableDisplay
    """

    table_style = table.style.background_gradient(colormap, vmin=0, vmax=maxVal, axis=None)
    return table_style


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
    elif index == 0:  # PEANUT
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

    return HTMLWrapper(f'<div style="{style_font};{style_extra}">{html_str}</div>')
