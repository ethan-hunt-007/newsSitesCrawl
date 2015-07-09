# -*- coding: cp1252 -*-
# 2015 ©Jayant Jaiswal. All rights reserved.
# This program uses headless selenium and crawls google for specific news sites
# for the first person in the sets given and returns the links for all the
# news for the that person...

from selenium import webdriver as wb
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from PIL import Image
from pprint import pprint
import os,signal,time,sys


def driver_get(url):
    try:
        check_sum=1
        driver.get(url)
        check_sum=0
    except:
        while check_sum==1:
            try:
                driver.get(url)
                check_sum=0
            except:
                print "Network Error...Trying to Reconnect!!!"
    if 'ipv4' in driver.current_url:
        driver.save_screenshot('C:\Users\Jayant\Desktop\Tomato\IIM_internship\dump\dump.png')
        t=raw_input("Enter the robot text:")
        driver.find_element_by_xpath('//*[@id="captcha"]').send_keys(t,Keys.RETURN)
    return driver


def fetch_google_pages(driver):
    pages = []
    visited = []
    try:
        pages = [page.get_attribute('href') for page in driver.find_elements_by_class_name('fl')]
    except:
        return []
    try:
        while False:
            print True
            print pages[-1]
            try:
                if pages[-1][-10:] not in visited:
                    visited.append(pages[-1][-10:])
                    print page[-1]
                else:
                    break
            except:
                '''Do nothing...'''
                print 'part 2'
            print "Midway"
            driver=driver_get(pages[-1])
            print "End Here"
            for page in driver.find_elements_by_class_name('fl'):
                page=page.get_attribute('href')
                if page not in pages:
                    pages.append(page)
    except:
        '''Do Nothing...'''
        print "Do nothing"
    return pages

def google_fetch_links(string,site,stopwords_list,driver):
    links_fetched = []
    string='"'+string+'"'
    url='https://www.google.com/search?q='+string+' site:'+site
    for word in stopwords_list:
        url=url+' -inurl:'+word.strip()
    url+='&tbs=cdr:1,cd_min:31/12/2008,cd_max:01/01/1970'
    url=url.replace(' ','+')
    driver=driver_get(url)
    print url
    try:
        elem=driver.find_elements_by_class_name('r')
    except:
        return []
    for i in elem:
        i=i.find_element_by_tag_name('a').get_attribute('href')
        if i not in links_fetched:
            links_fetched.append(i)
    '''try:
        links = driver.find_elements_by_class_name('fl')
    except:
        return links_fetched
    links = [link.get_attribute('href') for link in links]'''
    links=fetch_google_pages(driver)
    for i in links:
        driver=driver_get(i)
        elem=driver.find_elements_by_class_name('r')
        for link in elem:
            link=link.find_element_by_tag_name('a').get_attribute('href')
            if link not in links_fetched:
                links_fetched.append(link)
    driver.quit()
    return links_fetched

driver=wb.PhantomJS()
links=google_fetch_links("Edward Liddy","nytimes.com",['stocks','quotes','lists','pdf'],driver)
print len(links)
#pprint(links)
