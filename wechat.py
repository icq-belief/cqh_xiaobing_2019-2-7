# -*- coding:utf-8 -*-
from __future__ import unicode_literals
# import getemotion
import json
import itchat
import requests
# import platform
import os
import re
import random
import threading
from beta import wav2text
# 登录和初始化

# 设置已回复人员列表,限制刷消息的人
replied = {}
userId = ''
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# 设置回复消息的最大次数
# MAX_LIMIT_TEXT = 5
# MAX_LIMIT_PICTURE = 5
MAX_LIMIT_MSG = 10
MAX_LIMIT_VIDEO = 4
MAX_LIMIT_GROUPTEXT = 3

def main():
    itchat.auto_login(enableCmdQR=2 ,hotReload=True)
    itchat.run()


# def checkapi():
#     try:
#         inf = open('api.inf', 'r')
#         api = inf.readline().replace('\n','')
#         inf.close()
#     except:
#         print('请前往 http://www.tuling123.com 申请机器人API，并填写在相同目录下的“api.inf”文件首行！')
#         input()


# 图灵机器人回复部分

# def talk(info, userid=None):
#     url = 'http://www.tuling123.com/openapi/api'
#     inf = open('api.inf', 'r')
#     api = inf.readline()
#     inf.close()
#     param = json.dumps(
#         {"key": api, "info": info, "userid": userid})
#     callback = requests.post(url, data=param)
#     result = eval(callback.text)
#     code = result['code']
#     if code == 100000:
#         recontent = result['text']
#     elif code == 200000:
#         recontent = result['text'] + result['url']
#     elif code == 302000:
#         recontent = result['text'] + result['list'][0]['info'] + \
#             result['list'][0]['detailurl']
#     elif code == 308000:
#         recontent = result['text'] + result['list'][0]['info'] + \
#             result['list'][0]['detailurl']
#     else:
#         recontent = '[助理Neo暂时还不会回应你的这句话.Sad Face.]'
#     return recontent


# userid通过用户名的md5产生
# 用于用户名的加密
def md5(str):
    import hashlib
    md = hashlib.md5()
    md.update(str.encode('utf-8'))
    return md.hexdigest()


# 注册微信消息,对于微信接受到的文字消息的回复,设置了每个人每天4次的回复频率
@itchat.msg_register([itchat.content.TEXT,itchat.content.PICTURE])
def text_reply(msg):
    # 让小冰回答
    global userId
    userId = msg['FromUserName']
    xbAnswer(msg)
    print(getUserNickName(msg) + "发来的消息:\n" + getText(msg))


# 获取昵称
def getUserNickName(msg):
    fromUserName = msg['FromUserName']
    fromUser = itchat.search_friends(userName=fromUserName)
    nickName = fromUser['NickName']
    return nickName


# 获取文字
def getText(msg):
    if msg['Type'] == 'Text':
        return msg['Text']
    else:
        return "发送的其他类型回复"


# 向智能小冰提问
def xbAnswer(msg):
    xb = itchat.search_mps(name='小冰')[0]
    quest = getText(msg)
    print(quest)
    if msg['Type'] == 'Picture':
        # msg['Text'](msg['FileName'])
        msg['Text']('./images/' + msg['FileName'])
        res_path = './images/' + msg['FileName']
        itchat.send_image(res_path, xb['UserName'])
        # itchat.send_image(msg['FileName'], xb['UserName'])
    else:
        itchat.send_msg(quest, xb['UserName'])
        # 回复给好友
    # elif replied[md5(msg['FromUserName']+'_MSG')] < MAX_LIMIT_TEXT:
    #     replied[md5(msg['FromUserName']+'_MSG')] += 1
    #     if msg['Type'] == 'Picture':
    #         # msg['Text'](msg['FileName'])
    #         msg['Text']('./images/' + msg['FileName'])
    #         res_path = './images/' + msg['FileName']
    #         itchat.send_image(res_path, xb['UserName'])
    #     else:
    #         itchat.send_msg(quest, xb['UserName'])
    # elif replied[md5(msg['FromUserName']+'_MSG')] > MAX_LIMIT_TEXT:
    #
    #     pass
    # else:
    #     replied[md5(msg['FromUserName']+'_MSG')] += 1
    #     itchat.send_msg(u"[主人不让我欺负你.So,have a nice day & See you!]", msg['FromUserName'])
    #
    # if msg['Type'] == 'Picture':
    #     # msg['Text'](msg['FileName'])
    #     itchat.send_image(msg['FileName'], xb['UserName'])
    # else:
    #     itchat.send_msg(quest, xb['UserName'])


