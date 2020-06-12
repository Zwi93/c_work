# -*- coding: utf-8 -*-
"""
Created on Mon Dec 10 14:25:14 2018

@author: zwa

This script contains work on bootstrapping curves. It interacts with another script 
(instrument_generators_class) to perform the process.
The function get_instrument_details interacts with a csv file that contains relevant 
information about the instruments and then dumps this info in a pandas dataframe.
The other functions, i.e get_swap_object, then use this output df to initiate 
a swap object (or futures object) and saves the results in a list object type.
The function get_interpol_swap_rates performs the interpolation between quoted
swap rates. Currently, only linear interpolation has been implemented.
 
"""

import pandas as pd
import datetime 
import Instrument_Generator_Class as ig
from datetime import timedelta
import numpy as np

def get_instrument_details (location):
                
	df = pd.read_csv(location, names = ['Tp', 'Start date', 'Generator', 'Maturity',\
                                     'Tenor', 'Discount factor',\
									         'Yield', 'H', 'I', 'Market quote',\
                                     'Curve spread', 'Selected'],\
                    sep = ';'
                    )
    
	df = df.drop(index = [0, 1])
	#df = df.drop(['H', 'I', 'Curve spread'])

	list_1 = df['Start date'].astype('str')
	list_2 = df['Maturity'].astype('str')

	list_3 = []
	for elem in list_1:

         
         year = int('20' + elem[-2:])
         year_np = '20' + elem[-2:]
         mon = int(elem[-5:-3])
         mon_np = elem[-5:-3]
         day = int(elem[0:2])
         day_np = elem[0:2]
         date = datetime.datetime(year, mon, day, 0, 0, 0)
         date_in_str_type = year_np + '-' + mon_np + '-' + day_np
         date_in_np = np.datetime64(date_in_str_type)
         list_3.append(date)
         		      

	list_4 = []
	for elem in list_2:
        
         year = int('20' + elem[-2:])
         year_np = '20' + elem[-2:]
         mon = int(elem[-5:-3])
         mon_np = elem[-5:-3]
         day = int(elem[0:2])
         day_np = elem[0:2]
         date = datetime.datetime(year, mon, day, 0, 0, 0)
         date_in_str_type = year_np + '-' + mon_np + '-' + day_np
         date_in_np = np.datetime64(date_in_str_type)
         list_4.append(date)

		

 
	df['Adjusted Start date'] = list_3
	df['Adjusted Maturity'] = list_4
	
    
	return df

def identify_instr_type (dataframe, instrument):
	
	list_1 = dataframe['Tp']
	#instru_type_set = set(list_1)
	#size_instru_type_set = len(instru_type_set)
	instrument = instrument

	instru_collector = []

	for instru in list_1:

		if instru == instrument:
			instru_collector.append(instru)

	return instru_collector

def get_swap_object (swap_type, dataframe, location):

	'''
   This function collects and saves the swap objects obtained from the 
	the class SwapGenerator in a list object.
   ''' 


	swap_list = identify_instr_type(dataframe, swap_type)
	size_swap_list = len(swap_list)
	df = get_instrument_details(location)
	df.set_index('Tp')
	condition = df['Tp'] == swap_type
	df1 = df.loc[condition]
	start_dates = df1['Adjusted Start date'].tolist()
	end_dates = df1['Adjusted Maturity'].tolist()
	swap_rates = df1['Market quote'].tolist()
	tenors = df1['Tenor'].tolist()
	generator_name = df1['Generator'].tolist()

	swap_objects = []

	for i in range(size_swap_list):
		name = tenors[i] + ' ' + generator_name[i]
		start_date = start_dates[i]
		end_date = end_dates[i]
		rate = swap_rates[i]
		swap_object = ig.SwapInstrument(name, swap_type, start_date, end_date, rate)
		swap_objects.append(swap_object)

	return swap_objects

def get_interpol_swap_object (swap_type, location):
	  
    '''
    This function creates swap ojects from the interpolated swap rates obtained from 
	 the excel spreadsheet currency_3m_interpol.Swap_type is either Sw, Bs, or Sp.
    '''  
        
    
    df = pd.read_excel(location, names = ['Adjusted Maturity', 'Adjusted Start date',\
                                          'Generator', 'Market quote', 'Tenor', 'Tp']\
        )
     
    swap_list = identify_instr_type(df, swap_type)
    size_swap_list = len(swap_list)
    df.set_index('Tp')
    condition =  df['Tp'] == swap_type
    df1 = df.loc[condition]
    start_dates = df1['Adjusted Start date'].tolist()
    end_dates = df1['Adjusted Maturity'].tolist()
    swap_rates = df1['Market quote'].tolist()
    tenors = df1['Tenor'].tolist()
    generator_name = df1['Generator'].tolist()

    swap_objects = []

    for i in range(size_swap_list):

    	name = tenors[i] + ' ' + generator_name[i]
    	start_date = start_dates[i]
    	end_date = end_dates[i]
    	rate = swap_rates[i]
    	swap_object = ig.InterpolatedSwapInstrument(name, swap_type, start_date, end_date, rate)
    	swap_objects.append(swap_object)

    return swap_objects


	

