import pandas
from blaseball_mike.models import Item, Player, Modification
from blaseball_mike import database
from display.general import *


def get_held_items():
    """
    Get a list of all items currently held by players

    :return: list of Items objects
    """
    players = Player.load_all()
    carried_items = []
    for p in players.values():
        carried_items.extend(p.items)
    return carried_items


def get_item_stats(items, include_wielder=False):
    """
    Display item information

    :param items: Item or list of items
    :param include_wielder: Whether to include wielder information
    :return: pandas DataFrame
    """
    if not isinstance(items, (Item, list, dict)):
        return

    if isinstance(items, Item):
        items = [items]
    elif isinstance(items, dict):
        items = list(items.values())

    table = []
    for i in items:
        mods = [Modification.load_one(a["mod"]).title for a in i.adjustments if a["type"] == 0]
        entry = {}
        if include_wielder:
            ret = database.get_players_by_item(i.id)
            if isinstance(ret, list):
                wielder = Player(ret[0])
                entry["Wielder"] = wielder.name
                entry["Team"] = wielder.league_team.nickname
        entry = {"Max Durability": i.durability, "Modifications": mods}
        table.append(pandas.Series(entry, name=i.name))
    return pandas.DataFrame(table)
