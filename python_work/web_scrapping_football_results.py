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
import matplotlib.pyplot as plt

url_championship = "https://www.skysports.com/championship-results/"
url_championship_2019_20 = "https://www.skysports.com/championship-results/2019-20"

url_league_one = "https://www.skysports.com/league-1-results/"

url_league_two = "https://www.skysports.com/league-2-results/"

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

url_laliga = "https://www.skysports.com/la-liga-results/"

url_farmers_league = "https://www.skysports.com/ligue-1-results/"

url_serie_a = "https://www.skysports.com/serie-a-results/"

#Add the two scores arrays; 1st convert them numpy arrays.
#fixture_score = np.array(fixture_score)
#hidden_scores = np.array(hidden_scores).flatten()
#all_fixtures_scores = np.concatenate((fixture_score, hidden_scores)).flatten()
#all_fixtures_scores = all_fixtures_scores
#all_fixtures_scores = all_fixtures_scores[type(all_fixtures_scores) is bs4.element.Tag][0]


async def write_scores_to_file (url, league):
    html = urlopen(url)
    soup_object = BeautifulSoup(html, 'lxml')

    fixture_score = soup_object.find_all('div', 'fixres__item')
    #fixture_score = soup_object.find_all('a', 'matches__item matches__link')
    hidden_scores = soup_object.find_all('script', type='text/show-more')[0].string
    hidden_scores_soup_object = BeautifulSoup(hidden_scores, 'lxml')
    hidden_scores = hidden_scores_soup_object.find_all('div', 'fixres__item')
    file_name = "/home/zwi/zwi_work/python_work/database/score_results_" + url[-7:] + "_" + league + ".csv"
    
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

def scrap_leagues (league_url, league_name):
    "Function to scrap the url league_url and write the fixtures scores to a file"

    counter = 1 

    while counter < 11:
        this_year = datetime.date.today().year 
        prev_year = this_year - counter 
        counter += 1
        url = league_url + str(prev_year - 1) + "-" + str(prev_year)[-2:]
        print(url)
        asyncio.get_event_loop().run_until_complete(write_scores_to_file(url, league_name))

def draw_trends (filename, teams_in_league):
    "Function to analyze historic behaviour of draws in a given game-week."
    #Read the file into a pandas dataframe.
    data_df = pd.read_csv(filename)
    nrows = int(data_df.shape[0])

    total_gameweeks = int((teams_in_league - 1)*2)
    fixtures_per_gw = int(teams_in_league/2)

    x_data = range(total_gameweeks)
    y_data = []

    for i in range(total_gameweeks):
        #Slice the data frame in chuncks of size 10.
        chuncked_df = data_df[nrows - fixtures_per_gw*i - fixtures_per_gw : nrows - fixtures_per_gw*i] 
        #chuncked_df = data_df[fixtures_per_gw*i:fixtures_per_gw*i + fixtures_per_gw]
        draws_df = chuncked_df[chuncked_df['Home Score'] == chuncked_df['Away Score']]
        y_data.append(draws_df.shape[0])

    #plt.plot(x_data, y_data)
    #plt.show()

    return x_data, y_data

def get_size_of_league (filename):
    "Function to determine the size of a league, i.e number of teams"
    data_df = pd.read_csv(filename)
    teams_list = np.array(data_df['Home Team'])
    unique_teams = np.unique(teams_list)
    no_of_teams = unique_teams.size
    return no_of_teams

def aggregate_draw_trends (league_list):
    "Function to analyze draws trends in various leagues."
    
    container_list = []
    
    for filename in league_list:
        no_of_teams = get_size_of_league(filename)
        x_data, y_data = draw_trends(filename, no_of_teams)  # Assuming 20 teams per league.
        container_list.append(y_data)
        #plt.scatter(x_data, y_data)

    df = pd.DataFrame(container_list)
    transposed_df = df.transpose()
    transposed_df.fillna(0)
    transposed_df['sum'] = transposed_df[0] + transposed_df[1] + transposed_df[2] + transposed_df[3] + transposed_df[4]
    #print(transposed_df)
    

    #plt.show()

league_list = ['/home/zwi/zwi_work/python_work/database/score_results_2010-11_bundesliga.csv', '/home/zwi/zwi_work/python_work/database/score_results_2010-11_pl.csv', 
'/home/zwi/zwi_work/python_work/database/score_results_2010-11_laliga.csv', '/home/zwi/zwi_work/python_work/database/score_results_2010-11_serie_a.csv', 
'/home/zwi/zwi_work/python_work/database/score_results_2010-11_efl.csv']

aggregate_draw_trends(league_list)

#draw_betting('/home/zwi/zwi_work/python_work/database/score_results_2016-17_efl.csv', 24)