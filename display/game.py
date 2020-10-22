## GAME DISPLAY

from blaseball_mike.models import Player, Team, Game, SimulationData
from IPython.display import HTML, display
import tabulate
from utils import *

def _emoji_parse(val):
    try:
        return chr(int(val, 16))
    except ValueError:
        return val

def display_game_results(game):
    if not isinstance(game, Game):
        return

    away_emoji = _emoji_parse(game.away_team_emoji)
    home_emoji = _emoji_parse(game.home_team_emoji)

    weather_style = ""

    if game.shame:
        game_status = "SHAME"
        game_status_style = "background:#800878;"
    elif not game.game_start:
        game_status = "UPCOMING"
        game_status_style = "background:#9a9531;"
    elif game.game_complete:
        game_status = "FINAL"
        if game.inning > 9:
            game_status += f" ({game.inning})"
        game_status_style = "background:red;"
    else:
        top_mark = "▲" if game.top_of_inning else "▼"
        game_status = f"LIVE - {game.inning} {top_mark}"
        game_status_style = "background:green;"

    if len(game.outcomes) > 1:
        outcomes = "\n".join(game.outcomes)
    elif len(game.outcomes) > 0:
        outcomes = game.outcomes[0]
    else:
        outcomes = ""

    if game.game_complete:
        if game.home_score > game.away_score:
            home_win = "border: 2px solid;"
            away_win = ""
        else:
            away_win = "border: 2px solid;"
            home_win = ""
    else:
        home_win = ""
        away_win = ""


    html = f"""
    <div style="font-family:"Open Sans","Helvetica Neue",sans-serif;display:flex;flex-direction:column;border-radius:5px;background-color:#111;width:390px;font-size:1rem;font-weight:400;line-height:1.5;color:#fff;box-sizing:border-box;">
        <div style="height:32px;display:flex;justify-content:space-between;flex-direction:row;align-items:center;font-size:14px;background:rgba(30,30,30,.64)">
            <div style=" display:flex;flex-direction:row;height:32px">
                <div style="{game_status_style}display:flex;padding:0 8px;height:100%;border-radius:5px;align-items:center">
                    {game_status}
                </div>
                <div style="{weather_style}display:flex;padding-left:10px;padding-right:10px;height:32px;border-radius:5px;align-items:center;font-size:14px;justify-content:center">
                    {game.weather.text}
                </div>
            </div>
        </div>
        <div style="display:flex;flex:1 0 auto;flex-direction:column;justify-content:space-around;padding:10px 0 10px 10px;">
            <div style="display:grid;grid-template-columns:60px auto 15%;grid-gap:10px;gap:10px;width:100%;align-items:center">
                <div style="background:{game.away_team_color};display:flex;width:50px;height:50px;margin-left:8px;border-radius:50%;font-size:29px;justify-content:center;align-items:center;">
                    {away_emoji}
                </div>
                <div style="color:{game.away_team_secondary_color};font-size:24px; font-family:"Lora","Courier New",monospace,serif;">
                    {game.away_team_nickname}
                </div>
                <div style="{away_win}display:flex;font-size:24px;font-family:"Lora","Courier New",monospace,serif;align-items:center;justify-content:center;width:46px;height:46px;margin:0 auto;border-radius:50%;">
                    {game.away_score}
                </div>
            </div>
            <div style="display:grid;grid-template-columns:60px auto 15%;grid-gap:10px;gap:10px;width:100%;align-items:center">
                <div style="background:{game.home_team_color};display:flex;width:50px;height:50px;margin-left:8px;border-radius:50%;font-size:29px;justify-content:center;align-items:center;">
                    {home_emoji}
                </div>
                <div style="color:{game.home_team_secondary_color};font-size:24px; font-family:"Lora","Courier New",monospace,serif;">
                    {game.home_team_nickname}
                </div>
                <div style="{home_win}display:flex;font-size:24px;font-family:"Lora","Courier New",monospace,serif;align-items:center;justify-content:center;width:46px;height:46px;margin:0 auto;border-radius:50%;">
                    {game.home_score}
                </div>
            </div>
            <div style="font-size:14px;">
                {outcomes}
            </div>
        </div>
    </div>
    """
    display(HTML(html))