#! /usr/bin/evn python

import sys
import time

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