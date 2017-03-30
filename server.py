#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 30 20:13:45 2017

@author: root
"""

import getInfo
import time

while(1):
    content = getInfo.write()
    if not content:
        print 'sleep....'
        time.sleep(60)
    else:
        getInfo.send(content)
        is_send = True
        print 'sleep....'
        time.sleep(43200)

    

