#!/bin/python2.7
#coding=utf-8

import re
import sys
import urllib
import urllib2
import json

isen = True
url  = 'http://dict.youdao.com/w/eng/'

def get_html(word):
    try:
        global url
        request   = urllib2.Request(url + word)
        response  = urllib2.urlopen(request)
        html = response.read()
        return html
    except urllib2.URLError, e:
        if hasattr(e, 'reason'):
            print e.reason

def get_soundmark(html):
    pa = re.compile('<span class="phonetic">(.*?)</span>')
    soundmark = pa.findall(html)
    return soundmark

def get_definition(html):
    pa_container = re.compile('<div class="trans-container">.*?<ul>(.*?)</ul>.*?</div>', re.S)
    ma_container = pa_container.search(html)
    str_container = ''
    definition = []

    if ma_container:
        str_container = ma_container.group(1)
    if isen:
        pdef = re.compile('<li>(.*?)</li>')
        items = pdef.findall(str_container)
        for item in items:
            definition.append(item)
    else:
        pa_wordgroup = re.compile('<p class="wordGroup">(.*?)</p>', re.S)
        ma_wordgroup = pa_wordgroup.findall(str_container)
        pa_span = re.compile('<(span|a).*?>([^<^>]*?)</(span|a)>', re.S)
        for item in ma_wordgroup:
            ma_span = pa_span.findall(item)
            exi = ''
            for w in ma_span:
                if ('.' in w[1] and len(w[1]) <= 4):
                    exi += (w[1] + ' ' * (4-len(w[1])))
                else:
                    exi += w[1]
            definition.append(exi)
    return definition


def get_examples(html):
    examples = []
    pa_bilingual = re.compile('<div id="bilingual".*?>(.*?)</div>', re.S)
    pa_group = pa_bilingual.search(html)
    if pa_group:
        ma_bilingual = pa_group.group()
    else:
        return []
    pa_p = re.compile('<p>(.*?)</p>', re.S)
    ma_p = pa_p.findall(ma_bilingual)
    pa_span = re.compile('<span.*?>(.*?)</span>', re.S)
    for item in ma_p:
        ma_span = pa_span.findall(item)
        exi = ''
        for w in ma_span:
            exi += w
        exi = re.sub('<.?\w>', '', exi)
        examples.append(exi)
    return examples

def get_suggestion(word):
    url = 'http://dsuggest.ydstatic.com/suggest.s?query=' + word + '&keyfrom=dict2.index.suggest&o=form&rn=10&h=4&le=eng'
    request = urllib2.Request(url)
    response = urllib2.urlopen(request)
    html = response.read()
    unquote_html = urllib.unquote(html)
    ma = re.findall(r'<td align=left.*?>(.*?)</td', unquote_html)
    if ma:
        print 'do you mean: ' + ', '.join(ma) + ' ?'

def get_definition_by_ydapi(word):
    if not isen:word = urllib.quote(word)
    url = 'http://fanyi.youdao.com/openapi.do?keyfrom=yddict123&key=185765201&type=data&doctype=json&version=1.1&q={}'.format(word)
    request = urllib2.Request(url)
    response = urllib2.urlopen(request)
    json_stream = response.read()
    ret_info = json.loads(json_stream)
    if 'errorCode' in ret_info and ret_info['errorCode'] == 0:
        return ret_info['translation']


def search(word_list):
    global isen
    word = word_list[0]
    pcn = re.compile(r'[\x80-\xff]+', re.S)
    if pcn.search(word) : isen = False
    html = get_html(word)
    # fail to connect the internet
    if not html or "<h4> 您要找的是不是:</h4>" in html:
        get_suggestion(word)
        return False, word, None, None, None
    else:
        soundmark = get_soundmark(html)
        definition = get_definition(html)
        examples = get_examples(html)
        if not definition:
            definition = get_definition_by_ydapi(word)
        return True, word, soundmark, definition, examples

def test():
    search(sys.argv[1:])

if __name__ == "__main__":
    test()
