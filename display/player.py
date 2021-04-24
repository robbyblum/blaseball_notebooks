"""
Helper functions to display Player info in Jupyter Notebooks
"""
import pandas
from blaseball_mike.models import SimulationData, Player
from blaseball_mike import reference
from statistics import mean
from display.general import *
from matplotlib import pyplot
import requests
import numpy as np

def display_vibes(player, day=None):
    """
    Display a player's current vibes

    :param player: Player
    :param day: Game Day to get vibes for, defaults to current day
    :return: vibes str
    """
    if not isinstance(player, Player):
        return

    if not day:
        day = SimulationData.load().day + 1

    vibe = player.get_vibe(day)
    print(vibe_to_string(vibe))

def display_season_vibes(player):
    # TODO: Finish this
    days = range(1, 100)
    if isinstance(player, list):
        vibes = [mean([y.get_vibe(x) for y in player]) for x in days]
    elif isinstance(player, dict):
        vibes = [mean([y.get_vibe(x) for y in player.values()]) for x in days]
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

def get_stars(values, include_team=False):
    """
    Display player stars

    :param values: Player or list of Players
    :param include_team: If true include team name in index
    :return: pandas DataFrame
    """
    if not isinstance(values, (Player, list, dict)):
        return

    if isinstance(values, Player):
        values = [values]
    elif isinstance(values, dict):
        values = list(values.values())

    if include_team:
        indexes = pandas.MultiIndex.from_arrays([[x.name for x in values],
                                                 [x.league_team.nickname if x.league_team is not None
                                                  else '----' for x in values]], names=["", "Team"])
    else:
        indexes = [x.name for x in values]
    return pandas.DataFrame([{"Batting": x.batting_stars, "Pitching": x.pitching_stars,
                              "Baserunning": x.baserunning_stars, "Defense": x.defense_stars} for x in values],
                            index=indexes)


def get_total_stars(values):
    """
    Get a list of Total Stars for players

    :param values: Player or list of Players
    :return: dictionary of total star values keyed by player ID
    """
    if not isinstance(values, (Player, list, dict)):
        return

    if isinstance(values, Player):
        values = [values]
    elif isinstance(values, dict):
        values = list(values.values())

    data = {}
    for player in values:
        data[player.id] = (player.batting_rating * 5) + (player.pitching_rating * 5) + (player.baserunning_rating * 5) +\
                          (player.defense_rating * 5)
    return data

def get_batting_stats(values, season=None, filter=None):
    """
    Display player batting stats (from Blaseball-Reference)

    :param values: Player or list of Players
    :param season: Season to get stats for. Default is Career stats
    :param filter: List of stat names to include, eg: ['home_runs', 'singles']
    :return: pandas DataFrame
    """
    if not isinstance(values, (Player, list, dict)):
        return

    if isinstance(values, list):
        ids = [x.id for x in values]
    elif isinstance(values, dict):
        ids = values.keys()
    else:
        ids = values.id

    if season:
        type_ = "season"
        season = season - 1
    else:
        type_ = "career"
        season = None

    table = pandas.DataFrame()
    for player in ids:
        ret = reference.get_stats(player_id=player, group='hitting', type_=type_, season=season, fields=filter)[0]
        if ret["totalSplits"] != 1:
            continue
        data = ret["splits"][0]["stat"]
        name = ret["splits"][0]["player"]["fullName"]
        table = table.append(pandas.Series(data, name=name))
    return table


def get_pitching_stats(values, season=None, filter=None):
    """
    Display player pitching stats (from Blaseball-Reference)

    :param values: Player or list of Players
    :param season: Season to get stats for. Default is Career stats
    :param filter: List of stat names to include, eg: ['strikeouts', 'walks']
    :return: pandas DataFrame
    """
    if not isinstance(values, (Player, list, dict)):
        return

    if isinstance(values, list):
        ids = [x.id for x in values]
    elif isinstance(values, dict):
        ids = values.keys()
    else:
        ids = values.id

    if season:
        type_ = "season"
        season = season - 1
    else:
        type_ = "career"
        season = None

    table = pandas.DataFrame()
    for player in ids:
        ret = reference.get_stats(player_id=player, group='pitching', type_=type_, season=season, fields=filter)[0]
        if ret["totalSplits"] != 1:
            continue
        data = ret["splits"][0]["stat"]
        name = ret["splits"][0]["player"]["fullName"]
        table = table.append(pandas.Series(data, name=name))
    return table

