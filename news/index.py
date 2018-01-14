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
from selenium import webdriver


# 打印
def dump(obj):
    # print(type(obj))
    print(obj)
    sys.exit(0)
    return


# 今日0点时间戳
def getTimeOClockOfToday():
    t = time.localtime(time.time())
    time1 = time.mktime(time.strptime(time.strftime('%Y-%m-%d 00:00:00', t), '%Y-%m-%d %H:%M:%S'))
    return int(time1)


# 判断是否已爬取
db = pymysql.connect(host='localhost', user='root', passwd='root', db='news', charset='utf8')
cursor = db.cursor()
sql = "SELECT addTime FROM `163` ORDER BY addTime DESC LIMIT 1"
cursor.execute(sql)
result = cursor.fetchone()
if result is not None:
    todayTime = getTimeOClockOfToday()
    if result[0] > todayTime:
        sys.exit(0)


# 爬取网易新闻
content = urllib.request.urlopen('http://163.com').read()
soup = BeautifulSoup(content, "html.parser")
ps = soup.find_all(attrs={'ne-module': "modules/tech/tech.js"})
dataArr = []
nowTime = int(time.time())
mailContent1 = ''
title = ''
href = ''
for p in ps:
    ass = p.find_all('a')
    for a in ass:
        title = a.get_text().strip()
        if (title != '' and len(title) > 10):
            href = a.get('href')
            dataArr.append((title, href, nowTime))
            mailContent1 = mailContent1 + '<li style="color:#323232;"><a href="%s">%s</a></li>' % (href, title)
        if (len(dataArr) > 8):
            break
# dump(mailContent1)


# 保存数据
sql = "INSERT INTO `163` (name,url,addTime) values(%s,%s,%s)"
results = cursor.executemany(sql, dataArr)
db.commit()
cursor.close()
db.close()


# 爬取网易云音乐新歌榜
driver = webdriver.PhantomJS('D:/software/it/phantomjs-2.1.1/bin/phantomjs.exe')
driver.get('http://music.163.com/discover/toplist?id=3779629')
driver.switch_to.frame('contentFrame')
content = ''
titleArr = []
urlArr = []
elements = driver.find_elements_by_css_selector('.m-table-rank tbody .txt b')
for element in elements:
    content += element.get_attribute('title') + '\n'
    titleArr.append(element.get_attribute('title'))
    if len(titleArr) > 4:
        break
elements = driver.find_elements_by_css_selector('.m-table-rank tbody .txt a')
for element in elements:
    content += element.get_attribute('href') + '\n'
    urlArr.append(element.get_attribute('href'))
    if len(urlArr) > 4:
        break
mailContent2 = ''
for title in titleArr:
    url = urlArr.pop(0)
    mailContent2 = mailContent2 + '<li style="color:#323232;"><a href="%s">%s</a></li>' % (url, title)


# 获取笑话
content = urllib.request.urlopen('http://www.joke-of-the-day.com/').read()
soup = BeautifulSoup(content, 'html.parser')
quote = soup.find('div', {'class': 'quote'})
mailContent3 = quote.get_text().strip()


