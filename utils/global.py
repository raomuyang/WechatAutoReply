#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import sys
import logging
import logging.config
from os import path

try:
    default_encoding = 'utf-8'
    if sys.getdefaultencoding() != default_encoding:
        reload(sys)
        sys.setdefaultencoding(default_encoding)
except:
    pass

_root_path = path.dirname(path.abspath(__file__))
project_path = _root_path + "/../"
config_path = "/".join([project_path, "config"])
resource_path = "/".join([project_path, "resources"])

# get properties
data = {}
with open('/'.join([config_path, 'config.json']), "rb") as f:
    data = json.load(f)


def init_logging():
    logging.config.fileConfig("/".join([config_path, 'logging.conf']))
    return logging.getLogger("robot-j")

# init logger
logger = init_logging()


def get_robot_name():
    return data.get('name')


def get_robot_api():
    return data.get("tuling", None)


def get_db():
    pass


def hello():
    logger.info("hello, robot-j")


if __name__ == '__main__':
    hello()