# 接收到小冰的公众号消息发来之后,转发给原用户
@itchat.msg_register([itchat.content.TEXT,itchat.content.PICTURE,itchat.content.RECORDING], isMpChat=True)
def map_reply(msg):
    text = getText(msg)
    global userId
    if not replied.get(md5(userId+'_MSG')):
        replied[md5(userId+'_MSG')] = 1
        if msg['Type'] == 'Picture':
            # msg['Text'](msg['FileName'])
            msg['Text']('./images/' + msg['FileName'])
            res_path = './images/' + msg['FileName']
            itchat.send_msg("[陈主人不在.暂由助理Neo开始回复你.有事请留言.主人看到后会及时回复你.] ", userId)
            itchat.send_image(res_path, userId)
        elif msg['Type'] == 'Recording':
            try:
                wav2text.transcode('./records/' + msg['FileName'])
                filename = msg['FileName'].replace('mp3', 'wav')
                text = wav2text.wav_to_text('./records/' + filename)
                itchat.send_msg("[陈主人不在.暂由助理Neo开始回复你.有事请留言.主人看到后会及时回复你.] " + text, userId)
            except Exception as e:
                print('转换期间出错,错误信息:%s.回复默认表情' % e)
        else:
            itchat.send_msg("[陈主人不在.暂由助理Neo开始回复你.有事请留言.主人看到后会及时回复你.]  " + text, userId)
    elif replied[md5(userId+'_MSG')] < MAX_LIMIT_MSG:
        replied[md5(userId+'_MSG')] += 1
        if msg['Type'] == 'Picture':
            # msg['Text'](msg['FileName'])
            msg['Text']('./images/' + msg['FileName'])
            res_path = './images/' + msg['FileName']
            itchat.send_msg("[陈主人不在.暂由助理Neo开始回复你.有事请留言.主人看到后会及时回复你.] ", userId)
            itchat.send_image(res_path, userId)
        elif msg['Type'] == 'Recording':
            try:
                wav2text.transcode('./records/' + msg['FileName'])
                filename = msg['FileName'].replace('mp3', 'wav')
                text = wav2text.wav_to_text('./records/' + filename)
                itchat.send_msg("[陈主人不在.暂由助理Neo开始回复你.有事请留言.主人看到后会及时回复你.] " + text, userId)
            except Exception as e:
                print('转换期间出错,错误信息:%s.回复默认表情' % e)
        else:
            itchat.send_msg("[陈主人不在.暂由助理Neo开始回复你.有事请留言.主人看到后会及时回复你.]  " + text, userId)
    elif replied[md5(userId + '_MSG')] > MAX_LIMIT_MSG:
        pass
    else:
        replied[md5(userId + '_MSG')] += 1
        itchat.send_msg(u"[陈主人不让我欺负你.So,have a nice day & See you!]", userId)
        # itchat.send_msg('上图为微软小冰回答', userId)
    # else:
    #     if not replied.get(md5(userId + '_MSG_TEXT')):
    #         # 当消息不是由自己发出的时候
    #         replied[md5(userId + '_MSG_TEXT')] = 1
    #         itchat.send_msg("[陈主人不在.暂由助理Neo开始回复你.有事请留言.主人看到后会及时回复你.]  " + text, userId)
    #     elif replied[md5(userId + '_MSG_TEXT')] < MAX_LIMIT_TEXT:
    #         replied[md5(userId + '_MSG_TEXT')] += 1
    #         itchat.send_msg("[陈主人不在.暂由助理Neo开始回复你.有事请留言.主人看到后会及时回复你.]  " + text, userId)
    #     elif replied[md5(userId + '_MSG_TEXT')] > MAX_LIMIT_TEXT:
    #         pass
    #     else:
    #         replied[md5(userId + '_MSG_TEXT')] += 1
    #         itchat.send_msg(u"[陈主人不让我欺负你.So,have a nice day & See you!]", userId)

    # elif replied[md5(userId+'_MSG')] < MAX_LIMIT_TEXT:
    #     replied[md5(userId+'_MSG')] += 1
    #     if msg['Type'] == 'Picture':
    #         # msg['Text'](msg['FileName'])
    #         msg['Text']('./images/' + msg['FileName'])
    #         res_path = './images/' + msg['FileName']
    #         itchat.send_msg("[Master陈不在.暂由助理Neo开始回复你.有事请留言.主人看到后会及时回复你.] ", userId)
    #         itchat.send_image(res_path,userId)
    #         # itchat.send_msg('上图为微软小冰回答', userId)
    #     else:
    #         itchat.send_msg("[Master陈不在.暂由助理Neo开始回复你.有事请留言.主人看到后会及时回复你.]  "+ text, userId)
    # elif replied[md5(userId+'_MSG')] > MAX_LIMIT_MSG:
    #     pass
    # else:
    #     replied[md5(userId+'_MSG')] += 1
    #     itchat.send_msg(u"[主人不让我欺负你.So,have a nice day & See you!]", msg['FromUserName'])
