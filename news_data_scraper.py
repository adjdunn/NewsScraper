# -*- coding: utf-8 -*-
"""
Created on Thu Jun  3 10:47:47 2021

@author: aaron
"""

# =============================================================================
# This module scrapes, cleans and preps text from news articles and to be 
# used as the dataset for a news classifier / ranking app.  
# =============================================================================

from selenium import webdriver
from bs4 import BeautifulSoup
import csv
from nltk.tokenize import sent_tokenize
import pandas as pd



#Scrapes news release urls from a single webpage.
#Input (driver) is selenium scraper object.   
def get_news_links(driver):
    
    #Get page html
    html = driver.execute_script('return document.body.innerHTML;')
    soup = BeautifulSoup(html,'lxml')
    
    #Get table containing news releases. 
    news_table = soup.find('div', class_='press-releases-content')
    
    if news_table != None: #The webpage contained news content.
        
        #Get list of news release rows.
        news_rows = news_table.findAll('td', class_='pr-headline')
        
        #Main page for news site. Append scraped uls to this str.
        main_page_url = 'https://stockhouse.com' 
        news_urls = [] #Array to store urls. 
        
        for row in news_rows:
            url = row.find('a')['href']
            full_url = main_page_url + url
            news_urls.append([full_url])
            
    else: #The webpage was empty.
        news_urls = None
        
    return news_urls   




#Scrolls through series of webpages, scrapes news urls and saves output to csv file. 
def scroll_scrape_news(start_date, end_date):
    """Inputs: (str) in format: month-day-year.
    """
    
    PATH = 'C:\Program Files (x86)\chromedriver.exe'
    driver = webdriver.Chrome(PATH)
    
    news_url_data = [] #Array to store news urls. 
    
    list_of_dates = pd.date_range(start=start_date, end=end_date) #Dates to scrape news. 
    
    for date in list_of_dates:
    
        for page_num in range(1, 100):
            
            #webpage with news release urls. 
            news_url = "https://stockhouse.com/news/canadian-press-releases?page=%s&sdate=%s" % (page_num, date)
            driver.get(news_url)
            
            page_urls = get_news_links(driver) #Extract urls from page.
            
            if page_urls == None: #Exit loop if no more pages to scrape. 
                break
            
            news_url_data += page_urls #Add urls from page to array of urls.
            
    #Save urls to csv file.
    with open('news_url_data.csv', 'w', newline="") as f:
        w = csv.writer(f)
        w.writerows(news_url_data)
     
    return news_url_data



#Scrapes and sentence tokenizes individual news article.
def get_news_article(url):
    """
    Input is html link (str) for text document.
    
    Returns a list of lists containing the individual sentences in the text
    document. 
    """
    PATH = 'C:\Program Files (x86)\chromedriver.exe'
    driver = webdriver.Chrome(PATH)
    
    driver.get(url)

    html = driver.execute_script('return document.body.innerHTML;')
    soup = BeautifulSoup(html, 'lxml')
    
    body = soup.find('body')
    
    #Seperate paragraphs. 
    paragraphs = [para.get_text() for para in body.findAll('p')]
    
    #Add periods so that all segments of bulleted text will be treated 
    #like sentences. 
    paragraphs_seperated = []
    for p in paragraphs:
        
        if len(p) > 0:
            if p[-1] != '.':
                sentence = p+'.'
            else:
                sentence = p
                
            paragraphs_seperated.append(sentence)
    
    doc = ' '.join(p for p in paragraphs_seperated)
    
    #Divide document into sentences. 
    sentences = sent_tokenize(doc)
        
    return sentences








