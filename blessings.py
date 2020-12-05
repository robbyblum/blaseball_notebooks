from blaseball_mike.models import Player, Team, Game, Idol
from statistics import mean
from matplotlib import pyplot
from utils import *


def horde_hallucinations(team, amount):
    """
    Improve Team Baserunning from between -8% and +24%
    Configurable by setting amount to between -0.08 and 0.24
    """
    current = team.lineup

    new = improve_team_baserunning(team, amount)
    table = pandas.DataFrame([{"Name":x.name, "old_baserunning_stars":x.baserunning_rating * 5} for x in current]).set_index("Name")
    table = table.join(pandas.DataFrame([{"Name": x.name, "new_baserunning_stars": x.baserunning_rating * 5} for x in new]).set_index("Name"))
    table['change_in_baserunning_stars'] = table.apply(lambda row: row.new_baserunning_stars - row.old_baserunning_stars, axis=1)

    return table

def katamari(team, amount):
    """
    Improve Team Defense from between -8% and +24%
    Configurable by setting amount to between -0.08 and 0.24
    """
    changes = []
    for player in team.lineup:
        new_player = player.simulated_copy(buffs={'defense_rating': amount})
        changes.append((player.name, new_player.defense_stars, player.defense_stars))

    return changes

def rollback(team, amount):
    """
    Improve Overall rating by -3% to +9%
    Configurable by setting amount to between -0.03 and 0.09
    """
    changes = []
    all = team.lineup + team.rotation
    for player in all:
        new_player = player.simulated_copy(buffs={'overall_rating': amount})
        changes.append({
            "name": player.name,
            "batting": (new_player.batting_stars, player.batting_stars),
            "pitching": (new_player.pitching_stars, player.pitching_stars),
            "baserunning": (new_player.baserunning_stars, player.baserunning_stars),
            "defense": (new_player.defense_stars, player.defense_stars)
        })
    return changes

def plan(team):
    """
    Get the best Hitting pitcher and best Pitching hitter of a team
    """
    best_hitting_pitcher = max(team.rotation, key=lambda x: x.batting_rating)
    best_pitching_hitter = max(team.lineup, key=lambda x: x.pitching_rating)

    return(best_hitting_pitcher, best_pitching_hitter)

def vulture(division):
    """
    Get list of best pitchers and best hitters in the division
    """
    all_pitchers = []
    all_hitters = []
    for team in division.teams.values():
        all_hitters.extend(team.lineup)
        all_pitchers.extend(team.rotation)

    all_hitters.sort(key=lambda x: x.batting_rating, reverse=True)
    all_pitchers.sort(key=lambda x: x.pitching_rating, reverse=True)

    return all_hitters[0:3] + all_pitchers[0:3]

def headhunter(subleague):
    """
    Get list of best hitters in a subleague
    """
    all_hitters = []
    for div in subleague.divisions.values():
        for team in div.teams.values():
            all_hitters.extend(team.lineup)

    all_hitters.sort(key=lambda x: x.batting_rating, reverse=True)

    return all_hitters[0:3]

def mutual_aid(team):
    """
    Swap a teams worst hitter and pitcher, returns affected players and change in stars
    """
    worst_hitter = min(team.lineup, key=lambda x: x.batting_rating)
    worst_pitcher = min(team.rotation, key=lambda x: x.pitching_rating)

    batting_delta = worst_pitcher.batting_stars - worst_hitter.batting_stars
    pitching_delta = worst_hitter.pitching_stars - worst_pitcher.pitching_stars
    baserunning_delta = worst_pitcher.baserunning_stars - worst_hitter.baserunning_stars
    defense_delta = worst_pitcher.defense_stars - worst_hitter.defense_stars

    return (worst_pitcher.name, worst_hitter.name, batting_delta, pitching_delta, baserunning_delta, defense_delta)

