# -*- coding: utf-8 -*-
"""
Created on Fri Dec  7 10:17:52 2018

@author: zwa

This script provides the OOP work on yield curve construction.
The classes defined here generate instruments (swaps, futures, fras, and deposit)
needed for constructing a zero curve.
"""
from datetime import timedelta
import datetime

class SwapInstrument ():
    
    def __init__ (self, name, swap_type, start_date, end_date, rate):
        
        self.name = name
        self.start_date = start_date
        self.end_date = end_date
        self.rate = rate
        self.swap_type = swap_type

    def get_tenor (self):

        start_date = self.start_date
        end_date = self.end_date
        tenor_1 = end_date - start_date
        tenor = tenor_1/timedelta(days = 1)

        return tenor

    
        
class FutureInstrument ():

	def __init__ (self, name, start_date, end_date, price):

		self.name = name
		self.start_date = start_date
		self.end_date = end_date
		self.rate = 100 - price

	def get_tenor (self):

		start_date = self.start_date
		end_date = self.end_date
		tenor_1 = end_date - start_date
		tenor = tenor_1/timedelta(days = 1)
     
      

		return tenor

class DepositInstrument ():

	def __init__ (self, name, start_date, end_date, rate):

		self.name = name
		self.start_date = start_date
		self.end_date = end_date
		self.rate = rate

	def get_tenor (self):

		start_date = self.start_date
		end_date = self.end_date
		tenor_1 = end_date - start_date
		tenor = tenor_1/timedelta(days = 1)
        

		return tenor


class FraInstrument ():

	def __init__ (self, name, start_date, end_date, rate):

		self.name = name
		self.start_date = start_date
		self.end_date = end_date
		self.rate = rate

	def get_tenor (self):

		start_date = self.start_date
		end_date = self.end_date
		tenor_1 = end_date - start_date
		tenor = tenor_1/timedelta(days = 1)

		return tenor
    
class InterpolatedSwapInstrument ():
    
    def __init__ (self, name, swap_type, start_date, end_date, rate):
       
        
        self.name = name
        self.start_date = start_date
        self.end_date = end_date
        self.rate = rate 
        self.swap_type = swap_type
        
    def get_tenor (self):
        
        start_date = self.start_date
        end_date = self.end_date
        tenor = end_date - start_date
        tenor = tenor/timedelta(days=1)
        
        return tenor
    
class Country ():
    
    '''
    The dictionary below holds information about a given country; be it its 
    day count convertion, location of the par rates for any curve relevant in 
    that country. The class Country defines functions able to retrieve such 
    information.
    '''
    
    country_details = {}
    
    country_details['usd'] = [360, 'usd_libor_3m.csv', '']
    country_details['eur'] = [360, 'eur_euribor_3m.csv', 'eur_fx.csv']
    country_details['gbp'] = [365, 'gbp_libor_3m.csv', 'gbp_fx.csv']
    country_details['zar'] = [365, 'zar_jibar_3m.csv', 'zar_fx.csv']
    country_details['bwp'] = [365, 'bwp_bobc_3m.csv', 'bwp_fx.csv']
    country_details['nad'] = [365, 'nad_ibor_3m.csv', ''] #empty string=no curve.
    
    def __init__ (self, currency):
        
        self.currency = currency
        
    def get_day_count_convention (self):
        
        currency = self.currency
        day_count_convent = Country.country_details[currency][0]
        
        return day_count_convent
    
    def get_zero_curve_location (self):
        
        #This gives out the location of the csv file containing details about 
        #the calibrating instruments.
        
        currency = self.currency
        csv_location = Country.country_details[currency][1]
    
        return csv_location
    
    def get_supporting_sheet_location (self):
        
        currency = self.currency
        csv_location = Country.country_details[currency][1]
        excel_location_1 = csv_location[:-4] + '_' + 'interpol.xlsx'
        excel_location_2 = csv_location[:-4] + '_' + 'calcs.xlsx'
        
        return excel_location_1, excel_location_2