# -*- coding: cp1252 -*-
# 2015 ©Jayant Jaiswal. All rights reserved.
# This program uses the news_bot.py to first crawl the data for different
# personalities and then creates the matrix for different combination of names
# against the different websites...



from news_bot import *
from selenium import webdriver
from itertools import combinations as comb
import os,signal,time,csv
chromedriver = 'F:\Tools\chromedriver'

# This return the driver to chrome to the crawl functions that use selenium
def driver():
    driver = webdriver.Chrome(chromedriver)
    return driver

'''# This function is for validating a nameSet combination
def validate(nameSet,data,hash_back):
    for name in nameSet:
        if hash_back[name] not in data:
            return False
    return True'''

# This function is for validating a nameSet combination in a by checking each part(eg. First,Second) in each name against the data...
def validate(nameSet,data,hash_back):
    for name in nameSet:
        for part in hash_back[name].split():
            if part not in data:
                return False
    return True

# This function controls the part of crawling the links and downloading the data
def crawl_bot(path,total_sets):
    names = []
    for i in xrange(38,total_sets+1):
        file_name = path + r'\SETS\SET' + str(i) + '.txt'
        f=open(file_name,'r')
        names.append(f.next().strip())
        f.close()
    for name,set_no in zip(names,xrange(38,total_sets+1)):
        # *********** Crawling and downloading from FORBES **************
        print "\nCrawling the links from FORBES for SET =",set_no," ..."
        links = forbes_fetch_links(name)
        print "\n...Crawling for SET =",set_no,"from FORBES done!!!\n"
        print "\nStarting the downloading of data from the links fetched...\n"
        pages_crawl(links,path,"SET"+str(set_no),"FORBES")
        print "\n...Data downloaded from FORBES for SET =",set_no,"!!!\n"
        # *********** Crawling and downloading from NYTimes *************
        print "\nCrawling the links from NYTimes for SET =",set_no," ..."
        links = nytimes_fetch_links(name,driver())
        print "\n...Crawling for SET =",set_no,"from NYTimes done!!!\n"
        print "\nStarting the downloading of data from the links fetched...\n"
        pages_crawl(links,path,"SET"+str(set_no),"NYTimes")
        print "\n...Data downloaded from NYTimes for SET =",set_no,"!!!\n"
        # *********** Crawling and downloading from BusinessInsider******
        print "\nCrawling the links from BusinessInsider for SET =",set_no," ..."
        links = businessinsider_fetch_links(name,driver())
        print "\n...Crawling for SET =",set_no,"from BusinessInsider done!!!\n"
        print "\nStarting the downloading of data from the links fetched...\n"
        pages_crawl(links,path,"SET"+str(set_no),"BusinessInsider")
        print "\n...Data downloaded from BusinessInsider for SET =",set_no,"!!!\n"
        # *********** Crawling and downloading from TheWeek **************
        print "\nCrawling the links from TheWeek for SET =",set_no," ..."
        links = theweek_fetch_links(name)
        print "\n...Crawling for SET =",set_no,"from TheWeek done!!!\n"
        print "\nStarting the downloading of data from the links fetched...\n"
        pages_crawl(links,path,"SET"+str(set_no),"TheWeek")
        print "\n...Data downloaded from TheWeek for SET =",set_no,"!!!\n"
        # ***********Crawling and downloading from Money.CNN *************
        print "\nCrawling the links from Money.CNN for SET =",set_no," ..."
        links = moneyCnn_fetch_links(name,driver())
        print "\n...Crawling for SET =",set_no,"from Money.CNN done!!!\n"
        print "\nStarting the downloading of data from the links fetched...\n"
        pages_crawl(links,path,"SET"+str(set_no),"Money.CNN")
        print "\n...Data downloaded from Money.CNN for SET =",set_no,"!!!\n"
        # ***********Crawling and downloading from Bloomberg *************
        print "\nCrawling the links from Bloomberg for SET =",set_no," ..."
        links = bloomberg_fetch_links(name)
        print "\n...Crawling for SET =",set_no,"from Bloomberg done!!!\n"
        print "\nStarting the downloading of data from the links fetched...\n"
        pages_crawl(links,path,"SET"+str(set_no),"Bloomberg")
        print "\n...Data downloaded from Bloomberg for SET =",set_no,"!!!\n"
        # ***********Crawling and downloading from REUTERS ***************
        print "\nCrawling the links from REUTERS for SET =",set_no," ..."
        links = reuters_fetch_links(name,driver())
        print "\n...Crawling for SET =",set_no,"from REUTERS done!!!\n"
        print "\nStarting the downloading of data from the links fetched...\n"
        pages_crawl(links,path,"SET"+str(set_no),"REUTERS")
        print "\n...Data downloaded from REUTERS for SET =",set_no,"!!!\n"
        # ***********Crawling and downloading from FORTUNE ***************
        print "\nCrawling the links from FORTUNE for SET =",set_no," ..."
        links = fortune_fetch_links(name,driver())
        print "\n...Crawling for SET =",set_no,"from FORTUNE done!!!\n"
        print "\nStarting the downloading of data from the links fetched...\n"
        pages_crawl(links,path,"SET"+str(set_no),"FORTUNE")
        print "\n...Data downloaded from FORTUNE for SET =",set_no,"!!!\n"
    print "\n\n*************Crawling and Downloading of ALL Data Done*******\n\n"