#
# @itchat.msg_register(itchat.content.TEXT)
# def text_reply(msg):
#     # reply = talk(msg['Text'], md5(msg['FromUserName']))
#     reply = u"[Master陈不在 我是助理Neo 有事请留言]  {}".format(talk(msg['Text']), md5(msg['FromUserName']))
#     User = itchat.search_friends(userName=msg['FromUserName'])
#     if User['RemarkName'] == '':
#         NickName = User['NickName']
#     else:
#         NickName = '%s(%s)' % (User['NickName'], User['RemarkName'])
#     print('------------------------------------------------------------------------------')
#     print('%s悄悄对您说：%s' % (NickName, msg['Text']))
#     print('AI帮您回复%s：%s' % (NickName, reply))
#     print('------------------------------------------------------------------------------')
#
#     if not replied.get(md5(msg['FromUserName']+'_TEXT')):
#         # 当消息不是由自己发出的时候
#         replied[md5(msg['FromUserName']+'_TEXT')] = 1
#         return reply
#         # 回复给好友
#     elif replied[md5(msg['FromUserName']+'_TEXT')] < MAX_LIMIT_TEXT:
#         replied[md5(msg['FromUserName']+'_TEXT')] += 1
#         return reply
#     elif replied[md5(msg['FromUserName']+'_TEXT')] > MAX_LIMIT_TEXT:
#         pass
#     else:
#         replied[md5(msg['FromUserName']+'_TEXT')] += 1
#         return u"[主人不让我多跟你聊天.So,have a nice day!]"


# 对于地图分享的回复,每天只会回复每人一次
@itchat.msg_register(itchat.content.MAP)
def map_reply(msg):
    # reply = talk(msg['Text'], md5(msg['FromUserName']))
    User = itchat.search_friends(userName=msg['FromUserName'])
    if User['RemarkName'] == '':
        NickName = User['NickName']
    else:
        NickName = '%s(%s)' % (User['NickName'], User['RemarkName'])
    print('------------------------------------------------------------------------------')
    print('%s向您分享了地点：%s' % (NickName, msg['Text']))
    # print('AI帮您回复%s：%s' % (NickName, reply))
    print('------------------------------------------------------------------------------')
    if not replied.get(md5(msg['FromUserName']+'_MAP')):
        replied[md5(msg['FromUserName'] + '_MAP')] = 1
        return u"[%s,在%s玩得开心.就不要调戏我的助理Neo了.航留.] " % (NickName, msg['Text'])
    else:
        pass


# 对于名片分享的回复,每天只会回复每人一次
@itchat.msg_register(itchat.content.CARD)
def card_reply(msg):
    User = itchat.search_friends(userName=msg['FromUserName'])
    if User['RemarkName'] == '':
        NickName = User['NickName']
    else:
        NickName = '%s(%s)' % (User['NickName'], User['RemarkName'])

    reply = '[%s,助理Neo代主人谢谢你的推荐,我们会成为好朋友的!今天就不再回复你的名片推荐了,谢谢. ] ' % NickName
    print('------------------------------------------------------------------------------')
    print('%s向您推荐了%s' % (NickName, msg['Text']['NickName']))
    print('AI帮您回复%s：%s' % (NickName, reply))
    print('------------------------------------------------------------------------------')
    if not replied.get(md5(msg['FromUserName']+'_CARD')):
        replied[md5(msg['FromUserName'] + '_CARD')] = 1
        return reply
    else:
        pass


@itchat.msg_register(itchat.content.NOTE)
def note_reply(msg):
    print(msg)