def tbd(team):
    """
    Swap best hitting pitcher with worst hitter, returns affected players and change in stars
    """
    best_hitting_pitcher = max(team.rotation, key=lambda x: x.batting_rating)
    worst_hitter = min(team.lineup, key=lambda x: x.batting_rating)

    batting_delta = best_hitting_pitcher.batting_stars - worst_hitter.batting_stars
    pitching_delta = worst_hitter.pitching_stars - best_hitting_pitcher.pitching_stars
    baserunning_delta = best_hitting_pitcher.baserunning_stars - worst_hitter.baserunning_stars
    defense_delta = best_hitting_pitcher.defense_stars - worst_hitter.defense_stars

    return (best_hitting_pitcher.name, worst_hitter.name, batting_delta, pitching_delta, baserunning_delta, defense_delta)

def tbo(team):
    """
    Swap best pitching hitter with worst pitcher, returns affected players and change in stars
    """
    best_pitching_hitter = max(team.lineup, key=lambda x: x.pitching_rating)
    worst_pitcher = min(team.rotation, key=lambda x: x.pitching_rating)

    batting_delta = worst_pitcher.batting_stars - best_pitching_hitter.batting_stars
    pitching_delta = best_pitching_hitter.pitching_stars - worst_pitcher.pitching_stars
    baserunning_delta = worst_pitcher.baserunning_stars - best_pitching_hitter.baserunning_stars
    defense_delta = worst_pitcher.defense_stars - best_pitching_hitter.defense_stars

    return (best_pitching_hitter.name, worst_pitcher.name, batting_delta, pitching_delta, baserunning_delta, defense_delta)

def ooze(team):
    """
    Boost power by 10%
    """
    changes = []
    for player in team.lineup:
        new_player = player.simulated_copy(buffs={'divinity': 0.10, 'musclitude': 0.10})
        changes.append((player.name, new_player.batting_stars, player.batting_stars))

    return changes

def spin_attack(team):
    """
    Boost speed by 15%
    """
    #TODO: determine which attributes this actually changed
    changes = []
    for player in team.lineup:
        new_player = player.simulated_copy(buffs={'laserlikeness': 0.15, 'groundFriction': 0.15})
        changes.append((player.name, new_player.baserunning_stars, player.baserunning_stars))

    return changes

def sharing_signs(division):
    """
    Improve division by +10% hitting, -5% pitching
    """
    results = []
    for team in division.teams.values():
        new_lineup = [x.simulated_copy(buffs={'batting_rating': 0.10}) for x in team.lineup]
        new_rotation = [x.simulated_copy(buffs={'pitching_rating': -0.05}) for x in team.rotation]

        bat_total = sum([x.batting_stars for x in new_lineup]) - sum([x.batting_stars for x in team.lineup])
        pitch_total = sum([x.pitching_stars for x in new_rotation]) - sum([x.pitching_stars for x in team.rotation])
        bat_avg = mean([x.batting_stars for x in new_lineup]) - mean([x.batting_stars for x in team.lineup])
        pitch_avg = mean([x.pitching_stars for x in new_rotation]) - mean([x.pitching_stars for x in team.rotation])

        results.append((team.nickname, bat_total, pitch_total, bat_avg, pitch_avg))

    return results

def move_mounds(division):
    """
    Improve division by +10% pitching, -5% hitting
    """
    results = []
    for team in division.teams.values():
        new_lineup = [x.simulated_copy(buffs={'batting_rating': -0.05}) for x in team.lineup]
        new_rotation = [x.simulated_copy(buffs={'pitching_rating': 0.10}) for x in team.rotation]

        bat_stars = sum([x.batting_stars for x in new_lineup]) - sum([x.batting_stars for x in team.lineup])
        pitch_stars = sum([x.pitching_stars for x in new_rotation]) - sum([x.pitching_stars for x in team.rotation])

        results.append((team.nickname, bat_stars, pitch_stars))

    return results

def mutually_arising(division):
    """
    Improve division by 2% overall
    """
    results = []
    for team in division.teams.values():
        new_lineup = [x.simulated_copy(buffs={'overall_rating': 0.02}) for x in team.lineup]
        new_rotation = [x.simulated_copy(buffs={'overall_rating': 0.02}) for x in team.rotation]

        bat_stars = sum([x.batting_stars for x in new_lineup]) - sum([x.batting_stars for x in team.lineup])
        pitch_stars = sum([x.pitching_stars for x in new_rotation]) - sum([x.pitching_stars for x in team.rotation])
        baserun_stars = sum([x.baserunning_stars for x in new_lineup]) - sum([x.baserunning_stars for x in team.lineup])
        defense_stars = sum([x.defense_stars for x in new_lineup + new_rotation]) - sum([x.defense_stars for x in team.lineup + team.rotation])

        results.append((team.nickname, bat_stars, pitch_stars, baserun_stars, defense_stars))

    return results