def get_interpol_swap_dataframe(dataframe, swap_object, location, swap_type):
        
    '''
    This function gets, as one of the its inputs, the interpolated swap objects
    and then creates a dataframe for these new objects, adding them on top of 
    the old dataframe (supplied as input).
    '''
    
    colmn1 = dataframe['Tp'].tolist()
    colmn2 = dataframe['Generator'].tolist()
    colmn3 = dataframe['Market quote'].tolist()
    colmn4 = dataframe['Adjusted Start date'].tolist()
    colmn5 = dataframe['Adjusted Maturity'].tolist()
    colmn6 = dataframe['Tenor'].tolist()
    
    interpol_swap_rates, swap_reset_dates = get_swap_interpol_rates (dataframe, swap_object,\
                                                                     location, swap_type)
                                                                     
                                                                   
    
    size_swap_list = len(interpol_swap_rates)
    
    for i in range(size_swap_list):
        
        colmn1.append(colmn1[-1])
        colmn2.append(colmn2[-1])
        colmn4.append(colmn4[-1])
        colmn3.append(interpol_swap_rates[i])
        colmn5.append(swap_reset_dates[i])
        colmn6.append(colmn6[-1])
    
        
    df = pd.DataFrame({'Tp': colmn1,
                           'Generator': colmn2,
                           'Market quote': colmn3,
                           'Adjusted Start date': colmn4,
                           'Adjusted Maturity': colmn5,
                           'Tenor': colmn6
                           }
        )
    
    
    new_df = df.sort_values(by='Adjusted Maturity')
    
    return new_df



def get_consecutive_tenors (instrument_type, dataframe, location):
    
    
    '''
    This function allows one to get the difference between the end_dates of 
    the calibration instruments.The result is stored in a list format.
    '''
    
    if (instrument_type == 'Sw') or (instrument_type == 'Bs') or (instrument_type == 'Sp')  :
        
        objects = get_swap_object(instrument_type, dataframe, location)
        
        
    elif instrument_type == 'Fr':
        
        objects = get_fra_instrument(dataframe, location)
        
        
    elif instrument_type == 'Sf':
        
        objects = get_future_object(dataframe, location)
        
        
    elif instrument_type == 'Dg':
        
        objects = get_deposit_instrument(dataframe, location)
        
        
    size_obj = len(objects)
    tenors = []
    
    for i in range(size_obj - 1):
        
        ith_obj = objects[i]
        jth_obj = objects[i + 1]
        ith_obj_end_date = ith_obj.end_date
        jth_obj_end_date = jth_obj.end_date
        tenor_diff = (jth_obj_end_date - ith_obj_end_date)/timedelta(days=1)
        tenor_diff = tenor_diff/360
        tenors.append(tenor_diff)
        
    return tenors

def get_swap_interpol_rates (dataframe, swap_object, location, swap_type):
    
    '''
    This function performs the linear interpolation between quoted swap rates
    which are retrievable from the swap objects.
    '''
    
    swap_consecutive_tenors = get_consecutive_tenors(swap_type, dataframe,\
                                                     location)
    size_swap_consecutive_tenors = len(swap_consecutive_tenors)
    end_dates_list = []
    swap_rates_list = []
    
    for elem in swap_object:
        
        end_date = elem.end_date
        swap_rate = elem.rate
        end_dates_list.append(end_date)
        swap_rates_list.append(swap_rate)
        
    swap_reset_dates = []
    interpol_swap_rates_list = []
    
    for i in range(size_swap_consecutive_tenors):
        
        tenor = swap_consecutive_tenors[i]
        tenor = round(tenor)*360 #converting to an even number of days within a year divisible by 90
        number = round(tenor/90)
        upper_reset_date = end_dates_list[i+1]
        lower_reset_date = end_dates_list[i] 
        #swap_reset_dates.append(lower_reset_date)
        lower_swap_rate = swap_rates_list[i]
        #interpol_swap_rates_list.append(lower_swap_rate)
        upper_swap_rate = swap_rates_list[i+1]
        
        
        for j in range(1, number):
            
            reset_date = lower_reset_date + timedelta(days = j*91)                        
            interpol_swap_rate = interpolate_function(lower_reset_date, reset_date,\
                                                      upper_reset_date, lower_swap_rate,\
                                                      upper_swap_rate)
            swap_reset_dates.append(reset_date)            
            interpol_swap_rates_list.append(interpol_swap_rate)
            
        #interpol_swap_rates_list.append(upper_swap_rate)
        #swap_reset_dates.append(upper_reset_date)
        
    interpol_swap_rates_list_1 = list(interpol_swap_rates_list)
    swap_reset_dates_1 = list(swap_reset_dates)
    
    return interpol_swap_rates_list_1, swap_reset_dates_1
        
        
