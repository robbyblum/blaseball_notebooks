"""
Helper functions to display things nicely in Jupyter Notebooks
"""
from blaseball_mike.models import Player, Team


def _display_name(value):
    if isinstance(value, Player):
        print(value.name)
    elif isinstance(value, Team):
        print(value.full_name)

def display_name(values):
    if isinstance(values, list):
        for x in values:
            _display_name(x)
    else:
        _display_name(values)