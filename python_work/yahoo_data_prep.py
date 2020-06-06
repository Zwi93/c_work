import pandas as pd 
import numpy as np
import yfinance as yf
from pandas_datareader import data, wb 

def get_ticker(ticker, start, end):
    
    ticker = data.DataReader(ticker, data_source='yahoo', start=start, end=end)
    
    return ticker

#tickers = [['CN20.CBT', 'CORN2020-07']]#, ['SOL.JO', 'SOL'], ['SBK.JO', 'SBK']]
#prices = pd.DataFrame({ ticker[1] : get_ticker(ticker[0], '01-01-2001', '30-04-2020')['Adj Close'] for ticker in tickers}).dropna()
#prices.to_excel("comm_futures.xlsx") 

def create_features (fname, col_name):
    """Function to compute the essential features for the Machine Learning algos to be able to construct feature vectors.
    """
    df = pd.read_excel(fname, index_col=0, usecols = ["Date", col_name])
    df_temp = df.copy()
    df_size = df.shape[0]

    df['return'] = np.log(df_temp/df_temp.shift(1))

    #Create more sophisticated features; Momentum, MA, EMA, and Std.
    #Momentum
    df['momentum_1d'] = np.subtract(df_temp.shift(1), df_temp.shift(2))
    df['momentum_5d'] = np.subtract(df_temp.shift(1), df_temp.shift(6))

    #Simple 5d MA.
    df['SMA'] = (df_temp.shift(1) + df_temp.shift(2) + df_temp.shift(3) + df_temp.shift(4) + df_temp.shift(5))/5

    #Exponential 7d MA.
    moving_ema = np.zeros(df_size)
    for i in range(df_size):
        if i < 6:
            moving_ema[i] = None
        elif i == 7:
            moving_ema[i] = np.mean(df[col_name][:i])  # Starting estimate for the exponential moving average.
        else:
            moving_ema[i] = moving_ema[i - 1] + 0.92*(df[col_name][i] - moving_ema[i - 1])
    
    moving_ema[7] = None
    df['EMA'] = moving_ema

    #Determine 21 days moving std.
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

def get_colums_names (fname, col_name):
    df = create_features(fname, col_name)
    df.drop([col_name, 'return', 'return_sign'], axis=1, inplace=True)
    colms = df.columns
    return colms

def get_dates (fname, col_name):
    df = create_features(fname, col_name)
    df = df[df['return_sign'] != 0.0]
    return df.index
