"""
REST API CLASS
"""
# -*- coding: utf-8 -*-
import requests
from requests.exceptions import RequestException

class RestApi():
    """
    REST API CLASS
    """
    def __init__(self, url):
        self.url = url
        self.response_data = None

    def api_request(self, search_dict):
        """
        API呼び出し
        """
        try:
            self.response_data = requests.get(self.url, params=search_dict)
        except RequestException:
            raise Exception('APIアクセスに失敗しました')
