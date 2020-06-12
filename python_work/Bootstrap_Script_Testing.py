# -*- coding: utf-8 -*-
"""
Created on Fri Dec 14 10:08:47 2018

@author: zwa
testing script for bootstrapper class
"""

import ZeroCurve_Bootstrapper_Class as bts
import Bootstrapper_Helper_Function as btf

import pandas as pd


location = bts.location
df = btf.get_instrument_details(location) #Contains un-interpolated details of 
                                          #instruments.

calibr_swaps = btf.get_swap_object('Sw', df, location)
new_df = btf.get_interpol_swap_dataframe(df, calibr_swaps, location, 'Sw')

#The new_df contains interpolated swap rates and consequently a larger dataframe.

#Saving new_df to a spreadsheet for ease of access later on.
path = bts.spreadsheet_path1
writer = pd.ExcelWriter(path, engine = 'xlsxwriter') 
spreadsheet = new_df.to_excel(writer, sheet_name = 'Sheet1', index = False)
writer.save()

#Now we store the inintialized objects in variables interpol_swaps, fras, etc. 
interpol_swaps = btf.get_interpol_swap_object('Sw', path)
fras = btf.get_fra_instrument(new_df, location)
futures = btf.get_future_object(new_df, location)
deposits = btf.get_deposit_instrument (new_df, location)

#Next, we initialize the zero curve object and then call some of its methods.
w1 = bts.ZeroCurve(location[:-4], deposits, futures, fras, interpol_swaps) 


dfs_for_all_instr = w1.get_swap_dfs()
future_dfs = w1.get_future_dfs()
deposit_dfs = w1.get_deposit_dfs()
fra_dfs = w1.get_fra_dfs()
fra_zero_rate_1 = w1.get_fra_zero_rates()



new_df['Discount factor'] = dfs_for_all_instr




#with pd.option_context('display.max_rows', None, 'display.max_columns', None):
    
#    print(new_df)

#The next piece is just for reporting where we only need calibration instruments
#to appear in our report. The report is in an excel format.    
df_for_calibr_instru = btf.get_df_for_calibr_instr(df, new_df)
murex_disc_fact = list(df['Discount factor'])
murex_zero_rates = list(df['Yield'])
df_for_calibr_instru['Murex Discount factor'] = murex_disc_fact
df_for_calibr_instru['Murex Zero rate'] = murex_zero_rates  


swap_zero_rate = btf.get_swap_zero_rate(df_for_calibr_instru, 'Sw')

#future_zero_rate = w1.get_future_rate()
fra_zero_rate_2 = w1.get_fra_zero_rates()

depo_rate = w1.get_deposit_zero_rate()

zero_rates_list = depo_rate

for elem in fra_zero_rate_2:
    
    zero_rates_list.append(elem)
    
for elem in swap_zero_rate:
    
    zero_rates_list.append(elem)
    

  
df_for_calibr_instru['Zero rates'] = zero_rates_list

cols = ['Tp', 'Generator', 'Adjusted Start date', 'Tenor',\
        'Adjusted Maturity', 'Market quote', 'Discount factor',\
        'Murex Discount factor','Zero rates', 'Murex Zero rate'\
        ]
        
        

df_for_calibr_instru = df_for_calibr_instru[cols]
rate_diff_list = btf.get_rates_difference(df_for_calibr_instru)
df_for_calibr_instru['Rate Difference'] = rate_diff_list

path1 = bts.spreadsheet_path2
writer1 = pd.ExcelWriter(path1, engine = 'xlsxwriter') 
spreadsheet1 =  df_for_calibr_instru.to_excel(writer1, sheet_name = 'Sheet1',\
                                              index = False)

writer1.save()

fwd_rates = btf.get_forward_rates(df_for_calibr_instru, 'Sf')

print(df_for_calibr_instru)

