#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import urllib.request
from collections import namedtuple

# import BeautifulSoup
from bs4 import BeautifulSoup

class END(Exception):
    pass

def cut_data(cnv_data, erase_data):
    cnv_data = cnv_data.replace(erase_data, '')
    cnv_data = cnv_data[0:cnv_data.find('。')]
    
    # 複数ある場合で①がついているものは①の文言を削除
    m = re.match('① *', cnv_data)
    if m:
        cnv_data = cut_data(cnv_data, m.group(0))

    # 略称のものは文言を削除
    m = re.match('.*」の略', cnv_data)
    if m:
        cnv_data = cnv_data.replace('」の略', '')
        cnv_data = cnv_data[1:len(cnv_data)]
    
    return cnv_data

def lookup(word):
    url = "https://www.weblio.jp/content/" + urllib.parse.quote_plus(word, encoding='utf-8')
    
    html = urllib.request.urlopen(url).read().decode('utf-8')
    soup = BeautifulSoup(html, "html.parser")

    for data in soup.findAll('meta', {'name':'description'}):
        cnv_data = str(data)
        #print(data)

        #print("---------------------------")

        m = re.match('.*（\D+?） スル *', cnv_data)
        if m:
            cnv_data = cut_data(cnv_data, m.group(0))
            return cnv_data
        
        m = re.match('.*〔.*〕 *', cnv_data)
        if m:
            cnv_data = cut_data(cnv_data, m.group(0))
            return cnv_data
            
        m = re.match('.*① *', cnv_data)
        if m:
            cnv_data = cut_data(cnv_data, m.group(0))
            return cnv_data

        start = cnv_data.index(' ', 7) + 1

        # 単語の意味がある場合
        if re.match('.*。.*', cnv_data[start:len(cnv_data)]):
            end = cnv_data.index('。', start)
            return cnv_data[start:end]

        else:
            return word