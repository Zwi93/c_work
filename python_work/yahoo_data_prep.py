import pandas as pd 
import numpy as np
from random import choice
import sklearn.linear_model as skl_lm
from sklearn.naive_bayes import GaussianNB
import matplotlib.pyplot as plt
import yfinance as yf
from pandas_datareader import data, wb 

def get_ticker(ticker, start, end):
    
    ticker = data.DataReader(ticker, data_source='yahoo', start=start, end=end)
    
    return ticker

#tickers = [['^GSPC', 'SP500'], ['^VIX', 'VIX']]#, ['^FTSE', 'FTSE100']]
#prices = pd.DataFrame({ ticker[1] : get_ticker(ticker[0], '01-01-2010', '30-04-2020')['Adj Close'] for ticker in tickers}).dropna()
#prices.to_excel("index_data.xlsx") 

def create_features (fname, col_name):

    df = pd.read_excel(fname, index_col=0, usecols = ["Date", col_name])
    df_temp = df.copy()

    df['return'] = np.log(df_temp/df_temp.shift(1))

    #Create more sophisticated features; Momentum, MA, EMA, and Std.
    #Momentum
    df['momentum_1d'] = np.subtract(df_temp.shift(1), df_temp.shift(2))
    df['momentum_5d'] = np.subtract(df_temp.shift(1), df_temp.shift(6))

    #Simple MA.
    df['SMA'] = (df_temp.shift(1) + df_temp.shift(2) + df_temp.shift(3) + df_temp.shift(4) + df_temp.shift(5))/5

    #Exponential MA.

    #Determine 21 days moving std.
    df_size = df.shape[0]
    moving_std = np.zeros(df_size)
    for i in range(df_size):
        if i < 21:
            moving_std[i] = None
        else:    
            moving_std[i] = np.std(df['return'][i - 21: i - 1])

    df['Std_Dev_21d'] = moving_std

    #Create cols of lagged log returns.
    lags = 3
    cols = []
    for lag in range(1, lags+1):
        col = 'ret_%d' % lag
        df[col] = df['return'].shift(lag)
        cols.append(col)

    df.dropna(inplace=True)
    df['return_sign'] = np.sign(df['return'].values)

    del df_temp

    return df
