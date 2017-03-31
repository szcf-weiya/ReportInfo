#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 30 16:43:45 2017

@author: root
"""

import requests
from bs4 import BeautifulSoup
import re

from smtplib import SMTP
import smtplib
import json
from email import Encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header

from datetime import date

def visit():
    session = requests.Session()
    url = "http://www.math.zju.edu.cn/news.asp?id=6624&TabName=%B1%BE%BF%C6%BD%CC%D1%A7"
    
    try:
        req = session.get(url)
        if req.status_code == 200:
            print 'This session work.'
        else:
            print 'Not work'
    except:
        print 'This session not work'
    
    try:
        page = req.content
    except:
        print 'can not get the content'
    
    content = page.decode('gb2312')
    #soup = BeautifulSoup(content, 'lxml')
    soup = BeautifulSoup(content, 'html.parser')
    return(soup)

def getLink(soup):
    link_pattern = re.compile('jinshuju')
    
    link = soup.find('td', {"class":"NewsBody"}).findAll('a')
    
    urlList = []
    for i in xrange(len(link)):
        tmp = link[i]
        url = tmp['href']
        if link_pattern.findall(url):
            urlList.append(url)
    
    return(urlList)

def getDate(soup):    
    news = soup.find('td', {"class":"NewsBody"}).findAll('p')
    date_pattern = re.compile("([1-9]\.[0-9]{1,2})")
    datelist = []
    for i in xrange(len(news)):
        for child in news[i].children:
            try:
                info = date_pattern.findall(str(child))
                if len(info) >= 1:
                    datelist.append(info[0])
            except:
                continue
            
    newsdate = []
    today = date.today()
    for i in xrange(len(datelist)):
        tmp = datelist[i]
        m, d = tmp.split('.')
        try:
            tmp = date(today.year, int(m), int(d))
            if tmp >= today:
                newsdate.append(tmp)
        except:
            continue
    
    latest = []
    if not newsdate:
        return None
    latest.append(newsdate[0])
    for i in xrange(len(newsdate)):
        if newsdate[i] > latest[len(latest)-1]:
            latest.append(newsdate)
            
    return(latest)
        

#def sendMail(fromEmail, username,  password, serverAddress, subject, htmlContent, toEmail):
#    '''
#    fromEmail: 使用哪个邮箱地址发送
#    username: 登陆邮箱服务器的用户名，一般与fromEmail相同
#    password: 登陆的密码
#    serverAddress: 邮箱服务的地址（包含端口）
#    subject: 邮件主题
#    htmlContent: 邮件正文，使用html格式编写
#    toEmail: 要发送到的邮箱地址，可以写多个
#    '''
#    msg = MIMEMultipart('alternative')
#    msg['Subject'] = subject
#    msg['From'] = fromEmail
#    msg['To'] = ', '.join(toEmail)
#    #msg['To'] = toEmail
#    msg["Accept-Language"]="zh-CN"                      #指定语言环境是中文
#    msg["Accept-Charset"]="ISO-8859-1,utf-8"        #指定使用特定的编码，防止乱码
#    part = MIMEText(htmlContent, 'html', 'UTF-8')
#    msg.attach(part)
#    
#    s = smtplib.SMTP(serverAddress)
#    print "Try to login"
#    s.login(username, password)
#    print "login successfully, try to send"
#    s.sendmail(fromEmail, toEmail, msg.as_string())
#    print "send successfully"
#    s.quit()
    
def send_email(SMTP_host, from_account, from_passwd, to_account, subject, content):
    email_client = SMTP(SMTP_host)
    email_client.login(from_account, from_passwd)
    # create msg
    msg = MIMEText(content, 'plain', 'utf-8')
    msg['Subject'] = Header(subject, 'utf-8')  # subject
    msg['From'] = from_account
    #msg['To'] = to_account
    msg['To'] = ', '.join(to_account)
    email_client.sendmail(from_account, to_account, msg.as_string())

    email_client.quit()




def write():
    soup = visit()
    urlList = getLink(soup)
    latest = getDate(soup)
    if not latest:
        return (None)
    content = ""
    for i in xrange(len(latest)):
        content = content + date.strftime(latest[i], '%Y.%m.%d') + " : "  + urlList[len(urlList)-1-i] + "\n"
        print(content)
        
    content = content + "---from python(by weiya)"
    return(content)
    
def send(content):
    send_email(SMTP_host='smtp.email.com:25',
           from_account='from@email.com',
           from_passwd='password',
           to_account=['to@email.com'],
           subject='new report!!!',   
           content=content)
    

if __name__ == '__main__':
    send(write())