# 对于分享的文章或者链接进行回复,进行一些次数的限制
@itchat.msg_register(itchat.content.SHARING)
def sharing_reply(msg):
    # reply = talk(msg['Text'], md5(msg['FromUserName']))
    User = itchat.search_friends(userName=msg['FromUserName'])
    if User['RemarkName'] == '':
        NickName = User['NickName']
    else:
        NickName = '%s(%s)' % (User['NickName'], User['RemarkName'])
    reply = u"[%s,助理Neo代主人感谢你的分享,陈主人会在闲暇时间查看你分享的内容的.今天Neo就不再回复你的内容分享了,谢谢.] " % NickName
    print('------------------------------------------------------------------------------')
    print('%s向您分享了链接：%s' % (NickName, msg['Text']))
    print('AI帮您回复%s：%s' % (NickName, reply))
    print('------------------------------------------------------------------------------')
    if not replied.get(md5(msg['FromUserName']+'_SHARING')):
        replied[md5(msg['FromUserName'] + '_SHARING')] = 1
        return reply
    else:
        pass


# 收到别人的私聊图片时候,回复爬取到的斗图啦上的图片,只会回复5次
# @itchat.msg_register(itchat.content.PICTURE)
# def pic_reply(msg):
#     # msg['Text']('./images/' + msg['FileName'])
#     User = itchat.search_friends(userName=msg['FromUserName'])
#     if User['RemarkName'] == '':
#         NickName = User['NickName']
#     else:
#         NickName = '%s(%s)' % (User['NickName'], User['RemarkName'])
#     print('------------------------------------------------------------------------------')
#     print('%s给您发送了一个表情/图片，已经存入img目录，文件名：%s' % (NickName, msg['FileName']))
#     print('AI帮您回复%s默认表情default.gif' % NickName)
#     print('------------------------------------------------------------------------------')
#
#     path_list = return_image_path()
#     res_path = './images/%s' % (path_list[random.randint(0, (len(path_list)-1))])
#
#     # res_path = getemotion.getRandomEmoticon()
#     res_path = '@img@./%s' % res_path
#
#     if not replied.get(md5(msg['FromUserName']+'_PICTURE')):
#         # 当消息不是由自己发出的时候
#         replied[md5(msg['FromUserName']+'_PICTURE')] = 1
#         return u"[主人暂时不在.继续发送图片,助理Neo将会与你斗图,就一下下.Don't be too serious.] "
#         # 回复给好友
#     elif replied[md5(msg['FromUserName']+'_PICTURE')] < MAX_LIMIT_PICTURE:
#         replied[md5(msg['FromUserName']+'_PICTURE')] += 1
#         return res_path
#     elif replied[md5(msg['FromUserName']+'_PICTURE')] > MAX_LIMIT_PICTURE:
#         pass
#     else:
#         replied[md5(msg['FromUserName']+'_PICTURE')] += 1
#         return u"[主人让Neo斗图让着你.See you!] "


@itchat.msg_register(itchat.content.RECORDING)
def rec_reply(msg):
    print('我发送的语音类型',msg['Type'])
    global userId
    userId = msg['FromUserName']
    xb = itchat.search_mps(name='小冰')[0]
    # 是否开启语音识别，需要安装ffmpeg和pydub
    enable_voice_rec = True
    # enable_voice_rec = False
    msg['Text']('./records/' + msg['FileName'])
    User = itchat.search_friends(userName=msg['FromUserName'])
    if User['RemarkName'] == '':
        NickName = User['NickName']
    else:
        NickName = '%s(%s)' % (User['NickName'], User['RemarkName'])

    if enable_voice_rec:
        msg['Text']('./records/' + msg['FileName'])
        # from beta import wav2text
        try:
            wav2text.transcode('./records/' + msg['FileName'])
            filename = msg['FileName'].replace('mp3','wav')
            text = wav2text.wav_to_text('./records/' + filename)
            itchat.send_msg(text, xb['UserName'])
        except Exception as e:
            print('转换期间出错,错误信息:%s.回复默认表情' % e)
            return '@img@./records/default.gif'
        # reply = talk(text, md5(msg['FromUserName']))
        print('------------------------------------------------------------------------------')
        print('%s给您发送了一条语音，已经存入records目录，文件名：%s' % (NickName, msg['FileName']))
        print('智能识别该消息内容为：%s' % text)
        # print('AI帮您回复%s：%s' % (NickName, reply))
        print('------------------------------------------------------------------------------')
        # return reply
    else:
        print('------------------------------------------------------------------------------')
        print('%s给您发送了一条语音，已经存入records目录，文件名：%s' % (NickName, msg['FileName']))
        print('AI帮您回复%s默认表情default.gif' % NickName)
        print('------------------------------------------------------------------------------')
        return '@img@./records/default.gif'


