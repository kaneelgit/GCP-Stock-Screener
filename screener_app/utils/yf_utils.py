import pandas as pd
import requests, time, re, os
from datetime import datetime
import numpy as np
import yfinance as yf

#performs Linear regression 
def stock_info(stock):
    """
    Inputs stock name and returns stock information.
    """
    #create dictionary to store data
    stock_details = {}

    #initialize yf instance
    data = yf.Ticker(stock)

    #collect data
    stock_details['price_history'] = data.history()

    #put/call ratio
    p2c_ratio = []
    for expiration in data.options:

        options = data.option_chain(expiration)
        put_volume = options.puts['volume'].sum()
        call_volume = options.calls['volume'].sum()
        p2c_ratio.append((expiration, put_volume/call_volume))


    stock_details['p2c_ratio'] = p2c_ratio

    #recommendations
    df_rec = data.recommendations
    rec_count = df_rec.value_counts('To Grade')
    stock_details['recommendations'] = rec_count

    #price targetrs
    stock_details['price_targets'] = data.analyst_price_target
    
    return stock_details
