"""
Various functions to apply either generic or blessing-specific changes to players or teams
"""

from blaseball_mike.models import Team
from statistics import mean
import pandas

# Teams that cannot be the targets or recipients of blessings
INVALID_TEAMS = {"Hall Stars": "c6c01051-cdd4-47d6-8a98-bb5b754f937f",
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

UNREFORMED_MODS = ["RETURNED",
                   "ALTERNATE",
                   "SHELLED",
                   "INVERTED",
                   "BASE_INSTINCTS",
                   "GROWTH",
                   "O",
                   "H2O",
                   "O_NO",
                   "ELECTRIC",
                   "LOVE",
                   "INHABITING",
                   "UNDERPERFORMING",
                   "OVERPERFORMING",
                   "EGO1",
                   "EGO2",
                   "EGO3",
                   "EGO4",
                   "LEGENDARY",
                   "FUGITIVE",
                   "DEBT",
                   "HARD_BOILED",
                   "ELSEWHERE",
                   "SCATTERED",
                   "STATIC",
                   "ECHO",
                   "FIRST_BORN",
                   "COFFEE_EXIT",
                   "RETIRED",
                   "REDACTED",
                   "OVERUNDER",
                   "UNDEROVER"]


def sort_lineup(team, num=None, order="worst"):
    """
    Sort a teams lineup by batting stars

    :param team: Team
    :param num: number of desired results, returns all by default
    :param order: sort by 'best' or 'worst', default 'worst'
    :return: list of Players
    """
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
    """
    Sort a teams rotation by pitching stars

    :param team: Team
    :param num: number of desired results, returns all by default
    :param order: sort by 'best' or 'worst', default 'worst'
    :return: list of Players
    """
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
    """
    Sort a teams bench (hitting shadows) by batting stars

    :param team: Team
    :param num: number of desired results, returns all by default
    :param order: sort by 'best' or 'worst', default 'worst'
    :return: list of Players
    """
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
    """
    Sort a teams bullpen (pitching shadows) by pitching stars

    :param team: Team
    :param num: number of desired results, returns all by default
    :param order: sort by 'best' or 'worst', default 'worst'
    :return: list of Players
    """
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
    """
    Sort a teams players by stars depending on position

    :param team: Team
    :param num: number of desired results, returns all by default
    :param order: sort by 'best' or 'worst', default 'worst'
    :return: list of Players
    """
    if order.lower() == "best":
        reverse=True
    else:
        reverse=False

    lineup_sorted = sort_lineup(team, num)
    rotation_sorted = sort_rotation(team, num)

    # Sort by different ratings depending on position
    line_ids = [(x, x.batting_rating) for x in lineup_sorted]
    rot_ids = [(x, x.pitching_rating) for x in rotation_sorted]
    sorted_ids = line_ids + rot_ids
    sorted_ids.sort(key=lambda x: x[1], reverse=reverse)

    if num is None or num > len(sorted_ids):
        num = len(sorted_ids)
    return [k[0] for k in sorted_ids[0:num]]

def improve_team_batting(team, amount):
    """
    Improve a Team's batting

    :param team: Team
    :param amount: amount to increase or decrease, as a decimal (0.10 is +10%, -0.05 is -5%)
    :return: list of improved players
    """
    new_team = []
    for player in team.lineup:
        new_team.append(player.simulated_copy(buffs={"batting_rating": amount}))
    return new_team

def improve_team_pitching(team, amount):
    """
    Improve a Team's pitching

    :param team: Team
    :param amount: amount to increase or decrease, as a decimal (0.10 is +10%, -0.05 is -5%)
    :return: list of improved players
    """
    new_team = []
    for player in team.rotation:
        new_team.append(player.simulated_copy(buffs={"pitching_rating": amount}))
    return new_team

def improve_team_baserunning(team, amount):
    """
    Improve a Team's baserunning

    :param team: Team
    :param amount: amount to increase or decrease, as a decimal (0.10 is +10%, -0.05 is -5%)
    :return: list of improved players
    """
    new_team = []
    for player in team.lineup:
        new_team.append(player.simulated_copy(buffs={"baserunning_rating": amount}))
    return new_team

def improve_team_defense(team, amount):
    """
    Improve a Team's defense

    :param team: Team
    :param amount: amount to increase or decrease, as a decimal (0.10 is +10%, -0.05 is -5%)
    :return: list of improved players
    """
    new_team = []
    for player in team.lineup:
        new_team.append(player.simulated_copy(buffs={"defense_rating": amount}))
    return new_team

def improve_team_power(team, amount):
    """
    Improve a Team's power

    :param team: Team
    :param amount: amount to increase or decrease, as a decimal (0.10 is +10%, -0.05 is -5%)
    :return: list of improved players
    """
    new_team = []
    for player in team.lineup:
        new_team.append(player.simulated_copy(buffs={"divinity": amount, "musclitude": amount,
                                                     "groundFriction": amount*0.5}))
    return new_team

def improve_team_speed(team, amount):
    """
    Improve a Team's speed

    :param team: Team
    :param amount: amount to increase or decrease, as a decimal (0.10 is +10%, -0.05 is -5%)
    :return: list of improved players
    """
    new_team = []
    for player in team.lineup:
        new_team.append(player.simulated_copy(buffs={"laserlikeness": amount*0.8, "continuation": amount*0.5,
                                                     "groundFriction": amount*0.5, "musclitude": amount*0.15}))
    return new_team

def improve_team_overall(team, amount, position="all"):
    """
    Improve a Team's overall stats

    :param team: Team
    :param amount: amount to increase or decrease, as a decimal (0.10 is +10%, -0.05 is -5%)
    :param postion: whether to improve 'lineup', 'rotation', or 'all'. Default is 'all'
    :return: list of improved players
    """
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

def improve_team_batting_table(team, amount):
    """
    Improve a Team's batting

    :param team: Team
    :param amount: amount to increase or decrease, as a decimal (0.10 is +10%, -0.05 is -5%)
    :return: pandas Dataframe of players star change, pandas Series of total star change, pandas Series of average team star change
    """
    new = improve_team_batting(team, amount)
    table = pandas.DataFrame([{"old_batting_stars": x.batting_rating * 5} for x in team.lineup],
                             index=[x.name for x in team.lineup])
    table = table.join(pandas.DataFrame([{"new_batting_stars": x.batting_rating * 5} for x in new],
                                        index=[x.name for x in new]))
    table['change_in_batting_stars'] = table.apply(lambda row: row.new_batting_stars - row.old_batting_stars, axis=1)

    total = table.sum(axis=0)
    avg = table.mean(axis=0)

    return table, total, avg

def improve_team_pitching_table(team, amount):
    """
    Improve a Team's pitching

    :param team: Team
    :param amount: amount to increase or decrease, as a decimal (0.10 is +10%, -0.05 is -5%)
    :return: pandas Dataframe of players star change, pandas Series of total star change, pandas Series of average team star change
    """
    new = improve_team_pitching(team, amount)
    table = pandas.DataFrame([{"old_pitching_stars": x.pitching_rating * 5} for x in team.rotation],
                             index=[x.name for x in team.rotation])
    table = table.join(pandas.DataFrame([{"new_pitching_stars": x.pitching_rating * 5} for x in new],
                                        index=[x.name for x in new]))
    table['change_in_pitching_stars'] = table.apply(lambda row: row.new_pitching_stars - row.old_pitching_stars, axis=1)

    total = table.sum(axis=0)
    avg = table.mean(axis=0)

    return table, total, avg

def improve_team_baserunning_table(team, amount):
    """
    Improve a Team's baserunning

    :param team: Team
    :param amount: amount to increase or decrease, as a decimal (0.10 is +10%, -0.05 is -5%)
    :return: pandas Dataframe of players star change, pandas Series of total star change, pandas Series of average team star change
    """
    new = improve_team_baserunning(team, amount)
    table = pandas.DataFrame([{"old_baserunning_stars": x.baserunning_rating * 5} for x in team.lineup],
                             index=[x.name for x in team.lineup])
    table = table.join(pandas.DataFrame([{"new_baserunning_stars": x.baserunning_rating * 5} for x in new],
                                        index=[x.name for x in new]))
    table['change_in_baserunning_stars'] = table.apply(lambda row: row.new_baserunning_stars - row.old_baserunning_stars, axis=1)

    total = table.sum(axis=0)
    avg = table.mean(axis=0)

    return table, total, avg

def improve_team_defense_table(team, amount):
    """
    Improve a Team's defense

    :param team: Team
    :param amount: amount to increase or decrease, as a decimal (0.10 is +10%, -0.05 is -5%)
    :return: pandas Dataframe of players star change, pandas Series of total star change, pandas Series of average team star change
    """
    new = improve_team_defense(team, amount)
    table = pandas.DataFrame([{"old_defense_stars": x.defense_rating * 5} for x in team.lineup],
                             index=[x.name for x in team.lineup])
    table = table.join(pandas.DataFrame([{"new_defense_stars": x.defense_rating * 5} for x in new],
                                        index=[x.name for x in new]))
    table['change_in_defense_stars'] = table.apply(lambda row: row.new_defense_stars - row.old_defense_stars, axis=1)

    total = table.sum(axis=0)
    avg = table.mean(axis=0)

    return table, total, avg

def make_team_big_table(team):
    """
    Simulate making a team "big". This is +0.6 to power, -0.4 to baserunning (and some change to cinnamon)

    :param team: Team
    :return: pandas Dataframe of players star change, pandas Series of total star change, pandas Series of average team star change
    """
    new = improve_team_power(team, 0.6)
    new = [x.simulated_copy(buffs={"baserunning_rating": -0.4}) for x in new]
    table = pandas.DataFrame([{"old_batting_stars": x.batting_rating * 5,
                               "old_baserunning_stars": x.baserunning_rating * 5} for x in team.lineup],
                             index=[x.name for x in team.lineup])
    table = table.join(pandas.DataFrame([{"new_batting_stars": x.batting_rating * 5,
                                          "new_baserunning_stars": x.baserunning_rating * 5} for x in new],
                                        index=[x.name for x in new]))
    table['change_in_batting_stars'] = table.apply(lambda row: row.new_batting_stars - row.old_batting_stars, axis=1)
    table['change_in_baserunning_stars'] = table.apply(lambda row: row.new_baserunning_stars - row.old_baserunning_stars, axis=1)

    total = table.sum(axis=0)
    avg = table.mean(axis=0)

    return table, total, avg

def improve_team_overall_table(team, amount):
    """
    Improve a Team's overall stats

    :param team: Team
    :param amount: amount to increase or decrease, as a decimal (0.10 is +10%, -0.05 is -5%)
    :return: pandas Dataframe of players star change, pandas Series of total star change, pandas Series of average team star change
    """
    # Gaze upon my works ye mighty, and despair

    new_lineup = improve_team_overall(team, amount, position="lineup")
    new_rotation = improve_team_overall(team, amount, position="rotation")

    # Generate total change table
    table = pandas.DataFrame([{"old_batting_stars": x.batting_rating * 5,
                               "old_pitching_stars": x.pitching_rating * 5,
                               "old_baserunning_stars": x.baserunning_rating * 5,
                               "old_defense_stars": x.defense_rating * 5} for x in team.lineup + team.rotation],
                             index=[x.name for x in team.lineup + team.rotation])
    table = table.join(pandas.DataFrame([{"new_batting_stars": x.batting_rating * 5,
                                          "new_pitching_stars": x.pitching_rating * 5,
                                          "new_baserunning_stars": x.baserunning_rating * 5,
                                          "new_defense_stars": x.defense_rating * 5} for x in new_lineup + new_rotation],
                                        index=[x.name for x in new_lineup + new_rotation]))
    table['change_in_batting_stars'] = table.apply(lambda row: row.new_batting_stars - row.old_batting_stars, axis=1)
    table['change_in_pitching_stars'] = table.apply(lambda row: row.new_pitching_stars - row.old_pitching_stars, axis=1)
    table['change_in_baserunning_stars'] = table.apply(lambda row: row.new_baserunning_stars - row.old_baserunning_stars, axis=1)
    table['change_in_defense_stars'] = table.apply(lambda row: row.new_defense_stars - row.old_defense_stars, axis=1)

    # To calculate Total & Average Stars, we need to do some magic:
    #   Not all stats are useful for all players, depending on position, so generate DataFrames that only include the correct columns
    #   THEN join the two (with NaNs filling the empty cells) to do the sum & mean calls on
    table_lineup = pandas.DataFrame([{"old_batting_stars": x.batting_rating * 5,
                                      "old_baserunning_stars": x.baserunning_rating * 5,
                                      "old_defense_stars": x.defense_rating * 5} for x in team.lineup],
                                    index=[x.name for x in team.lineup])
    table_lineup = table_lineup.join(pandas.DataFrame([{"new_batting_stars": x.batting_rating * 5,
                                                        "new_baserunning_stars": x.baserunning_rating * 5,
                                                        "new_defense_stars": x.defense_rating * 5} for x in new_lineup],
                                                      index=[x.name for x in new_lineup]))
    table_lineup['change_in_batting_stars'] = table_lineup.apply(lambda row: row.new_batting_stars - row.old_batting_stars, axis=1)
    table_lineup['change_in_baserunning_stars'] = table_lineup.apply(lambda row: row.new_baserunning_stars - row.old_baserunning_stars, axis=1)
    table_lineup['change_in_defense_stars'] = table_lineup.apply(lambda row: row.new_defense_stars - row.old_defense_stars, axis=1)

    table_rotation = pandas.DataFrame([{"old_pitching_stars": x.pitching_rating * 5} for x in team.rotation],
                                      index=[x.name for x in team.rotation])
    table_rotation = table_rotation.join(pandas.DataFrame([{"new_pitching_stars": x.pitching_rating * 5} for x in new_rotation],
                                                          index=[x.name for x in new_rotation]))
    table_rotation['change_in_pitching_stars'] = table_rotation.apply(lambda row: row.new_pitching_stars - row.old_pitching_stars, axis=1)

    table_relative = table_lineup.append(table_rotation)

    total = table_relative.sum(axis=0)
    avg = table_relative.mean(axis=0)

    return table, total, avg

def maximize(player, position="lineup", overall=False):
    """
    Maximize a player

    :param player: Player
    :param position: player's position ('lineup', 'rotation', 'bench', 'bullpen'). default is 'lineup'
    :param overall: whether to maximize all stats. default is False
    :return: maximized Player
    """
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
        if increase in ("pitching_rating", "overall_rating"):
            player.total_fingers = player.total_fingers + 1

    if not overall:
        player = player.simulated_copy(buffs={increase: 0.01})
        if increase in ("pitching_rating", "overall_rating"):
            player.total_fingers = player.total_fingers + 1

    return player

def minimize(player, position, overall=False):
    """
    Minimize a player

    :param player: Player
    :param position: player's position ('lineup', 'rotation', 'bench', 'bullpen'). default is 'lineup'
    :param overall: whether to minimize all stats. default is False
    :return: minimized Player
    """
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
    """
    Clone a player

    :param player: Player
    :return: cloned Player
    """
    player = player.simulated_copy(buffs={"overall_rating": -0.05})
    player.total_fingers = player.total_fingers + 1
    player.name = player.name + " II"
    return player

def best_pitching_hitter(team):
    """
    Get the best Pitching Hitter on a team (highest pitching stars in lineup)
    """
    return max(team.lineup, key=lambda x: x.pitching_rating)

def best_hitting_pitcher(team):
    """
    Get the best Hitting Pitcher on a team (highest batting stars in rotation)
    """
    return max(team.rotation, key=lambda x: x.batting_rating)

def _get_avg_stars_dict(team, bat, pitch, run, def_):
    bat_str = "{:+.4f}%".format(bat * 100)
    pitch_str = "{:+.4f}%".format(pitch * 100)
    baserun_str = "{:+.4f}%".format(run * 100)
    defense_str = "{:+.4f}%".format(def_ * 100)

    return pandas.Series({"batting_change": bat_str, "pitching_change": pitch_str, "baserunning_change": baserun_str,
                          "defense_change": defense_str}).rename(team.nickname)

def _get_player_position(team, player):
    if player in team.lineup:
        return 'lineup'
    elif player in team.rotation:
        return 'rotation'
    elif player in team.bench:
        return 'bench'
    elif player in team.bullpen:
        return 'bullpen'
    else:
        raise Exception("Player not on team")

def replace_player(team, player, bat_star=None, pitch_star=None, run_star=None, def_star=None):
    """
    Replace a player on the team with a new player, with star values defined
    Useful for rerolls or significant stat changes
    :return: Pandas Series containing change in average stars
    """
    bat_mean = 0.0
    pitch_mean = 0.0
    baserun_mean = 0.0
    defense_mean = 0.0

    position = _get_player_position(team, player)

    if bat_star is not None and position == 'lineup':
        bat_mean = mean([x.batting_rating for x in team.lineup if x.id != player.id] + [bat_star/5.0]) - mean([x.batting_rating for x in team.lineup])
    if pitch_star is not None and position == 'rotation':
        pitch_mean = mean([x.pitching_rating for x in team.rotation if x.id != player.id] + [pitch_star/5.0]) - mean([x.pitching_rating for x in team.rotation])
    if run_star is not None and position == 'lineup':
        baserun_mean = mean([x.baserunning_rating for x in team.lineup if x.id != player.id] + [run_star/5.0]) - mean([x.baserunning_rating for x in team.lineup])
    if def_star is not None and position == 'lineup':
        defense_mean = mean([x.defense_rating for x in team.lineup if x.id != player.id] + [def_star/5.0]) - mean([x.defense_rating for x in team.lineup])

    return _get_avg_stars_dict(team, bat_mean, pitch_mean, baserun_mean, defense_mean)

def add_player(team, bat_star=None, pitch_star=None, run_star=None, def_star=None, position=None):
    """
    Add a new player, with star values defined
    :return: Pandas Series containing change in average stars
    """
    bat_mean = 0.0
    pitch_mean = 0.0
    baserun_mean = 0.0
    defense_mean = 0.0

    if bat_star is not None and position != "rotation":
        bat_mean = mean([x.batting_rating for x in team.lineup] + [bat_star/5.0]) - mean([x.batting_rating for x in team.lineup])
    if pitch_star is not None and position != "lineup":
        pitch_mean = mean([x.pitching_rating for x in team.rotation] + [pitch_star/5.0]) - mean([x.pitching_rating for x in team.rotation])
    if run_star is not None and position != "rotation":
        baserun_mean = mean([x.baserunning_rating for x in team.lineup] + [run_star/5.0]) - mean([x.baserunning_rating for x in team.lineup])
    if def_star is not None and position != "rotation":
        defense_mean = mean([x.defense_rating for x in team.lineup] + [def_star/5.0]) - mean([x.defense_rating for x in team.lineup])

    return _get_avg_stars_dict(team, bat_mean, pitch_mean, baserun_mean, defense_mean)

def swap_players(team, player1, player2):
    """
    Swap 2 players within the same team
    :param player1: first player
    :param player2: second player
    :return: Pandas Series containing change in average stars
    """
    if player1 == player2:  # Spiderman pointing at Spiderman
        return _get_avg_stars_dict(team, 0.0, 0.0, 0.0, 0.0)
    if player1.league_team is None or player2.league_team is None:
        raise Exception("Players do not have valid team info, is this old data?")
    if player1.league_team.id != team.id or player2.league_team.id != team.id:
        raise Exception("Both players must be on the same team, use trade_players instead")

    # Scooby Doo, where are you
    p1_list = [x for x in (team.lineup, team.rotation, team.bench, team.bullpen) if player1.id in [y.id for y in x]]
    if len(p1_list) != 1:
        raise Exception("Player1 is either not in any position or has 2 positions at once????")
    p2_list = [x for x in (team.lineup, team.rotation, team.bench, team.bullpen) if player2.id in [y.id for y in x]]
    if len(p2_list) != 1:
        raise Exception("Player2 is either not in any position or has 2 positions at once????")
    p1_list = p1_list[0]
    p2_list = p2_list[0]

    # Since we're doing star averages only do the lineup & rotation
    new_lineup = [x for x in team.lineup if x.id not in (player1.id, player2.id)]
    new_rotation = [x for x in team.rotation if x.id not in (player1.id, player2.id)]
    if p1_list == team.lineup:
        new_lineup += [player2]
    if p1_list == team.rotation:
        new_rotation += [player2]
    if p2_list == team.lineup:
        new_lineup += [player1]
    if p2_list == team.rotation:
        new_rotation += [player1]

    bat_mean = mean([x.batting_rating for x in new_lineup]) - mean([x.batting_rating for x in team.lineup])
    pitch_mean = mean([x.pitching_rating for x in new_rotation]) - mean([x.pitching_rating for x in team.rotation])
    baserun_mean = mean([x.baserunning_rating for x in new_lineup]) - mean([x.baserunning_rating for x in team.lineup])
    defense_mean = mean([x.defense_rating for x in new_lineup]) - mean([x.defense_rating for x in team.lineup])

    return _get_avg_stars_dict(team, bat_mean, pitch_mean, baserun_mean, defense_mean)


def trade_players(team, player1, player2):
    """
    Swap 2 players between teams, to the same relative position
    :param team: reference team, one of the players must be on this team
    :param player1: Player on one end of trade
    :param player2: Player on other end of trade
    :return: Pandas Series containing change in average stars
    """
    if player1.league_team is None or player2.league_team is None:
        raise Exception("Players do not have valid team info, is this old data?")
    on_team = [x for x in (player1, player2) if x.league_team.id == team.id]
    if len(on_team) == 0:
        raise Exception("Neither of these players are on team")
    if len(on_team) == 2:
        raise Exception("Both of these players are on the same team, use swap_players instead")

    on_team = on_team[0]
    off_team = [x for x in (player1, player2) if x.id != on_team.id][0]

    new_lineup = team.lineup
    new_rotation = team.rotation
    if on_team.id in [x.id for x in team.lineup]:
        new_lineup = [x for x in team.lineup if x.id != on_team.id] + [off_team]
    if on_team.id in [x.id for x in team.rotation]:
        new_rotation = [x for x in team.rotation if x.id != on_team.id] + [off_team]

    bat_mean = mean([x.batting_rating for x in new_lineup]) - mean([x.batting_rating for x in team.lineup])
    pitch_mean = mean([x.pitching_rating for x in new_rotation]) - mean([x.pitching_rating for x in team.rotation])
    baserun_mean = mean([x.baserunning_rating for x in new_lineup]) - mean([x.baserunning_rating for x in team.lineup])
    defense_mean = mean([x.defense_rating for x in new_lineup]) - mean([x.defense_rating for x in team.lineup])

    return _get_avg_stars_dict(team, bat_mean, pitch_mean, baserun_mean, defense_mean)

def remove_player(team, player):
    """
    Remove a player on the team, with no replacement
    :return: Pandas Series containing change in average stars
    """
    if player.league_team is None:
        raise Exception("Player does not have valid team info, is this old data?")
    if player.league_team.id != team.id:
        raise Exception("Player being removed is not on team")

    new_lineup = [x for x in team.lineup if x.id != player.id]
    new_rotation = [x for x in team.rotation if x.id != player.id]

    bat_mean = mean([x.batting_rating for x in new_lineup]) - mean([x.batting_rating for x in team.lineup])
    pitch_mean = mean([x.pitching_rating for x in new_rotation]) - mean([x.pitching_rating for x in team.rotation])
    baserun_mean = mean([x.baserunning_rating for x in new_lineup]) - mean([x.baserunning_rating for x in team.lineup])
    defense_mean = mean([x.defense_rating for x in new_lineup]) - mean([x.defense_rating for x in team.lineup])

    return _get_avg_stars_dict(team, bat_mean, pitch_mean, baserun_mean, defense_mean)

def night_thief(home_team):
    """
    Get average stars for players in division bullpens (ignoring the home_team)
    """
    teams = [x for x in Team.load_all().values() if x.id not in INVALID_TEAMS.values()]
    teams = [x for x in teams if x.id != home_team.id]

    pitching = {}
    defense = {}
    for team in teams:
        stars = [x.pitching_stars for x in team.bullpen]
        pitching[team.nickname] = {x: stars.count(x) for x in stars}

        stars = [x.defense_stars for x in team.bullpen]
        defense[team.nickname] = {x: stars.count(x) for x in stars}

    pitch_table = pandas.DataFrame(pitching).fillna(0).sort_index()
    pitch_table["Total"] = pitch_table.sum(axis=1)

    def_table = pandas.DataFrame(defense).fillna(0).sort_index()
    def_table["Total"] = def_table.sum(axis=1)

    return pitch_table, def_table

def grab_and_smash(home_team):
    """
    Get average stars for players in division benches (ignoring the home_team)
    """
    teams = [x for x in Team.load_all().values() if x.id not in INVALID_TEAMS.values()]
    teams = [x for x in teams if x.id != home_team.id]

    batting = {}
    baserunning = {}
    defense = {}
    for team in teams:
        stars = [x.batting_stars for x in team.bench]
        batting[team.nickname] = {x: stars.count(x) for x in stars}

        stars = [x.baserunning_stars for x in team.bench]
        baserunning[team.nickname] = {x: stars.count(x) for x in stars}

        stars = [x.defense_stars for x in team.bench]
        defense[team.nickname] = {x: stars.count(x) for x in stars}

    bat_table = pandas.DataFrame(batting).fillna(0).sort_index()
    bat_table["Total"] = bat_table.sum(axis=1)

    base_table = pandas.DataFrame(baserunning).fillna(0).sort_index()
    base_table["Total"] = base_table.sum(axis=1)

    def_table = pandas.DataFrame(defense).fillna(0).sort_index()
    def_table["Total"] = def_table.sum(axis=1)

    return bat_table, base_table, def_table