def paracausal(team):
    """
    Get worst 3 hitters
    """
    hitters = team.lineup
    hitters.sort(key=lambda x: x.batting_rating)
    return hitters[0:3]

def pretty_plz(team, amount):
    """
    Improve Team Hitting from between -5% and +15%
    Configurable by setting amount to between -0.05 and 0.15
    """
    changes = []
    for player in team.lineup:
        new_player = player.simulated_copy(buffs={'batting_rating': amount})
        changes.append((player.name, new_player.batting_stars, player.batting_stars))
    return changes

def exploratory(team):
    """
    Get 3 worst pitchers
    """
    pitchers = team.rotation
    pitchers.sort(key=lambda x: x.pitching_rating)
    return pitchers[0:3]

def jelly_legs(team):
    """
    Get 3 worst baserunners
    """
    runners = team.lineup
    runners.sort(key=lambda x: x.baserunning_rating)
    return runners[0:3]

def stickum(team):
    """
    Get 3 worst defenders
    """
    defenders = team.lineup + team.rotation
    defenders.sort(key=lambda x: x.defense_rating)
    return defenders[0:3]

def new_recruit(team, bat_star, run_star, def_star):
    """
    Calculate average star rating change if adding an additional batter with star values of bat_star, run_star, and def_star
    """
    base_lineup = [x for x in team.lineup]

    size = len(base_lineup)

    bat_stars = mean([x.batting_stars for x in base_lineup] + [bat_star]) - mean([x.batting_stars for x in base_lineup])
    baserun_stars = mean([x.baserunning_stars for x in base_lineup] + [run_star]) - mean([x.baserunning_stars for x in base_lineup])
    defense_stars = mean([x.defense_stars for x in base_lineup] + [def_star]) - mean([x.defense_stars for x in base_lineup])

    return {"batting": bat_stars, "baserunning": baserun_stars, "defense": defense_stars}

def downsizing(team, player=None):
    """
    Calculate average star rating change if removing a batter (either worst or passed player)
    """
    if player is None:
        worst = min(team.lineup, key=lambda x: x.batting_rating)
    else:
        worst = player
    new_lineup = [x for x in team.lineup if x.id != worst.id]
    base_lineup = [x for x in team.lineup]

    bat_stars = mean([x.batting_stars for x in new_lineup]) - mean([x.batting_stars for x in base_lineup])
    baserun_stars = mean([x.baserunning_stars for x in new_lineup]) - mean([x.baserunning_stars for x in base_lineup])
    defense_stars = mean([x.defense_stars for x in new_lineup]) - mean([x.defense_stars for x in base_lineup])

    return (bat_stars, baserun_stars, defense_stars)

def idol_stars():
    """
    Get the min, max, and average stars of the top 20 idol board players
    """
    list = Idol.load()
    players = [i.player for i in list.values()]

    return {
        "batting": {
            "max": max([p.batting_stars for p in players]),
            "min": min([p.batting_stars for p in players]),
            "avg": mean([p.batting_stars for p in players])
        },
        "pitching": {
            "max": max([p.pitching_stars for p in players]),
            "min": min([p.pitching_stars for p in players]),
            "avg": mean([p.pitching_stars for p in players])
        },
        "baserunning": {
            "max": max([p.baserunning_stars for p in players]),
            "min": min([p.baserunning_stars for p in players]),
            "avg": mean([p.baserunning_stars for p in players])
        },
        "defense": {
            "max": max([p.defense_stars for p in players]),
            "min": min([p.defense_stars for p in players]),
            "avg": mean([p.defense_stars for p in players])
        }
    }

def bullpen(team):
    """
    Get bullpen players
    """
    all = list()
    for player in team.bullpen:
        all.append((player.name, player.batting_stars, player.pitching_stars, player.baserunning_stars, player.defense_stars))
    return all

