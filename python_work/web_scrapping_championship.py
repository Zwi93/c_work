"""
Script info to go here......

Created on 2021/01/13 ....
"""

from urllib.request import urlopen
from bs4 import BeautifulSoup
import bs4 as bs4
import numpy as np
import pandas as pd

url_championship = "https://www.skysports.com/championship-results"
url_championship_2019_20 = "https://www.skysports.com/championship-results/2019-20"

html = urlopen(url_championship_2019_20)
soup_object = BeautifulSoup(html, 'lxml')

fixture_score = soup_object.find_all('div', 'fixres__item')
#fixture_score = soup_object.find_all('a', 'matches__item matches__link')
hidden_scores = soup_object.find_all('script', type='text/show-more')[0].string
hidden_scores_soup_object = BeautifulSoup(hidden_scores, 'lxml')
hidden_scores = hidden_scores_soup_object.find_all('div', 'fixres__item') 

#Add the two scores arrays; 1st convert them numpy arrays.
#fixture_score = np.array(fixture_score)
#hidden_scores = np.array(hidden_scores).flatten()
#all_fixtures_scores = np.concatenate((fixture_score, hidden_scores)).flatten()
#all_fixtures_scores = all_fixtures_scores
#all_fixtures_scores = all_fixtures_scores[type(all_fixtures_scores) is bs4.element.Tag][0]

"""
for elem in all_fixtures_scores[:2]:#, all_fixtures_scores[201]):
    #match_link = elem.find_all('a', 'matches__item matches__link')[0].get('href')
    home_team = elem.find_all('span', 'swap-text__target')[0].string
    away_team = elem.find_all('span', 'swap-text__target')[1].string
    match_score_home = elem.find_all('span', 'matches__teamscores-side')[0].string.strip()
    match_score_away = elem.find_all('span', 'matches__teamscores-side')[0].string.strip()

    print('home: ', home_team)
    print('away: ', away_team)
    print('score: ', match_score_home)
    print('score: ', match_score_away)

"""
for elem in fixture_score:
    match_link = elem.find_all('a', 'matches__item matches__link')[0].get('href')
    html_match_stats = urlopen(match_link)
    soup_obj = BeautifulSoup(html_match_stats, 'lxml')
    match_date = soup_obj.find_all('time')[0].string
    home_team = elem.find_all('span', 'swap-text__target')[0].string
    away_team = elem.find_all('span', 'swap-text__target')[1].string
    match_score_home = elem.find_all('span', 'matches__teamscores-side')[0].string.strip()
    match_score_away = elem.find_all('span', 'matches__teamscores-side')[1].string.strip()

    print('home: ', home_team)
    print('away: ', away_team)
    print('score: ', match_score_home)
    print('score: ', match_score_away)
    print(match_date)

for elem in hidden_scores:
    match_link = elem.find_all('a', 'matches__item matches__link')[0].get('href')
    html_match_stats = urlopen(match_link)
    soup_obj = BeautifulSoup(html_match_stats, 'lxml')
    match_date = soup_obj.find_all('time')[0].string
    home_team = elem.find_all('span', 'swap-text__target')[0].string
    away_team = elem.find_all('span', 'swap-text__target')[1].string
    match_score_home = elem.find_all('span', 'matches__teamscores-side')[0].string.strip()
    match_score_away = elem.find_all('span', 'matches__teamscores-side')[1].string.strip()

    print('home: ', home_team)
    print('away: ', away_team)
    print('score: ', match_score_home)
    print('score: ', match_score_away)
    print(match_date)

#print(hidden_scores)