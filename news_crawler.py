import bs4 as bs
import urllib.request
import pandas as pd
import sys
import csv
import os, fnmatch

import time

#from selenium import webdriver
#from selenium.webdriver.support.ui import WebDriverWait
#chrome = r"/Users/siuhongnai/Documents/chromedriverpath/chromedriver"
#driver = webdriver.Chrome(executable_path = chrome)



edge_home  = "https://www.theedgemarkets.com/categories/corporate?page="
#edge_links = []

links = []
title = []
useful_links = []
date = []
count =0

companies = os.listdir('./stock') 
for i in range(0, len(companies)):
    companies[i] = companies[i][5:-11]
    companies[i] = (companies[i].replace(" Bhd",""))
    companies[i] = (companies[i].replace("(Malaysia)",""))
    companies[i] = (companies[i].replace("(M)","")) 
    companies[i] = (companies[i].replace("Ltd","")) 
#    print (i,companies[i])
#    count +=1


#print (comp)
#sys.exit()



first= ["links","title","articles","date"]
with open('updated.csv', 'w',newline='') as csvFile:
    writer = csv.writer(csvFile)
    writer.writerow(first)

df=pd.DataFrame(columns=["links","title","articles","date"])
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
reg_url = "https:XXXXOOOO"

for i in range(881,2023):
    useful_links = []
    arti=1
    the_edge=edge_home+str(i)
    req = urllib.request.Request(url=the_edge, headers=headers) 
    html = urllib.request.urlopen(req).read() 
    print('page',i)
    #edge_links.append(the_edge)
    
# for items in edge_links:
#     driver.get(items)
    time.sleep(5)
#     html = driver.page_source
    edge = bs.BeautifulSoup(html,'lxml') 
#64
    #========================== Scrapped Links================================================
    links=[]
    section = edge.find("div",attrs={"class":"views-view-grid cols-3"})
    for url in section.find_all('a'): 
        links.append(url.get('href'))
#    print (useful_links)
    for i in range(0,len(links)):
        try:
            if '/article' in links[i]:
                
#                print (links[i])
                if links[i] != links[i-1]:                    
                    useful_links.append(links[i])
                    useful_links= list(dict.fromkeys(useful_links))
                        
        except:
            pass
#    print (useful_links)
#    sys.exit()
    for link in useful_links:
#        print (link)
        req = urllib.request.Request("http://www.theedgemarkets.com"+link,headers=headers)
        response = urllib.request.urlopen(req).read()
        article= bs.BeautifulSoup(response,'lxml')
        title=(article.find("meta", {"property":"og:title"})['content'])
        content = article.find('article', attrs={"class":"node node-article und post post-large blog-single-post"})
#        print (content)
#        sys.exit()
        date = content.find('span', attrs={"class":"post-created"}).get_text()
        date = date[:-6]
#        print (title,date)
#        print(comp)
        

        for paragraph in article.find_all('article', attrs={"class":"node node-article und post post-large blog-single-post"}):
            
            
                
            matched = [i for i in companies if i in paragraph.text.strip()]
            if matched:
                row=[link,title,paragraph.text.strip(),date]
                for i in matched:
                    row.append(i)
                print (arti,title)
                with open('updated.csv', 'a',newline='') as csvFile:
                    writer = csv.writer(csvFile)
                    writer.writerow(row)
            else:
                print(arti)
            arti +=1
    sys.exit()
csvFile.close()
#df.to_csv("the_edge_articles.csv")

