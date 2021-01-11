"""
Script info to go here......
"""

from urllib.request import urlopen
from bs4 import BeautifulSoup

url_2018_19_season = "https://www.premierleague.com/results?co=1&se=210&cl=-1"
url_2019_20_season = "https://www.premierleague.com/results?co=1&se=274&cl=-1"
url = "https://www.premierleague.com/match/38678"



def get_prev_fixtures_ids (url):
    "Function to obtain ids of matches of previous seasons from the web; premier league website"
    html_source = urlopen(url)
    soup_object = BeautifulSoup(html_source, 'lxml')

    season_fixture_ids = soup_object.body.main.contents[9].get('data-fixturesids').split(',')
    max_ids = sorted(season_fixture_ids)[-1] # This is the last fixture of the given season. 

    return int(max_ids)

def get_prev_fixtures_scores (url):
    "Function to obtain scors of fixtures played in a single PL season."
    single_fixture_url = "https://www.premierleague.com/match/"
    last_fixture_id = get_prev_fixtures_ids(url)
    index = 0

    while index < 3:
        fixture_id = str(last_fixture_id - index)
        fixture_url = single_fixture_url + fixture_id
        index += 1

        html = urlopen(fixture_url)

        soup_object = BeautifulSoup(html, 'lxml')

        fixture_score = soup_object.body.main.find_all('div', 'score')
        home_team = soup_object.body.main.find_all('div', 'team home')[0].find('span', 'long')
        away_team = soup_object.body.main.find_all('div', 'team away')[0].find('span', 'long')
        matchweek = soup_object.body.main.div.header.find_all('div', 'long')[0].string
        print(fixture_score[0].get_text().split('-'))
        print(home_team.string)
        print(away_team.string)

get_prev_fixtures_scores(url_2018_19_season)