# 生成邮件html
mailMsg = """
<!DOCTYPE html>
<html>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
    <meta name="viewport" content="width=device-width,initial-scale=1.0">
    <style type="text/css">
        div, tr, td, p, a, h1, h2, h3, h4, h5, h6, ul, li {
            margin: 0;
            padding: 0;
        }
        a {
            text-decoration: none;
        }
        img {
            max-width: 100%;
            border: none;
            outline: none;
            text-decoration: none;
            -ms-interpolation-mode: bicubic;
        }
        a img {
            border: none;
        }
    </style>
</head>

<body>
    <div style="font:Verdana normal 14px;color:#000;">
        <table cellpadding="0" cellspacing="0" border="0" width="100%" style="padding:0px;  background:#F2F2F2;">
            <tbody>
                <tr>
                    <td align="center" style="background-color: #eeeeee;padding-top: 30px;padding-bottom:60px;">
                        <table border="0" cellpadding="0" cellspacing="0" width="600">
                            <tbody>
                                <tr>
                                    <td align="center" style="padding: 20px 0px; background-color:#eeeeee;" valign="middle">

                                    </td>
                                </tr>
                                <tr>
                                    <td align="center" valign="top">
                                        <table border="0" cellpadding="0" cellspacing="0" style="" width="100%">
                                            <tbody>
                                                <tr>
                                                    <td align="center" valign="top">
                                                        <table border="0" cellpadding="0" cellspacing="0" style="background-color:#3e9de1; padding:25px 45px;" width="100%">
                                                            <tbody>
                                                                <tr>
                                                                    <td valign="top">
                                                                        <table cellpadding="0" cellspacing="0">
                                                                            <tbody>
                                                                            <tr>
                                                                                <td width="160" style="width:160px; padding-right:20px;" align="right">
                                                                                    <img width="153" title="Welcome mail" src="https://www.zoho.com/bugtracker/images/mailtemp-icon.png">
                                                                                </td>
                                                                                <td>
                                                                                    <div style="font-family:Lucida Grande,Lucida Sans,Lucida Sans Unicode,Arial,Helvetica,Verdana,sans-serif; font-size:13px; text-align:left; color:#fff;">
                                                                                        <h3 style="font-size: 22px;">Welcome sir</h3>
                                                                                        <p style="font-size: 18px; ">May the force be with you!</p><div style="text-decoration: none; outline: none; background-color: rgb(253, 216, 22); float: left; border-bottom: 2px solid rgb(246, 174, 18); color: rgb(51, 51, 51); margin-top: 8px; cursor: pointer; width: 160px; height: 20px; line-height: 20px; text-align: center; padding: 5px 9px;"><a href="#" style="color: rgb(51, 51, 51);"> </a></div>
                                                                                    </div>
                                                                                </td>
                                                                            </tr>
                                                                           </tbody>
                                                                        </table>
                                                                    </td>
                                                                </tr>
                                                            </tbody>
                                                        </table>
                                                    </td>
                                                </tr>
                                                <tr>
                                                    <td align="center" valign="top">
                                                        <table border="0" cellpadding="0" cellspacing="0" style="background-color: #fff;" width="100%">
                                                            <tbody>
                                                            <tr>
                                                                <td valign="top" style="padding: 25px 40px;">
                                                                    <h3 style=" font-family:Lucida Grande,Lucida Sans,Lucida Sans Unicode,Arial,Helvetica,Verdana,sans-serif; font-size:15px; font-weight:400; color:#363c43; margin:0px 0px 10px; text-align: left;">Hi there,</h3>
                                                                    <div style="font-family:Lucida Grande,Lucida Sans,Lucida Sans Unicode,Arial,Helvetica,Verdana,sans-serif; font-size:15px; text-align:left;  margin-bottom:5px; color:#323232; line-height:25px;">I wish you happy everyday!</div>
                                                                </td>
                                                            </tr>
                                                            </tbody>
                                                        </table>
                                                    </td>
                                                </tr>
                                                <tr>
                                                    <td style="padding:25px 40px 15px; background-color:#f6f7fb;">
                                                        <div style="font-family:Lucida Grande,Lucida Sans,Lucida Sans Unicode,Arial,Helvetica,Verdana,sans-serif; color:#323232; font-size:18px; font-weight:600; padding-bottom:10px;">科技新闻:</div>
                                                        <ul style="padding: 5px 0px 10px 35px; margin: 0px; font-family: Lucida Grande,Lucida Sans,Lucida Sans Unicode,Arial,Helvetica,Verdana,sans-serif; line-height:25px; font-size: 14px;">
                                                            %mailContent1
                                                        </ul>
                                                        <div style="font-family:Lucida Grande,Lucida Sans,Lucida Sans Unicode,Arial,Helvetica,Verdana,sans-serif; color:#323232; font-size:18px; font-weight:600; padding-bottom:10px;">最新音乐:</div>
                                                        <ul style="padding: 5px 0px 10px 35px; margin: 0px; font-family: Lucida Grande,Lucida Sans,Lucida Sans Unicode,Arial,Helvetica,Verdana,sans-serif; line-height:25px; font-size: 14px;">
                                                            %mailContent2
                                                        </ul>
                                                    </td>
                                                </tr>
                                                <tr>
                                                    <td align="center" valign="top" style="background-color: #fff;">
                                                        <table border="0" cellpadding="0" cellspacing="0" width="100%">
                                                            <tbody>
                                                                <tr>
                                                                    <td valign="top" style="padding: 25px 40px 5px;">
                                                                        <div style="text-align: left; font-family:Lucida Grande,Lucida Sans,Lucida Sans Unicode,Arial,Helvetica,Verdana,sans-serif; font-size: 15px; margin-bottom: 5px; color: #323232; line-height: 25px;">
                                                                            %mailContent3
                                                                        </div>
                                                                    </td>
                                                                </tr>
                                                            </tbody>
                                                        </table>
                                                    </td>
                                                </tr>
                                                <tr>
                                                    <td align="center" valign="top" width="650" style="padding: 15px 40px; background-color: #fff;">
                                                        <div style="text-align: left; font-family: Lucida Grande,Lucida Sans,Lucida Sans Unicode,Arial,Helvetica,Verdana,sans-serif; font-size: 15px; margin-bottom: 5px; color: #323232; line-height: 25px;">Cheers,<br>Python System</div><div style="text-align: left; font-family: Lucida Grande,Lucida Sans,Lucida Sans Unicode,Arial,Helvetica,Verdana,sans-serif; font-size: 15px; margin-bottom: 5px; color: #323232; line-height: 25px;"><br></div><div style=" text-align: right ; ; ; ; ; ; ; ; ; ; "><span style="font-size: x-small;"></span></div>
                                                    </td>
                                                </tr>
                                            </tbody>
                                        </table>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </td>
                </tr>
            </tbody>
        </table>
    </div>
</body>
</html>
"""
mailMsg = mailMsg.replace('%mailContent1', mailContent1)
mailMsg = mailMsg.replace('%mailContent2', mailContent2)
mailMsg = mailMsg.replace('%mailContent3', mailContent3)


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