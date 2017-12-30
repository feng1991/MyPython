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
import time

# 打印
def dump(obj):
    # print(type(obj))
    print(obj)
    sys.exit(0)
    return

def getTimeOClockOfToday():
    t = time.localtime(time.time())
    time1 = time.mktime(time.strptime(time.strftime('%Y-%m-%d 00:00:00', t),'%Y-%m-%d %H:%M:%S'))
    return int(time1)


# 判断是否已爬取
db = pymysql.connect(host='localhost',user='root',passwd='root',db='news',charset='utf8')
cursor = db.cursor()
sql = "SELECT addTime FROM `163` ORDER BY addTime LIMIT 1"
cursor.execute(sql)
result = cursor.fetchone()
if result is not None:
    todayTime = getTimeOClockOfToday()
    if result[0] > todayTime:
        sys.exit(0)


# 爬取数据
content = urllib.request.urlopen('http://163.com').read()
soup = BeautifulSoup(content,"html.parser")
ps = soup.find_all(attrs={'ne-module':"modules/tech/tech.js"})
dataArr = []
nowTime = time.time()
mailMsg = '<table align="center" border="1px solid #666666">'
title = ''
href = ''
for p in ps:
    ass = p.find_all('a')
    for a in ass:
        title = a.get_text().strip()
        if(title != '' and len(title) > 10):
            href = a.get('href')
            dataArr.append((title,href,nowTime))
            mailMsg = mailMsg + '<tr><td style="padding:5px"><a href="%s">%s</td></tr>' % (href, title)
mailMsg += '</table>'
# dump(mailMsg)


# 保存数据
sql = "INSERT INTO `163` (name,url,addTime) values(%s,%s,%s)"
results = cursor.executemany(sql,dataArr)
db.commit()
cursor.close()
db.close()


# 发送email
sender = ''
receiver = ['']
timeStr = time.strftime('%Y/%m/%d',time.localtime())
message = MIMEText(mailMsg,'html','utf-8')
message['From'] = Header('新闻系统','utf-8')
message['To'] = Header('尊敬的张奕枫','utf-8')
message['Subject'] = Header(timeStr+' 163新闻','utf-8')
server = smtplib.SMTP('smtp.qq.com',25)
server.login('','')
server.sendmail(sender,receiver,message.as_string())