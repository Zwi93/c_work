"""
Script info to go here......

Created on 2021/01/04 or close.
"""

import requests as rq
from fpl import FPL
import aiohttp
import asyncio
import csv

url = "https://fantasy.premierleague.com/api/element-summary/1/"
url_1 = "https://fantasy.premierleague.com/api/bootstrap-static/"
url_2 = "https://fantasy.premierleague.com/api/fixtures/?event=1"

my_user_id = 4463037

async def my_teams_performance (id):
    "Function to assess FPL team performance throughout the season. Player's previous records are analyzed, and future points per game assessed"
    session = aiohttp.ClientSession()
    fpl = FPL(session)

    #Connect to my fpl account.
    fpl_username = "zwima93@gmail.com"
    with open('/home/zwi/fpl_config_file.txt', 'r') as file1:
        fpl_psswrd = ''
        text_from_file = csv.reader(file1, delimiter=' ')
        for line in text_from_file:
            fpl_psswrd = fpl_psswrd + line[0]
        
        await fpl.login(fpl_username, fpl_psswrd)
        this_user = await fpl.get_user(id)
        my_team = await this_user.get_team()

        for player in my_team:
            player_id = player['element']
            player_dict = await fpl.get_player(player_id, return_json=True)
            player_team_id = player_dict['team']
            players_team_obj = await fpl.get_team(player_team_id)

            #Use the player's team to find his next 3 games.
            next_fixtures = await players_team_obj.get_fixtures(return_json=False)
            next_3_fixtures = next_fixtures[:3]

            #Get player's summary.
            player_summary = await fpl.get_player_summary(player_id, return_json=True)


            print('Name: ', player_dict['second_name'])
            print('points_per_game: ',player_dict['points_per_game'])
            print('form: ', player_dict['form'])
            print('Availability: ', player_dict['status'])
            print('discipline (cards total): \n', player_dict['yellow_cards'] + player_dict['red_cards'])
            print('player 3 previous games: \n', player_summary['history'][-3:])
            print('player 3 next games: \n', player_summary['fixtures'][:3])
            print('\n')

        await session.close()

asyncio.get_event_loop().run_until_complete(my_teams_performance(my_user_id))