@itchat.msg_register(itchat.content.ATTACHMENT)
def att_reply(msg):
    # msg['Text']('./attachments/' + msg['FileName'])
    User = itchat.search_friends(userName=msg['FromUserName'])
    if User['RemarkName'] == '':
        NickName = User['NickName']
    else:
        NickName = '%s(%s)' % (User['NickName'], User['RemarkName'])
    print('------------------------------------------------------------------------------')
    print('%s给您发送了一个文件，已经存入attachments目录，文件名：%s' % (NickName, msg['FileName']))
    print('AI帮您回复% s：这是什么东西？我收下了。' % NickName)
    print('------------------------------------------------------------------------------')
    if not replied.get(md5(msg['FromUserName']+'_ATTACHMENT')):
        replied[md5(msg['FromUserName'] + '_ATTACHMENT')] = 1
        return '[%s,给我家主人发送的%s. Neo代为收下了.今天就不再回复你的文件分享了.谢谢] ' % (NickName, msg["FileName"])
    else:
        pass


# 别人发送的视频时,自动回复视频,视频事先从抖音上爬取好了
@itchat.msg_register(itchat.content.VIDEO)
def video_reply(msg):
    # msg['Text']('./videos/' + msg['FileName'])
    User = itchat.search_friends(userName=msg['FromUserName'])
    if User['RemarkName'] == '':
        NickName = User['NickName']
    else:
        NickName = '%s(%s)' % (User['NickName'], User['RemarkName'])
    print('------------------------------------------------------------------------------')
    print('%s给您发送了一个视频，已经存入videos目录，文件名：%s' % (NickName, msg['FileName']))
    print('AI帮您回复% s默认表情default.gif' % NickName)
    print('------------------------------------------------------------------------------')
    path_list = return_video_path()
    res_path = './videos/%s' % (path_list[random.randint(0, (len(path_list)-1))])

    if not replied.get(md5(msg['FromUserName']+'_VIDEO')):
        # 当消息不是由自己发出的时候
        replied[md5(msg['FromUserName']+'_VIDEO')] = 1
        return u"[陈主人暂时不在.继续发送视频.助理Neo将会发送一些小视频给你.Don't be too serious.] "
        # 回复给好友
    elif replied[md5(msg['FromUserName']+'_VIDEO')] < MAX_LIMIT_VIDEO:
        replied[md5(msg['FromUserName']+'_VIDEO')] += 1
        itchat.send_video(res_path, msg['FromUserName'])
    elif replied[md5(msg['FromUserName']+'_VIDEO')] > MAX_LIMIT_VIDEO:
        pass
    else:
        replied[md5(msg['FromUserName']+'_VIDEO')] += 1
        return u"[福利 are not free.发送红包后继续.Have a nice day & See you!] "

    # res_path = './videos/40.mp4'

    # itchat.send_video(res_path, msg['FromUserName'])
    # print(itchat.send_video(res_path, msg['FromUserName']))


# def return_image_path():
#     s = os.listdir('./images')
#     # print(s)
#     return_s = []
#     for i in s:
#         if re.findall('(^\d+\.gif)|(^\d+\.jpg)', i):
#             return_s.append(i)
#         else:
#             pass
#     return return_s


def return_video_path():
    s = os.listdir('./videos')
    return_s = []
    for i in s:
        if i[-4:] != '.mp4':
            pass
        else:
            return_s.append(i)
    return return_s


def del_pic():
    s = os.listdir('./images')
    for i in s:
        if (re.findall('(^.*\.png)|(^.*\.gif)',i)):
            file_path = os.path.join(BASE_DIR, 'images',i)
            os.remove(file_path)
            print(file_path)


def del_rec():
    s = os.listdir('./records')
    for i in s:
        if (re.findall('(^.*\.mp3)|(^.*\.wav)',i)):
            file_path = os.path.join(BASE_DIR, 'records',i)
            os.remove(file_path)
            print(file_path)