def get_batting_stlats(values):
    """
    Display player batting stlats (FK attributes)

    :param values: Player or list of Players
    :return: pandas DataFrame
    """
    if not isinstance(values, (Player, list, dict)):
        return

    if isinstance(values, Player):
        values = [values]
    elif isinstance(values, dict):
        values = list(values.values())

    return pandas.DataFrame([{"Batting Rating": x.batting_rating,
                              "Thwackability": x.thwackability, "Divinity": x.divinity,
                              "Musclitude": x.musclitude, "Moxie": x.moxie,
                              "Patheticism": x.patheticism, "Martyrdom": x.martyrdom,
                              "Tragicness": x.tragicness, "Buoyancy":x.buoyancy
                              } for x in values], index=[x.name for x in values])

def get_pitching_stlats(values):
    """
    Display player pitching stlats (FK attributes)

    :param values: Player or list of Players
    :return: pandas DataFrame
    """
    if not isinstance(values, (Player, list, dict)):
        return

    if isinstance(values, Player):
        values = [values]
    elif isinstance(values, dict):
        values = list(values.values())

    return pandas.DataFrame([{"Pitching Rating": x.pitching_rating,
                              "Unthwackability": x.unthwackability, "Ruthlessness": x.ruthlessness,
                              "Overpowerment": x.overpowerment, "Shakespearianism": x.shakespearianism,
                              "Coldness": x.coldness, "Suppression": x.suppression
                              } for x in values], index=[x.name for x in values])

def get_baserunning_stlats(values):
    """
    Display player baserunning stlats (FK attributes)

    :param values: Player or list of Players
    :return: pandas DataFrame
    """
    if not isinstance(values, (Player, list, dict)):
        return

    if isinstance(values, Player):
        values = [values]
    elif isinstance(values, dict):
        values = list(values.values())

    return pandas.DataFrame([{"Baserunning Rating": x.baserunning_rating,
                              "Laserlikeness": x.laserlikeness, "Continuation": x.continuation,
                              "Base Thirst": x.base_thirst, "Indulgence": x.indulgence,
                              "Ground Friction": x.ground_friction,
                              } for x in values], index=[x.name for x in values])

def get_defense_stlats(values):
    """
    Display player defense stlats (FK attributes)

    :param values: Player or list of Players
    :return: pandas DataFrame
    """
    if not isinstance(values, (Player, list, dict)):
        return

    if isinstance(values, Player):
        values = [values]
    elif isinstance(values, dict):
        values = list(values.values())

    return pandas.DataFrame([{"Defense Rating": x.defense_rating,
                              "Omniscience": x.omniscience, "Tenaciousness": x.tenaciousness,
                              "Watchfulness": x.watchfulness, "Anticapitalism": x.anticapitalism,
                              "Chasiness": x.chasiness
                              } for x in values], index=[x.name for x in values])

def get_similar_player(player, stat='batting', num_players=10, include_shadows=False, filter_by_postion=True, filter_dead=True):
    """
    Get a list of players that have statlines similar to the selected player.
    TODO: Weight the attributes based on importance?

    :param player: player to compare
    :param stat: stats to compare: 'batting', 'pitching', 'baserunning', 'defense', 'offense'
    :param num_players: number of players to return
    :param include_shadows: whether to include shadows players in the comparison
    :param filter_by_postion: if True, do not include players that are not currently active in this position
    :param filter_dead: if True, do not include dead players
    :return: dictionary with players as values and relative similarity as the key
    """
    bat = ["thwackability", "divinity", "musclitude", "moxie", "patheticism", "martyrdom", "tragicness", "buoyancy"]
    pitch = ["unthwackability", "ruthlessness", "overpowerment", "shakespearianism", "coldness", "suppression"]
    run = ["laserlikeness", "continuation", "baseThirst", "indulgence", "groundFriction"]
    def_ = ["omniscience", "tenaciousness", "watchfulness", "anticapitalism", "chasiness"]

    if stat == 'batting':
        attrs = bat
        position = 'BATTER'
    elif stat == 'pitching':
        attrs = pitch
        position = 'PITCHER'
    elif stat == 'baserunning':
        attrs = run
        position = 'BATTER'
    elif stat == 'defense':
        attrs = def_
        position = 'BATTER'
    elif stat == 'offense':
        attrs = bat + run
        position = 'BATTER'
    else:
        raise ValueError(f"Invalid stat {stat}")

    # Generate table of all players
    url = "https://api.sibr.dev/datablase/v1/allPlayers"
    if include_shadows:
        url += f"?includeShadows={include_shadows}"
    all_players = [reference._apply_type_map(p) for p in requests.get(url).json()]
    if filter_dead:
        all_players = [x for x in all_players if x["deceased"] is False]
    all_players_table = pandas.DataFrame(all_players, index=[x["player_id"] for x in all_players])
    if filter_by_postion:
        all_players_table = all_players_table[all_players_table["position_type"] == position]
    all_table = all_players_table.filter(items=attrs)
    min_stat = all_table.min(axis=0)
    max_stat = all_table.max(axis=0)
    all_scaled = (2.0 * ((all_table - min_stat)/(max_stat - min_stat))) - 1.0

    # Generate table row of selected player
    player_array = pandas.Series(player.json())
    player_array = player_array.filter(items=attrs)
    player_scaled = (2.0 * ((player_array - min_stat)/(max_stat - min_stat))) - 1.0

    # PERFORM THE RITUAL
    all_norm = all_scaled.apply(np.linalg.norm, axis=1)
    player_norm = np.linalg.norm(player_scaled)
    results = all_scaled.dot(player_scaled)/(all_norm*player_norm)

    # Sort and organize output
    results = results.drop(index=player.id, errors='ignore')
    sorted_ = results.sort_values(ascending=False)
    players = Player.load(*sorted_.index[0:num_players])
    players = [players.get(id_) for id_ in sorted_.index[0:num_players]]
    return {results[x.id]: x for x in players}


