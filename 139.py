#!/usr/bin/python
# coding=utf-8
# FileName: 139.py

import smtplib
import sys
import email

from email.mime.text import MIMEText
#========================================
#需要配置
send_mail_host="smtp.163.com"      # 发送的smtp
send_mail_user="发送邮件的用户名"
send_mail_user_name="发送时显示的名字"
send_mail_pswd="发件的密码"
send_mail_postfix="163.com"  #发邮件的域名

get_mail_user="139邮件的帐号"
#以下不用配置=============================

get_mail_postfix="139.com"
get_mail_host="pop.139.com"


#========================================
def semd_mail(sub,content):
    '''
    sub:主题
    content:内容
    send_mail("xxxxx@xxx.xxx","主题","内容")
    '''
    send_mail_address=send_mail_user_name+"<"+send_mail_user+"@"+send_mail_postfix+">"
    msg=email.mime.text.MIMEText(content)
    msg['Subject']=sub
    msg['From']=send_mail_address
    msg['to']=to_adress="139SMSserver<"+get_mail_user+"@"+get_mail_postfix+">"
    try:
        stp = smtplib.SMTP()
        stp.connect(send_mail_host)
        stp.login(send_mail_user,send_mail_pswd)
        stp.sendmail(send_mail_address, to_adress, msg.as_string())
        stp.close()
        return True
    except Exception, e:
        print str(e)
        return False


if __name__ == '__main__':
   
    if semd_mail(sys.argv[1],sys.argv[2]):
        print "发送成功"
    else:
        print '发送失败'
