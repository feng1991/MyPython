#! /usr/bin/evn python
# coding=utf-8
# -*- coding:utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import sys
import time

class QQZone:
    username = ''
    password = ''
    driver = ''

    def __init__(self,u,p):
        self.username = u
        self.password = p
        self.driver = webdriver.PhantomJS('D:/software/it/phantomjs-2.1.1/bin/phantomjs.exe')
        self.driver.implicitly_wait(3)
        self.driver.get('https://user.qzone.qq.com/%s/infocenter' % u)
        # print(self.driver.title)

    # 输出到文本
    def output(self):
        content = self.driver.page_source.encode('utf-8')
        fileObj = open('d:/data/programming/python/OP/test.txt', 'wb')
        # fileObj = open('d:/data/programming/python/OP/test.txt','w',encoding='utf-8')
        fileObj.write(content)
        fileObj.close()

    # 登录
    def login(self):
        # 切换到登录iframe
        self.driver.switch_to.frame('login_frame')
        # content = self.driver.page_source.encode('utf-8')
        # 点击账号密码输入
        self.driver.find_element_by_id('switcher_plogin').click();
        time.sleep(3)
        # 填入账号密码
        elem = self.driver.find_element_by_id('u')
        elem.send_keys(self.username)
        elem = self.driver.find_element_by_id('p')
        elem.send_keys(self.password)
        # elem.send_keys(Keys.ENTER)  #点击键盘上的Enter按钮
        self.driver.find_element_by_id('login_button').click()
        print('登录完成')
        # self.driver.refresh()
        time.sleep(5)
        # cookies = self.driver.get_cookies()
        # self.dirver.execute_script('window.scrollTo(0,document.body.scrollHeight)')
        # self.driver.save_screenshot('screenshot.png')
        for i in range(5):
            self.driver.execute_script('window.scrollBy(0,800)')
            time.sleep(1)
        print('加载完成')

    # 自动点赞
    def praise(self):
        praises = self.driver.find_elements_by_css_selector('.qz_like_btn_v3')
        print('动态数量:%s' % len(praises))
        for v in praises:
            className = v.get_attribute('class')
            if 'item-on' not in className:
                icon = v.find_element_by_css_selector('.icon-op-praise')
                # icon.click() 很奇怪，可以获得a标签的属性，但不能触发点击事件
                ActionChains(self.driver).click(icon).perform()
                time.sleep(1)
        # print(self.driver.find_element_by_css_selector('#feed_friend_list').text)
        # self.driver.execute_script("document.querySelector('.qz_like_btn_v3').click()")
        self.driver.close()



qqzone = QQZone('这里是账号','这里是密码')
qqzone.login()
qqzone.praise()
sys.exit()
