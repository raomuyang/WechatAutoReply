#!/usr/bin/env python
# -*- coding: utf-8 -*-
from abc import abstractmethod
from utils import globals

import json
import requests


class AutoReplyAPI(object):
    def __init__(self):
        self.logger = globals.logger
        self.api_info = globals.get_robot_api()

    @abstractmethod
    def ask(self, message, user_id=None, location=None):
        pass


class TulingAutoReply(AutoReplyAPI):
    def ask(self, message, user_id=None, location=None):
        return self.request_api1(msg=message, user_id=user_id, loc=location)

    def __init__(self):
        AutoReplyAPI.__init__(self)
        self.api_keys = self.api_info.get('keys', [])

    def request_api1(self, msg, user_id=None, loc=None):
        count = len(self.api_keys)
        retry = count

        response = None
        response_msg = None
        while retry > 0:
            api_key = self.api_keys[count - retry]
            api, data = self.get_request_entity_v1_0(api_key=api_key, msg=msg, user_id=user_id, location=loc)

            self.logger.info("request by tuling api v1, msg: {}, user_id: {}, location: {}".format(msg, user_id, loc))

            response = requests.post(api, json=data)
            response_msg = json.loads(response.text.replace("\'", "\""))

            if response.status_code / 100 == 2 and int(response_msg['code'] / 10000) != 4:
                break
            retry -= 1

        if response.status_code / 100 != 2 or int(response_msg['code'] / 10000) == 4:
            self.logger.error("Request answer failed, {}".format(response_msg))
            return None
        return self.format_msg_v1(response_msg)

    def request_api2(self, msg, user_id=None, loc=None):
        count = len(self.api_keys)
        if count == 0:
            self.logger.warning("Tuling api keys not found.")
            return

        retry = count
        response = None
        response_msg = None

        while retry > 0:
            api_key = self.api_keys[count - retry]
            api, entity = self.get_request_entity_v2_0(api_key, msg, user_id, loc)
            self.logger.info("request by tuling api v2, msg: {}, user_id: {}, location: {}".format(msg, user_id, loc))
            response = requests.post(api, json=entity)

            if response.status_code / 100 == 2:
                response_msg = json.loads(response.text.replace("\'", "\""))
                break
            retry -= 1

        if response.status_code / 100 != 2:
            self.logger.error("Request answer failed, {}".format(response_msg))
            return None
        return self.format_msg_v2(response_msg)

    def get_request_entity_v1_0(self, api_key, msg, user_id=None, location=None):
        api_v1 = self.api_info.get("api1")
        if not user_id:
            user_id = "11235813214465"
        if location is None:
            location = "江西省南昌市江西财经大学麦庐园校区"
        data = {
            "key": api_key,
            "userid": user_id,
            "info": msg,
            "loc": location
        }
        return api_v1, data

    def get_request_entity_v2_0(self, api_key, msg, user_id=None, location=None):
        api_v2 = self.api_info.get("api2")
        if not user_id:
            user_id = "11235813214465"

        if location is None:
            location = "南昌"

        entity = {
            "perception": {
                "inputText": {
                    "text": msg
                },
                "selfInfo": {
                    "city": location
                }
            },
            "userInfo": {
                "apiKey": api_key,
                "userId": user_id
            }
        }

        return api_v2, entity

    def format_msg_v1(self, response_msg):
        """
        api v1
        自动解析图灵机器人返回的消息，列出url
        :param response_msg:
        :return:
        """
        self.logger.debug("Response: {}".format(response_msg))
        if int(response_msg['code']) == 308000:
            # 返回至多15条搜索结果
            url_list = response_msg['list']
            if not url_list or type(url_list) != list:
                return response_msg['text']

            result = url_list[:15]
            items = str(response_msg["text"])
            for item in result:
                i_str = "{}\n{}\n{}".format(item["name"], item["info"], item["detailurl"])
                items = "\n\n".join([items, i_str])
            return items

        if int(response_msg['code']) == 302000:

            url_list = response_msg['list']
            if not url_list or type(url_list) != list:
                return response_msg['text']

            result = url_list[:15]
            items = str(response_msg["text"])

            for news in result:
                if not news["article"] or news["article"] == '':
                    continue
                n_str = "{}\n来源:{}\n{}".format(news["article"], news['source'], news["detailurl"])
                items = "\n\n".join([items, n_str])
            return items

        if int(response_msg['code']) == 200000:
            items = response_msg["text"] + "\n" + response_msg["url"]
            return items
        return response_msg['text']

    def format_msg_v2(self, response_msg):
        self.logger.debug("Response: {}".format(response_msg))
        code = response_msg.get("intent", {}).get('code', None)
        if not code:
            return "error, error!!! hot hot hot affsafa asdfkl/ adsfma f."

        results = response_msg.get("results", [])[:15]

        msg = ""
        info = ""
        for result in results:
            result_type = result.get("resultType")
            if result_type == 'text':
                msg = result.get('values', {}).get('text', "None")
                continue
            if result_type == "news":
                news = result.get('values', {}).get("news", [])[:15]
                news = list(filter(lambda n: True if n and n.get('name') and n.get('name') != '' else False, news))
                generator = lambda x: "[{}] {}\n{}".format(x.get('info'), x.get('name'), x.get('detailurl'))
                news_list = map(generator, news)
                info = "\n".join(news_list)
                continue
            if result_type == 'url':
                info = {"url": result.get('values', {}).get('url', "http://atomicer.cn")}
                continue
        if type(info) == str:
            return "\n".join([msg, info])
        else:
            return info


api = TulingAutoReply()

if __name__ == '__main__':
    tuling = TulingAutoReply()
    resp = tuling.request_api1("近期有哪些新闻.")
    print(resp)

    resp = tuling.request_api2("近期有哪些新闻.")
    print(resp)

