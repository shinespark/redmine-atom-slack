#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import json


class Slack(object):
    def __init__(self, webhook_url: str, channel: str = 'general',
                 footer: str = 'Redmine Slacker', color: str = '#d11a1f'):
        self.url = webhook_url
        self.channel = channel
        self.footer = footer
        self.color = color
        self.headers = {'Content-type': 'application/json'}

    def post(self, author_name: str, title: str, title_link: str, text: str):
        params = {
            'attachments': [
                {
                    'color': self.color,
                    'author_name': author_name,
                    'title': title,
                    'title_link': title_link,
                    'text': text,
                    'footer': self.footer
                }
            ],
            'channel': self.channel
        }
        json_params = json.dumps(params).encode('utf-8')
        return requests.post(self.url, data=json_params, headers=self.headers)
