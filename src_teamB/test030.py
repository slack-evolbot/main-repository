import sys
import os
from selenium import webdriver
#import pandas
import time

def get_merucari_data(goods_name):
        #Googleにアクセスして、タイトルをとってこれるかテスト
        #browser = webdriver.Chrome(executable_path='/home/pi/chromedriver')
        browser = webdriver.Chrome('/home/pi/chromedriver')

        #args = sys.argv
        #df = pandas.read_csv('default.csv', index_col=0)

        #browser.get("https://www.mercari.com/jp/search/?sort_order=price_desc&keyword={}&category_root=&brand_name=&brand_id=&size_group=&price_min=&price_max=".format(goods_name))
        
        page = 1

        while True: #continue until getting the last page
                if len(browser.find_elements_by_css_selector("li.pager-next .pager-cell:nth-child(1) a")) > 0:
                        print("######################page: {} ########################".format(page))
                        print("Starting to get posts...")

                        posts = browser.find_elements_by_css_selector(".items-box")

                        for post in posts:
                                title = post.find_element_by_css_selector("h3.items-box-name").text
                                price = post.find_element_by_css_selector(".items-box-price").text
                                price = price.replace('\\', '')

                                sold = 0
                                if len(post.find_elements_by_css_selector(".item-sold-out-badge")) > 0:
                                        sold = 1

                                url = post.find_element_by_css_selector("a").get_attribute("href")

                                print(title, price, sold,url)
                                #se = pandas.Series([title, price, sold,url],['title','price','sold','url'])
                                #df = df.append(se, ignore_index=True)

                        page+=1

                        btn = browser.find_element_by_css_selector("li.pager-next .pager-cell:nth-child(1) a").get_attribute("href")
                        print("next url:{}".format(btn))
                        browser.get(btn)
                        print("Moving to next page......")

                else:
                        print("no pager exist anymore")
                        break

        #df.to_csv("{}.csv".format(goods_name))
        print("DONE")

get_merucari_data("ルンバ")