def interpolate_function (date1, date2, date3, lower_rate, upper_rate):
    
    #This is the linear interpolation function
    
    time_diff_1 = (date2 - date1)/timedelta(days=1)
    time_diff_2 = (date3 - date2)/timedelta(days=1)
    time_diff_3 = (date3 - date1)/timedelta(days=1)
    lower_rate = float(lower_rate)
    upper_rate = float(upper_rate)
       
    interpol_rate = (time_diff_1/time_diff_3)*upper_rate\
                     + ((time_diff_2/time_diff_3)*lower_rate)
    
    return interpol_rate
    
	
def get_future_object (dataframe, location):
    
    instrument_1 = 'Sf'
    future_list = identify_instr_type(dataframe, instrument_1)
    instrument_2 = 'Dg'
    dep_instr_list = identify_instr_type(dataframe, instrument_2)
    size_fut_list = len(future_list)
    size_dep_instr_list = len(dep_instr_list)
    df = get_instrument_details(location)
    df.set_index('Tp')
    condition = df['Tp'] == 'Sf'
    df1 = df.loc[condition]
    start_dates = df1['Adjusted Start date'].tolist()
    end_dates = df1['Adjusted Maturity'].tolist()
    future_price = df1['Market quote'].tolist()
    tenors = df1['Tenor'].tolist()
    generator_name = df1['Generator'].tolist()
    
    future_objects = []
    
    for i in range(size_fut_list):
        
        name = tenors[i] + ' ' + generator_name[i]
        start_date = start_dates[i]
        end_date = end_dates[i]
        price = float(future_price[i])
        fut_obj = ig.FutureInstrument(name, start_date, end_date, price)
        future_objects.append(fut_obj)
        
    return future_objects

def get_deposit_instrument (dataframe, location):
    
    instrument = 'Dg'
    dep_instr_list = identify_instr_type(dataframe, instrument)
    size_dep_instr_list = len(dep_instr_list)
    df = get_instrument_details(location)
    df.set_index('Tp')
    condition = df['Tp'] == 'Dg'
    df1 = df.loc[condition]
    start_dates = df1['Adjusted Start date'].tolist()
    end_dates = df1['Adjusted Maturity'].tolist()
    dep_rates = df1['Market quote'].tolist()
    tenors = df1['Tenor'].tolist()
    generator_name = df1['Generator'].tolist()
    
    deposit_objects = []
    
    for i in range(size_dep_instr_list):
        
        name = tenors[i] + ' ' + generator_name[i]
        start_date = start_dates[i]
        end_date = end_dates[i]
        rate = dep_rates[i]
        dep_obj = ig.DepositInstrument(name, start_date, end_date, rate)
        deposit_objects.append(dep_obj)
        
    return deposit_objects

def get_fra_instrument (dataframe, location):
    
    instrument_1 = 'Fr'
    fra_list = identify_instr_type(dataframe, instrument_1)
    instrument_2 = 'Dg'	      
    dep_instr_list = identify_instr_type(dataframe, instrument_2)
    size_fra_list = len(fra_list)
    size_dep_instr_list = len(dep_instr_list)
    df = get_instrument_details(location)
    df.set_index('Tp')
    condition = df['Tp'] == 'Fr'
    df1 = df.loc[condition]
    start_dates = df1['Adjusted Start date'].tolist()
    end_dates = df1['Adjusted Maturity'].tolist()
    fra_rate = df1['Market quote'].tolist()
    tenors = df1['Tenor'].tolist()
    generator_name = df1['Generator'].tolist()
    
    fra_objects = []
    
    for i in range(size_fra_list):
        
        name = tenors[i] + ' ' + generator_name[i]
        start_date = start_dates[i]
        end_date = end_dates[i]
        price = float(fra_rate[i])
        fra_obj = ig.FraInstrument(name, start_date, end_date, price)
        fra_objects.append(fra_obj)
        
    return fra_objects

