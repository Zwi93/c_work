# -*- coding: utf-8 -*-
"""
Created on Wed Dec 12 10:39:58 2018

@author: zwa
Below is the code for bootstrapping a curve from a list of different instruments.
The instruments are defined in another class and only come in the form of 
input to our class.
"""

import datetime 
from datetime import timedelta
import statistics as stats
import math
from decimal import Decimal, getcontext
getcontext().prec = 14
import numpy as np
import Bootstrapper_Helper_Function as bhf
from Instrument_Generator_Class import Country

country_currency = 'zar'
country_object = Country(country_currency)
location = country_object.get_zero_curve_location()
spreadsheet_path1 = country_object.get_supporting_sheet_location()[0]
spreadsheet_path2 = country_object.get_supporting_sheet_location()[1]
day_count_conv = country_object.get_day_count_convention()

class ZeroCurve ():

    '''
    This class contains the tools used to perform bootstrapping on a given curve.
    The input curve may have fra or futures instruments as input. This is accounted 
    for in the definitions of get_fra_dfs and get_future_dfs functions.
    '''
    
    value_date = datetime.datetime(2018, 9, 6, 0, 0, 0)
   
    
    def __init__ (self, curve_name, deposit_obj, future_obj, fra_obj, swap_obj):
        
        self.curve_name = curve_name
        self.depo_obj = deposit_obj
        self.fut_obj = future_obj
        self.fra_obj = fra_obj
        self.swap_obj = swap_obj
        
        
    def get_swap_dfs (self):
        
        swaps_list = self.swap_obj
        size_swaps_list = len(swaps_list)
        
        if self.fut_obj == [] and self.fra_obj != []:
            
            #In this case, there are some FRAs which are not relevant for the
            #computation of further swap discount factors;1*4, 2*5, 4*7 months.
            instrument_list = self.fra_obj
            size_instru_list = len(instrument_list)
            instrument_dfs_array_0 = self.get_fra_dfs()
            instrument_dfs_array = [instrument_dfs_array_0[0]]
            
            relevant_indices = [3, 6, 9, 10, 11, 12, 13]
            
            for ii in relevant_indices:
                
                relevant_elem = instrument_dfs_array_0[ii]
                instrument_dfs_array.append(relevant_elem)
            
            instrument = 'Fr'
            first_reset_date = instrument_list[-2].end_date #only valid if size of instrument_list is > 1.
            second_reset_date = instrument_list[-1].end_date
            df = bhf.get_instrument_details(location)
            df0 = df.set_index('Tenor')
            #irrelevant_fra_tenors = ['1M-4M','2M-5M','4M-7M','5M-8M','7M-10M','8M-11M']
            relevant_fra_tenors = ['3M-6M','6M-9M','9M-12M','12M-15M','15M-18M','18M-21M','21M-24M']
            df1 = df0.loc[relevant_fra_tenors]
            #consecutive_tenors_instrum = bhf.get_consecutive_tenors(instrument, df1, location)
            consecutive_tenors_instrum = [0.25,0.25,0.2489, 0.25, 0.25, 0.25]
            swap_df_array_0 = instrument_dfs_array_0 #keeping track of full fra_dfs list
            
        if self.fut_obj != [] and self.fra_obj == []:
            
            instrument_list = self.fut_obj
            size_instru_list = len(instrument_list)
            instrument_dfs_array = self.get_future_dfs()
            instrument = 'Sf'
            first_reset_date = instrument_list[-2].end_date #only valid if size of instrument_list is > 1.
            second_reset_date = instrument_list[-1].end_date
            df = bhf.get_instrument_details(location)
            consecutive_tenors_instrum = bhf.get_consecutive_tenors(instrument, df, location)
            swap_df_array_0 = instrument_dfs_array

        #We have to handle the case where both self.fut_obj and self.fra_obj are empty.

        if self.fut_obj == [] and self.fra_obj == []:

            instrument_list = self.depo_obj
            size_instru_list = len(instrument_list)
            instrument = 'Dg'
            df = bhf.get_instrument_details(location)
            consecutive_tenors_instrum = bhf.get_consecutive_tenors(instrument, df, location)
            

            if size_instru_list == 1:

                instrument_dfs_array = []
                swap_df_array_0 = instrument_dfs_array #This is to be extended further.

            else:

                #We have to interpolate the rate between the last depo instrument
                #and the first swap.
                instrument_dfs_array = self.get_deposit_dfs()
                swap_df_array_0 = instrument_dfs_array
                last_instru_rate = float(instrument_list[-1].rate)
                first_swap_rate = float(swaps_list[0].rate) 
                mean_rate = (last_instru_rate + first_swap_rate)/2
                mean_rate = mean_rate/100
                #date_increment = (swaps_list[0].end_date -\
                #                  instrument_list[-1].end_date)/timedelta(days=1)
                
                #date_increment = date_increment/2
                mean_date = (instrument_list[-1].end_date + \
                             timedelta(days=91)
                             )
                tau = (mean_date - ZeroCurve.value_date)/timedelta(days=1)
                tau = tau/day_count_conv
                interpol_dfs = (1/(1 + mean_rate*tau))
                instrument_dfs_array.append(interpol_dfs)
                swap_df_array_0.append(interpol_dfs)
                first_reset_date = instrument_list[-1].end_date 
                second_reset_date = mean_date
                
                
        
        swap_df_array = instrument_dfs_array
        
        #First i had to extrapolate the discount factors from the ones obtained from
        #fras/futures.
       
        
        first_df = instrument_dfs_array[-2]
        second_df = instrument_dfs_array[-1]

        first_swap = swaps_list[0]
        first_swap_end_date = first_swap.end_date
        end_date = first_swap.end_date
        number = (first_swap_end_date - second_reset_date)/timedelta(days=1)
        number = round(number/91)
        #The function substract cannot operate on operands of different type.
        
        if number == 1:
            
            swap_reset_dates = [second_reset_date]
            
        else:
                
            swap_reset_dates = []    
        
        
        #The next step is to handle the interpolation at the point where the 
        #instrument changes type; i.e from fra/fut to swap.
        
        for i in range(number - 1):
            
            following_reset_date = second_reset_date + timedelta(days = (i+1)*91)
            time_diff_1 = (second_reset_date - first_reset_date)/timedelta(days=1)
            time_diff_2 = (following_reset_date - second_reset_date)/timedelta(days=1)
            time_diff_3 = (following_reset_date - first_reset_date)/timedelta(days=1)
            
            following_df = ((time_diff_3/time_diff_1)*second_df - \
                            (time_diff_2/time_diff_1)*first_df)
            
            swap_reset_dates.append(following_reset_date)
            swap_df_array.append(following_df)
            swap_df_array_0.append(following_df)
            consecutive_tenors_instrum.append(0.25)
        
        
        
        instru_dfs = swap_df_array[2:] #removing the depo and first fra/fut df.
        time_diff_4 = (instrument_list[0].end_date - ZeroCurve.value_date)/timedelta(days=1)
        time_diff_4 = time_diff_4/day_count_conv
        dotprod_instr_df_tenors = (np.vdot(instru_dfs, consecutive_tenors_instrum) + \
                                   swap_df_array[1]*(time_diff_4)\
                                    )#The last term is to include the contribution
        #of the first instrument disc factr, represented by swap_df_array[1].
        #and also instrument_list[0]
                                                   
        swap_rate = float(first_swap.rate)        
        swap_rate = swap_rate/100
        swap_tenor = (end_date - swap_reset_dates[-1])/timedelta(days=1)
        swap_tenor = swap_tenor/day_count_conv
        first_df = (1 - swap_rate*dotprod_instr_df_tenors)/(1 + swap_rate*swap_tenor)
        swap_df_array.append(first_df)
        swap_df_array_0.append(first_df)

        consecutive_tenors_swaps = []

        for i in range(size_swaps_list - 1):

            jth_swap = swaps_list[i+1]
            ith_swap = swaps_list[i]
            ith_swap_end_date = ith_swap.end_date
            jth_swap_end_date = jth_swap.end_date
            tenor_diff = (jth_swap_end_date - ith_swap_end_date)/np.timedelta64(1, 'D')
            tenor_diff = tenor_diff/day_count_conv
            consecutive_tenors_swaps.append(tenor_diff)

        
        size_swap_df_array = len(swap_df_array)
        new_swap_df_array = swap_df_array
        
        for i in range(1, size_swaps_list):
           
           ith_swap = swaps_list[i]
           
           ith_swap_rate = float(ith_swap.rate)
           ith_swap_rate = ith_swap_rate/100
           tau = consecutive_tenors_swaps[:i]
           ith_dfs_list = new_swap_df_array[size_swap_df_array - 1:i + size_swap_df_array - 1]
           
           df_tau_dotprod = np.vdot(tau, ith_dfs_list) + dotprod_instr_df_tenors
 
           #sum_swap_dfs = float(sum(swap_df_array))
           next_df = (float(1) - (ith_swap_rate)*df_tau_dotprod)/(float(1) + ith_swap_rate*tau[-1])
           new_swap_df_array.append(next_df)
           swap_df_array_0.append(next_df)
       
        del new_swap_df_array[size_instru_list: number - 1 + size_instru_list]
        del swap_df_array_0[size_instru_list: number - 1 + size_instru_list]
        
        if (self.fut_obj == [] and self.fra_obj == []) and size_instru_list > 1 :
        
                del new_swap_df_array[size_instru_list + number] #Only in the case of no future and fra objects.
                del swap_df_array_0[size_instru_list + number]
   
        return swap_df_array_0
    
    def get_future_dfs (self):
        
        fut_list = self.fut_obj
        
        if fut_list == []:
           future_dfs_array = []
           global future_rates_array_1 
           future_rates_array_1 = []
           print('There is no futures instrument')
            
        else:
            
            fut_rates_list = []
            
            for elem in fut_list[:4]:
                rate = elem.rate
                rate = rate/100
                fut_rates_list.append(rate)
            
            size_fut_list = len(fut_list)
            depo_list = self.depo_obj
        
            sigma = stats.stdev(fut_rates_list)
            init_rate = float(depo_list[-1].rate)
            init_rate = init_rate /100
            depo_dfs_array = self.get_deposit_dfs()
        
            future_rates_array = [init_rate]
            equivalent_fra_rates = []
            
            for i in range(size_fut_list):
            
                ith_future = fut_list[i]
                ith_fut_rate = ith_future.rate #This is on an actual/360 basis compounded quartely.
                ith_fut_tenor = ith_future.get_tenor()
            
                end_date = ith_future.end_date            
                start_date = ith_future.start_date
                t1 = start_date - ZeroCurve.value_date
                t1 = t1/timedelta(days = 1)
                t1 = t1/day_count_conv  #converting t1 to number of years
                t2 = end_date - ZeroCurve.value_date
                t2 = t2/timedelta(days = 1)
                t2 = t2/day_count_conv
                ith_fut_rate_new = (365/ith_fut_tenor)*math.log(1 + ith_fut_rate/4)
                convexity_adj = ((sigma**2)*t1*t2)/2
                convexity_adj = convexity_adj*100 #converting to percentage form
                ith_fra_rate = ith_fut_rate_new - convexity_adj
                ith_fra_rate = ith_fra_rate/100 #This rate is in naca form
                next_fra_zero_rate = (ith_fra_rate*(t2 - t1)\
                                      + future_rates_array[i]*t1)/t2
                
                                      
                equivalent_fra_rates.append(ith_fra_rate)
            
                future_rates_array.append(next_fra_zero_rate)
                
            future_rates_array = np.array(future_rates_array)*100

            global future_rates_array_2
            future_rates_array_2 = list(future_rates_array[1:])
            
           
            future_dfs_array = depo_dfs_array 
            
            first_equiv_fra_rate = equivalent_fra_rates[0] #nominal annual compounded annually
            first_future = fut_list[0]
            depo_instr = depo_list[0]
            start_date = depo_instr.start_date
            end_date = first_future.end_date
            
            tau = (end_date - start_date)/timedelta(days=1)
            tau = tau/day_count_conv
            first_fut_df = future_dfs_array[-1]/(1 + first_equiv_fra_rate*tau)
            
            future_dfs_array.append(first_fut_df)
            
            for i in range(1, size_fut_list):
                
                ith_future = fut_list[i]
                ith_equiv_fut_rate = equivalent_fra_rates[i]
                start_date = fut_list[i - 1].end_date
                end_date = ith_future.end_date
                
                tau = (end_date - start_date)/timedelta(days=1)
                tau = tau/day_count_conv
                next_df = future_dfs_array[i]/(1 + tau*ith_equiv_fut_rate)
                future_dfs_array.append(next_df)
                
        #future_dfs_array = future_dfs_array[1:] 
            
        return future_dfs_array
                
                            
    def get_deposit_dfs (self):
        
        
        
        depo_list = self.depo_obj
        size_depo_list = len(depo_list)
        
        depo_dfs_array = []
        
        for i in range(size_depo_list):
            
            depo_instrument = depo_list[i]
            depo_rate = float(depo_instrument.rate)
            depo_rate = depo_rate/100
            start_date = depo_instrument.start_date 
            days_to_value_date = (start_date -\
                                  ZeroCurve.value_date)/timedelta(days=1)
            depo_tenor = depo_instrument.get_tenor() + days_to_value_date
            day_count = (depo_tenor)/day_count_conv 
            depo_df = 1/(1 + day_count*depo_rate)
            #depo_df_continuous = math.exp(-(day_count*depo_rate))
            depo_dfs_array.append(depo_df)
        
        return depo_dfs_array

    def get_deposit_zero_rate (self):

        depo_list = self.depo_obj
        size_depo_list = len(depo_list)
        depo_dfs_list = self.get_deposit_dfs()

        depo_zero_rates = []
    
        for i in range(size_depo_list):

            depo_instrument = depo_list[i]
            ith_df = Decimal(depo_dfs_list[i])
            end_date = depo_instrument.end_date
            value_date = ZeroCurve.value_date
            depo_tenor = Decimal((end_date - value_date)/timedelta(days=1))
            depo_zero_rate = (1/ith_df - 1)*(day_count_conv/depo_tenor)
            depo_zero_rate = depo_zero_rate*Decimal(100)
            depo_zero_rates.append(depo_zero_rate)

        return depo_zero_rates


    def get_fra_zero_rates (self):
        
        fra_list = self.fra_obj
        depo_list = self.depo_obj
        depo_zero_rates = self.get_deposit_zero_rate()
        
        if fra_list == []:
            
            fra_rates_array = []
            print('There are no fra instruments' )
            
        else:
            
            fra_rates_array = depo_zero_rates
            first_fra = fra_list[0]
            first_fra_rate = Decimal(first_fra.rate)
            #first_fra_rate = first_fra_rate/400 #is it necessary to convert?
            first_fra_end_date = first_fra.end_date
            last_depo_instru = depo_list[-1]
            depo_zero_rate = Decimal(fra_rates_array[-1])
            #depo_zero_rate = depo_zero_rate/400
            depo_end_date = last_depo_instru.end_date
            t1 = (depo_end_date - ZeroCurve.value_date)/timedelta(days=365)
            t2 = (first_fra_end_date - ZeroCurve.value_date)/timedelta(days=365)    
            first_fra_zero_rate = (first_fra_rate*(t2 -t1) +\
                                   depo_zero_rate*t1)/t2
            
            fra_rates_array.append(first_fra_zero_rate)
            size_fra_list = len(fra_list)
            
            for i in range(1, size_fra_list):
                
                ith_fra = fra_list[i]
                ith_fra_rate = ith_fra.rate
                #ith_fra_rate = ith_fra_rate/400
                start_date = ith_fra.start_date
                end_date = ith_fra.end_date
                t1 = start_date - ZeroCurve.value_date
                t1 = t1/timedelta(days=365)
                
                t2 = end_date - ZeroCurve.value_date
                t2 = t2/timedelta(days=365)
                
                
                next_fra_rate = (ith_fra_rate*(t2 - t1) +\
                                 fra_rates_array[i]*t1)/t2
                
                fra_rates_array.append(next_fra_rate)
            fra_rates_array = np.array(fra_rates_array)
                
        return fra_rates_array[1:]
    
    def get_fra_dfs (self):
        
        fra_list = self.fra_obj
        depo_dfs_array = self.get_deposit_dfs()
        
        if fra_list == []:
            
            fra_dfs_array = []
            print('There are no fra instruments' )
            
        else:
            
            fra_dfs_array = depo_dfs_array
            size_fra_list = len(fra_list)
            depo_list = self.depo_obj
            
            first_fra = fra_list[0]
            first_fra_rate = first_fra.rate
            first_fra_rate = first_fra_rate/100
            depo_instr = depo_list[-1]
            start_date = first_fra.start_date
            end_date = first_fra.end_date
        
            tau = (end_date - start_date)/timedelta(days=1)
            tau = tau/day_count_conv
            first_fra_df = fra_dfs_array[-1]/(1 + first_fra_rate*tau)
            
            fra_dfs_array.append(first_fra_df)
            
        
            
            for i in range(1, size_fra_list):
                
                ith_fra = fra_list[i]
                ith_fra_rate = ith_fra.rate
                ith_fra_rate = ith_fra_rate/100
                start_date = fra_list[i-1].end_date
                end_date = ith_fra.end_date
                
                tau = (end_date - start_date)/timedelta(days=1)
                tau = tau/day_count_conv
                next_df = fra_dfs_array[i]/(1 + tau*ith_fra_rate)
                fra_dfs_array.append(next_df)
                
        return fra_dfs_array

    def get_future_rate(self):

        self.get_future_dfs()
        return future_rates_array_2
           

    
    
        
        
                    
    
    
    

       
        
                      
    
           
        
        
