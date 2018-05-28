import MeCab
import re
import webliodict
from googletrans import Translator

translator = Translator()

text = "近代の日本人は暴飲暴食に気をつけなければならない"
print(text)
mc = MeCab.Tagger()

word_list = mc.parse(text).split('\n')

remake_words = ''
for word in word_list:
    #print(word)
    word_data = re.split('\t|,', word)
    if len(word_data) != 1 and word_data[7] != 'する' and word_data[7] != 'こと':
        if word_data[1] == '名詞' and word_data[2] != '固有名詞' and word_data[3] != '一般':
            if word_data[7] == '気':
                remake_words += word_data[0]
            else:
                remake_words += webliodict.lookup(word=word_data[7])
        else:
            remake_words += word_data[0]

print(remake_words)
en_remake_words = translator.translate(remake_words, src='ja', dest='en').text
print(en_remake_words)
jp_remake_words = translator.translate(en_remake_words, src='en', dest='ja').text
print(jp_remake_words)