def replacement_elbows(team):
    """
    Improve pitching by 20%
    Blessing affects 3 random, but calculates change for all players
    """
    pitchers = team.rotation
    new_pitchers = []
    for p in pitchers:
        new_pitchers.append((p, p.simulated_copy(buffs={"pitching_rating": 0.2})))
    return new_pitchers

def promo_code(team, pitch_star):
    """
    Calculate average star rating change if adding an additional pitcher with star value of pitch_star
    """
    pitching_stars = mean([x.pitching_stars for x in team.rotation] + [pitch_star]) - mean([x.pitching_stars for x in team.rotation])

    return pitching_stars

def composite(team, player=None):
    """
    Calculate average star rating change if removing a pitcher (either worst or passed player)
    """
    if player is None:
        worst = min(team.rotation, key=lambda x: x.pitching_rating)
    else:
        worst = player
    new_rotation = [x for x in team.rotation if x.id != worst.id]

    pitch_stars = mean([x.pitching_stars for x in new_rotation]) - mean([x.pitching_stars for x in team.rotation])
    return pitch_stars

def night_thief(division, home_team):
    """
    Get average pitching stars for players in division bullpens & graph all star values
    """
    teams = list(division.teams.values())
    teams = [x for x in teams if x.id != home_team.id]
    avg = 0
    num = 0
    number = {
        0: 0,
        0.5: 0,
        1: 0,
        1.5: 0,
        2: 0,
        2.5: 0,
        3: 0,
        3.5: 0,
        4: 0,
        4.5: 0,
        5: 0
    }
    for t in teams:
        for p in t.bullpen:
            num += 1
            number[p.pitching_stars] += 1
            avg += p.pitching_stars

    vals = list(number.values())
    ticks = list(number.keys())
    tick_pos = [i for i, _ in enumerate(ticks)]
    pyplot.bar(tick_pos, vals)
    pyplot.xticks(tick_pos, ticks)
    pyplot.show()

    avg = avg / num
    return avg

def grab_and_smash(home_team):
    """
    Get average batting stars for players in division bullpens & graph all star values
    """
    teams = [x for x in Team.load_all().values() if x.id not in INVALID_TEAMS.values()]
    teams = [x for x in teams if x.id != home_team.id]
    b_avg = 0
    p_avg = 0
    br_avg = 0
    d_avg = 0
    num = 0
    number = {
        0: 0,
        0.5: 0,
        1: 0,
        1.5: 0,
        2: 0,
        2.5: 0,
        3: 0,
        3.5: 0,
        4: 0,
        4.5: 0,
        5: 0
    }
    for t in teams:
        for p in t.bench:
            num += 1
            number[p.batting_stars] += 1
            b_avg += p.batting_stars
            p_avg += p.pitching_stars
            br_avg += p.baserunning_stars
            d_avg += p.defense_stars

    vals = list(number.values())
    ticks = list(number.keys())
    tick_pos = [i for i, _ in enumerate(ticks)]
    pyplot.bar(tick_pos, vals)
    pyplot.xticks(tick_pos, ticks)
    pyplot.xlabel("Stars")
    pyplot.ylabel("Number of Players")
    pyplot.show()

    b_avg = b_avg / num
    p_avg = p_avg / num
    br_avg = br_avg / num
    d_avg = d_avg / num

    return {"batting": b_avg, "pitching": p_avg, "baserunning": br_avg, "defense": d_avg}

def precognition(team):
    """
    Improve batting by 20%
    Blessing affects 3 random, but calculates change for all players
    """
    batters = team.lineup
    new_batters = []
    for p in batters:
        new_batters.append((p, p.simulated_copy(buffs={"batting_rating": 0.2})))
    return new_batters

def relief_averages():
    """
    Calculate star averages for all players INCLUDING bullpen players
    """
    teams = Team.load_all()
    avgs = {}
    for t in teams.values():
        all = t.rotation + t.bullpen
        avgs[t.nickname] = (mean([x.pitching_stars for x in all]), mean([x.pitching_stars for x in t.rotation]))
    return avgs

