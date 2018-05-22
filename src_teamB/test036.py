# coding: utf-8
import re
import sys
import MeCab
import test035
import MySQLdb

def get_name(message):
    mc = MeCab.Tagger()

    word_list = mc.parse(message).split('\n')

    for word in word_list:
        word_data = re.split('\t|,', word)
        if len(word_data) != 1:
            if word_data[2] == '固有名詞':
                return word_data[0]

you_name = get_name(input('あなたは誰ですか？ > '))
print(you_name + 'さんこんにちは')

while True:

    me = 'evolbot'
    me_flg = False

    # 名詞
    noun = []
    # 動詞
    verb = ''
    # 助詞
    particle = ''
    # 形容詞
    adjective = ''
    # 助動詞
    au_verb = ''
    # 形容動詞
    ad_verb = ''
    # 記号
    symbol = ''

    input_message = input('何か話かけてください > ')

    #text = "あの犬は可愛いですよね？"
    text = input_message
    mc = MeCab.Tagger()

    word_list = mc.parse(text).split('\n')

    for word in word_list:
        #print(word)
        word_data = re.split('\t|,', word)
        if len(word_data) != 1:
            #print(word_data)
            if word_data[1] == '名詞':
                if word_data[0] == me or word_data[0] == 'あなた':
                    me_flg = True
                else:
                    if word_data[2] == '一般':     
                        if word_data[7] == '*':
                            noun.append(word_data[0])
                        else:
                            noun.append(word_data[7])
                    elif word_data[2] == '形容動詞語幹' and ad_verb == '':
                        if word_data[7] == '*':
                            ad_verb = word_data[0]
                        else:
                            ad_verb = word_data[7]
                
            elif word_data[1] == '動詞' and verb == '':
                if word_data[7] == '*':
                    verb = word_data[0]
                else:
                    verb = word_data[7]

            elif word_data[1] == '形容詞' and adjective == '':
                if word_data[7] == '*':
                    adjective = word_data[0]
                else:
                    adjective = word_data[7] 

            elif word_data[1] == '助動詞' and au_verb == '':
                if word_data[7] == '*':
                    au_verb = word_data[0]
                else:
                    au_verb = word_data[7]

            elif word_data[1] == '助詞' and particle == '':
                if word_data[7] == '*':
                    particle = word_data[0]
                else:
                    particle = word_data[7]

            elif word_data[1] == '記号':
                if word_data[7] == '*':
                    symbol = word_data[0]
                else:
                    symbol = word_data[7]

    if symbol == '？':
        if me_flg == True:
            print('私は' + noun[0] + particle + ad_verb + au_verb)
        elif len(noun) >= 2:
            print(noun[0] + 'は' + noun[1] + particle + ad_verb + au_verb)
        elif adjective != '':
            print(noun[0] + 'は' + adjective + ad_verb + au_verb)
        else:
            print(noun[0] + particle + ad_verb + au_verb)

    else:
        list_value = test035.main(text)

        connection = MySQLdb.connect(host='localhost', user='pi', passwd='pass', db='raspberry', charset='utf8')
        
        try:
            with connection.cursor() as cursor:
                sql = "SELECT WORD, TYPE FROM ARTIFICIAL_INTELLIGENCE_TABLE WHERE WORD IN ('" + "','".join(list_value) + "')"
                
                cursor.execute(sql)
                result = cursor.fetchall()

                if result[0][1] == 'あいさつ':
                    print(list_value[0])

        except:
            print('例外が発生しました')


