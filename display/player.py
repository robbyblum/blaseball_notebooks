import pandas
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
    table["overall_rating"] = table[["batting_rating", "pitching_rating", "running_rating", "defense_rating", "vibes_rating"]].mean(axis=1)


def boost_stats(table, stats, amount):
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
    table[stats] += amount
    recompute_ratings(table)


def get_stars(table):
    x = table[['player_name', 'overall_rating', 'batting_rating', 'pitching_rating', 'running_rating', 'defense_rating', 'vibes_rating']].set_index("player_name")
    x[['overall_rating', 'batting_rating', 'pitching_rating', 'running_rating', 'defense_rating', 'vibes_rating']] *= 5
    return x


def get_batting_stlats(table):
    return table[table['position'] == "LINEUP"].sort_values(by=['position_index'])[['player_name', 'batting_rating'] + BATTING_ATTRIBUTES].set_index("player_name")


def get_pitching_stlats(table):
    return table[table['position'] == "ROTATION"].sort_values(by=['position_index'])[['player_name', 'pitching_rating'] + PITCHING_ATTRIBUTES].set_index("player_name")


def get_running_stlats(table):
    return table[table['position'] == "LINEUP"].sort_values(by=['position_index'])[['player_name', 'running_rating'] + RUNNING_ATTRIBUTES].set_index("player_name")


def get_defense_stlats(table):
    return table[table['position'] == "LINEUP"].sort_values(by=['position_index'])[['player_name', 'defense_rating'] + DEFENSE_ATTRIBUTES].set_index("player_name")