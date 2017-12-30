# coding=utf-8
# -*- coding:utf-8 -*-
import urllib.request
import sys
import pymysql
import time
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
from email.header import Header

# 打印
def dump(obj):
    # print(type(obj))
    print(obj)
    sys.exit(0)
    return


# 爬取数据
content = urllib.request.urlopen('http://163.com').read()
soup = BeautifulSoup(content,"html.parser")
ps = soup.find_all(attrs={'ne-module':"modules/tech/tech.js"})
dataArr = []
nowTime = time.time()
mailMsg = ''
title = ''
href = ''
for p in ps:
    ass = p.find_all('a')
    for a in ass:
        title = a.get_text().strip()
        if(title != '' and len(title) > 8):
            href = a.get('href')
            dataArr.append((title,href,nowTime))
            mailMsg = mailMsg + '<p><a href="%s">%s</a></p>' % (href, title)
# dump(dataArr)


# 保存数据
db = pymysql.connect(host='localhost',user='root',passwd='root',db='news',charset='utf8')
cursor = db.cursor()
sql = "INSERT INTO `163` (name,url,addTime) values(%s,%s,%s)"
results = cursor.executemany(sql,dataArr)
db.commit()
cursor.close()
db.close()


# 发送email
sender = '22222@qq.com'
receiver = ['111111@qq.com']
message = MIMEText(mailMsg,'html','utf-8')
message['From'] = Header('新闻系统','utf-8')
message['To'] = Header('尊敬的张奕枫','utf-8')
message['Subject'] = Header('新闻','utf-8')
server = smtplib.SMTP('smtp.qq.com',25)
server.login('222222@qq.com','3333333')
server.sendmail(sender,receiver,message.as_string())