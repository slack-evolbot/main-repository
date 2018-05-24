import re
import MySQLdb
import test035
import MeCab

input_message = "あの男の子は見た目は肉食系、中身は草食系の男子だよね"

mc = MeCab.Tagger()

word_list = mc.parse(input_message).split('\n')

conv_message = ''
for word in word_list:
    word_data = re.split('\t|,', word)
    if len(word_data) != 1:
        # 名詞、動詞、形容詞を日本語の基本形に変換する
        if word_data[1] == '名詞' or word_data[1] == '動詞' or word_data[1] == '形容詞':
            if word_data[7] == '*':
                conv_message.append(word_data[0])
            else:
                conv_message.append(word_data[7]) 

# DBからギャル語を取得する
connection = MySQLdb.connect(host='localhost', user='pi', passwd='pass', db='raspberry', charset='utf8')

try:
    with connection.cursor() as cursor:
        sql = "SELECT GYARU_WORD, BASIC_WORD FROM GYARU_WORD_TABLE ORDER BY BASIC_WORD"

        cursor.execute(sql)
        result = cursor.fetchall()

        # DBから取得したギャル語に紐づくワードを取得する
        for data in result:
            similar_words = test035.main(data[1])

            for similar_word in similar_words:
                m = re.match('.*' + similar_word + '.*', input_message)
                if m:
                    conv_message = conv_message.replace(data[1], data[0])
                    break

    print(conv_message)

except:
    pass