def _html_attr(attr_list, border_color):
    ret = ""
    for attr in attr_list:
        ret += \
            f"""
            <div style="font-weight:700;display:flex;margin-right:10px;padding-left:5px;padding-right:5px;height:32px;border-radius:5px;align-items:center;justify-content:center;color:{attr.color};background:{attr.background} none repeat scroll 0% 0%;border:2px solid {border_color}">
                {attr.title}
            </div>
        """
    return ret

def display_player(player, day=None):
    """
    Display a player page similarly to the Blaseball website

    :param player: Player
    :param day: gameday for vibes. defaults to current day
    :return: ipython Display
    """
    if isinstance(player, list):
        if len(player) > 1:
            raise ValueError("Can only display one player at a time")
        player = player[0]

    if isinstance(player, dict):
        if len(player) > 1:
            raise ValueError("Can only display one player at a time")
        player = list(player.values())[0]

    if not isinstance(player, Player):
        raise ValueError("Player is not a player")

    if not day:
        sim = SimulationData.load()
        day = sim.day + 1

    if getattr(player, "_perm_attr_ids", None):
        retired = "RETIRED" in player._perm_attr_ids

        if retired or "COFFEE_EXIT" in player._perm_attr_ids:
            soul_name = "Soulsong"
        else:
            soul_name = "Soulscream"
    else:
        retired = False
        soul_name = "Soulscream"

    player_team = ""
    if player.league_team and not retired:
        player_team = f"""
            <div style="display:flex;flex-direction:row;justify-content:space-between;align-items:center;margin-bottom:10px;">
                <div style="font-size:18px;display:flex;align-items:center;border-radius:50%;height:30px;width:30px;justify-content:center;flex-shrink:0;background-color:{player.league_team.main_color};">
                    {parse_emoji(player.league_team.emoji)}
                </div>
                <div style="padding:0 10px;">
                    {player.league_team.full_name}
                </div>
            </div>"""

    if retired:
        soul_color = "#5988ff"
    else:
        soul_color = "#F00"

    try:
        vibe = player.get_vibe(day)
    except AttributeError:
        vibe = 0

    if player.deceased:
        player_status = f"""<div style="padding:15px 40px;display:flex;flex-direction:row;justify-content:space-between;align-items:center;background:#111;border-bottom:1px solid #fff;">
            <div style="padding:0 10px;display:flex;align-items:center;font-size:18px;">
                Deceased
            </div>
        </div>"""
    else:
        player_status = ""

    if getattr(player, "ritual", None):
        ritual = player.ritual
    else:
        ritual = "None?"

    if getattr(player, "fate", None):
        fate = player.fate
    else:
        fate = "????"

    # ATTRIBUTES
    player_attributes = ""
    if len(player.perm_attr) > 0 or len(player.seas_attr) > 0 or len(player.week_attr) > 0 or len(player.game_attr) > 0 or player.bat.attr or player.armor.attr:
        player_attributes += """<div style="padding:5px 40px;display:flex;flex-direction:row;background:#111;border-bottom:1px solid #fff;">
        <div style="display:flex;flex-direction:row;padding:5px;border-radius:5px;background:#222;">"""
        if len(player.perm_attr) > 0:
            player_attributes += _html_attr(player.perm_attr, "#dbbc0b")
        if len(player.seas_attr) > 0:
            player_attributes += _html_attr(player.seas_attr, "#c2157a")
        if len(player.week_attr) > 0:
            player_attributes += _html_attr(player.week_attr, "#0a78a3")
        if len(player.game_attr) > 0:
            player_attributes += _html_attr(player.game_attr, "#639e47")
        if player.bat.attr:
            player_attributes += _html_attr([player.bat.attr], "#bababa")
        if player.armor.attr:
            player_attributes += _html_attr([player.armor.attr], "#bababa")
        player_attributes += "</div></div>"

    html = f"""
    <div style="width:500px;background:#000;border:1px solid #fff;color:#fff;display:flex;flex-direction:column;box-sizing:border-box;font-size:14px;">
        <div style="border-bottom:1px solid #fff;display:flex;flex-direction:column;align-items:flex-start;justify-content:space-between;padding:40px 40px 20px;">
            <div style="font-size:24px;">
                {player.name}
            </div>
            {player_team}
        </div>
        {player_status}
        {player_attributes}
        <div style="padding:20px 0;">
            <div style="display:flex;flex-direction:row;align-items:center;padding:2px 40px;background:rgba(30,30,30,1)">
                <div style="width:180px;font-weight:700;">
                    Current Vibe
                </div>
                <span style="color:{vibe_to_color(vibe)};">
                    {vibe_to_string(vibe)}
                </span>
            </div>
            <div style="display:flex;flex-direction:row;align-items:center;padding:2px 40px;">
                <div style="width:180px;font-weight:700;">
                    Batting
                </div>
                <span>
                    {stars_to_string(player.batting_stars)}
                </span>
            </div>
            <div style="display:flex;flex-direction:row;align-items:center;padding:2px 40px;background:rgba(30,30,30,1)">
                <div style="width:180px;font-weight:700;">
                    Pitching
                </div>
                <span>
                    {stars_to_string(player.pitching_stars)}
                </span>
            </div>
            <div style="display:flex;flex-direction:row;align-items:center;padding:2px 40px;">
                <div style="width:180px;font-weight:700;">
                    Baserunning
                </div>
                <span>
                    {stars_to_string(player.baserunning_stars)}
                </span>
            </div>
            <div style="display:flex;flex-direction:row;align-items:center;padding:2px 40px;background:rgba(30,30,30,1)">
                <div style="width:180px;font-weight:700;">
                    Defense
                </div>
                <span>
                    {stars_to_string(player.defense_stars)}
                </span>
            </div>
            <div style="padding:10px;40px;display:flex;flex-direction:row;justify-content:space-around;">
                <div style="display:flex;flex-direction:column;justify-content:space-between;align-items:center;width:auto;min-width:150px;height:80px;margin:5px;padding:10px 0;background:#111;border-radius:5px;">
                    <div style="font-weight:700;">
                        ITEM
                    </div>
                    <div>
                        {player.bat.name}
                    </div>
                </div>
                <div style="display:flex;flex-direction:column;justify-content:space-between;align-items:center;width:auto;min-width:150px;height:80px;margin:5px;padding:10px 0;background:#111;border-radius:5px;">
                    <div style="font-weight:700;">
                        ARMOR
                    </div>
                    <div>
                        {player.armor.name}
                    </div>
                </div>
            </div>
            <div style="display:flex;flex-direction:row;align-items:center;padding:2px 40px;background:rgba(30,30,30,1)">
                <div style="width:180px;font-weight:700;">
                    Evolution
                </div>
                <span>
                    Base
                </span>
            </div>
            <div style="display:flex;flex-direction:row;align-items:center;padding:2px 40px;">
                <div style="width:180px;font-weight:700;">
                    Pregame Ritual
                </div>
                <span>
                    {ritual}
                </span>
            </div>
            <div style="display:flex;flex-direction:row;align-items:center;padding:2px 40px;background:rgba(30,30,30,1)">
                <div style="width:180px;font-weight:700;">
                    Coffee Style
                </div>
                <span>
                    {player.coffee}
                </span>
            </div>
            <div style="display:flex;flex-direction:row;align-items:center;padding:2px 40px;">
                <div style="width:180px;font-weight:700;">
                    Blood Type
                </div>
                <span>
                    {player.blood}
                </span>
            </div>
            <div style="display:flex;flex-direction:row;align-items:center;padding:2px 40px;background:rgba(30,30,30,1)">
                <div style="width:180px;font-weight:700;">
                    Fate
                </div>
                <span>
                    {fate}
                </span>
            </div>
            <div style="display:flex;flex-direction:row;align-items:center;padding:2px 40px;">
                <div style="width:180px;font-weight:700;">
                    {soul_name}
                </div>
                <span style="max-width:240px;height:auto;border-radius:5px;font-size:16px;font-weight:700;font-style:italic;word-wrap:break-word;color:{soul_color}">
                    {player.soulscream[0:110]}
                </span>
            </div>
        </div>
    </div>
    """

    return HTMLWrapper(html)