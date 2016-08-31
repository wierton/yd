#!/bin/python2.7
#coding=utf-8

import re
import sys
import urllib
import urllib2

isen = True
url  = 'http://dict.youdao.com/w/eng/'
word = ''
html = ''
soundmark  = []
definition = []
examples   = []

def get_html():
    global html, url, word
    try:
        request   = urllib2.Request(url + word)
        response  = urllib2.urlopen(request)
        html = response.read()
    except urllib2.URLError, e:
        if hasattr(e, 'reason'):
            print e.reason

def get_soundmark():
    global soundmark
    pa = re.compile('<span class="phonetic">(.*?)</span>')
    soundmark = pa.findall(html)

def get_definition():
    pa = re.compile('<div class="trans-container">.*?<ul>(.*?)</ul>.*?</div>', re.S)
    tmp = pa.search(html)
    defht = ''
    if tmp:
        defht = tmp.group(1)
    if isen:
        pdef = re.compile('<li>(.*?)</li>')
        items = pdef.findall(defht)
        for item in items:
            definition.append(item)
    else:
        pp = re.compile('<p.*?>(.*?)</p>', re.S)
        bp = pp.findall(defht)
        ps = re.compile('<(span|a).*?>([^<^>]*?)</(span|a)>', re.S)
        for item in bp:
            bs = ps.findall(item)
            exi = ''
            for w in bs:
                if ('.' in w[1] and len(w[1]) <= 4):
                    exi += (w[1] + ' ' * (4-len(w[1])))
                else:
                    exi += w[1]
            definition.append(exi)


def get_examples():
    pbi = re.compile('<div id="bilingual".*?>(.*?)</div>', re.S)
    bi = (pbi.search(html)).group()
    pp = re.compile('<p>(.*?)</p>', re.S)
    bp = pp.findall(bi)
    ps = re.compile('<span.*?>(.*?)</span>', re.S)
    for item in bp:
        bs = ps.findall(item)
        exi = ''
        for w in bs:
            exi += w
        exi = re.sub('<.?\w>', '', exi)
        examples.append(exi)

def search(args):
    try:
        global word
        word = args[0]
        pcn = re.compile(r'[\x80-\xff]+', re.S)
        if pcn.search(word):
            isen = False
        get_html()
        get_soundmark()
        get_definition()
        get_examples()
        return word, soundmark, definition, examples
    except:
        return None, word, None, None