def get_df_for_calibr_instr (df1, df2):
    
    '''
    This function allows one to obtain data for specific instruments (calibration
    instruments) with just supplying the two inputs, df1 (old_df) and df2(new_df).    
    '''
    
    size_df1 = int(df1.size/14) #14 is the current number of columns in df1. This might change.
    #index_list = list(range(size_df1))
    condition = df2.index <= size_df1 - 1
    new_df = df2.iloc[condition]
    
    return new_df

def get_swap_zero_rate (dataframe, swap_type):
    
    '''
    This function gets the calibration swap objects from the dataframe and 
    performs a conversion to zero rates.
    '''
    
    dataframe.set_index('Tp')
    condition = dataframe['Tp'] == swap_type
    df = dataframe.loc[condition]
    swap_dfs_list = df['Discount factor'].tolist()
    swap_start_date_list = df['Adjusted Start date'].tolist()
    swap_end_dates_list = df['Adjusted Maturity'].tolist() #This can be used to calcu the years to maturity.
    size_swap_df_list = len(swap_dfs_list)
    
    swap_zero_rates_list = []
    
    for i in range(size_swap_df_list):
        
        number_of_yrs = (swap_end_dates_list[i]\
                         - swap_start_date_list[i])/np.timedelta64(1, 'D')
        number_of_yrs = (number_of_yrs + 4)/365
        #number_of_yrs = round(number_of_yrs)
        ith_df = swap_dfs_list[i]
        expon_arg =1/(number_of_yrs*4)
        swap_zero_rate = (1/(ith_df**expon_arg) - 1)*400
        swap_zero_rates_list.append(swap_zero_rate)
        
    return swap_zero_rates_list
    
def get_forward_rates (dataframe, instrument_type):
    
    '''
    This function takes the dataframe for calibration instruments and calculates 
    the forward rates implied by the disc fact from this dataframe.
    '''
    
    dataframe.set_index('Tp')
    condition = dataframe['Tp'] == instrument_type
    new_df = dataframe.loc[condition]
    start_dates = new_df['Adjusted Start date'].tolist()
    end_dates = new_df['Adjusted Maturity'].tolist()
    disc_factr = new_df['Discount factor'].tolist()    
    size_colmns = len(disc_factr)

    
    foward_rates_list = []
    
    for i in range(1, size_colmns - 1):
        
        ith_date = end_dates[i]
        jth_date = end_dates[i+1]
        ith_dfs = disc_factr[i]
        jth_dfs = disc_factr[i+1]
        tau = (jth_date - ith_date)/timedelta(days=1)
        tau = tau/365
        next_fwd_rate = (ith_dfs/jth_dfs - 1)*(1/tau)
        foward_rates_list.append(next_fwd_rate)
        
    return foward_rates_list
    
def get_rates_difference (dataframe):

    calculated_zero_rates = dataframe['Zero rates'].tolist()
    murex_zero_rates = dataframe['Murex Zero rate'].tolist()
    size_colmn = len(calculated_zero_rates)
    rate_diff_list = []
    
    for i in range(size_colmn):
        
        rate_diff = float(murex_zero_rates[i]) - calculated_zero_rates[i]
        rate_diff_list.append(rate_diff)
        
    return rate_diff_list

def get_fra_fut_zero_rates (dataframe, instrument_type):
    
    '''
    This function performs the calculation of zero rates from the discount factor
    obtained from the dataframe of calibration instruments of a zero curve for     
    any country.
    '''
    
    dataframe.set_index('Tp')
    condition = dataframe['Tp'] == instrument_type
    new_df = dataframe.loc[condition]
    
    disc_fact = new_df['Discount factor'].tolist()
    end_dates = new_df['Adjusted Maturity'].tolist()
    size_colmn = len(end_dates)
    value_date = datetime.datetime(2018, 9, 6, 0, 0, 0)
    
    fra_zero_rates = []
    
    for i in range(size_colmn):
        
        ith_dfs = disc_fact[i]
        ith_end_date = end_dates[i]
        days_to_value_date = (ith_end_date - value_date)/timedelta(days=1)
        
        ith_fra_rate = (1/float(ith_dfs) - 1)*(365/days_to_value_date)
        ith_fra_rate = ith_fra_rate*100
        fra_zero_rates.append(ith_fra_rate)
        
    return fra_zero_rates
        
	
   
       
     
     

    


         
                    

	
	 



