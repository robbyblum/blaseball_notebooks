import matplotlib.pyplot as pyplot
from matplotlib.transforms import Affine2D
import mpl_toolkits.axisartist.floating_axes as floating_axes
from mpl_toolkits.axisartist.grid_finder import MaxNLocator
from statistics import mean

BATTING_ATTRIBUTES = ["sight", "thwack", "ferocity"]
PITCHING_ATTRIBUTES = ["control", "stuff", "guile"]
DEFENSE_ATTRIBUTES = ["reach", "magnet", "reflex"]
RUNNING_ATTRIBUTES = ["hustle", "stealth", "dodge"]
VIBES_ATTRIBUTES = ["thrive", "survive", "drama"]


def recompute_ratings(table):
    table["batting_rating"] = table[BATTING_ATTRIBUTES].mean(axis=1)
    table["pitching_rating"] = table[PITCHING_ATTRIBUTES].mean(axis=1)
    table["running_rating"] = table[RUNNING_ATTRIBUTES].mean(axis=1)
    table["defense_rating"] = table[DEFENSE_ATTRIBUTES].mean(axis=1)
    table["vibes_rating"] = table[VIBES_ATTRIBUTES].mean(axis=1)
    table["overall_rating"] = table[["batting_rating", "pitching_rating", "running_rating",
                                     "defense_rating", "vibes_rating"]].mean(axis=1)


def boost_stats(table, stats, amount, players=None):
    if stats == 'overall':
        stats = BATTING_ATTRIBUTES + PITCHING_ATTRIBUTES + RUNNING_ATTRIBUTES + DEFENSE_ATTRIBUTES + VIBES_ATTRIBUTES
    elif stats == 'batting':
        stats = BATTING_ATTRIBUTES
    elif stats == 'pitching':
        stats = PITCHING_ATTRIBUTES
    elif stats == 'running':
        stats = RUNNING_ATTRIBUTES
    elif stats == 'defense':
        stats = DEFENSE_ATTRIBUTES
    elif stats == 'vibes':
        stats = VIBES_ATTRIBUTES

    if players is None:
        table[stats] += amount
    elif isinstance(players, str):
        table.loc[table['player_name'] == players, stats] += amount
    else:
        table.loc[table['player_name'].isin(players), stats] += amount
    recompute_ratings(table)


def get_stars(table):
    x = table[['player_name', 'overall_rating', 'batting_rating', 'pitching_rating', 'running_rating',
               'defense_rating', 'vibes_rating']].set_index("player_name")
    x[['overall_rating', 'batting_rating', 'pitching_rating', 'running_rating', 'defense_rating', 'vibes_rating']] *= 5
    return x


def get_batting_stlats(table, include_shadows=False):
    pos = ['LINEUP', ]
    if include_shadows:
        pos.append("SHADOWS")
    return table[table['position'].isin(pos)].sort_values(by=['position_index'])[['player_name', 'batting_rating'] + BATTING_ATTRIBUTES].set_index("player_name")


def get_pitching_stlats(table, include_shadows=False):
    pos = ['ROTATION', ]
    if include_shadows:
        pos.append("SHADOWS")
    return table[table['position'].isin(pos)].sort_values(by=['position_index'])[['player_name', 'pitching_rating'] + PITCHING_ATTRIBUTES].set_index("player_name")


def get_running_stlats(table, include_shadows=False):
    pos = ['LINEUP', ]
    if include_shadows:
        pos.append("SHADOWS")
    return table[table['position'].isin(pos)].sort_values(by=['position_index'])[['player_name', 'running_rating'] + RUNNING_ATTRIBUTES].set_index("player_name")


def get_defense_stlats(table, include_shadows=False):
    pos = ['LINEUP', ]
    if include_shadows:
        pos.append("SHADOWS")
    return table[table['position'].isin(pos)].sort_values(by=['position_index'])[['player_name', 'defense_rating'] + DEFENSE_ATTRIBUTES].set_index("player_name")


def plot_field_positions(table):
    t = table[table['position'] == "LINEUP"][['player_name', "location_x", "location_y"]]

    fig = pyplot.figure(figsize=(8, 8))
    r = Affine2D().rotate_deg(45)
    h = floating_axes.GridHelperCurveLinear(r, (0, 6, 0, 6), grid_locator1=MaxNLocator(nbins=7), grid_locator2=MaxNLocator(nbins=7))
    ax1 = fig.add_subplot(111, axes_class=floating_axes.FloatingAxes, grid_helper=h)
    ax1.axis["left"].toggle(ticklabels=False)
    ax1.axis["bottom"].toggle(ticklabels=False)
    aux_ax = ax1.get_aux_axes(r)
    for index, row in t.iterrows():
        aux_ax.annotate(row['player_name'], xy=(row['location_x']+0.5, row['location_y']+0.5), ha='center', va='center')
    pyplot.rc('grid', linestyle="-")
    pyplot.grid(True)

    return ax1
