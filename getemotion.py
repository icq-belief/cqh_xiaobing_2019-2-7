# -*- coding=utf-8 -*-

# 导入模块
import random
import requests
import re
from bs4 import BeautifulSoup
import bs4
import os

# 创建请求头列表，帮助我们在进行数据爬取的时候伪装成浏览器
my_headers = [
    "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/537.75.14",
    "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Win64; x64; Trident/6.0)",
]

kv = {"User-Agent": "Mozilla/5.0"}

num = 1

def getHTMLText(url, headers):
    try:
        # 随机从headers列表中选择一个header使用
        random_header = random.choice(headers)
        r = requests.get(url, headers={"User-Agent": random_header}, timeout=30)
        # 校验是否爬取成功，如果获取失败，输出“爬取失败”
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        # print r.text
        return r.text
    except:
        print("爬取失败")


def getImgList(Ilist, html):
    # 使用python自带的html解析器，html.parser进行返回的html数据的解析工作
    soup = BeautifulSoup(html, "html.parser")
    # print html

    # 分析解析后的html代码，通过正则表达式获取每一个图片对应的url地址，然后组成获取url的正则表达式
    pattern_img = re.compile(r'data-original="(.+?)"')
    # 获取图片对应的标题
    pattern_title = re.compile(r'alt="(.+?)"')
    # 找到所有的图片url值
    imgList = re.findall(pattern_img, html)
    # print imgList
    # 获取所有的图片对应的标题信息
    titleList = re.findall(pattern_title, html)
    # print titleList[0].encode('utf-8')

    # 将每一对urli地址和title组成一个列表项，放入到另外一个列表项中可以通过下表进行调用
    for i in range(len(imgList)):
        # print i,
        titleList[i] = titleList[i].encode('utf-8')
        # print titleList[i]
        Ilist.append([imgList[i], titleList[i]])
    return Ilist


# 判断是否存在指定的文件夹，然后创建文件夹
def mkdir():
    if not os.path.exists('img'):
        os.mkdir('img')


# 发送图片,并且保存图片
def saveImg(Ilistcontent):
    # print (Ilistcontent[0],Ilistcontent[1])
    # mkdir()
    img_content = requests.get(Ilistcontent[0]).content
    # t = chinese_to_alpha.main(Ilistcontent[1].decode('utf-8'))
    global num
    img_title = '%s' % num
    num += 1
    # img_title = test.hanzi2pinyin_split(string=Ilistcontent[1].decode('utf-8'), split="", firstcode=True)
    # print (img_title)
    img_path = ""
    print (Ilistcontent[0])
    if (Ilistcontent[0][-8:-4] == '.jpg'):
        # img_path = 'images/%s.jpg' % (Ilistcontent[1].decode('utf-8'))
        img_path = 'images/%s.jpg' % img_title

    elif (Ilistcontent[0][-8:-4] == '.gif'):
        # img_path = 'images/%s.gif' % (Ilistcontent[1].decode('utf-8'))
        img_path = "images/%s.gif" % img_title

    elif (Ilistcontent[0][-4:] == '.jpg'):
        img_path = 'images/%s.jpg' % img_title
    elif (Ilistcontent[0][-4:] == '.gif'):
        img_path = "images/%s.gif" % img_title
    # if os.path.exists(img_path):
    #     return img_path

    with open(img_path, 'wb') as f:
        f.write(img_content)
        f.close()
    return img_path


def download(page):
    Ilist = []
    url = "https://www.doutula.com/photo/list/?page=%d" % page
    html = getHTMLText(url, my_headers)
    Ilist = getImgList(Ilist, html)
    # printImg(Ilist,page)
    return Ilist


# page = 1
def getRandomEmoticon():
    print("下载图片")
    num = random.randint(1,500)
    page = num
    print("第%d页" % page)
    Ilist = download(page)
    i = random.randint(0, len(Ilist) - 1)
    print("第%d张图" % i)
    path = saveImg(Ilist[i])
    return path


if __name__ == '__main__':
    print(getRandomEmoticon())