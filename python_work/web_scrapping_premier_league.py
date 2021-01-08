"""
Script info to go here......
"""

from urllib.request import urlopen
from bs4 import BeautifulSoup

url_2019_20_season = "https://www.premierleague.com/results?co=1&se=210&cl=-1"
url = "https://www.premierleague.com/match/38678"

html = urlopen(url_main)

soup_object = BeautifulSoup(html, 'lxml')

#page_sections = soup_object.find_all('section')
#fixtures_section = page_sections.get('fixtures')
#list_of_fixtures = soup_object.find_all('ul')
#score_results = soup_object.find_all('span')
#fixture_score = soup_object.body.main.find_all('div', 'score')
#home_team = soup_object.body.main.find_all('div', 'team home')[0].find('span', 'long')
#away_team = soup_object.body.main.find_all('div', 'team away')[0].find('span', 'long')
#match_date = soup_object.body.main.div.header.find_all('div', 'long')[0].string

def get_prev_fixtures_ids (url):
    "Function to obtain ids of matches of previous seasons from the web; premier league website"
    html_source = urlopen(url)
    soup_object = BeautifulSoup(html_source)

    season_fixture_ids = soup_object.body.main.contents[9].get('data-fixturesids')
    

print(season_fixture_ids)

#for section in score_results:
    #print(section)
    
    #print(fixture.get('class'))# == ["matchFixtureContainer"]:
        #print(fixture.parent)