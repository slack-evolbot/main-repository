# -*- coding: utf-8 -*-
# Wordnet via Python3
#
# ref:
#   WordList_JP: http://compling.hss.ntu.edu.sg/wnja/
#   python3: http://sucrose.hatenablog.com/entry/20120305/p1
import sys, sqlite3
from collections import namedtuple
from pprint import pprint

conn = sqlite3.connect("/home/pi/wnjpn.db")

Word = namedtuple('Word', 'wordid lang lemma pron pos')
Sense = namedtuple('Sense', 'synset wordid lang rank lexid freq src')
Synset = namedtuple('Synset', 'synset pos name src')

def getWords(lemma):
    cur = conn.execute("select * from word where lemma=?", (lemma,))
    return [Word(*row) for row in cur]

def getSenses(word):
    cur = conn.execute("select * from sense where wordid=?", (word.wordid,))
    return [Sense(*row) for row in cur]

def getSynset(synset):
    cur = conn.execute("select * from synset where synset=?", (synset,))
    return Synset(*cur.fetchone())

def getWordsFromSynset(synset, lang):
    cur = conn.execute("select word.* from sense, word where synset=? and word.lang=? and sense.wordid = word.wordid;", (synset,lang))
    return [Word(*row) for row in cur]

def getWordsFromSenses(sense, lang="jpn"):
    synonym = {}
    for s in sense:
        lemmas = []
        syns = getWordsFromSynset(s.synset, lang)
        for sy in syns:
            lemmas.append(sy.lemma)
            synonym[getSynset(s.synset).name] = lemmas
    return synonym

def getSynonym (word):
    synonym = {}
    words = getWords(word)
    if words:
        for w in words:
            sense = getSenses(w)
            s = getWordsFromSenses(sense)
            synonym = dict(list(synonym.items()) + list(s.items()))
    return synonym

#if __name__ == '__main__':
#    if len(sys.argv) >= 2:
#        synonym = getSynonym(sys.argv[1])
#       pprint(synonym)
#        for word in synonym['delicious']:
#            print(word)
# 
#    else:
#        print("You need at least 1 argument as a word like below.\nExample:\n  $ python3 wordnet_jp 楽しい")

def main(search_word):
    word_data = []
    
    word_list = getSynonym(search_word)

    if len(word_list) == 0:
        word_data.append(search_word)
        return word_data
    else:
        for words in word_list:
            for word in word_list[words]:
                word_data.append(word)

        word_data = list(set(word_data))
        return word_data
    
result = main('放火')
print(result)
