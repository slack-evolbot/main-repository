import MeCab
import re

text = "私は放火すること決めた"
print(text)
mc = MeCab.Tagger()

word_list = mc.parse(text).split('\n')

for word in word_list:
    word_data = re.split('\t|,', word)
    if len(word_data) != 1:
        print(word_data)
