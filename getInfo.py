#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 30 16:43:45 2017

@author: root
"""

import requests
from bs4 import BeautifulSoup
import re
import json

from smtplib import SMTP
#import smtplib
#from email import Encoders
#from email.mime.base import MIMEBase
#from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header

from datetime import date, timedelta
import time

def visit():
    session = requests.Session()
    url = "http://www.math.zju.edu.cn/news.asp?id=6624&TabName=%B1%BE%BF%C6%BD%CC%D1%A7"
    
    try:
        req = session.get(url)
        if req.status_code == 200:
            pass#print 'This session work.'
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
    for match in soup.findAll('font'):
        match.unwrap()
    for match in soup.findAll('span'):
        match.unwrap()
    soup = BeautifulSoup(str(soup), 'html.parser')
    return(soup)

def getLink(soup):
    link_pattern = re.compile('mikecrm')
    
    link = soup.find('td', {"class":"NewsBody"}).findAll('a')
    
    urlList = []
    for i in xrange(len(link)):
        tmp = link[i]
        url = tmp['href']
        if link_pattern.findall(url):
            if len(urlList) >= 1 and url == urlList[len(urlList)-1]:
                continue
            urlList.append(url)
    
    return(urlList)

def getDate(soup, num):
    #news = soup.find('td', {"class":"NewsBody"}).findAll('p')
    news = soup.find('td', {"class":"NewsBody"}).find_all('p')
    #print(len(news))
    date_pattern = re.compile(u'([1-9]{1,2}\u6708[0-9]{1,2}\u65e5)') # 不要双斜杠
    datelist = []
    details = []
#    for i in xrange(len(news)):
#        for child in news[i].children:
#            try:
#                info = date_pattern.findall(str(child))
#                if len(info) >= 1:
#                    datelist.append(info[0])
#            except:
#                continue

    for i in xrange(len(news)):
        try:
            info = date_pattern.findall(str(news[i]).decode('utf8'))
            if len(info) >= 1:
                #print info[0]
                #print news[i].string
                s1 = news[i].string
                s2 = u'\uff09'
                nPos = s1.index(s2)
                #tmp2 = s1[nPos+1:]
                #tmp1, tmp2 = news[i].string.split(u'\uff08'+info+u'\uff09')
                #print tmp2
                details.append(s1[nPos+1:])
                datelist.append(info[0])
        except:
            continue
    #print(len(datelist))
    newsdate = []
    newdetails = []
    today = date.today() - timedelta(num)
    for i in xrange(len(datelist)):
        tmp = datelist[i]
        m, d = tmp.split(u'\u6708')
        d, l = d.split(u'\u65e5')
        try:
            tmp = date(today.year, int(m), int(d))
            if int(m) >= 11: # @2018.02.27 new semster skip the reports from 2017.11.01 to 2017.12.31
                continue
            if tmp >= today:
                newsdate.append(tmp)
                newdetails.append(details[i])
        except:
            continue

#    latest = []
## 正序
#    if not newsdate:
#        return None
#    latest.append(newsdate[0])
#    for i in xrange(len(newsdate)):
#        if newsdate[i] > latest[len(latest)-1]:
#            latest.append(newsdate)
            
    return([newsdate, newdetails])
        

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

def getLatest():
    soup = visit()
    latest, details = getDate(soup, 0)
    content = "Update at " + time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) + "\n"
    if not latest:
        pass
        content = content + "No New Seminar Yet!!\n"
    else:
        print len(latest)
        content = content + "New Seminar!!\n"
        urlList = getLink(soup)        
        for i in xrange(len(latest)):
            content = content + date.strftime(latest[i], '%Y.%m.%d') + " : "  + urlList[i] + "\n"
    print(content)
    return(content)
    

def getHistory():
    soup = visit()
    latest, details = getDate(soup, 7)
    today = date.today()
    flag = 1
    hist_len = len(latest)
    for i in xrange(hist_len):
        if (latest[i] >= today):
            continue
        else:
            flag = 0
            break
    pos = i
    content = u"上一周学术讲座信息\n"
    if flag == 1:
        pass
        content = content + u"上周没有学术讲座！\n"
    else:
        content = content + u"上周共" + str(len(latest)-pos) + u"场讲座\n"
        urlList = getLink(soup)        
        for j in xrange(len(latest)-pos):
            content = content + date.strftime(latest[pos+j], '%Y.%m.%d') + " : "  + urlList[pos+j] + "\n"
    print(content)
    return(content.encode('utf8'))


    
def returnJson():
    # make a copy of original stdout route
    #stdout_backup = sys.stdout
    #log_file = open("message.log", "w")
    # redirect print output to log file
    #sys.stdout = log_file
    soup = visit()
    latest, details = getDate(soup, 0)
    #log_file.close()
    # restore the output to initial pattern
    #sys.stdout = stdout_backup
    num = len(latest)
    full_res = {}
    if not latest:
        latest, details = getDate(soup, 7)
    urlList = getLink(soup)        
    for i in xrange(len(latest)):
        res = {}
        res["date"] = date.strftime(latest[i], '%Y.%m.%d') 
        if num == 0:
            pass
        else:    
            res["url"] = urlList[i]
        res["details"] = details[i]
        full_res[i] = res
    content = {}
    content["full_res"] = full_res
    content["num"] = num
    jsonStr = json.dumps(content)
    return(jsonStr)    

def write():
    soup = visit()
    urlList = getLink(soup)
    #print(len(urlList))
    #print(urlList[0])
    #for i in range(1, len(urlList)):
    #    print(urlList[i])
    latest, details = getDate(soup, 0)
    content = ""
    if not latest:
        return (content)
    
    for i in xrange(len(latest)):
        #content = content + date.strftime(latest[i], '%Y.%m.%d') + " : "  + urlList[len(urlList)-1-i] + "\n"
        #for sms
        content = content + date.strftime(latest[i], '%m.%d') + ": "  + urlList[len(urlList)-1-i]
        
    #content = content + "---from python(by weiya)"
    return(content)
    
def send(content):
    send_email(SMTP_host='smtp.zju.edu.cn:25',
           from_account='weiya@zju.edu.cn',
           from_passwd='***',
           to_account=['szcfweiya@gmail.com'],
           subject='new report!!!',   
           content=content)

def sendSMS(content):
    url = 'https://sms-api.upyun.com/api/messages'
    mobiles = ['17816859236']
    
    postdata = {
        'mobile' : '...',
        'template_id': 1220,
        'vars' : '...'
        }
    headers = {
        'Content-type' : 'application/x-www-form-urlencoded',
        'Authorization': '*******'
        }
    postdata['vars'] = content
    for i in xrange(len(mobiles)):
        postdata['mobile'] = mobiles[i]
        requests.post(url, headers = headers, data=postdata)        

if __name__ == '__main__':
    #send(write())
    print(write())
    #sendSMS(write())
    #getLatest()
    #print(sendSMS())
    #print returnJson()