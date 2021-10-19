#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
@author: aaron
@contact: hi121073215@gmail.com
@date: 2021-10-18
@version: 0.0.0
@license:
@copyright:
"""
import json
import requests
import time

from elastalert.alerts import Alerter, DateTimeEncoder
from elastalert.util import elastalert_logger, EAException
from requests.exceptions import RequestException


class FeishuAlert(Alerter):

    required_options = frozenset(
        ['feishualert_botid', "feishualert_title", "feishualert_body"])

    def __init__(self, rule):
        super(FeishuAlert, self).__init__(rule)
        self.url = self.rule.get(
            "feishualert_url", "https://open.feishu.cn/open-apis/bot/v2/hook/")
        self.bot_id = self.rule.get("feishualert_botid", "")
        self.title = self.rule.get("feishualert_title", "")
        self.body = self.rule.get("feishualert_body", "")
        self.rule["feishualert_time"] = time.strftime(
            "%Y-%m-%d %H:%M:%S", time.localtime())
        if self.bot_id == "" or self.title == "" or self.body == "":
            raise EAException("Configure botid|title|body is invalid")

    def get_info(self):
        return {
            "type": "FeishuAlert"
        }

    def get_rule(self):
        return self.rule

    def alert(self, matches):
        headers = {
            "Content-Type": "application/json;",
        }
        body = {
            "msg_type": "text",
            "content": {
                "title": self.title,
                "text": self.body
            }
        }

        if len(matches) > 0:
            try:
                merge = dict(**matches[0], **self.rule)
                body["content"]["text"] = self.body.format(**merge)
            except Exception as e:
                pass

        try:
            url = self.url + self.bot_id
            res = requests.post(data=json.dumps(
                body), url=url, headers=headers)
            res.raise_for_status()

        except RequestException as e:
            raise EAException("Error request to feishu: {0}".format(str(e)))
