# -*- coding: utf-8 -*-
"""
Created on Tue Dec 27 22:02:33 2016

@author: shi
"""

from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import time
import re
import urllib2
#import Image
#import cStringIO
import os
from httplib import BadStatusLine

keywords="beautiful girls"
binary = FirefoxBinary(r'C:\Program Files (x86)\Mozilla Firefox\firefox.exe')

driver = webdriver.Firefox(firefox_binary=binary)

#driver.get("http://image.baidu.com/search/index?ct=201326592&cl=2&st=-1&lm=-1&nc=1&ie=utf-8&tn=baiduimage&ipn=r&rps=1&pv=&fm=rs2&word=%E8%A1%A3%E6%9C%8D&oriquery=clothes&ofr=clothes")
driver.get("https://www.google.com/search?biw=629&bih=599&tbm=isch&sa=1&q="+keywords)
js="var q=document.documentElement.scrollTop=100000"
driver.execute_script(js)
driver.implicitly_wait(5)
content=driver.page_source.encode("utf-8")
x=0
number = 0
for page_num in range(20):
    waitCount = 0
    print('page:'+str(page_num+1))
    driver.execute_script(js)
    while(content==driver.page_source.encode("utf-8")):
        waitCount += 1
        time.sleep(0.2)
        print ("waitCount:" + str(waitCount))
        if(waitCount >= 20):
            break
    if(waitCount >= 20):
        break
    print ("new content")
    content = driver.page_source.encode("utf-8")
original=r'"ou":"(.*?)"'
address=re.findall(original,str(content))

hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}

def checkURL(link):
    try:
        response=urllib2.urlopen(link)
    except BadStatusLine:
        print "could not fetch %s" % link
    except urllib2.HTTPError,e:
        print 'The server couldn\'t fulfill the request.'
        print 'Error code: ',e.code
        print 'Error reason: ',e.reason   
        return False
    except urllib2.URLError,e:
        print 'We failed to reach a server.'
        print 'Reason: ', e.reason
        return False
    else:
        req = urllib2.Request(link)
        response=urllib2.urlopen(req)
        url=response.geturl()
        if url==link:
            return True
        return False
    

path='E:\\Scrawls\\' + keywords 
isExists=os.path.exists(path) 
if not isExists:    
    # create dir
    os.makedirs(path)
    # 
    print path+ '. Dir created successfully'    
else:
    # if there is already a dir
    print 'Path is :' + path
    
listAdd=list(set(address))
for link in listAdd[:-1]:
    file_object = open('E:\\Scrawls\\summary_'+keywords+'.txt', 'a')
    file_object.write(link+'\n')
    file_object.close()

file_object = open('E:\\Scrawls\\summary_'+keywords+'.txt', 'a')
file_object.write(listAdd[-1])
file_object.close()

x=1
length=5000
for link in listAdd[83:]:   
    print(x)
    if x>length:
        break
    print(link)
    ext = link.split('.')[-1] 
    
    if ext in ['jpg','JPG','png','PNG'] and checkURL(link):                
        filename = str(x) + '.' + ext                
        #    #save images 
        data = urllib2.urlopen(link).read()  
        f = open(path + '\\' + filename, 'wb')  
        f.write(data)  
        f.close() 
        x=x+1
        

