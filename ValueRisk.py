import bs4 as bs
import urllib.request
import pandas as pd
import sys
import csv
import os, fnmatch
import numpy as np
import time
from datetime import datetime
from textblob import TextBlob
import talib as ta

pip install ta-lib
    
data=pd.DataFrame(columns=["Company", "VaR at 95","loss at 95","VaR at 99","loss at 99"])

exceldir = './stock/done'
companies = os.listdir(exceldir) 
company=[]
count=0
for excel in companies:
    stock = pd.read_csv( exceldir+'/'+excel, index_col = 'Date')    



    stock['EMA10'] = ta.EMA(stock['Settle'].values, timeperiod=10)
    stock['EMA30'] = ta.EMA(stock['Settle'].values, timeperiod=30)
    stock['ATR'] = ta.ATR(stock['High'].values, stock['Low'].values, stock['Settle'].values, timeperiod=14)
    stock['ADX'] = ta.ADX(stock['High'].values, stock['Low'].values, stock['Settle'].values, timeperiod=14)
    stock['RSI'] = ta.RSI(stock['Settle'].values, timeperiod=14)
    macd, macdsignal, macdhist = ta.MACD(stock['Settle'].values, fastperiod=12, slowperiod=26, signalperiod=9)
    stock['MACD'] = macd
    stock['MACDsignal'] = macdsignal
    stock.tail()
    sys.exit()


    data.to_csv('VAR.csv')

    


#
#    at99= stock.Return.quantile(0.01)
#    at95= stock.Return.quantile(0.05)
#    print (at99,at95)
#    val99 = at99 * 1000
#    val95 = at95 * 1000
#    data = data.append({"Company":excel, "VaR at 99":at99,"loss at 99":val99,"VaR at 95":at95,"loss at 95":val95},ignore_index=True)