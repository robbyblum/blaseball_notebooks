from blaseball_mike.models import Base, Player
import pandas

# The average stats of a rerolled player
NEW_PLAYER = {"batting": 2, "pitching": 1.5, "baserunning": 2.5, "defense": 2.5}

# Teams that cannot be the targets or recipients of blessings
INVALID_TEAMS = {"Hall Stars": "c6c01051-cdd4-47d6-8a98-bb5b754f937f",
                 "Baltimore Crabs": "8d87c468-699a-47a8-b40d-cfb73a5660ad",
                 "The Shelled One's Pods": "40b9ec2a-cb43-4dbb-b836-5accb62e7c20"}

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

def sort_lineup(team, num=None, order="worst"):
    if order == "best":
        reverse=True
    else:
        reverse=False

    batters = team.lineup
    batters.sort(key=lambda x: x.batting_rating, reverse=reverse)

    if num is None or num > len(batters):
        num = len(batters)
    return batters[0:num]

def sort_rotation(team, num=None, order="worst"):
    if order.lower() == "best":
        reverse=True
    else:
        reverse=False

    pitchers = team.rotation
    pitchers.sort(key=lambda x: x.pitching_rating, reverse=reverse)

    if num is None or num > len(pitchers):
        num = len(pitchers)
    return pitchers[0:num]

def sort_bench(team, num=None, order="worst"):
    if order == "best":
        reverse=True
    else:
        reverse=False

    batters = team.bench
    batters.sort(key=lambda x: x.batting_rating, reverse=reverse)

    if num is None or num > len(batters):
        num = len(batters)
    return batters[0:num]

def sort_bullpen(team, num=None, order="worst"):
    if order.lower() == "best":
        reverse=True
    else:
        reverse=False

    pitchers = team.bullpen
    pitchers.sort(key=lambda x: x.pitching_rating, reverse=reverse)

    if num is None or num > len(pitchers):
        num = len(pitchers)
    return pitchers[0:num]

def sort_overall(team, num=None, order="worst"):
    if order.lower() == "best":
        reverse=True
    else:
        reverse=False

    lineup_sorted = sort_lineup(team, num)
    rotation_sorted = sort_rotation(team, num)
    player_dict = {x.id: x for x in lineup_sorted + rotation_sorted}

    # Sort by different ratings depending on position
    line_ids = [(x.id, x.batting_rating) for x in lineup_sorted]
    rot_ids = [(x.id, x.pitching_rating) for x in rotation_sorted]
    sorted_ids = line_ids + rot_ids
    sorted_ids.sort(key=lambda x: x[1], reverse=reverse)

    if num is None or num > len(sorted_ids):
        num = len(sorted_ids)
    return [player_dict[k[0]] for k in sorted_ids[0:num]]

def improve_team_batting(team, amount):
    new_team = []
    for player in team.lineup:
        new_team.append(player.simulated_copy(buffs={"batting_rating": amount}))
    return new_team

def improve_team_pitching(team, amount):
    new_team = []
    for player in team.rotation:
        new_team.append(player.simulated_copy(buffs={"pitching_rating": amount}))
    return new_team

def improve_team_baserunning(team, amount):
    new_team = []
    for player in team.lineup:
        new_team.append(player.simulated_copy(buffs={"baserunning_rating": amount}))
    return new_team

def improve_team_defense(team, amount):
    new_team = []
    for player in team.lineup + team.rotation:
        new_team.append(player.simulated_copy(buffs={"defense_rating": amount}))
    return new_team

def improve_team_overall(team, amount):
    new_team = []
    for player in team.lineup + team.rotation:
        new_team.append(player.simulated_copy(buffs={"overall_rating": amount}))
    return new_team

def maximize(player, position="lineup", overall=False):
    if position in ("lineup", "bench"):
        compare = "batting_stars"
    elif position in ("rotation", "bullpen"):
        compare = "pitching_stars"
    else:
        raise ValueError("invalid position")

    if overall:
        increase = "overall_rating"
    else:
        increase = compare[:-5] + "rating"

    while getattr(player, compare, 5.0) < 5.0:
        player = player.simulated_copy(buffs={increase: 0.01})
        if increase in ("pitching_rating", "overall_rating"): player.total_fingers = player.total_fingers + 1

    if not overall:
        player = player.simulated_copy(buffs={increase: 0.01})
        if increase in ("pitching_rating", "overall_rating"): player.total_fingers = player.total_fingers + 1

    return player

def minimize(player, position, overall=False):
    if position in ("lineup", "bench"):
        compare = "batting_rating"
    elif position in ("rotation", "bullpen"):
        compare = "pitching_rating"
    else:
        raise ValueError("invalid position")

    if overall:
        decrease = "overall_rating"
    else:
        decrease = compare

    while getattr(player, compare, 0.03) > 0.03:
        player = player.simulated_copy(buffs={decrease: -0.01})
        if decrease in ("pitching_rating", "overall_rating"): player.total_fingers = player.total_fingers + 1

    return player


def clone(player):
    player = player.simulated_copy(buffs={"overall_rating": -0.05})
    player.total_fingers = player.total_fingers + 1
    player.name = player.name + " II"
    return player


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