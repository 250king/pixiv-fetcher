# P站图片抓取程序 v1.0
# 仅用于个人用途
# Copyright 2020 250king. All rights reserved.
# Apache License v2.0
# Power by Python v3.8.1
import requests
import time  # 这个玩意就很有必要了，尤其对于这种图片大站
from win32com.client import Dispatch
from urllib import parse

cookie = input("cookie：")
UA = input("UA：")
keyword = parse.quote(input("搜索词（日文）："))  # URL编码
k = int(input("开始页数："))  # 搜索页面从1开始
end = int(input("结束页数："))
api = Dispatch('ThunderAgent.Agent64.1')  # 针对迅雷最新版本
i = j = 0
count = 0  # 计数有多少个图片
begin = int(time.time())  # 好奇算一下时长
while k <= end:  # 至于要爬多少你自己定了
    URL = "https://www.pixiv.net/ajax/search/artworks/" + keyword + "?word=%E7%A7%81%E3%81%AB%E5%A4%A9%E4%BD%BF%E3%81%8C%E8%88%9E%E3%81%84%E9%99%8D%E3%82%8A%E3%81%9F&order=date_d&mode=all&p=" + str(k) + "&s_mode=s_tag&type=all"
    headers = {
        "cookie": cookie,
        "user-agent": UA,
        "referer": URL
    }
    session = requests.get(URL, headers=headers)
    print("获得" + URL + "的JSON数据")
    JSON = session.json()
    session.close()
    while i < len(JSON["body"]["illustManga"]["data"]):
        ID = JSON["body"]["illustManga"]["data"][i]["id"]
        URL = "https://www.pixiv.net/ajax/illust/" + ID + "/pages?lang=zh"
        session = requests.get(URL, headers=headers)
        print("\t获得" + URL + "的JSON数据")
        JSON1 = session.json()
        session.close()
        while j < len(JSON1["body"]):
            URL = JSON1["body"][j]["urls"]["original"]
            api.AddTask(URL)
            print("将" + URL + "加入到待下载队列")
            count += 1
            j += 1
        j = 0
        i += 1
        time.sleep(0.5)
    i = 0
    k += 1
api.CommitTasks()
print("共抓取" + str(count) + "，时长" + str(int(time.time()) - begin) + "秒")