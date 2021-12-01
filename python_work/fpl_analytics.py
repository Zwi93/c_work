"""
Script info to go here......

Created on 2021/01/04 or close.
"""

import requests as rq
from fpl import FPL
import aiohttp
import asyncio
import csv
import pandas as pd
from sklearn import svm 
import sklearn.linear_model as skl_lm


url = "https://fantasy.premierleague.com/api/element-summary/1/"
url_1 = "https://fantasy.premierleague.com/api/bootstrap-static/"
url_2 = "https://fantasy.premierleague.com/api/fixtures/?event=1"

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

        for player in my_team[:1]:
            player_id = player['element']
            player_dict = await fpl.get_player(player_id, return_json=True)
            player_team_id = player_dict['team']
            players_team_obj = await fpl.get_team(player_team_id)

            #Use the player's team to find his next 3 games.
            next_fixtures = await players_team_obj.get_fixtures(return_json=False)
            next_3_fixtures = next_fixtures[:3]

            #Get player's summary.
            player_summary = await fpl.get_player_summary(player_id, return_json=True)

            player_prev_games = player_summary['history']
            print(player_summary.keys)
            print('Name: ', player_dict['second_name'])
            print('points_per_game: ',player_dict['points_per_game'])
            print('form: ', player_dict['form'])
            print('Availability: ', player_dict['status'])
            print('discipline (cards total): \n', player_dict['yellow_cards'] + player_dict['red_cards'])
            print('player 3 previous games: \n', player_summary['history'][-3:])
            print('player 3 next games: \n', player_summary['fixtures'][:3])
            print('\n')

        await session.close()


async def find_fpl_captain ():
    "Function to try and predict the optimal choice of fpl captain."
    session = aiohttp.ClientSession()
    fpl = FPL(session)
    
    #First get the top 5 players from all 20 teams in the epl.
    all_pl_teams = await fpl.get_teams()

    for team in all_pl_teams[:1]:
        players = await team.get_players(return_json=True)
        name_of_team = team.name

        print(name_of_team + '\n')

        #Create dataframe of the players.
        players_df_raw = pd.DataFrame(players)
        players_df_raw['goal_involvement'] = players_df_raw['goals_scored'] + players_df_raw['assists']
        players_df = players_df_raw.sort_values(by=['goal_involvement', 'points_per_game', 'form', 'threat'], ascending=False)
        
        #print(players_df.columns)
        print(players_df[['web_name','form', 'points_per_game', 'threat', 'goals_scored', 'assists', 'goal_involvement','bonus','clean_sheets', 'own_goals','penalties_order', 'now_cost']].head(3))

    await session.close()


#asyncio.get_event_loop().run_until_complete(my_teams_performance(my_user_id))
asyncio.get_event_loop().run_until_complete(find_fpl_captain())

