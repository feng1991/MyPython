
import urllib.request
import json
import sys
import pygame
import time
import math


#获得access_token
def getAccessToken():
    # 百度语言
    apiKey = "q4NM67RFvDFbLa7SEDffNQNG"
    secretKey = "pGuDxDuixpol1EIli7Kb5VGG0RkYWLDQ"
    url = 'https://openapi.baidu.com/oauth/2.0/token?grant_type=client_credentials&client_id=%s&client_secret=%s' % (apiKey,secretKey)
    content = urllib.request.urlopen(url).read().decode()
    #print(content)
    result = json.loads(content)
    access_token = result['access_token']
    #print(result['access_token'])
    return access_token


def getAnswer(say):
    # 图灵机器人
    showapi_appid = "59348"
    showapi_sign = "7d9ca85135904b0ea7b1c78eb7b27a2c"
    # 获得回答
    send_data = urllib.parse.urlencode([
        ('showapi_appid', showapi_appid),
        ('showapi_sign', showapi_sign),
        ('info', say),
        ('userid', "userid")
    ])
    url = "http://route.showapi.com/60-27"
    req = urllib.request.Request(url)
    try:
        response = urllib.request.urlopen(req, data=send_data.encode('utf-8'), timeout=10)  # 10秒超时反馈
    except Exception as e:
        print(e)
    result = response.read().decode('utf-8')
    result_json = json.loads(result)
    answer = result_json['showapi_res_body']['text']
    return answer


def sayAnswer(order,answer,access_token):
    # 请求生成语音文件
    text = urllib.parse.quote(answer)
    per = 0
    spd = 4
    pit = 5
    vol = 9
    cuid = "123456Python"
    url = 'http://tsn.baidu.com/text2audio?tex=%s&per=%s&spd=%s&pit=%s&vol=%s&cuid=%s&tok=%s&lan=zh&ctp=1' % (
    text, per, spd, pit, vol, cuid, access_token)
    content = urllib.request.urlopen(url).read()
    soundFile = 'D:/data/programming/python/AI/sound/sound%s.mp3' % order
    open(soundFile, 'wb').write(content)
    # 播放声音
    pygame.mixer.init()
    pygame.mixer.music.load(soundFile)
    pygame.mixer.music.play()
    time.sleep(math.ceil(len(answer) / 4))
    pygame.mixer.music.stop()







access_token = getAccessToken()
order = 0
say = ''
#交互
while 1 == 1:
    say = input('随便说点什么吧: ')
    if len(say) == 0:
        continue
    if say == 'quit':
        break
    order = order + 1
    answer = getAnswer(say)
    print ('管家答到: ', answer)
    sayAnswer(order,answer,access_token)

