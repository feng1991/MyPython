# coding=utf-8
# -*- coding:utf-8 -*-
import urllib.request
import sys
import pymysql
from bs4 import BeautifulSoup

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
for p in ps:
    ass = p.find_all('a')
    for a in ass:
        buf = a.get_text().strip()
        if(buf != '' and len(buf) > 8):
            dataArr.append((buf,a.get('href'),1))
# dump(dataArr)

# 保存数据
db = pymysql.connect(host='localhost',user='root',passwd='root',db='news',charset='utf8')
cursor = db.cursor()
sql = "INSERT INTO `163` (name,url,addTime) values(%s,%s,%s)"
results = cursor.executemany(sql,dataArr)
db.commit()
cursor.close()
db.close()
dump(results)