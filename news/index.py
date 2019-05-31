#! /usr/bin/evn python
# coding=utf-8
# -*- coding:utf-8 -*-

import urllib.request
import sys
import pymysql
import time
from bs4 import BeautifulSoup
import time
from selenium import webdriver
import tool
import sendEmail


class News:
    db = ''
    cursor = ''
    mailContent1 = ''
    mailContent2 = ''
    mailContent3 = ''

    # 判断是否已爬取
    def isRunToday(self):
        self.db = pymysql.connect(host='localhost', user='root', passwd='root', db='news', charset='utf8')
        self.cursor = self.db.cursor()
        sql = "SELECT addTime FROM `163` ORDER BY addTime DESC LIMIT 1"
        self.cursor.execute(sql)
        result = self.cursor.fetchone()
        if result is not None:
            todayTime = tool.getTimeOClockOfToday()
            if result[0] > todayTime:
                return 1
        return 0


    # 爬取网易新闻
    def getTechNews(self):
        content = urllib.request.urlopen('http://163.com').read()
        soup = BeautifulSoup(content, "html.parser")
        # ps = soup.find_all(attrs={'ne-module': "modules/tech/tech.js"}) 20190531作废
        ps = soup.find_all(attrs={'ne-module': "/www/index20170701/modules/tech/tech.js"})
        dataArr = []
        nowTime = int(time.time())
        title = ''
        href = ''
        for p in ps:
            ass = p.find_all('a')
            for a in ass:
                title = a.get_text().strip()
                if (title != '' and len(title) > 10):
                    href = a.get('href')
                    dataArr.append((title, href, nowTime))
                    self.mailContent1 = self.mailContent1 + '<li style="color:#323232;"><a href="%s">%s</a></li>' % (href, title)
                if (len(dataArr) > 8):
                    break
        # tool.dump(mailContent1)

        # 保存数据
        sql = "INSERT INTO `163` (name,url,addTime) values(%s,%s,%s)"
        results = self.cursor.executemany(sql, dataArr)
        self.db.commit()
        self.cursor.close()
        self.db.close()


    # 爬取网易云音乐新歌榜
    def getMusicNews(self):
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
        for title in titleArr:
            url = urlArr.pop(0)
            self.mailContent2 = self.mailContent2 + '<li style="color:#323232;"><a href="%s">%s</a></li>' % (url, title)


    # 获取笑话
    def getJoke(self):
        content = urllib.request.urlopen('http://www.joke-of-the-day.com/').read()
        soup = BeautifulSoup(content, 'html.parser')
        quote = soup.find('div', {'class': 'quote'})
        self.mailContent3 = quote.get_text().strip()


    # 发送邮件
    def sendEmail(self):
        server = sendEmail.SendEmail('smtp.qq.com', 'XXXXXXXX', 'XXXXXXXX')
        server.fillTpl(self.mailContent1, self.mailContent2, self.mailContent3)
        server.send('XXXXXXXX', ['XXXXXXXX'], 'Python系统', '尊敬的XXXXXXXX', '每日邮件')


    # 运行
    def run(self):
        if(self.isRunToday() == 0):
            print('开始执行')
            self.getTechNews()
            self.getMusicNews()
            self.getJoke()
            self.sendEmail()
            print('执行完成')
        else:
            print('今天已经执行过了哦~')




news = News();
news.run()






