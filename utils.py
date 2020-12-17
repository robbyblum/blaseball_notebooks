from blaseball_mike.models import Base, Player
import pandas
from beakerx import ThreeColorHeatmapHighlighter, HighlightStyle, TableDisplay

# The average stats of a rerolled player
NEW_PLAYER = {"batting": 2, "pitching": 1.5, "baserunning": 2.5, "defense": 2.5}

# Teams that cannot be the targets or recipients of blessings
INVALID_TEAMS = {"Hall Stars": "c6c01051-cdd4-47d6-8a98-bb5b754f937f",
                 "Baltimore Crabs": "8d87c468-699a-47a8-b40d-cfb73a5660ad",
                 "The Shelled One's Pods": "40b9ec2a-cb43-4dbb-b836-5accb62e7c20",
                 "Real Game Band": "7fcb63bc-11f2-40b9-b465-f1d458692a63",
                 "FWXBC": "e3f90fa1-0bbe-40df-88ce-578d0723a23b",
                 "Club de Calf": "a3ea6358-ce03-4f23-85f9-deb38cb81b20",
                 "BC Noir": "f29d6e60-8fce-4ac6-8bc2-b5e3cabc5696",
                 "Atlético Latte": "49181b72-7f1c-4f1c-929f-928d763ad7fb",
                 "Cold Brew Crew": "4d921519-410b-41e2-882e-9726a4e54a6a",
                 "Royal PoS": "9a5ab308-41f2-4889-a3c3-733b9aab806e",
                 "Cream & Sugar United": "b3b9636a-f88a-47dc-a91d-86ecc79f9934",
                 "Pandemonium Artists": "3b0a289b-aebd-493c-bc11-96793e7216d5",
                 "Society Data Witches": "d2634113-b650-47b9-ad95-673f8e28e687",
                 "Inter Xpresso": "d8f82163-2e74-496b-8e4b-2ab35b2d3ff1",
                 "Milk Proxy Society": "a7592bd7-1d3c-4ffb-8b3a-0b1e4bc321fd",
                 "Macchiato City": "9e42c12a-7561-42a2-b2d0-7cf81a817a5e",
                 "Light & Sweet Electric Co.": "70eab4ab-6cb1-41e7-ac8b-1050ee12eecc",
                 "Americano Water Works": "4e5d0063-73b4-440a-b2d1-214a7345cf16",
                 "Heavy FC": "e8f7ffee-ec53-4fe0-8e87-ea8ff1d0b4a9"}

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

def set_heatmap(table, maxVal=None):
    """Set a heatmap on each individual column"""
    goodColor = "#74d8b4"
    midColor = "#ffdac1"
    badColor = "#ff4857"

    for column in table.chart.columnNames:
        if column.lower() in ("patheticism", "tragicness"):
            maxC = badColor
            minC = goodColor
        else:
            maxC = goodColor
            minC = badColor

        if maxVal:
            midVal = maxVal/2
        else:
            midVal = None

        table.addCellHighlighter(ThreeColorHeatmapHighlighter(column, style=HighlightStyle.SINGLE_COLUMN, minVal=0, midVal=midVal, maxVal=maxVal, maxColor=maxC, midColor=midColor, minColor=minC))
    return table

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

def improve_team_power(team, amount):
    new_team = []
    for player in team.lineup:
        new_team.append(player.simulated_copy(buffs={"divinity": amount, "musclitude": amount}))
    return new_team

def improve_team_overall(team, amount, position="all"):
    new_team = []
    if position == "lineup":
        vals = team.lineup
    elif position == "rotation":
        vals = team.rotation
    else:
        vals = team.lineup + team.rotation

    for player in vals:
        new_team.append(player.simulated_copy(buffs={"overall_rating": amount}))
    return new_team

# Fancy versions for calculating Pandas Tables of the above
def improve_team_batting_pandas(team, amount):
    new = improve_team_batting(team, amount)
    table = pandas.DataFrame([{"Name":x.name, "old_batting_stars":x.batting_rating * 5} for x in team.lineup]).set_index("Name")
    table = table.join(pandas.DataFrame([{"Name": x.name, "new_batting_stars": x.batting_rating * 5} for x in new]).set_index("Name"))
    table['change_in_batting_stars'] = table.apply(lambda row: row.new_batting_stars - row.old_batting_stars, axis=1)

    total = table.sum(axis=0)
    avg = table.mean(axis=0)

    return table, total, avg

def improve_team_pitching_pandas(team, amount):
    new = improve_team_pitching(team, amount)
    table = pandas.DataFrame([{"Name":x.name, "old_pitching_stars":x.pitching_rating * 5} for x in team.rotation]).set_index("Name")
    table = table.join(pandas.DataFrame([{"Name": x.name, "new_pitching_stars": x.pitching_rating * 5} for x in new]).set_index("Name"))
    table['change_in_pitching_stars'] = table.apply(lambda row: row.new_pitching_stars - row.old_pitching_stars, axis=1)

    total = table.sum(axis=0)
    avg = table.mean(axis=0)

    return table, total, avg

