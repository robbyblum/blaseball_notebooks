from blaseball_mike.models import Player
from blaseball_mike.tables import Modification
from statistics import mean

# The average stats of a rerolled player
NEW_PLAYER = {"batting": 2, "pitching": 1.5, "baserunning": 2.5, "defense": 2.5}

# Teams that cannot be the targets or recipients of blessings
INVALID_TEAMS = {"Hall Stars": "c6c01051-cdd4-47d6-8a98-bb5b754f937f",
                 "Baltimore Crabs": "8d87c468-699a-47a8-b40d-cfb73a5660ad",
                 "The Shelled One's Pods": "40b9ec2a-cb43-4dbb-b836-5accb62e7c20"}

def worst_lineup(team, num=1):
    """
    Get the worst X players in a teams lineup
    """
    batters = team.lineup
    batters.sort(key=lambda x: x.batting_rating)
    return batters[0:num]

def worst_rotation(team, num=1):
    """
    Get the worst X players in a teams rotation
    """
    pitchers = team.rotation
    pitchers.sort(key=lambda x: x.pitching_rating)
    return pitchers[0:num]

def worst_overall(team, num=1):
    """
    Get the worst X players on a team
    """
    line_ids = [(x.id, x.batting_rating) for x in worst_lineup(team, num)]
    rot_ids = [(x.id, x.pitching_rating) for x in worst_rotation(team, num)]
    sorted_ids = line_ids + rot_ids
    sorted_ids.sort(key=lambda x: x[1])
    return [Player.load_one(x[0]) for x in sorted_ids[0:num]]

def avg_stars(player_list):
    """
    Calculate average stars for a list of players
    This does not include shelled players for any stats except defense
    """
    ret = {}
    ret["batting"] = mean([x.batting_stars for x in player_list if Modification.SHELLED not in x.perm_attr])
    ret["baserunning"] = mean([x.baserunning_stars for x in player_list if Modification.SHELLED not in x.perm_attr])
    ret["defense"] = mean([x.defense_stars for x in player_list])
    ret["pitching"] = mean([x.pitching_stars for x in player_list if Modification.SHELLED not in x.perm_attr])
    return ret

def team_avg_stars(team):
    """
    Calculate average stars for a team
    """
    line_avg = avg_stars(team.lineup)
    rot_avg = avg_stars(team.rotation)
    all_avg = avg_stars(team.rotation + team.lineup)

    return {"batting": line_avg["batting"], "pitching": rot_avg["pitching"],
            "baserunning": line_avg["baserunning"], "defense": all_avg["defense"]}

def total_stars(player_list):
    """
    Calculate total stars for a list of players
    This does not include shelled players for any stats except defense
    """
    ret = {}
    ret["batting"] = sum([x.batting_stars for x in player_list])
    ret["baserunning"] = sum([x.baserunning_stars for x in player_list])
    ret["defense"] = sum([x.defense_stars for x in player_list])
    ret["pitching"] = sum([x.pitching_stars for x in player_list])
    return ret

def team_total_stars(team):
    """
    Calculate total stars for a team
    """
    line_total = total_stars(team.lineup)
    rot_total = total_stars(team.rotation)

    return {"batting": line_total["batting"], "pitching": rot_total["pitching"],
            "baserunning": line_total["baserunning"], "defense": line_total["defense"] + rot_total["defense"]}

def star_compare(new_dict, old_dict):
    """
    Determine the delta between two star dicts (see above functions)
    """
    return {k:v - old_dict[k] for k, v in new_dict.items()}

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

def get_game_by_team(games, team):
    if isinstance(games, dict):
        games = games.values()
    games = [x for x in games if x._away_team_id == team.id or x._home_team_id == team.id]
    if len(games) == 0:
        return None
    return games[0]

def parse_emoji(val):
    try:
        return chr(int(val, 16))
    except ValueError:
        return val