# -*- coding: cp1252 -*-
# 2015 ©Jayant Jaiswal. All rights reserved. 
# This program gathers the links for the first person in the SET's from
# different news sites, downlaod's the data for further processing and saves
# it to a specific location under a specific name specified by the user in the
# program...


#Modules to be imported for crawling
from bs4 import BeautifulSoup as bs
import requests as rq
from selenium import webdriver as wb
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from itertools import combinations as comb
from pprint import pprint
from math import ceil
import csv
import os
import sys
import signal
import time
chromedriver="F:\Tools\chromedriver"

'''# This function checks for the presence of names in the soup text file
def validate_names(data,name):
    if name in data:
        return 'yes'
    return 'no'
'''
# Function to crawl a link
def crawl(link):
    try:
        check_sum=1
        r=rq.get(link)
        check_sum=0
    except:
        while check_sum==1:
            try:
                time.sleep(2)
                r=rq.get(link)
                check_sum=0
            except:
                print "HTTP Error"
    data=r.text
    soup=bs(data)
    return soup


# This function would return links to be crawled to gather data from FORBES
def forbes_fetch_links(string):
    url="http://www.forbes.com"
    pages = []
    to_return = []
    pages.append(url+"/search/?q="+'"'+string.replace(' ','+')+'"')
    soup=crawl(pages[0])
    pages.pop()
    for page in soup.find_all('li',attrs={'class':'page'}):
        page=page.findChild('a')
        try:
            pages.append(url+page.get('href'))
        except:
            print
    pages.reverse()
    while pages:
        soup=crawl(pages.pop())
        links=soup.find_all('h2')
        times=soup.find_all('time',attrs={'class':'date'})
        for link,time in zip(links,times):
            link=link.findChild('a')
            try:
                if int(time.get_text()[-4:])<=2008:
                    to_return.append(link.get('href'))
            except:
                print
    return to_return

# This function would returns  links to be crawled to gather data from NYTimes
def nytimes_fetch_links(string,driver):
    url='http://query.nytimes.com/search/sitesearch/?action=click&contentCollection&region=TopBar&WT.nav=searchWidget&module=SearchSubmit&pgtype=Homepage#/%22'
    date='%22/from19700101to20081231/'
    string=string.replace(' ','+')
    links_fetched = []
    check_sum=0
    try:
        driver.get(url+string+date)
        check_sum=1
        WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.XPATH,'//*[@id="main"]/div/div/div[1]/div[1]/div/div[1]/ul/li[2]/a')))
    except:
        while check_sum==1:
            try:
                driver.get(url+string+date)
                WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.XPATH,'//*[@id="main"]/div/div/div[1]/div[1]/div/div[1]/ul/li[2]/a')))
                check_sum=0
                print '\n\nReconnected...\n\n'
            except:
                print "Network Error... Trying to Reconnect..."
    time.sleep(5)
    try:
        while driver.find_element_by_xpath('//*[@id="searchPagination"]/a').text[:4]=='Next':
            try:
                links=driver.find_elements_by_xpath('//*[@id="searchResults"]/ol/li/div/h3/a')
            except:
                driver.refresh()
                time.sleep(5)
                links=driver.find_elements_by_xpath('//*[@id="searchResults"]/ol/li/div/h3/a')
            for link in links:
                if link.get_attribute('href') not in links_fetched:
                    links_fetched.append(link.get_attribute('href'))
                print link.get_attribute('href')
            driver.find_element_by_xpath('//*[@id="searchPagination"]/a').click()
            time.sleep(5)
            try:
                driver.find_element_by_xpath('//*[@id="searchPagination"]/a')
            except:
                driver.refresh()
                time.sleep(5)
    except:
        '''Do nothing...'''
    try:
        links=driver.find_elements_by_xpath('//*[@id="searchResults"]/ol/li/div/h3/a')
    except:
        driver.refresh()
        time.sleep(5)
        links=driver.find_elements_by_xpath('//*[@id="searchResults"]/ol/li/div/h3/a')
    for link in links:
        if link.get_attribute('href') not in links_fetched:
            links_fetched.append(link.get_attribute('href'))
    driver.quit()
    return links_fetched


