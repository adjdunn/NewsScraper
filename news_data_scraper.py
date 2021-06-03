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



#Scrapes news release urls from a single webpage.
#Input (driver) is selenium scraper object.   
def get_news_links(driver):
    
    #Get page html
    html = driver.execute_script('return document.body.innerHTML;')
    soup = BeautifulSoup(html,'lxml')
    
    #Get table containing news releases. 
    news_table = soup.find('div', class_='press-releases-content')
    
    #Get list of news release rows.
    news_rows = news_table.findAll('td', class_='pr-headline')
    
    #Main page for news site. Append scraped uls to this str.
    main_page_url = 'https://stockhouse.com' 
    news_urls = [] #Array to store urls. 
    
    for row in news_rows:
        url = row.find('a')['href']
        full_url = main_page_url + url
        news_urls.append([full_url])
        
    return news_urls   



#Scrolls through series of webpages, scrapes news urls and saves output to csv file. 
def scroll_scrape_news():
    
    PATH = 'C:\Program Files (x86)\chromedriver.exe'
    driver = webdriver.Chrome(PATH)
    
    news_url_data = []  
    
    for page_num in range(1, 10):
        
        #webpage with news release urls. 
        news_url = "https://stockhouse.com/news/canadian-press-releases?page=%s" % (page_num)
        driver.get(news_url)
        
        page_urls = get_news_links(driver) #Extract urls from page. 
        news_url_data += page_urls #Add urls from page to array of urls.
        
    #Save urls to csv file.
    with open('news_url_data.csv', 'w', newline="") as f:
        w = csv.writer(f)
        w.writerows(news_url_data)
     
    return news_url_data





#Scrapes individual news article.
def get_news_article(url):
    pass



#Processes text from individual article into seperate sentences. 
def process_article():
    pass





