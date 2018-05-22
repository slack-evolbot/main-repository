#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import urllib
from collections import namedtuple

import BeautifulSoup

DictResult = namedtuple("YahooDictResult", "type lemma defins opts")
DictDefin  = namedtuple("YahooDictDefin" , "index defin opts")

BASE_URL     = 'http://dic.search.yahoo.co.jp/search'
QUERY_STRING = '?stype=exact&ei=UTF-8&p=%s'


def lookup(word, yomi=None, using=None):
    """Yahoo!辞書で言葉を調べる"""
    
    if using is None: using = ('JJ', 'seiji', 'singo')
    
    q = u' '.join((word, yomi)) if yomi else word
    if isinstance(q, unicode):
        q = q.encode('utf-8')
    url = BASE_URL + QUERY_STRING % urllib.quote(q)
    
    html = urllib.urlopen(url).read().decode('utf-8')
    soup = BeautifulSoup.BeautifulSoup(html)
    
    result = [ ]
    for div in soup.findAll('div', {'class':'result-r'}):
        h2 = div.find('h2', {'class': using})
        if not h2: continue
        dict_type = h2['class']
        
        for li in div.findAll('li'):
            parse_result = None
            if dict_type == 'JJ':
                parse_result = _dict_parse_for_YahooDictionary_JJ(li)
            elif dict_type == 'seiji':
                parse_result = _dict_parse_for_YahooDictionary_seiji(li)
            elif dict_type == 'singo':
                parse_result = _dict_parse_for_YahooDictionary_singo(li)
            else:
                pass
            if not parse_result: continue
            result.append(parse_result)
    return result


def pp(results):
    lines = []
    for r in results:
        lines.append( u'辞書の種類: %s' % r.type  )
        lines.append( u'見出し語  : %s' % r.lemma )
        
        if r.opts:
            lines.append( u'その他の情報:' )
            for k, v in r.opts.iteritems():
                if not v: continue
                lines.append( u'  %s: %s' % (k, v) )
                
        for i in r.defins:
            lines.append( u'%s:%s' % (i.index, i.defin) )
            if not i.opts: continue
            
            for k, v in i.opts.iteritems():
                if not v: continue
                if isinstance(v, list): v = ','.join(v)
                lines.append( u'  %s: %s' % (k, v) )
        lines.append( u'' )
    return '\n'.join(lines)




# 長くなるので各辞書用の解析器はこの下に書く

def _dict_parse_for_YahooDictionary_JJ(elem):
    """国語辞典用の解析器"""
    
    # 見出しとふりがなを取得する
    m = re.search(ur'(.+?)【(.+?)】', elem.h3.a.text)
    if m:
        lemma = m.group(2)
        yomi  = m.group(1).replace(u'‐', '')
    else:
        lemma = elem.h3.a.text
        yomi  = None
        
    cands = [ ]
    idx, sub_idx = 0, 0
    for x in elem.div:
        
        if isinstance(x, BeautifulSoup.NavigableString):
            if sub_idx == -1: continue
            
            x = x.strip()
            if not x: continue
            
            if cands and cands[-1].index == (idx, sub_idx):
                new_cands = cands[-1].defin + x
                cands[-1] = DictDefin(cands[-1].index, new_cands, {})
            else:
                cands.append( DictDefin((idx, sub_idx), x, {}) )
            
        elif isinstance(x, BeautifulSoup.Tag):
            if x.name == 'img' and x.has_key('src'):
                src = x['src']
                if src.endswith('.gif'):
                    try:
                        src = src[src.rindex('/')+1:-4]
                        gaiji_idx = int(src)
                    except ValueError:
                        continue
                    
                    sub_idx = -1
                    if gaiji_idx == 1676: sub_idx = 1 # まる１
                    if gaiji_idx == 1678: sub_idx = 2 # まる２
                    if gaiji_idx == 2513: sub_idx = 3 # まる３
                    if gaiji_idx == 2531: sub_idx = 1 # 白四角１
                    if gaiji_idx == 2539: sub_idx = 1 # 黒四角１
                    if gaiji_idx == 2540: pass        # 黒四角２
                    
            elif x.name == 'b':
                i = ord(x.text[0]) -  0xff10
                if 1 <= i < 10:
                    idx = i
                elif cands and cands[-1].index == (idx, sub_idx):
                    new_cands = cands[-1].defin + x.text
                    cands[-1] = DictDefin(cands[-1].index, new_cands, {})
                else:
                    cands.append( DictDefin((idx, sub_idx), x.text, {}) )
    
    
    
    # 各定義に含まれる副次的な情報を抜き出す
    # 品詞情報、用例、対義語、リンクなど
    hinshi = None
    defin  = [ ]
    for x in cands:
        text = x.defin
        
        m = re.match(ur'［\D+?］(\(スル\))?', text)
        if m:
            hinshi = m.group(0)
            text = text.replace(hinshi, '')
            
        hint = re.search(ur'《.+?》', text)
        if hint:
            hint = hint.group(0)
            text = text.replace(hint, '')
        hint = None
        yourei = re.findall(ur'(「(?:[^」]*?)?(?:[^「]*?)」)', text)
        for i in yourei: text = text.replace(i, '')
        
        taigigo = None
        if u'⇔' in text:
            taigigo = text[text.rindex(u'⇔')+1:]
            if taigigo.endswith(u'。'): taigigo = taigigo[:-1]
            text = text[:text.rindex(u'⇔')]
            
        link = None
        if u'⇒' in text:
            link = text[text.rindex(u'⇒')+1:]
            if link.endswith(u'。'): link = link[:-1]
            text = text[:text.rindex(u'⇒')]
        elif u'→' in text:
            link = text[text.rindex(u'→')+1:]
            if link.endswith(u'。'): link = link[:-1]
            text = text[:text.rindex(u'→')]
        
        if text or hint or yourei or taigigo or link:
            defin_opts = dict(hint=hint, yourei=yourei, taigigo=taigigo, link=link)
            defin.append( DictDefin(x.index, text, defin_opts) )
    
    opts = dict(yomi=yomi, hinshi=hinshi)    
    return DictResult('JJ', lemma, defin, opts)



def _dict_parse_for_YahooDictionary_seiji(elem):
    """政治用語集の解析器"""
    lemma = elem.h3.a.text
    defin = [ DictDefin( (0, 0), elem.div.text, {}) ]
    return DictResult('seiji', lemma, defin, {})


def _dict_parse_for_YahooDictionary_singo(elem):
    """新語探検の解析器"""
    lemma = elem.h3.a.text
    defin = [ DictDefin( (0, 0), elem.div.text, {}) ]
    return DictResult('singo', lemma, defin, {})