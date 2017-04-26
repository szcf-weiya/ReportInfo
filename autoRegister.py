#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 21 01:08:34 2017

@author: root
"""

import requests
from bs4 import BeautifulSoup as bs

def get_session_id(raw_resp):
    soup = bs(raw_resp.text, 'lxml')
    token = soup.find_all('input', {'name': 'authenticity_token'})[0]['value']
    return token

payload = {
    'entry[field_1]': '3140000000',  # 21st checkbox# xuehao 
    'entry[field_2]': 'test1',  # first input-field
    'entry[field_3]': 'test',
    'entry[field_4]': '17800000000',
    }
def autoRegister(url):    
    with requests.session() as s:
        resp = s.get(url)
        payload['authenticity_token'] = get_session_id(resp)
        response_post = s.post(url, data=payload)
        soup = bs(response_post.text, 'lxml')
        msg = soup.find_all('div', {'class': 'message'})[0].string
        # if necessary
        # msg.encode('utf8')
        print msg
        
if __name__ == '__main__':
    #url = r'https://jinshuju.net/f/NvvjuS'
    url = r'https://jinshuju.net/f/uc93vs'
    autoRegister(url)
#    print response_post.text
