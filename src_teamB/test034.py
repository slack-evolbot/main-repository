# coding: utf-8
import re
import sys
import MeCab

text = "AIに脅かされないために、AIを作る側の人間になる"
#mc = MeCab.Tagger("-Ochasen")
mc = MeCab.Tagger()

word_list = mc.parse(text).split('\n')

for word in word_list:
    #print(word)
    word_data = re.split('\t|,', word)
    if len(word_data) != 1:
        if word_data[1] == '名詞':
            if word_data[2] == '一般':
                if word_data[7] == '*':
                    print(word_data[0])
                else:
                    print(word_data[7]) 
            
        elif word_data[1] == '動詞':
            if word_data[2] == '自立':
                if word_data[7] == '*':
                    print(word_data[0])
                else:
                    print(word_data[7]) 

#        elif word_data[1] == '助詞' or word_data[1] == '助動詞':
        elif word_data[1] == '助動詞':
            if word_data[7] == '*':
                print(word_data[0])
            else:
                print(word_data[7]) 

    #if 'EOS'
    #print(word)

