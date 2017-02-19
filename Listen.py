# !/usr/bin/env python
# __*__coding=utf8__*__
import itchat
from auto_reply import wechat

itchat.auto_login(hotReload=True, enableCmdQR=True)
itchat.run()
