import sys
import os
from selenium import webdriver
#import pandas
import time

def get_merucari_data(goods_name):
    #Googleにアクセスして、タイトルをとってこれるかテスト
    driver = webdriver.Firefox()
    driver.get("https://www.yahoo.co.jp/")
    
get_merucari_data("ルンバ")