def improve_team_baserunning_pandas(team, amount):
    new = improve_team_baserunning(team, amount)
    table = pandas.DataFrame([{"Name":x.name, "old_baserunning_stars":x.baserunning_rating * 5} for x in team.lineup]).set_index("Name")
    table = table.join(pandas.DataFrame([{"Name": x.name, "new_baserunning_stars": x.baserunning_rating * 5} for x in new]).set_index("Name"))
    table['change_in_baserunning_stars'] = table.apply(lambda row: row.new_baserunning_stars - row.old_baserunning_stars, axis=1)

    total = table.sum(axis=0)
    avg = table.mean(axis=0)

    return table, total, avg

def improve_team_defense_pandas(team, amount):
    new = improve_team_defense(team, amount)
    table = pandas.DataFrame([{"Name": x.name, "old_defense_stars": x.defense_rating * 5} for x in team.lineup]).set_index("Name")
    table = table.join(pandas.DataFrame([{"Name": x.name, "new_defense_stars": x.defense_rating * 5} for x in new]).set_index("Name"))
    table['change_in_defense_stars'] = table.apply(lambda row: row.new_defense_stars - row.old_defense_stars, axis=1)

    total = table.sum(axis=0)
    avg = table.mean(axis=0)

    return table, total, avg

def improve_team_overall_organized(team, amount):
    # Gaze upon my works ye mighty, and despair

    new_lineup = improve_team_overall(team, amount, position="lineup")
    new_rotation = improve_team_overall(team, amount, position="rotation")

    # Generate total change table
    table = pandas.DataFrame([{"Name": x.name, "old_batting_stars": x.batting_rating * 5,
                                      "old_pitching_stars": x.pitching_rating * 5,
                                      "old_baserunning_stars": x.baserunning_rating * 5,
                                      "old_defense_stars": x.defense_rating * 5} for x in team.lineup + team.rotation]).set_index("Name")
    table = table.join(pandas.DataFrame([{"Name": x.name, "new_batting_stars": x.batting_rating * 5,
                                      "new_pitching_stars": x.pitching_rating * 5,
                                      "new_baserunning_stars": x.baserunning_rating * 5,
                                      "new_defense_stars": x.defense_rating * 5} for x in new_lineup + new_rotation]).set_index("Name"))
    table['change_in_batting_stars'] = table.apply(lambda row: row.new_batting_stars - row.old_batting_stars, axis=1)
    table['change_in_pitching_stars'] = table.apply(lambda row: row.new_pitching_stars - row.old_pitching_stars, axis=1)
    table['change_in_baserunning_stars'] = table.apply(lambda row: row.new_batting_stars - row.old_batting_stars, axis=1)
    table['change_in_defense_stars'] = table.apply(lambda row: row.new_defense_stars - row.old_defense_stars, axis=1)

    # To calculate Total & Average Stars, we need to do some magic:
    #   Not all stats are useful for all players, depending on position, so generate DataFrames that only include the correct columns
    #   THEN join the two (with NaNs filling the empty cells) to do the sum & mean calls on
    table_lineup = pandas.DataFrame([{"Name": x.name, "old_batting_stars": x.batting_rating * 5,
                                      "old_baserunning_stars": x.baserunning_rating * 5,
                                      "old_defense_stars": x.defense_rating * 5} for x in team.lineup]).set_index("Name")
    table_lineup = table_lineup.join(pandas.DataFrame([{"Name": x.name, "new_batting_stars": x.batting_rating * 5,
                                          "new_baserunning_stars": x.baserunning_rating * 5,
                                          "new_defense_stars": x.defense_rating * 5} for x in new_lineup]).set_index("Name"))
    table_lineup['change_in_batting_stars'] = table_lineup.apply(lambda row: row.new_batting_stars - row.old_batting_stars, axis=1)
    table_lineup['change_in_baserunning_stars'] = table_lineup.apply(lambda row: row.new_batting_stars - row.old_batting_stars, axis=1)

    table_rotation = pandas.DataFrame([{"Name": x.name, "old_pitching_stars": x.pitching_rating * 5,
                                      "old_defense_stars": x.defense_rating * 5} for x in team.rotation]).set_index("Name")
    table_rotation = table_rotation.join(pandas.DataFrame([{"Name": x.name, "new_pitching_stars": x.pitching_rating * 5,
                                            "new_defense_stars": x.defense_rating * 5} for x in new_rotation]).set_index("Name"))
    table_rotation['change_in_pitching_stars'] = table_rotation.apply(lambda row: row.new_pitching_stars - row.old_pitching_stars, axis=1)

    table_relative = table_lineup.append(table_rotation)
    table_relative['change_in_defense_stars'] = table_lineup.apply(lambda row: row.new_defense_stars - row.old_defense_stars, axis=1)

    total = table_relative.sum(axis=0)
    avg = table_relative.mean(axis=0)

    return table, total, avg

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

def best_pitching_hitter(team):
    return max(team.lineup, key=lambda x: x.pitching_rating)

def best_hitting_pitcher(team):
    return max(team.rotation, key=lambda x: x.batting_rating)



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