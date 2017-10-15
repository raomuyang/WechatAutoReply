# __*__coding__*__

import os
import re
import shutil
import threading

import itchat
from itchat.content import *

from AutoReplyAPI import api
import Stand

mid = '@搅屎棍机器人'
lock = threading.Lock()


@itchat.msg_register(TEXT, isFriendChat=False, isGroupChat=True, isMpChat=False)
def auto_reply_group_text(msg):
    if re.findall(mid, msg["Text"]).__len__() > 0 and msg["Text"].__len__() - mid.__len__() < 3:
        itchat.send_msg(msg="我来了", toUserName=msg['FromUserName'])
        return "@img@resources/hello.jpg"

    elif re.findall("(@.*\s)", msg["Text"]).__len__() > 0 and re.findall(mid, msg["Text"]).__len__() == 0:
        return

    if re.findall(mid, msg["Text"]).__len__() > 0 and msg["Text"].__len__() - mid.__len__() >= 3:
        msg["Text"] = msg["Text"].replace(mid, ",")
    resp = api.ask(msg["Text"])
    if resp is not None:
        itchat.send_msg(msg=resp, toUserName=msg['FromUserName'])


@itchat.msg_register(TEXT, isFriendChat=True, isGroupChat=False)
def auto_reply_friends_text(msg):
    hello = Stand.is_say_hello(msg["Text"])
    if hello > 0:
        return "@img@resources/hello.jpg"
    resp = api.ask(msg["Text"])
    if resp is not None:
        itchat.send_msg(msg=resp, toUserName=msg['FromUserName'])


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
            resp = api.ask(loc + "的天气")
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
            f = open("result/received.txt", "a")
        except Exception:
            os.mkdir("result")
        res = {"type": _type, "id": _id}
        f.write(str(res) + "\n")
        f.close()
        shutil.move(_id, "result/" + _id)
    finally:
        lock.release()