# This function is general in sense that it crawls the links
#  returned by all the functions and puts them in a file at a path given in MAIN
def pages_crawl(links,file_path,set_name,site_name):
    links.reverse()
    if not os.path.exists(file_path+"\\"+set_name+"\\"+site_name):
        if not os.path.exists(file_path+'\\'+set_name):
            os.makedirs(file_path+'\\'+set_name)
        os.makedirs(file_path+"\\"+set_name+"\\"+site_name)
    path = file_path + '\\' + set_name + '\\' + site_name
    flink=open(path+r"\links.txt","w")
    i=1
    while links:
        link=links.pop()
        soup=crawl(link)
        print >>flink,str(i)+" "+link
        f=open(path+"\\"+str(i)+".txt","w")
        print >>f,link
        print >>f,'\n'
        print >>f,soup.get_text().encode('utf-8')
        f.close()
        i+=1
    flink.close()

# This function returns links to be crawled to gather data from BusinessInsider
def businessinsider_fetch_links(string,driver):
    check_sum=0
    links_fetched = []
    try:
        driver.get('http://www.businessinsider.com/?IR=C')
        check_sum=1
        WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[4]/div[1]/div/div[3]/div/ul[2]/div/li[3]/a[1]/i')))
    except:
        while check_sum==1:
            try:
                driver.get('http://www.businessinsider.com/?IR=C')
                WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[4]/div[1]/div/div[3]/div/ul[2]/div/li[3]/a[1]/i')))
                check_sum=0
            except:
                print "Network Error... Trying to Reconnect!!!"
    time.sleep(5)
    try:
        driver.find_element_by_xpath('/html/body/div[4]/div[1]/div/div[3]/div/ul[2]/div/li[3]/a[1]/i').click()
    except:
        time.sleep(2)
        driver.find_element_by_xpath('/html/body/div[4]/div[1]/div/div[3]/div/ul[2]/div/li[3]/a[1]/i').click()
    try:
        driver.find_element_by_xpath('/html/body/div[4]/div[2]/div/form/input').send_keys('"'+string+'"',Keys.RETURN)
    except:
        driver.find_element_by_xpath('/html/body/div[4]/div[1]/div/div[3]/div/ul[2]/div/li[3]/a[1]/i').click()
        time.sleep(2)
        driver.find_element_by_xpath('/html/body/div[4]/div[2]/div/form/input').send_keys('"'+string+'"',Keys.RETURN)
    try:
        WebDriverWait(driver,1000).until(EC.text_to_be_present_in_element_value((By.XPATH,'//*[@id="main-content"]/div[2]/div/div/div/div[2]/div/div[2]/div[1]/h3')))
        driver.find_element_by_xpath('//*[@id="main-content"]/div[2]/div/div/div/div[2]/div/div[2]/div[1]/h3')
    except:
        time.sleep(10)
    if driver.find_element_by_xpath('//*[@id="main-content"]/div[2]/div/div/div/div[2]/div/div[2]/div[1]/h3').text.split()[-2].strip()=='no':
        driver.quit()
        return []
    elif driver.find_element_by_xpath('//*[@id="main-content"]/div[2]/div/div/div/div[2]/div/div[2]/div[1]/h3').text.split()[-2].strip().isalpha:
        page=0
    else:
        page=int(driver.find_element_by_xpath('//*[@id="main-content"]/div[2]/div/div/div/div[2]/div/div[2]/div[1]/h3').text.split()[-2].strip())/20
    while page>=0:
        elem=driver.find_elements_by_xpath('//*[@id="main-content"]/div[2]/div/div/div/div[2]/div/div[2]/div[2]/div/div[2]/h3/a')
        date=driver.find_elements_by_class_name('river-post__date')
        for i,j in zip(elem,date):
            i=i.get_attribute('href')
            j=int(j.text.split(',')[1].strip())
            if j<=2008 and i not in links_fetched:
                links_fetched.append(i)
        if page>0:
            try:
                driver.find_element_by_xpath('//*[@id="main-content"]/div[2]/div/div/div/div[2]/div/div[2]/div[2]/ul/li[2]/a').click()
                WebDriverWait(driver,100).until(EC.text_to_be_present_in_element_value((By.XPATH,'//*[@id="main-content"]/div[2]/div/div/div/div[2]/div/div[2]/div[1]/h3')))
            except:
                '''Do Nothing...'''
        page-=1
    driver.quit()
    return links_fetched

