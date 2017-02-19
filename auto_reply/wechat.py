# __*__coding__*__

import itchat
from itchat.content import *
from auto_reply import Tuling
from auto_reply import Stand
import threading
import re


mid = '@搅屎棍机器人'
lock = threading.Lock()


@itchat.msg_register(TEXT, isFriendChat=False, isGroupChat=True, isMpChat=False)
def auto_reply_group_text(msg):
    if re.findall(mid, msg["Text"]).__len__() > 0 and msg["Text"].__len__() - mid.__len__() < 3:
        itchat.send_msg(msg="我来了", toUserName=msg['FromUserName'])
        return "@img@resources/hello.jpg"

    #这里要用正则表达式重新写一下
    elif re.findall("(@.*\s)", msg["Text"]).__len__() > 0 and re.findall(mid, msg["Text"]).__len__() == 0:
        return

    resp = Tuling.request_api1(msg["Text"])
    if resp is not None:
        is_send = reply_url(resp, msg)
        if not is_send:
            itchat.send_msg(msg=resp['text'], toUserName=msg['FromUserName'])


@itchat.msg_register(TEXT, isFriendChat=True, isGroupChat=False)
def auto_reply_friends_text(msg):
    hello = Stand.isSayHello(msg["Text"])
    if hello > 0:
        return "@img@resources/hello.jpg"
    resp = Tuling.request_api1(msg["Text"])
    if resp is not None:
        is_send = reply_url(resp, msg)
        if not is_send:
            itchat.send_msg(msg=resp['text'], toUserName=msg['FromUserName'])


@itchat.msg_register([PICTURE, CARD, NOTE, FRIENDS, SYSTEM], isFriendChat=True, isMpChat=False, isGroupChat=False)
def auto_reply_picture(msg):
    try:
        if msg["MsgType"] == 3:
            msg['Text'](msg["MsgId"])
            operate_tmp_file(PICTURE, msg["MsgId"])
        return "@img@resources/mengbi.gif"
    except Exception as e:
        print(str(e))


@itchat.msg_register(VIDEO, isFriendChat=True, isGroupChat=False)
def auto_reply_map(msg):
    try:
        msg['Text'](msg['MsgId'])
        operate_tmp_file(VIDEO, msg["MsgId"])
        return "@img@resources/mengbi.gif"
    except Exception as e:
        print(str(e))


@itchat.msg_register(RECORDING, isFriendChat=True, isGroupChat=False)
def auto_reply_map(msg):
    try:
        msg['Text'](msg['MsgId'])
        operate_tmp_file(RECORDING, msg["MsgId"])
        itchat.send_msg(msg="Oh闹我还听不懂语音", toUserName=msg['FromUserName'])
        return "@img@resources/mengbi.gif"
    except Exception as e:
        print(str(e))


@itchat.msg_register(MAP, isFriendChat=True, isGroupChat=True)
def auto_reply_map(msg):
    try:
        loc = msg["Content"].split(":")
        if loc is not None:
            loc = loc[0]
            itchat.send_msg(msg="我来帮你们查一下%s的天气吧" % loc, toUserName=msg['FromUserName'])
            resp = Tuling.request_api1(loc + "的天气")
            if resp is not None:
                itchat.send_msg(msg=resp['text'], toUserName=msg['FromUserName'])
            else:
                return "啊啊啊没有查到"
    except Exception as e:
        print(str(e))


def operate_tmp_file(_type, _id):
    print(type, _id)

    lock.acquire()
    try:
        try:
            f = open("result/reveiveds.txt", "a")
        except Exception:
            import os
            os.mkdir("result")
        res = {"type": _type, "id": _id}
        f.write(str(res) + "\n")
        f.close()
    finally:
        lock.release()


def reply_url(resp, msg):
    print("Response:", resp)
    if int(resp['code']) == 308000:
        count = 5
        url_list = resp['list']
        items = resp["text"]
        for item in url_list:
            if count <= 0:
                break
            i_str = item["name"] + " \n" + item["info"] + " \n" + item["detailurl"]
            items = items + "\n\n" + i_str
            count -= 1
        itchat.send_msg(msg=items, toUserName= msg['FromUserName'])
        return True
    if int(resp['code']) == 200000:
        items = resp["text"] + "\n" + resp["url"]
        itchat.send_msg(msg=items, toUserName=msg['FromUserName'])
        return True
    return False





