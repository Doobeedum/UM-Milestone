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

news = pd.read_csv('news.csv', encoding = "ISO-8859-1")
news.set_index('date', inplace=True)
polarity = pd.read_csv('polarity.csv')
    

exceldir = './stock/stock'
companies = os.listdir(exceldir) 
company=[]
count=0
for excel in companies:
    company = excel[5:-11]
    company = company.replace(" Bhd","")
    company = company.replace("(Malaysia)","")
    company = company.replace("(M)","")
    company = company.replace("Ltd","")
    count +=1
    print(count,company, excel)

    stock = pd.read_csv( exceldir+'/'+excel, index_col = 'Date')

    
    stock.rename({"Unnamed: 0":"a"}, axis="columns", inplace=True)
    stock.drop(["a"], axis=1, inplace=True)
    
    df1 = stock[['Close']] ##include variable that we need
    df2 = df1.pct_change()   ##Percentage change between the current and a prior element.
    df2.columns = ['Return']
    df2 = df2.replace([np.inf, -np.inf], np.nan)  ##replace infinity number into NaN
    df3 = df2.dropna()    

    stock=pd.concat([stock, df3], axis=1, sort=False)
    
    list = np.flatnonzero((news==company).values)//polarity.shape[1]
        
    if len(list) <=10: continue
    
    rows = []
    for i in range(len(list)):
        rows.append(list[i])
    
    selected_news =polarity.copy()
    selected_news .drop(selected_news .index, inplace=True)
    
    for i in rows:
        selected_news = selected_news.append(polarity.iloc[[i]],ignore_index=True)
    
    dftest = selected_news[['classify_news','date2']]
    
    dftemp = dftest.copy()
    
    dftemp = dftemp.drop_duplicates(subset='date2')
    
    dftemp = dftemp.reset_index()
    
    dftemp = dftemp.drop(['index'], axis = 1) 
    
    final = pd.DataFrame()
    
    for i in range(len(dftemp["date2"])):
            positive = 0
            neutral = 0
            negative = 0
            for j in range(len(dftest["date2"])): 
                date1 = dftemp.loc[i,"date2"]
                date2 = dftest.loc[j,"date2"]
                if date1 == date2:
                    if dftest.loc[i,"classify_news"] == 'positive':
                        positive +=1
                    if dftest.loc[i,"classify_news"] == 'neutral':
                        neutral +=1
                    if dftest.loc[i,"classify_news"] == 'negative':
                        negative +=1
            total = positive - negative
            if total > 0: score = 'good'
            if total == 0: score = 'neutral'
            if total < 0: score = 'bad'
            final = final.append({"date":date1,"positive":positive, "neutral":neutral,"negative":negative,"total":total, "score":score},ignore_index=True)
            
    final = final.set_index('date')
    
    result = pd.concat([stock, final], axis=1, sort=False)
    result =result.dropna(subset=['Close'])
    result.to_csv('./stock/done/'+excel)

    
