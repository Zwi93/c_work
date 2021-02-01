"""
Script info to go here......

Created on 2021/01/13 ....
"""

from urllib.request import urlopen
from bs4 import BeautifulSoup
import bs4 as bs4
import numpy as np
import pandas as pd
import csv
import asyncio 
import datetime 

url_championship = "https://www.skysports.com/championship-results/"
url_championship_2019_20 = "https://www.skysports.com/championship-results/2019-20"

url_pl_2020_21 = "https://www.skysports.com/premier-league-results"
url_pl_2019_20 = "https://www.skysports.com/premier-league-results/2019-20"
url_pl_2018_19 = "https://www.skysports.com/premier-league-results/2018-19"
url_pl_2017_18 = "https://www.skysports.com/premier-league-results/2017-18"
url_pl_2016_17 = "https://www.skysports.com/premier-league-results/2016-17"
url_pl_2015_16 = "https://www.skysports.com/premier-league-results/2015-16"
url_pl_2014_15 = "https://www.skysports.com/premier-league-results/2014-15"
url_pl_2013_14 = "https://www.skysports.com/premier-league-results/2013-14"
url_pl_2012_13 = "https://www.skysports.com/premier-league-results/2012-13"
url_pl_2011_12 = "https://www.skysports.com/premier-league-results/2011-12"
url_pl_2010_11 = "https://www.skysports.com/premier-league-results/2010-11"
url_pl_2009_10 = "https://www.skysports.com/premier-league-results/2009-10"

url_budesliga = "https://www.skysports.com/bundesliga-results/"

#Add the two scores arrays; 1st convert them numpy arrays.
#fixture_score = np.array(fixture_score)
#hidden_scores = np.array(hidden_scores).flatten()
#all_fixtures_scores = np.concatenate((fixture_score, hidden_scores)).flatten()
#all_fixtures_scores = all_fixtures_scores
#all_fixtures_scores = all_fixtures_scores[type(all_fixtures_scores) is bs4.element.Tag][0]


async def write_scores_to_file (url):
    html = urlopen(url)
    soup_object = BeautifulSoup(html, 'lxml')

    fixture_score = soup_object.find_all('div', 'fixres__item')
    #fixture_score = soup_object.find_all('a', 'matches__item matches__link')
    hidden_scores = soup_object.find_all('script', type='text/show-more')[0].string
    hidden_scores_soup_object = BeautifulSoup(hidden_scores, 'lxml')
    hidden_scores = hidden_scores_soup_object.find_all('div', 'fixres__item')
    file_name = "score_results_" + url[-7:] + "_efl.csv"
    
    with open(file_name, 'w') as file1:
        stream_to_file = csv.writer(file1, delimiter=',')
        stream_to_file.writerow(['Home Team', 'Home Score', 'Away Team', 'Away Score', 'Match Date'])
        for elem in fixture_score:
            match_link = elem.find_all('a', 'matches__item matches__link')[0].get('href')
            
            #await asyncio.sleep(10)
            
            home_team = elem.find_all('span', 'swap-text__target')[0].string
            away_team = elem.find_all('span', 'swap-text__target')[1].string
            match_score_home = elem.find_all('span', 'matches__teamscores-side')[0].string.strip()
            match_score_away = elem.find_all('span', 'matches__teamscores-side')[1].string.strip()

            try:
                html_match_stats = urlopen(match_link, timeout=60)
                soup_obj = BeautifulSoup(html_match_stats, 'lxml')
                match_date = soup_obj.find_all('time')[0].string.split(',')[1]
                stream_to_file.writerow([home_team, match_score_home, away_team, match_score_away, match_date])
            except:
                print('Error with match_stats link, writing the link instead ')
                stream_to_file.writerow([home_team, match_score_home, away_team, match_score_away, match_link])

            #stream_to_file.writerow(home_team + ' ' + match_score_home + ' ' + away_team + ' ' + match_score_away + ' ' + match_date + '\n')

            

        for elem in hidden_scores:
            match_link = elem.find_all('a', 'matches__item matches__link')[0].get('href')
            #await asyncio.sleep(10)
            
            home_team = elem.find_all('span', 'swap-text__target')[0].string
            away_team = elem.find_all('span', 'swap-text__target')[1].string
            match_score_home = elem.find_all('span', 'matches__teamscores-side')[0].string.strip()
            match_score_away = elem.find_all('span', 'matches__teamscores-side')[1].string.strip()

            try:
                html_match_stats = urlopen(match_link, timeout=60)
                soup_obj = BeautifulSoup(html_match_stats, 'lxml')
                match_date = soup_obj.find_all('time')[0].string.split(',')[1]
                stream_to_file.writerow([home_team, match_score_home, away_team, match_score_away, match_date])
            except:
                print('Error with match_stats link, writing the link instead ')
                stream_to_file.writerow([home_team, match_score_home, away_team, match_score_away, match_link])

            #stream_to_file.writerow(home_team + ' ' + match_score_home + ' ' + away_team + ' ' + match_score_away + ' ' + match_date + '\n')


#asyncio.get_event_loop().run_until_complete(write_scores_to_file(url_pl_2018_19))

#match_results = pd.read_csv('score_results_2019-20_pl.csv')

#stream_to_file.close()

#print(hidden_scores)

#for url in [url_pl_2016_17, url_pl_2015_16, url_pl_2014_15, url_pl_2013_14, url_pl_2012_13, url_pl_2011_12, url_pl_2010_11, url_pl_2009_10]:
#    asyncio.get_event_loop().run_until_complete(write_scores_to_file(url))

counter = 1 

while counter < 11:
    this_year = datetime.date.today().year 
    prev_year = this_year - counter 
    counter += 1
    url = url_budesliga + str(prev_year - 1) + "-" + str(prev_year)[-2:]
    print(url)
    asyncio.get_event_loop().run_until_complete(write_scores_to_file(url))