# This function crawls the links of TheWeek
def theweek_fetch_links(string):
    url='http://theweek.com/search/"'
    string=string.replace(' ','+')+'"?page='
    links_fetched = []
    dates = []
    links = []
    soup=crawl(url+string+'1')
    pages=int(soup.find_all('span',attrs={'id':'result-number'})[0].get_text())
    pages=int(ceil(pages/10.0))
    if pages==0:
        return []
    try:
        check_sum=1
        r=rq.get(url+string+str(pages),stream=True)
        check_sum=0
    except:
        while check_sum==1:
            try:
                time.sleep(2)
                r=rq.get(url+string+str(pages),stream=True)
                check_sum=0
            except:
                print "HTTP Error..."
    for chunk in r.iter_content(chunk_size=1024):
        if chunk:
            soup=bs(chunk)
            elem=soup.find_all('div',attrs={'class':'search-result-headline gray-rollover'})
            for i in elem:
                try:
                    i=i.findChild('a').get('href')
                    links_fetched.append(url[:-9]+i)
                except:
                    '''Do nothing...'''
            dat=soup.find_all('div',attrs={'class':'search-date'})
            for j in dat:
                try:
                    j=int(j.findChild('a').get_text().split(',')[-1].strip())
                    dates.append(j)
                except:
                    '''Do nothing...'''
    for i,j in zip(links_fetched,dates):
        if j<=2008 and i not in links:
            links.append(i)
    return links


# This function crawls the links for Money.cnn.com
def moneyCnn_fetch_links(string,driver):
    url='http://money.cnn.com/search/index.html?sortBy=date&primaryType=mixed&search=Search&query='
    string = '"'+string.replace(' ','+')+'"'
    url=url+string
    links_fetched = []
    check_sum=0
    try:
        driver.get(url)
        check_sum=1
        WebDriverWait(driver,1000).until(EC.visibility_of_element_located((By.ID,'business-link')))
        time.sleep(5)
    except:
        while check_sum==1:
            try:
                driver.get(url)
                WebDriverWait(driver,1000).until(EC.visibility_of_element_located((By.ID,'business-link')))
                check_sum=0
            except:
                print "Network Error... Trying to reconnect"
    c=0
    if len(driver.find_elements_by_xpath('//*[@id="mixedpagination"]/ul/li/span/a'))==1:
        c=1
    elif len(driver.find_elements_by_xpath('//*[@id="mixedpagination"]/ul/li/span/a'))>1:
        c=2
    try:
        while c>0:
            driver.find_element_by_xpath('//*[@id="mixedpagination"]/ul/li['+str(c)+']/span/a').click()
            WebDriverWait(driver,1000).until(EC.visibility_of_element_located((By.ID,'business-link')))
            time.sleep(1)
            elem=driver.find_elements_by_xpath('//*[@id="summaryList_mixed"]/div/div/a')
            date=driver.find_elements_by_xpath('//*[@id="summaryList_mixed"]/div/span[2]')
            for i,j in zip(elem,date):
                j=int(j.text.split(',')[-1].strip())
                i=i.get_attribute('href')
                if j<=2008 and i not in links_fetched:
                    links_fetched.append(i)
            c+=1
    except:
        '''Do Nothing...'''
    driver.quit()
    return links_fetched


# This function crawls the page Bloomberg.com aka BusinessWeek.com business page for links
def bloomberg_fetch_links(string):
    url='http://www.bloomberg.com/search?query='
    string=string.replace(' ','+')
    url=url+'"'+string+'"&page='
    links_fetched = []
    links = []
    soup=crawl(url+'1')
    try:
        page=int(soup.find_all('span',attrs={'class':'search-category-facet__count active'})[0].text)
        page=int(ceil(page/10.0))
    except:
        page=0
    for i in xrange(1,page+1):
        soup=crawl(url+str(i))
        elem=soup.find_all('h1',attrs={'class':'search-result-story__headline'})
        date=soup.find_all('time',attrs={'class':'published-at'})
        for i,j in zip(elem,date):
            i=i.findChild('a').get('href')
            i=url[:25]+i
            l=i.split('/')[-1].strip()
            j=int(j.text.split(',')[-1].strip())
            if j<=2008 and l not in links and 'video' not in l:
                links_fetched.append(i)
                links.append(l)
    return links_fetched


