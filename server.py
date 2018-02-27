#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 30 20:13:45 2017

@author: root
"""

import getInfo
import time

content = ""
content_copy = content
while(1):
    # sleep at night
    night = time.localtime().tm_hour
    if  night >= 0 and night <= 7:
        time.sleep(7*60*60)
    content = getInfo.write()
    if not content:
        print 'sleep....'
        time.sleep(60)
    elif content != content_copy:
        #getInfo.send(content)
        getInfo.sendSMS(content)
        print 'sleep....'
        time.sleep(60)
        content_copy = content
    else:
        time.sleep(60)
        continue
    

    

