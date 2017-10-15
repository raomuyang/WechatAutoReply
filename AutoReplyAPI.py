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
        super().__init__()
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
        return response_msg

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
        return response_msg

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
            location = "江西省南昌市江西财经大学麦庐园校区"

        entity = {
            "perception": {
                "inputText": {
                    "text": msg
                },
                "selfInfo": {
                    "nearest_poi_name": location
                }
            },
            "userInfo": {
                "apiKey": api_key,
                "userId": user_id
            }
        }
        return api_v2, entity


if __name__ == '__main__':
    tuling = TulingAutoReply()
    resp = tuling.request_api1("Hello, api v1.")
    print(resp)

    resp = tuling.request_api2("It' nice weather today.")
    print(resp)