# This function crawls the page for reuters
def reuters_fetch_links(string,driver):
    url='http://www.reuters.com/search/news?sortBy=&dateRange=&blob="'
    string = string.replace(' ','+')+'"'
    links_fetched = []
    check_sum=0
    try:
        driver.get(url+string)
        check_sum=1
        WebDriverWait(driver,1000).until(EC.visibility_of_element_located((By.XPATH,'//*[@id="newsTab"]/a')))
    except:
        while check_sum==1:
            try:
                driver.get(url+string)
                WebDriverWait(driver,1000).until(EC.visibility_of_element_located((By.XPATH,'//*[@id="newsTab"]/a')))
                check_sum=0
            except:
                print "Network Error... Trying to reconnect!!!"
    time.sleep(5)
    c=len(driver.find_elements_by_xpath('//*[@id="content"]/div[4]/div/div/div[1]/div[3]/div/div[4]/div/div/h3/a'))
    d=0
    while c>d:
        d=len(driver.find_elements_by_xpath('//*[@id="content"]/div[4]/div/div/div[1]/div[3]/div/div[4]/div/div/h3/a'))
        check_sum=0
        try:
            check_sum=1
            driver.find_element_by_xpath('//*[@id="content"]/div[4]/div/div/div[1]/div[3]/div/div[5]/div[1]').click()
        except:
            while check_sum==1:
                try:
                    driver.get(url+string)
                except:
                    print "Network Error... Trying to Reconnect!!!"
            d=0
        time.sleep(2)
        c=len(driver.find_elements_by_xpath('//*[@id="content"]/div[4]/div/div/div[1]/div[3]/div/div[4]/div/div/h3/a'))
    elem=driver.find_elements_by_xpath('//*[@id="content"]/div[4]/div/div/div[1]/div[3]/div/div[4]/div/div/h3/a')
    date=driver.find_elements_by_xpath('//*[@id="content"]/div[4]/div/div/div[1]/div[3]/div/div[4]/div/div/h5')
    for i,j in zip(elem,date):
        i=i.get_attribute('href')
        j=int(j.text.split(',')[1].strip().split()[0])
        if j<=2008 and i not in links_fetched:
            links_fetched.append(i)
    driver.quit()
    return links_fetched

# This function crawls the links for Fortune.com
def fortune_fetch_links(string,driver):
    url='http://fortune.com/?s="'+string.replace(' ','+')+'"'
    links_fetched = []
    check_sum=0
    try:
        driver.get(url)
        check_sum=1
        WebDriverWait(driver,100).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="content"]/div/div/div/aside/form/div/div/button')))
    except:
        while check_sum==1:
            try:
                driver.get(url)
                WebDriverWait(driver,100).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="content"]/div/div/div/aside/form/div/div/button')))
                check_sum=0
                print '\n\nReconnected...\n\n'
            except:
                print "Network Error... Trying to Reconnect..."
    time.sleep(5)
    try:
        scrolls=int(driver.find_element_by_xpath('//*[@id="content"]/div/div/div/section/section[2]/div[1]/h2').text.split()[0])/10+1
    except:
        scrolls=0
    for _ in xrange(scrolls):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)
    elem=driver.find_elements_by_xpath('//*[@id="content"]/div/div/div/section/section[2]/div[2]/div/div/article/h3/a')
    dates=driver.find_elements_by_xpath('//*[@id="content"]/div/div/div/section/section[2]/div[2]/div/div/article/time')
    for i,j in zip(elem,dates):
        i=i.get_attribute('href')
        j=int(j.text.split(',')[1].strip())
        if j<=2008 and i not in links_fetched:
            if 'video' not in i:
                links_fetched.append(i)
    driver.quit()
    return links_fetched
