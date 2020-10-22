"""
Helper functions to display Player info in Jupyter Notebooks
"""
from blaseball_mike.models import SimulationData
from blaseball_reference.api import player_stats
from utils import *
from .general import _display_table
from matplotlib import pyplot

def display_vibes(player, day=None):
    if not day:
        day = SimulationData.load().day + 1

    vibe = player.get_vibe(day)
    print(vibe_to_string(vibe))

def display_season_vibes(player):
    days = range(1, 100)
    if isinstance(player, list):
        vibes = [mean([y.get_vibe(x) for y in player]) for x in days]
    else:
        vibes = [player.get_vibe(x) for x in days]

    pyplot.plot(days, vibes)
    pyplot.axline(xy1=(1, 0.8), slope=0, linestyle=":", color="#888")
    pyplot.axline(xy1=(1, 0.4), slope=0, linestyle=":", color="#888")
    pyplot.axline(xy1=(1, 0.1), slope=0, linestyle=":", color="#888")
    pyplot.axline(xy1=(1, -0.1), slope=0, linestyle=":", color="#888")
    pyplot.axline(xy1=(1, -0.4), slope=0, linestyle=":", color="#888")
    pyplot.axline(xy1=(1,-0.8), slope=0, linestyle=":", color="#888")
    pyplot.yticks(ticks=[0.9, 0.6, 0.25, 0, -0.25, -0.6, -0.9], labels=["Most Excellent", "Excellent", "Quality", "Neutral", "Less Than Ideal", "Far Less Than Ideal", "Honestly Terrible"])
    pyplot.xlabel("Day")
    pyplot.show()

def display_stars(values):
    header = ["Name", "Batting Stars", "Pitching Stars", "Baserunning Stars", "Defense Stars"]
    if not isinstance(values, (Player, list)):
        return

    if not isinstance(values, list):
        values = [values]

    _display_table(header,
                   [[x.name, x.batting_stars, x.pitching_stars, x.baserunning_stars, x.defense_stars] for x in values])

def display_batting_stats(values, season=None):
    header = ["Name", "PA", "AB", "H", "2B", "3B", "HR", "RBI", "BB", "SO", "BA", "BA/RISP", "OBP", "SLG", "OPS", "TB", "GDP", "SH"]
    if not isinstance(values, (Player, list)):
        return

    if isinstance(values, list):
        ids = [x.id for x in values]
    else:
        ids = values.id

    if season:
        season = season - 1

    ret = player_stats(ids, "batting", season)
    _display_table(header,
        [[x["player_name"], x["plate_appearances"], x["at_bats"], x["hits"], x["doubles"],
          x["triples"], x["home_runs"], x["runs_batted_in"], x["walks"], x["strikeouts"],
          x["batting_average"], x["batting_average_risp"], x["on_base_percentage"], x["slugging"], x["on_base_slugging"],
          x["total_bases"], x["gidps"], x["sacrifices"]]
         for x in ret])

def display_pitching_stats(values, season=None):
    header = ["Name", "ERA", "IP", "H", "R", "HR", "BB", "SO", "SO/9"]
    if not isinstance(values, (Player, list)):
        return

    if isinstance(values, list):
        ids = [x.id for x in values]
    else:
        ids = values.id

    if season:
        season = season - 1

    ret = player_stats(ids, "pitching", season)
    _display_table(header,
        [[x["player_id"], x["era"], x["innings"], x["hits_allowed"], x["runs_allowed"], x["hrs_allowed"], x["walks"],
          x["strikeouts"], x["k_per_9"]]
         for x in ret])

def display_batting_stlats(values):
    header = ["Name", "Batting Rating", "Divinity", "Martyrdom", "Moxie", "Musclitude", "Patheticism", "Thwackability"]
    if not isinstance(values, (Player, list)):
        return

    if not isinstance(values, list):
        values = [values]

    _display_table(header,
        [[x.name, x.hitting_rating, x.divinity, x.martyrdom, x.moxie, x.musclitude, x.patheticism, x.thwackability]
         for x in values])

def display_pitching_stlats(values):
    header = ["Name", "Pitching Rating", "Coldness", "Overpowerment", "Ruthlessness", "Shakespearianism", "Suppression", "Unthwackability", "Number of Fingers"]
    if not isinstance(values, (Player, list)):
        return

    if not isinstance(values, list):
        values = [values]

    _display_table(header,
        [[x.name, x.pitching_rating, x.coldness, x.overpowerment, x.ruthlessness, x.shakespearianism, x.suppression,
          x.unthwackability, x.total_fingers] for x in values])

def display_baserunning_stlats(values):
    header = ["Name", "Baserunning Rating", "Base Thirst", "Continuation", "Ground Friction", "Indulgence", "Laserlikeness"]
    if not isinstance(values, (Player, list)):
        return

    if not isinstance(values, list):
        values = [values]

    _display_table(header,
        [[x.name, x.baserunning_rating, x.base_thirst, x.continuation, x.ground_friction, x.indulgence, x.laserlikeness]
         for x in values])


def display_defense_stlats(values):
    header = ["Name", "Defense Rating", "Anticapitalism", "Chasiness", "Omniscience", "Tenaciousness", "Watchfulness"]
    if not isinstance(values, (Player, list)):
        return

    if not isinstance(values, list):
        values = [values]

    _display_table(header,
        [[x.name, x.defense_rating, x.anticapitalism, x.chasiness, x.omniscience, x.tenaciousness, x.watchfulness]
         for x in values])