def home_field(team):
    """
    Get number of games where was home and either lost by one or went into overtime
    """
    # Get all games, this will take a while
    affected_games = []
    for day in range(1, 100):
        games = list(Game.load_by_day(season=7, day=day).values())
        games = [x for x in games if x.home_team.id == team.id]
        if len(games) == 0:
            continue
        home_game = games[0]
        if home_game.away_score - home_game.home_score == 1 or \
            home_game.inning > 9:
            affected_games.append(home_game)

    return affected_games

def bird_up(team):
    """
    Calculate change in player stars with Affinity for Crows stat boost
    """
    # TODO: Not sure this is actually how it works on the backend
    for p in team.lineup:
        t = p.simulated_copy(multipliers={'batting_rating': 0.5})
        print(t.name, t.batting_stars)
    for p in team.rotation:
        t = p.simulated_copy(multipliers={'pitching_rating': 0.5})
        print(t.name, t.pitching_stars)


def tag_team_pitching(team, opponent):
    """
    Improve Team and worst subleague opponent pitching by 10%
    """
    this_team = []
    for player in team.rotation:
        this_team.append(player.simulated_copy(buffs={'pitching_rating': 0.1}))

    opp_team = []
    for player in opponent.rotation:
        opp_team.append(player.simulated_copy(buffs={'pitching_rating': 0.1}))

    return this_team, opp_team

def tag_team_hitting(team, opponent):
    """
    Improve Team and worst subleague opponent pitching by 10%
    """
    this_team = []
    for player in team.lineup:
        this_team.append(player.simulated_copy(buffs={'batting_rating': 0.1}))

    opp_team = []
    for player in opponent.lineup:
        opp_team.append(player.simulated_copy(buffs={'batting_rating': 0.1}))

    return this_team, opp_team

def out_of_sight(team):
    """
    Replace worst 2 pitchers with top 2 pitchers from Shadows
    """
    relief = team.bullpen[0:2]
    worst_ids = [x.id for x in worst_rotation(team, 2)]
    new_rotation = [x for x in team.rotation if x.id not in worst_ids] + relief

    return total_stars(new_rotation)["pitching"] - total_stars(team.rotation)["pitching"], \
           avg_stars(new_rotation)["pitching"] - avg_stars(team.rotation)["pitching"]

def disappearing_acts(team):
    """
    Replace worst 3 batters with top 3 batters from Shadows
    """
    relief = team.bench[0:3]
    worst_ids = [x.id for x in worst_lineup(team, 3)]
    new_lineup = [x for x in team.lineup if x.id not in worst_ids] + relief

    new_total = total_stars(new_lineup)
    old_total = total_stars(team.lineup)

    new_avg = avg_stars(new_lineup)
    old_avg = avg_stars(team.lineup)

    return star_compare(new_total, old_total), star_compare(new_avg, old_avg)

def nut_button(team):
    """
    Return the number of players and percentage of the team that is allergic to peanuts
    """
    all = team.rotation + team.lineup
    x = sum([x.peanut_allergy for x in all])
    return x, x/len(all)

def black_hole(team):
    """
    Get number of games where a team won or lost by 10 points
    """
    # Get all games, this will take a while
    win_games = []
    lose_games = []
    for day in range(1, 100):
        games = list(Game.load_by_day(season=9, day=day).values())
        games = [x for x in games if x.home_team.id == team.id or x.away_team.id == team.id]
        if len(games) == 0:
            continue
        game = games[0]

        if game.away_score >= 10 or game.home_score >= 10:
            if (game.away_score >= 10 and game.away_team.id == team.id) or\
               (game.home_score >= 10 and game.home_team.id == team.id):
                win_games.append(game)
            else:
                lose_games.append(game)

    return win_games, lose_games

def selfdestruct(team):
    """
    Get number of games where a team shamed or was shamed
    """
    # Get all games, this will take a while
    win_games = []
    lose_games = []
    for day in range(1, 100):
        games = list(Game.load_by_day(season=9, day=day).values())
        games = [x for x in games if x.home_team.id == team.id or x.away_team.id == team.id]
        if len(games) == 0:
            continue
        game = games[0]

        if game.shame:
            if (game.away_score > game.home_score and game.away_team.id == team.id) or\
               (game.home_score > game.away_score and game.home_team.id == team.id):
                win_games.append(game)
            else:
                lose_games.append(game)

    return win_games, lose_games