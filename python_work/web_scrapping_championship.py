"""
Script info to go here......

Created on 2021/01/13 ....
"""

from urllib.request import urlopen
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd

url_championship = "https://www.skysports.com/championship-results"
url_championship_2019_20 = "https://www.skysports.com/championship-results/2019-20"

html = urlopen(url_championship_2019_20)
soup_object = BeautifulSoup(html, 'lxml')

fixture_score = soup_object.find_all('div', 'fixres__item')
hidden_scores = soup_object.find_all('script', type='text/show-more')[0].string
hidden_scores_soup_object = BeautifulSoup(hidden_scores, 'lxml')
hidden_scores_another = hidden_scores_soup_object.find_all('div', 'fixres__item') 

print(hidden_scores_another[0])