#!/bin/python2.7
#coding=utf-8

import re
import sys
import urllib
import urllib2

class dicti:
    def __init__(self):
        self.isen  = True
        self.dicti = 'http://dict.youdao.com/w/eng/'
        self.word  = ''
        self.html  = ''
        self.soundmark  = ''
        self.definition = []
        self.examples   = []

    def get_html(self):
        try:
            request   = urllib2.Request(self.dicti + self.word)
            response  = urllib2.urlopen(request)
            self.html = response.read()
        except urllib2.URLError, e:
            if hasattr(e, 'reason'):
                print e.reason

    def get_soundmark(self):
        pa = re.compile('<span class="phonetic">(.*?)</span>')
        self.soundmark = pa.findall(self.html)

    def get_definition(self):
        pa = re.compile('<div class="trans-container">.*?<ul>(.*?)</ul>.*?</div>', re.S)
        tmp = pa.search(self.html)
        defht = ''
        if tmp:
            defht = tmp.group(1)
        if self.isen:
            pdef = re.compile('<li>(.*?)</li>')
            items = pdef.findall(defht)
            for item in items:
                self.definition.append(item)
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
                self.definition.append(exi)


    def get_examples(self):
        pbi = re.compile('<div id="bilingual".*?>(.*?)</div>', re.S)
        bi = (pbi.search(self.html)).group()
        pp = re.compile('<p>(.*?)</p>', re.S)
        bp = pp.findall(bi)
        ps = re.compile('<span.*?>(.*?)</span>', re.S)
        for item in bp:
            bs = ps.findall(item)
            exi = ''
            for w in bs:
                exi += w
            exi = re.sub('<.?\w>', '', exi)
            self.examples.append(exi)

    def output(self):
        print '\033[0;31m', self.word,
        for mark in self.soundmark:
            print '\033[0;32m', mark,
        print ''
        for item in self.definition:
            print '\033[0;33m', item
        print ''
        count = 0
        pcn = re.compile(r'[\x80-\xff]+', re.S)
        for exi in self.examples:
            count = count + 1
            excn = pcn.search(exi)
            if (count % 2 != 0):
                print '\033[0;34m', 'ex.', exi
            else:
                print '\033[0;35m', '   ', exi
        print '\033[0m'

    def search(self, word):
        try:
            self.word = word
            pcn = re.compile(r'[\x80-\xff]+', re.S)
            if pcn.search(word):
                self.isen = False
            self.get_html()
            self.get_soundmark()
            self.get_definition()
            self.get_examples()
            self.output()
        except:
            print 'word \'%s\' not found!' %(self.word)

def main():
    tmp = dicti()
    if len(sys.argv) > 1:
        tmp.search(sys.argv[1])

if __name__ == '__main__':
    main()
