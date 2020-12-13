import utils
import blessings
import display
import pandas
from blaseball_mike.models import Game, Team, Player


if __name__ == "__main__":
    pandas.set_option('display.max_columns', None)

    #games = Game.load_by_day(season=6, day=5)
    #print(utils.blaseball_to_pandas(list(games.values())))

    team = Team.load_by_name("Philly")
    print(blessings.new_recruit(team, 2.5, 2.5, 2.5))
