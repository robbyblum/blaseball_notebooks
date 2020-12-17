from blaseball_mike.models import Player, Team, Game, Idol
from statistics import mean
from matplotlib import pyplot
from utils import *



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
    Swap a teams worst hitter and pitcher
    """
    worst_hitter = sort_lineup(team, num=1)[0]
    worst_pitcher = sort_rotation(team, num=1)[0]

    table = pandas.Series({"batting_change": (worst_pitcher.batting_rating - worst_hitter.batting_rating) * 5,
                           "pitching_change": (worst_hitter.pitching_rating - worst_pitcher.pitching_rating) * 5,
                           "baserunning_change": (worst_pitcher.baserunning_rating - worst_hitter.baserunning_rating) * 5})

    return table, worst_hitter.name, worst_pitcher.name

def tbd(team):
    """
    Swap best hitting pitcher with worst hitter
    """
    new_hitter = best_hitting_pitcher(team)
    worst_hitter = sort_lineup(team, num=1)[0]

    table = pandas.Series({"batting_change": (new_hitter.batting_rating - worst_hitter.batting_rating) * 5,
                           "pitching_change": (worst_hitter.pitching_rating - new_hitter.pitching_rating) * 5,
                           "baserunning_change": (new_hitter.baserunning_rating - worst_hitter.baserunning_rating) * 5})

    return table, worst_hitter.name, new_hitter.name

def tbo(team):
    """
    Swap best pitching hitter with worst pitcher
    """
    new_pitcher = best_pitching_hitter(team)
    worst_pitcher = sort_rotation(team, num=1)[0]

    table = pandas.Series({"batting_change": (worst_pitcher.batting_rating - new_pitcher.batting_rating) * 5,
                           "pitching_change": (new_pitcher.pitching_rating - worst_pitcher.pitching_rating) * 5,
                           "baserunning_change": (worst_pitcher.baserunning_rating - new_pitcher.baserunning_rating) * 5})

    return table, worst_pitcher.name, new_pitcher.name

def ooze(team, amount=0.10):
    """
    Boost power by 10%
    """
    new = improve_team_power(team, amount)
    table = pandas.DataFrame([{"Name": x.name, "old_batting_stars": x.batting_rating * 5} for x in team.lineup]).set_index("Name")
    table = table.join(pandas.DataFrame([{"Name": x.name, "new_batting_stars": x.batting_rating * 5} for x in new]).set_index("Name"))
    table['change_in_batting_stars'] = table.apply(lambda row: row.new_batting_stars - row.old_batting_stars, axis=1)

    total = table.sum(axis=0)
    avg = table.mean(axis=0)

    return table, total, avg

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

def replace_player(team, player, bat_star, pitch_star, run_star, def_star):
    bat_mean = mean([x.batting_stars for x in team.lineup if x.id != player.id] + [bat_star]) - mean([x.batting_stars for x in team.lineup])
    pitch_mean = mean([x.pitching_stars for x in team.rotation if x.id != player.id] + [pitch_star]) - mean([x.pitching_stars for x in team.rotation])
    baserun_mean = mean([x.baserunning_stars for x in team.lineup if x.id != player.id] + [run_star]) - mean([x.baserunning_stars for x in team.lineup])
    defense_mean = mean([x.defense_stars for x in team.lineup + team.rotation if x.id != player.id] + [def_star]) - mean([x.defense_stars for x in team.lineup + team.rotation])

    return pandas.DataFrame([{"batting_change": bat_mean, "pitching_change": pitch_mean, "baserunning_change": baserun_mean, "defense_change": defense_mean}])

def add_player(team, bat_star, run_star, def_star):
    bat_mean = mean([x.batting_stars for x in team.lineup] + [bat_star]) - mean([x.batting_stars for x in team.lineup])
    baserun_mean = mean([x.baserunning_stars for x in team.lineup] + [run_star]) - mean([x.baserunning_stars for x in team.lineup])
    defense_mean = mean([x.defense_stars for x in team.lineup + team.rotation] + [def_star]) - mean([x.defense_stars for x in team.lineup + team.rotation])

    return pandas.DataFrame([{"batting_change":bat_mean, "baserunning_change":baserun_mean, "defense_change":defense_mean}])

def remove_player(team, player):
    new_lineup = [x for x in team.lineup if x.id != player.id]

    bat_mean = mean([x.batting_stars for x in new_lineup]) - mean([x.batting_stars for x in team.lineup])
    baserun_mean = mean([x.baserunning_stars for x in new_lineup]) - mean([x.baserunning_stars for x in team.lineup])
    defense_mean = mean([x.defense_stars for x in new_lineup + team.rotation]) - mean([x.defense_stars for x in team.lineup + team.rotation])

    return pandas.DataFrame([{"batting_change": bat_mean, "baserunning_change": baserun_mean, "defense_change": defense_mean}])

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

    batting = {}
    baserunning = {}
    defense = {}
    for team in teams:
        stars = [x.batting_stars for x in team.bullpen]
        batting[team.nickname] = {x:stars.count(x) for x in stars}

        stars = [x.baserunning_stars for x in team.bullpen]
        baserunning[team.nickname] = {x:stars.count(x) for x in stars}

        stars = [x.defense_stars for x in team.bullpen]
        defense[team.nickname] = {x: stars.count(x) for x in stars}

    bat_table = pandas.DataFrame(batting).fillna(0).sort_index()
    bat_table["Total"] = bat_table.sum(axis=1)

    base_table = pandas.DataFrame(baserunning).fillna(0).sort_index()
    base_table["Total"] = base_table.sum(axis=1)

    def_table = pandas.DataFrame(defense).fillna(0).sort_index()
    def_table["Total"] = def_table.sum(axis=1)

    return bat_table, base_table, def_table

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

    table = pandas.DataFrame([{"Name": x.name, "old_pitching_stars": x.pitching_rating * 5} for x in team.rotation]).set_index("Name")
    table = table.join(pandas.DataFrame([{"Name": x.name, "new_pitching_stars": x.pitching_rating * 5} for x in this_team]).set_index("Name"))
    table['change_in_pitching_stars'] = table.apply(lambda row: row.new_pitching_stars - row.old_pitching_stars, axis=1)

    total = table.sum(axis=0)
    avg = table.mean(axis=0)

    return table, total, avg


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