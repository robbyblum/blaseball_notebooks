## TEAM DISPLAY

from blaseball_mike.models import Team, SimulationData
from IPython.display import HTML, display
from utils import *

def _vibe_to_arrow(vibe):
    if vibe > 0.8:
        vibe_str = "<span style=\"color:#15d400;\">▲▲▲</span>"
    elif vibe > 0.4:
        vibe_str = "<span style=\"color:#5de04f;\">▲▲</span>"
    elif vibe > 0.1:
        vibe_str = "<span style=\"color:#8fdb88;\">▲</span>"
    elif vibe > -0.1:
        vibe_str = "<span style=\"color:#d1d1d1;\">⬌</span>"
    elif vibe > -0.4:
        vibe_str = "<span style=\"color:#d97373;\">▼</span>"
    elif vibe > -0.8:
        vibe_str = "<span style=\"color:#de3c3c;\">▼▼</span>"
    else:
        vibe_str = "<span style=\"color:#e00000;\">▼▼▼</span>"
    return vibe_str

def _get_player_html(player, day, index, lineup=True):
    vibe = player.get_vibe(day)
    if lineup:
        stars = player.batting_stars
    else:
        stars = player.pitching_stars

    if not index % 2:
        background = "background:rgba(30,30,30,1);"
    else:
        background = ""

    player_html = f"""
        <div style="display:grid;grid-template-columns:auto 100px 140px; grid-template-rows:30px;align-items:center;margin:0 -40px;padding:0 20px 0 40px;line-height:1.2em;{background}">
            <div>
                {player.name}
            </div>
            <div style="display:flex;flex-direction:row;justify-content:center;">
                {_vibe_to_arrow(vibe)}
            </div>
            <div>
                {stars_to_string(stars)}
            </div>
        </div>
    """
    return player_html

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

def display_team(team, day=None):
    if not isinstance(team, Team):
        return

    if not day:
        sim = SimulationData.load()
        day = sim.day + 1

    emoji = parse_emoji(team.emoji)

    lineup_html = "".join([_get_player_html(x, day, i, True) for i, x in enumerate(team.lineup)])
    rotation_html = "".join([_get_player_html(x, day, i, False) for i, x in enumerate(team.rotation)])

    # ATTRIBUTES
    team_attributes = ""
    if len(team.perm_attr) > 0 or len(team.seas_attr) > 0 or len(team.week_attr) > 0 or len(team.game_attr) > 0:
        team_attributes += """<div style="padding:5px 40px;display:flex;flex-direction:row;background:#111;border-bottom:1px solid #fff;">
            <div style="display:flex;flex-direction:row;padding:5px;border-radius:5px;background:#222;">"""
        if len(team.perm_attr) > 0:
            team_attributes += _html_attr(team.perm_attr, "#dbbc0b")
        if len(team.seas_attr) > 0:
            team_attributes += _html_attr(team.seas_attr, "#c2157a")
        if len(team.week_attr) > 0:
            team_attributes += _html_attr(team.week_attr, "#0a78a3")
        if len(team.game_attr) > 0:
            team_attributes += _html_attr(team.game_attr, "#639e47")
        team_attributes += "</div></div>"

    html = f"""
    <div style="width:500px;background:#000;border:1px solid #fff;color:#fff;display:flex;flex-direction:column;box-sizing:border-box;font-size:14px;">
        <div style="padding: 40px 40px 20px;border-bottom:1px solid #fff;">
            <div style="width:100%;display:flex;flex-direction:row;justify-content:flex-start;align-items:center;">
                <div style="background-color:{team.main_color};border-radius:50%;height:60px;width:60px;font-size:36px;display:flex;align-items:center;justify-content:center;flex-shrink:0;">
                    {emoji}
                </div>
                <div style="display:flex;flex-direction:column;margin-left:10px;">
                    <div style="font-size:24px;">
                        {team.full_name}
                    </div>
                    <div>
                        <i>"{team.slogan}"</i>
                    </div>
                    <div style="margin-top:5px;margin-left:auto;border:1px solid #fff;padding:4px 10px;border-radius:5px;width:-webkit-fit-content;width:-moz-fit-content;width:fit-content;color:#fff">
                        {team.card.text}
                    </div>
                </div>
            </div>
        </div>
        {team_attributes}
        <div style="padding:20px 40px 20px;">
            <div style="margin-bottom:10px;">
                <div style="font-size:18px;margin-bottom:10px;color:#aaa;text-align:center;">
                    Lineup
                </div>
                <ul style="margin:0;padding:0;width:100%;">
                    {lineup_html}
                </ul>
            </div>
            <div style="margin-bottom:10px;">
                <div style="font-size:18px;margin-bottom:10px;color:#aaa;text-align:center;">
                    Rotation
                </div>
                <ul style="margin:0;padding:0;width:100%;">
                    {rotation_html}
                </ul>
            </div>
        </div>
    </div>
    """
    display(HTML(html))
