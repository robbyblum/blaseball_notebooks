import os
import nbformat
from blaseball_mike.models import SimulationData, OffseasonSetup

APPENDIX = """
---
## Appendix
* [Description of Attributes](https://www.blaseball.wiki/w/Player_Attributes)
* [Stlat Viewer](http://yoori.space/astrology/#baltimore-crabs-gamma)
* [Historical Player Graphs](http://yoori.space/hloroscopes/)"""

CODE_HEADER = """import pandas
%matplotlib inline
from blaseball_mike.models import *
from blaseball_mike.tables import StatType
import plotly.express as plot
import plotly.io as _pio
import plotly.subplots as subplot
from IPython.display import display, Markdown
from copy import deepcopy

import os
import sys
pdir = os.path.abspath(os.path.join(os.path.dirname(''), os.path.pardir))
sys.path.append(pdir)
from display import *
from blessings import *
sys.path.remove(pdir)

_pio.renderers.default = "notebook_connected"

crabs = Team.load_by_name("Baltimore Crabs")

# Fix Attractors
real_pies = deepcopy(pies)
for p in real_pies.lineup + real_pies.rotation:
    p.batting_rating = None
    p.pitching_rating = None
    p.baserunning_rating = None
    p.defense_rating = None

sim = SimulationData.load()
display(Markdown(f"**Last Updated Season {sim.season}, Day {sim.day}**"))"""


# Check that Notes for the current season do not currently exist
season = SimulationData.load().season
file_name = f"s{season}.ipynb"

if os.path.exists(file_name):
    print(f"Notes for Season {season} already exist, aborting")
    exit(-1)

notes_header = f"""# Season {season} Election Notes

>**FORBIDDEN KNOWLEDGE WARNING**
>
>This document contains some information that is not currently present on the main site and may be considered spoilers.
>Continue at your own discretion. Some information in this document cannot be shared on the Discord without spoiler tags.
"""

# Make new notebook
notes = nbformat.v4.new_notebook()
notes["cells"].extend([nbformat.v4.new_markdown_cell(notes_header),
                      nbformat.v4.new_code_cell(CODE_HEADER)])

election = OffseasonSetup.load()

decree_header = f"""---
## Decrees

Decrees are chosen by majority votes across all teams. `{election.decrees_to_pass}` decrees will pass this season."""

blessing_header = f"""___
## Blessings

Blessings are selected by raffle across all teams. Each blessing will be awarded to one random team, where teams with
more votes are more likely to be selected."""

will_header = f"""___
## Wills

Will are selected for each team by raffle. Each team will draw `{election.wills_to_pass}` random wills. The bottom 4 teams in the league by
standings will draw `{election.wills_to_pass + 1}`. The chosen wills are random, but wills with more votes are more likely to be selected.
"""

gift_header = f"""___
## Gifts

Gifts are awarded to teams based on contributions from other teams. Each team creates a Wishlist of items that they
would like, and the top items on the wishlist are awarded during the Latesiesta.
"""

# Decrees
notes["cells"].append(nbformat.v4.new_markdown_cell(decree_header))
for decree in election.decrees:
    text = f"""### {decree.title}

**{decree.description}**

TODO"""
    notes["cells"].append(nbformat.v4.new_markdown_cell(text))

# Wills
notes["cells"].append(nbformat.v4.new_markdown_cell(will_header))
for will in election.wills:
    text = f"""### {will.title}

**{will.description}**

TODO"""
    notes["cells"].extend([nbformat.v4.new_markdown_cell(text),
                          nbformat.v4.new_code_cell("")])

# Blessings
notes["cells"].append(nbformat.v4.new_markdown_cell(blessing_header))
for blessing in election.blessings:
    text = f"""### {blessing.title}

**{blessing.description}**

TODO"""
    code = f"""{str(getattr(blessing, "metadata", ""))}"""

    notes["cells"].extend([nbformat.v4.new_markdown_cell(text),
                          nbformat.v4.new_code_cell(code)])

# Appendix
notes["cells"].append(nbformat.v4.new_markdown_cell(APPENDIX))

# Write file
with open(file_name, 'w') as fp:
    nbformat.write(notes, fp)

print(f"Notes generated for Season {season}!")
