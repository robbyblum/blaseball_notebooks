## GAME DISPLAY

from blaseball_mike.models import Player, Team, Game, SimulationData
from IPython.display import HTML, display
import tabulate
from utils import *

def display_game_results(game):
    if not isinstance(game, Game):
        return

    html = """
    <div>
    </div>
    """