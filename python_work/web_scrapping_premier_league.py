"""
Script info to go here......

Created on 2021/01/04 or the 5th. somewhere close.
"""

from urllib.request import urlopen
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd

def get_prev_fixtures_ids (url):
    "Function to obtain ids of matches of previous seasons from the web; premier league website"
    html_source = urlopen(url)
    soup_object = BeautifulSoup(html_source, 'lxml')

    season_fixture_ids = soup_object.body.main.find('div', 'wrapper col-12 tabLoader u-hide').get('data-fixturesids').split(',')
    max_ids = sorted(season_fixture_ids)[-1] # This is the last fixture of the given season. 
    print(max_ids)

    return int(max_ids)

def get_prev_fixtures_scores (url):
    "Function to obtain scores of fixtures played in a single PL season."
    single_fixture_url = "https://www.premierleague.com/match/"
    last_fixture_id = get_prev_fixtures_ids(url)
    index = 0
    
    #previous_pl_scores = np.ndarray(shape=(3, 4), dtype=str)
    previous_pl_scores = []

    while index < 3:
        fixture_id = str(last_fixture_id - index)
        fixture_url = single_fixture_url + fixture_id
        index += 1

        html = urlopen(fixture_url)

        soup_object = BeautifulSoup(html, 'lxml')

        fixture_score = soup_object.body.main.find_all('div', 'score')
        fixture_score = fixture_score[0].get_text().split('-')
        home_team = soup_object.body.main.find_all('div', 'team home')[0].find('span', 'long').string
        away_team = soup_object.body.main.find_all('div', 'team away')[0].find('span', 'long').string
        matchweek = soup_object.body.main.div.header.find_all('div', 'long')[0].string.split()[1]
        previous_pl_scores.append([matchweek, home_team, away_team, fixture_score[0], fixture_score[1]])   
        
    
    previous_pl_scores_df = pd.DataFrame(previous_pl_scores)
    print(previous_pl_scores_df)


url_2018_19_season = "https://www.premierleague.com/results?co=1&se=210&cl=-1"
url_2019_20_season = "https://www.premierleague.com/results?co=1&se=274&cl=-1"
url_2017_18_season = "https://www.premierleague.com/results?co=1&se=79&cl=-1"
url_2020_21_season = "https://www.premierleague.com/results"

get_prev_fixtures_scores(url_2020_21_season)