#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 21 01:08:34 2017

@author: root
"""

import requests
from bs4 import BeautifulSoup as bs
import re

def get_session_id(raw_resp):
    soup = bs(raw_resp.text, 'lxml')
    token = soup.find_all('input', {'name': 'authenticity_token'})[0]['value']
    return token

payload = {
    'entry[field_1]': 'test',  
    'entry[field_2]': '1234567890',  
    'entry[field_3]': '1401',
    'entry[field_4]': '18888888888',
    }

url = r'https://jinshuju.net/f/uc93vs'

with requests.session() as s:
    resp = s.get(url)
    payload['authenticity_token'] = get_session_id(resp)
    response_post = s.post(url, data=payload)
    soup = bs(response_post.text, 'lxml');
    msg = soup.find_all('div', {'class': 'message'})[0].string
    print msg
#    print response_post.text
