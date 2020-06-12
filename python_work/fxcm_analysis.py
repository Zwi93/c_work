"""

date created : 2020/06/08
Author : Zwi Mudau

script written to perform rudimentary analysis on the fxcmpy wrapper package. 

"""

#import standard modules.
import fxcmpy
import numpy as np
import pandas as pd


rest_token_key = 'baf6d9afcbd8ac0c6523ff037437113376923ed7' #Key for the demo account to connect to demo servers.

#REST API object created here.
rest_api = fxcmpy.fxcmpy(access_token = rest_token_key, log_level = 'error')
#instruments = rest_api.get_instruments()
my_accounts = rest_api.get_accounts()
rest_api.close()
print(my_accounts)