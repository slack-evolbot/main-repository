"""
ぐるなびAPI
"""
# -*- coding: utf-8 -*-
from plugins.restapi import RestApi

class GnaviApi(RestApi):
    """
    ぐるなびAPI用クラス
    """
    def __init__(self, url):
        super().__init__(url)

    def url_list(self):
        """
        ResponseからレストランURLのリストを作って返す。
        """
        json_data = self.response_data.json()
        if 'error' in json_data:
            raise Exception('そのキーワードじゃ見つかんなかった・・・(´・ω・｀)')

        return [rest_data['url'] for rest_data in json_data['rest']]

