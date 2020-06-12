# -*- coding: utf-8 -*-
"""
Created on Thu Jan 31 11:49:38 2019

@author: zwa
"""

import datetime 
from datetime import timedelta
import statistics as stats
import math
import numpy as np
import Bootstrapper_Helper_Function as bhf

fx_curves_list = ['zar_fx.csv', 'eur_fx.csv']


class FxBasisCurve ():

    '''
    This class is a prototype for a given fx basis curve. It has the definitions for
    the relevant bootstrapping techniques performed on the basis curve calibration 
    instruments. It interacts with instances of other classes, which come as inputs 
    to its __init__ function.
    '''
    
    value_date = datetime.datetime(2018, 9, 6, 0, 0, 0)
    location = fx_curves_list[0]

    def __init__ (self, curve_name, fx_swap_obj, fx_basis_swap_obj):
        
        self.curve_name = curve_name
        self.fx_swap_obj = fx_swap_obj
        self.fx_basis_swap_obj = fx_basis_swap_obj
        