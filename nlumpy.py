import pandas
import api2
from statistics import mean

BATTING_ATTRIBUTES = ("sight", "thwack", "ferocity")
PITCHING_ATTRIBUTES = ("control", "stuff", "guile")
DEFENSE_ATTRIBUTES = ("reach", "magnet", "reflex")
RUNNING_ATTRIBUTES = ("hustle", "stealth", "dodge")
VIBES_ATTRIBUTES = ("thrive", "survive", "drama")


def parse_player(x):
    data = {"player_name": x["name"], "team_id": x["team"]["id"], "team_name": x["team"]["name"]}
    for pos in x["rosterSlots"]:
        data[f"position"] = pos["location"]
        data[f"position_index"] = pos["orderIndex"]
    data["batting_rating"] = mean([x["value"] for x in x["attributes"] if x["name"].lower() in BATTING_ATTRIBUTES])
    data["pitching_rating"] = mean([x["value"] for x in x["attributes"] if x["name"].lower() in PITCHING_ATTRIBUTES])
    data["defense_rating"] = mean([x["value"] for x in x["attributes"] if x["name"].lower() in DEFENSE_ATTRIBUTES])
    data["running_rating"] = mean([x["value"] for x in x["attributes"] if x["name"].lower() in RUNNING_ATTRIBUTES])
    data["vibes_rating"] = mean([x["value"] for x in x["attributes"] if x["name"].lower() in VIBES_ATTRIBUTES])
    data["overall_rating"] = mean([data["batting_rating"], data["pitching_rating"], data["running_rating"], data["defense_rating"], data["vibes_rating"]])
    for stat in x["categoryRatings"]:
        data[stat["name"].lower()] = stat["stars"]
    for stat in x["attributes"]:
        data[stat["name"].lower()] = stat["value"]
    return data


def nlumpy_get_all_players():
    all = api2.get_all_players()

    lines = []
    for p in all:
        x = api2.get_player(p["id"])
        data = parse_player(x)
        lines.append(pandas.Series(data, name=x["id"]))

    return pandas.DataFrame(lines)


def nlumpy_get_team_players(team_id):
    lines = []
    team = api2.get_team(team_id)
    for p in team["roster"]:
        x = api2.get_player(p["id"])
        data = parse_player(x)
        lines.append(pandas.Series(data, name=x["id"]))

    return pandas.DataFrame(lines)
