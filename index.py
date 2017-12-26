# coding=utf-8
# -*- coding:utf-8 -*-
import urllib.request
import sys
import pymysql
from bs4 import BeautifulSoup

# 打印
def dump(obj):
	print(type(obj))
	#print(obj)
	sys.exit(0)
	return

db = pymysql.connect('localhost','root','root','news')
cursor = db.cursor()
sql = "SELECT COUNT(*) FROM ifeng"
cursor.execute(sql)
results = cursor.fetchall()
db.close()
for row in results:
	print(row[0])
dump(results);


content = urllib.request.urlopen('http://163.com').read()
#dump(content)

#soup = BeautifulSoup("<html><body><p>hi</p></body></html>","html.parser")
soup = BeautifulSoup(content,"html.parser")
#dump(soup)

#ps = soup('p')
#ps = soup.find_all('html')
ps = soup.find_all(attrs={'ne-module':"modules/tech/tech.js"})
pStr = ''
for p in ps:
	ass = p.find_all('a')
	for a in ass:
		buf = a.get_text().strip()
		if(buf != '' and len(buf) > 8):
			#pStr = pStr + buf + '/' + a.get('href') + '\n'
			pStr = pStr + buf + '\n'
#print(pStr)


fileObj = open('d:/data/programming/python/test.txt','w',encoding='utf-8')
fileObj.write(pStr)
fileObj.close()