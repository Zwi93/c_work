import numpy as np
import pandas as pd

#Read in cds data from excel file.
cds_historical_data = pd.read_excel("cds_data.xlsx", names = ["DATE", "PFIZER", "MSI", "HPQ", "FCO", "CAT"])

#Calculate the correlation matrix.
correlation_matrix = cds_historical_data.corr()

#Write correlation matrix to .txt file.
correlation_matrix.to_csv("correlation_matrix.txt", header=None, index=None, sep=" ", mode="w")
#print(correlation_matrix)
