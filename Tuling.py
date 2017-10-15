# __*__coding=utf8__*__

import requests
import json

keys = ["da3d060333cd472a94523909709c2f80"]
api1 = "http://www.tuling123.com/openapi/api"
api2 = "http://openapi.tuling123.com/openapi/api/v2"


def ask(text, key):
    entity = {
        "perception": {
            "inputText": {
                "text": text
            },
            "selfInfo": {
            }
        },
        "userInfo": {
            "apiKey": key,
            "userId": "13221323442"
        }
    }

    return entity


def request_api_get(text):
    count = keys.__len__()
    retry = count
    while retry > 0:
        params = {
            "key": keys[count - retry],
            "info": text,
        }
        response = requests.get(api1, params=params)
        text = json.loads(response.text.replace("\'", "\""))
        if response.status_code / 100 == 2 and int(text['code'] / 10000) != 4:
            break
        retry -= 1

    if response.status_code / 100 != 2 or int(text['code'] / 10000) == 4:
        print("All keys is invalid")
        return None
    return text


def request_api1(text, loc=None):
    count = keys.__len__()
    retry = count

    if loc is None:
        loc = "江西省南昌市江西财经大学麦庐园校区"
    while retry > 0:
        data = {
            "key": keys[count - retry],
            "userid": "12345678",
            "info": text,
            "loc": loc
        }

        print("Reuqest:", data)
        response = requests.post(api1, json=data)
        text = json.loads(response.text.replace("\'", "\""))
        if response.status_code / 100 == 2 and int(text['code'] / 10000) != 4:
            break
        retry -= 1

    if response.status_code / 100 != 2 or int(text['code'] / 10000) == 4:
        print("All keys is invalid")
        return None
    return text


def request_api2(text):
    count = keys.__len__()
    retry = count
    while retry > 0:
        entity = ask(text, keys[count - retry])
        print("Reuqest:", entity)
        response = requests.post(api2, json=entity)
        text = json.loads(response.text.replace("\'", "\""))
        if response.status_code / 100 == 2:
            break
        retry -= 1

    if response.status_code / 100 != 2:
        print("All keys is invalid")
        return None
    return text


if __name__ == '__main__':
    re = request_api_get("你好,我是xx")
    print(re, '\n')
    re = request_api1("昌平区天气")
    print(re, '\n')
    re = request_api2("你好,我是xx")
    print(re)