# 设置定时器,每12个小时清理图片缓存,不再回复列表清单
def fun_timer():
    print('定时器开始工作')
    replied.clear()
    del_pic()
    del_rec()
    # for i in range(1,400):
    #     try:
    #         getemotion.getRandomEmoticon()
    #     except Exception as e:
    #         print('下载出现一个异常:%s,继续下一个下载' % e)
    #         continue
    global timer
    timer = threading.Timer(43200, fun_timer)
    timer.start()


# @itchat.msg_register(itchat.content.FRIENDS)
# def fri_reply(msg):
#     itchat.add_friend(**msg['Text'])
#     itchat.send_msg('你好，我的人类朋友！', msg['RecommendInfo']['UserName'])


# @itchat.msg_register(itchat.content.TEXT, isGroupChat=True)
# def group_reply(msg):
#     if msg['isAt']:
#         reply = talk(msg['Content'], md5(msg['ActualUserName']))
#         print(
#             '------------------------------------------------------------------------------')
#         print('%s在群聊中对您说：%s' % (msg['ActualNickName'], msg['Content'].replace('\u2005',' ')))
#         print('AI帮您回复%s：%s' % (msg['ActualNickName'], reply))
#         print(
#             '------------------------------------------------------------------------------')
#
#         if not replied.get('_GROUPTEXT'):
#             # 当消息不是由自己发出的时候
#             replied['_GROUPTEXT'] = 1
#             itchat.send('@%s %s' % (msg['ActualNickName'], u"[陈主人暂时不在.目前由助理Neo回复你.主人回来后会回复你.] "), msg['FromUserName'])
#             # 回复给好友
#         elif replied['_GROUPTEXT'] < MAX_LIMIT_GROUPTEXT:
#             replied['_GROUPTEXT'] += 1
#             itchat.send('@%s %s' % (msg['ActualNickName'],u"[陈主人暂时不在.目前由助理Neo回复你.主人回来后会回复你.] " + reply), msg['FromUserName'])
#         elif replied['_GROUPTEXT'] > MAX_LIMIT_GROUPTEXT:
#             pass
#         else:
#             replied['_GROUPTEXT'] += 1
#             # return u"[陈主人不让我太闹腾.Neo就不再回复你了.See you!] "
#             itchat.send('@%s %s' % (msg['ActualNickName'], u"[陈主人不让我太闹腾.Neo将不再回复群中消息.Everybody Have a nice day & See you!] "), msg['FromUserName'])
    # else:
    #     print(
    #         '------------------------------------------------------------------------------')
    #     print('%s在群聊中说：%s' % (msg['ActualNickName'], msg['Content']))
    #     print(
    #         '------------------------------------------------------------------------------')


# @itchat.msg_register(itchat.content.PICTURE, isGroupChat=True)
# def grouppic_reply(msg):
#         # msg['Text']('./images/group/' + msg['FileName'])
#         print('------------------------------------------------------------------------------')
#         print('%s在群聊中发了一个表情/图片，已经帮您存入images/group目录，文件名为：%s' % (msg['ActualNickName'], msg['FileName']))
#         print('------------------------------------------------------------------------------')
#         res_path = getemotion.getRandomEmoticon()
#         res_path = '@img@./%s' % res_path
#
#         if not replied.get(md5(msg['ActualNickName']+'_GROUPPICTURE')):
#             # 当消息不是由自己发出的时候
#             replied[md5(msg['ActualNickName']+'_GROUPPICTURE')] = 1
#             itchat.send('@%s %s' % (msg['ActualNickName'], u"[陈主人不在.助理Neo会开始与你斗一下图.Don't be serious.]"), msg['FromUserName'])
#             # 回复给好友
#         elif replied[md5(msg['ActualNickName']+'_GROUPPICTURE')] < 4:
#             replied[md5(msg['ActualNickName']+'_GROUPPICTURE')] += 1
#             itchat.send(res_path, msg['FromUserName'])
#         elif replied[md5(msg['ActualNickName']+'_GROUPPICTURE')] > 4:
#             pass
#         else:
#             replied[md5(msg['ActualNickName']+'_GROUPPICTURE')] += 1
#             itchat.send('@%s %s' % (msg['ActualNickName'], u"[陈主人让我斗图让着你.Neo就不发了.See you!]"), msg['FromUserName'])
#
#             # return u"[主人让我斗图让着你.Neo就不发了.See you!] "
#
#         # itchat.send(res_path, msg['FromUserName'])

if __name__ == '__main__':
    # checkapi()
    timer = threading.Timer(0, fun_timer)
    timer.start()
    main()

    # return_video_path()