# This is the MAIN program
def main():
    path = 'C:\Users\Jayant\Desktop\Tomato\IIM_internship'#raw_input("Enter the path to save to data : ")
    sets = 38#input("Enter the total sets : ")
    site_list = ['FORBES','NYTimes','BusinessInsider','TheWeek','Money.CNN','Bloomberg','REUTERS','FORTUNE']
    print "\n***************Starting the Data Download***********\n"
    crawl_bot(path,sets)
    print "\n***************Starting the processing part**********\n"
    for set_no in xrange(2,sets+1):
        n='a'
        hash_for = {}
        hash_back = {}
        nameSet_list = [' ']
        comb_str = ''
        f=open(path+r'\SETS\SET'+str(set_no)+'.txt','r')
        names = [name.strip() for name in f.readlines()]
        f.close()
        for name in names:
            hash_for[name]=n
            hash_back[n]=name
            comb_str+=n
            n=chr(ord(n)+1)
        for site_no in xrange(len(site_list)):
            f=open(path+r'\SET'+str(set_no)+'\\'+site_list[site_no]+r'\links.txt','r')
            total_links = len(f.readlines())
            f.close()
            count_list = []
            for r in xrange(1,len(comb_str[1:])+1):
                for com in comb(comb_str[1:],r):
                    links_list = []
                    count = 0
                    string='a'
                    for i in com:
                        string+=i
                    for link_no in xrange(1,total_links+1):
                        f=open(path+r'\SET'+str(set_no)+'\\'+site_list[site_no]+'\\'+str(link_no)+'.txt','r')
                        data=f.read()
                        if validate(string,data,hash_back):
                            count+=1
                            f.seek(0)
                            links_list.append(f.next().strip())
                            f.seek(0)
                            #print f.next(),string
                        f.close()
                    count_list.append(count)
                    nameSet=''
                    for i in string:
                        nameSet=nameSet+hash_back[i]+','
                    with open(path+r'\SET'+str(set_no)+'\\'+site_list[site_no]+'.csv','ab') as c:
                        f=csv.writer(c)
                        f.writerow([nameSet[:-1]]+links_list)
                    if site_no==0:
                        nameSet_list.append(nameSet)
            with open(path+r'\SET'+str(set_no)+r'\SET'+str(set_no)+'.csv','ab') as c:
                f=csv.writer(c)
                f.writerow([site_list[site_no]]+count_list)
        with open(path+r'\SET'+str(set_no)+r'\SET'+str(set_no)+'.csv','ab') as c:
            f=csv.writer(c)
            f.writerow(nameSet_list)

# This function is to PAUSE, RESUME and to TERMINATE the Main Program
def exit_gracefully(signum, frame):
    signal.signal(signal.SIGINT, original_sigint)
    try:
        if raw_input("\nReally quit? (y/n)> ").lower().startswith('y'):
            sys.exit(1)

    except KeyboardInterrupt:
        print("Ok ok, quitting")
        sys.exit(1)    
    signal.signal(signal.SIGINT, exit_gracefully)


# The Program is Invoked from this place...
original_sigint = signal.getsignal(signal.SIGINT)
signal.signal(signal.SIGINT, exit_gracefully)
main()
