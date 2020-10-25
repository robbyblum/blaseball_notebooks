"""
Helper functions to display things nicely in Jupyter Notebooks
"""
from blaseball_mike.models import Player, Team
from IPython.display import HTML, display
import tabulate

def _display_table(header, table):
    display(HTML(tabulate.tabulate(table, headers=header, tablefmt='html')))

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