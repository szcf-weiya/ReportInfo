#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 30 20:13:45 2017

@author: root
"""

import getInfo
import time

content_copy = content
while(1):
    content = getInfo.write()
    if not content:
        print 'sleep....'
        time.sleep(60)
    elif content != content_copy:
        getInfo.send(content)
        print 'sleep....'
        time.sleep(60)
        content_copy = content
    else:
        time.sleep(60)
        continue
    

    

