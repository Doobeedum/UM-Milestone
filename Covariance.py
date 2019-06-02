import numpy as np
import os
import pandas as pd
import datetime as dt
#import time
#import pymysql
from datetime import timedelta
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter

directory= r"C:\Users\Baqar\OneDrive\Desktop\UM\Data Mining\30-3-19"


def vol_clean(x):
    if x =="-":
        x = 0
    elif x[-1]=="K":
        x  = float(x[:-1])*1000
    elif x[-1]=="M":
        x  = float(x[:-1])*1000000
    return x
def cleaning(file):
    file.columns = ["Date","Close","Open","High","Low","Volume","Change"]
    file['Volume']=file['Volume'].apply(lambda x: vol_clean(x))
    file['Date'] = pd.to_datetime(file.Date).dt.strftime('%Y-%m-%d')
    file['Close'] = file['Close'].apply(lambda x:float((x.replace(",",""))))
    file['Open'] = file['Open'].apply(lambda x:float((x.replace(",",""))))
    file['Low'] = file['Low'].apply(lambda x:float((x.replace(",",""))))
    file['High'] = file['High'].apply(lambda x:float((x.replace(",",""))))
    return file

def cleaning_idx(file):
    file.columns = ["Date","Close","Open","High","Low","Volume","Change"]
    file['Volume']=file['Volume'].apply(lambda x: vol_clean(x))
    file['Date'] = pd.to_datetime(file.Date).dt.strftime('%Y-%m-%d')
    file['Close'] = file['Close'].apply(lambda x:float((x.replace(",",""))))
    file['Open'] = file['Open'].apply(lambda x:float((x.replace(",",""))))
    file['Low'] = file['Low'].apply(lambda x:float((x.replace(",",""))))
    file['High'] = file['High'].apply(lambda x:float((x.replace(",",""))))
    return file

index = pd.read_csv(r"C:\Users\Baqar\OneDrive\Desktop\UM\Data Mining\FTSE Malaysia KLCI Historical Data.csv")  
index=cleaning_idx(index)
index['Return']= index['Close'].pct_change()
index=index.sort_values('Date',ascending=True)
index['indexReturn']= index['Return']
index= index.drop([ 'Close', 'Open', 'High', 'Low', 'Volume','Change','Return'],axis=1)
index['Date']= pd.to_datetime(index.Date)
index = index[index['Date']>=dt.datetime(2018,1,1)]
index= index.sort_values("Date",ascending=True)

snp =  pd.read_csv(r"C:\Users\Baqar\OneDrive\Desktop\UM\Data Mining\S&P 500 Historical Data.csv")  
snp=cleaning_idx(snp)
snp['Return']= snp['Close'].pct_change()
snp=snp.sort_values('Date',ascending=True)
snp['snpReturn']= snp['Return']
snp= snp.drop([ 'Close', 'Open', 'High', 'Low', 'Volume','Change','Return'],axis=1)
snp['Date']= pd.to_datetime(snp.Date)
snp['Date'] = snp['Date']-timedelta(days=1)
snp = snp[snp['Date']>=dt.datetime(2018,1,1)]
snp= snp.sort_values("Date",ascending=True)
index= pd.merge(index,snp,on='Date',how='left').fillna(0)



for i in range(len(os.listdir(directory))):
    file = os.listdir(directory)[i]
    file_name = file[:-4]
    f = pd.read_csv(os.path.join(directory,file))
    f=f.drop("Unnamed: 0",axis=1)
    f['Date'] = pd.to_datetime(f['Date'])
    f= f.sort_values('Date',ascending=True)
    f = f[f['Date']>=dt.datetime(2018,1,1)]
    
    f['Change'] = f['Close'].pct_change()
    f=f.fillna(0)
    f = f.drop(['Close', 'Open', 'High', 'Low', 'Volume'],axis=1)
    index= pd.merge(index,f,on='Date',how='left').fillna(0)
    index[file_name] = index['Change']
    index=index.drop('Change',axis=1)

covar = index.cov()    
covar.to_pickle(r"C:\Users\Baqar\OneDrive\Desktop\UM\Data Mining\covar.pkl")
corr = index.corr()

corr = corr.fillna(0)
evalues ,evectors = np.linalg.eig(covar)

#The EigenVectors of the covariance matrix is the Principal Components

#klci = pd.read_csv(r"C:\Users\Baqar\OneDrive\Desktop\UM\Data Mining\FTSE Malaysia KLCI Historical Data.csv")  
#klci= cleaning_idx(klci)
#index=index.sort_values('Date',ascending=True)
#fig = plt.figure()
#klci['Close'].plot(x= klci['Date'] , y = klci['Close'])