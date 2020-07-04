import numpy as np
import pandas as pd

#Read in cds data from excel file.
cds_historical_data_daily = pd.read_excel("cds_data.xlsx", names = ["DATE", "PFIZER", "MSI", "HPQ", "FCO", "CAT"])

#Convert the daily data into weekly.
def daily_to_weekly (dataframe):
    rows = dataframe.shape[0]
    columns = dataframe.shape[1]

    weekly_data_array = np.zeros((rows, columns - 1))

    for i in range(0, rows, 5):
        weekly_data_array[int(i/5)] = dataframe[["PFIZER", "MSI", "HPQ", "FCO", "CAT"]].iloc[i]

    weekly_data_df = pd.DataFrame(weekly_data_array, columns = ["PFIZER", "MSI", "HPQ", "FCO", "CAT"])

    return weekly_data_df

cds_historical_data_weekly = daily_to_weekly(cds_historical_data_daily)

#Calculate the correlation matrix.
correlation_matrix = cds_historical_data_weekly.corr()

#Write correlation matrix to .txt file.
correlation_matrix.to_csv("correlation_matrix.txt", header=None, index=None, sep=" ", mode="w")
#print(correlation_matrix)
