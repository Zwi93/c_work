"""
Script info to go here......
"""

import requests as rq
from fpl import FPL
import aiohttp
import asyncio

url = "https://fantasy.premierleague.com/api/element-summary/1/"
url_1 = "https://fantasy.premierleague.com/api/bootstrap-static/"
url_2 = "https://fantasy.premierleague.com/api/fixtures/?event=1"

fpl_username = "zwima93@gmail.com"
fpl_psswrd = "HXez.tzMcW?44,i"
my_user_id = 4463037

async def my_team (id):
    session = aiohttp.ClientSession()
    fpl = FPL(session)

    #Connect to my fpl account.
    await fpl.login(fpl_username, fpl_psswrd)
    this_user = await fpl.get_user(id)
    my_team = await this_user.get_team()

    print(len(my_team))

asyncio.get_event_loop().run_until_complete(my_team(my_user_id))