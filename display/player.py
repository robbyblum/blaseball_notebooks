"""
Helper functions to display Player info in Junyper Notebooks
"""
from blaseball_mike.models import SimulationData
from IPython.display import HTML, display
import tabulate
from utils import *
from matplotlib import pyplot

def display_stars(values):
    header = ["Name", "Batting Stars", "Pitching Stars", "Baserunning Stars", "Defense Stars"]
    if not isinstance(values, (Player, list)):
        return

    if isinstance(values, list):
        display(HTML(tabulate.tabulate(
            [[x.name, x.batting_stars, x.pitching_stars, x.baserunning_stars, x.defense_stars] for x in values],
            headers=header, tablefmt='html')))
    else:
        display(HTML(tabulate.tabulate(
            [[values.name, values.batting_stars, values.pitching_stars, values.batting_stars, values.defense_stars]],
            headers=header, tablefmt='html')))

def display_vibes(player, day=None):
    if not day:
        day = SimulationData.load().day + 1

    vibe = player.get_vibe(day)
    print(vibe_to_string(vibe))

def display_season_vibes(player):
    # TODO: list of players & average
    days = range(1, 100)
    vibes = [player.get_vibe(x) for x in days]

    pyplot.plot(days, vibes)
    pyplot.axline(xy1=(1, 0.1), slope=0)
    pyplot.axline(xy1=(1,-0.1), slope=0)
    pyplot.xlabel("Day")
    pyplot.ylabel("Vibe")
    pyplot.show()

# STLAT DISPLAYS

def display_batting_stlats(values):
    header = ["Name", "Batting Rating", "Divinity", "Martyrdom", "Moxie", "Musclitude", "Patheticism", "Thwackability"]
    if not isinstance(values, (Player, list)):
        return

    if isinstance(values, list):
        display(HTML(tabulate.tabulate(
            [[x.name, x.hitting_rating, x.divinity, x.martyrdom, x.moxie, x.musclitude, x.patheticism, x.thwackability] for x in values],
            headers=header, tablefmt='html')))
    else:
        display(HTML(tabulate.tabulate(
            [[values.name, values.hitting_rating, values.divinity, values.martyrdom, values.moxie, values.musclitude, values.patheticism, values.thwackability]],
            headers=header, tablefmt='html')))

def display_pitching_stlats(values):
    header = ["Name", "Pitching Rating", "Coldness", "Overpowerment", "Ruthlessness", "Shakespearianism", "Suppression", "Unthwackability", "Number of Fingers"]
    if not isinstance(values, (Player, list)):
        return

    if isinstance(values, list):
        display(HTML(tabulate.tabulate(
            [[x.name, x.pitching_rating, x.coldness, x.overpowerment, x.ruthlessness, x.shakespearianism, x.suppression, x.unthwackability, x.total_fingers] for x in values],
            headers=header, tablefmt='html')))
    else:
        display(HTML(tabulate.tabulate(
            [[values.name, values.pitching_rating, values.coldness, values.overpowerment, values.ruthlessness, values.shakespearianism, values.suppression, values.unthwackability, values.total_fingers]],
            headers=header, tablefmt='html')))

def display_baserunning_stlats(values):
    header = ["Name", "Baserunning Rating", "Base Thirst", "Continuation", "Ground Friction", "Indulgence", "Laserlikeness"]
    if not isinstance(values, (Player, list)):
        return

    if isinstance(values, list):
        display(HTML(tabulate.tabulate(
            [[x.name, x.baserunning_rating, x.base_thirst, x.continuation, x.ground_friction, x.indulgence, x.laserlikeness] for x in values],
            headers=header, tablefmt='html')))
    else:
        display(HTML(tabulate.tabulate(
            [[values.name, values.baserunning_rating, values.base_thirst, values.continuation, values.ground_friction, values.indulgence, values.laserlikeness]],
            headers=header, tablefmt='html')))

def display_defense_stlats(values):
    header = ["Name", "Defense Rating", "Anticapitalism", "Chasiness", "Omniscience", "Tenaciousness", "Watchfulness"]
    if not isinstance(values, (Player, list)):
        return

    if isinstance(values, list):
        display(HTML(tabulate.tabulate(
            [[x.name, x.defense_rating, x.anticapitalism, x.chasiness, x.omniscience, x.tenaciousness, x.watchfulness] for x in values],
            headers=header, tablefmt='html')))
    else:
        display(HTML(tabulate.tabulate(
            [[values.name, values.defense_rating, values.anticapitalism, values.chasiness, values.omniscience, values.tenaciousness, values.watchfulness]],
            headers=header, tablefmt='html')))
