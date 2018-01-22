import os, sys
import commands
import sqlite3 as sql
from urllib import quote, unquote

import environ

preferred_encoding = environ.preferred_encoding

homedir = environ.homedir

yd_dir = '{}/.yd'.format(homedir)
dbfile = '{}/dict.db'.format(yd_dir).decode(preferred_encoding)


def init():
    if not os.path.exists(yd_dir):
        os.makedirs(yd_dir)

    db = sql.connect(dbfile)
    try:
        db = sql.connect(dbfile)
    except:
        print("fail to connect the local database")
        exit(-1)

    cursor = db.cursor()
    cursor.execute("select name from SQLITE_MASTER where type='table'".format(dbfile))
    result = cursor.fetchall()

    result = [row[0] for row in result]
    
    if u'dict' not in result:
        try:
            cursor.execute('create table dict (\
                    word char(255) not null default \'\',\
                    soundmark char(1023) not null,\
                    definition char(1023) not null,\
                    examples char(4095) not null,\
                    primary key(word))')
        except:
            print("fail to create table `dict` in dict.db")
            exit(-1)

    db.close()
    return True

def search(word):
    # query database
    qword = quote(word)
    try:
        db = sql.connect(dbfile)
    except:
        print("fail to connect the local database")
        exit(-1)
    cursor = db.cursor()
    cursor.execute('select * from dict where word="{}"'.format(qword))
    result = cursor.fetchone()
    db.close()
    if result:
        result = [s.encode('ascii') for s in result]
        soundmark = map(unquote, result[1].split('&'))
        definition = map(unquote, result[2].split('&'))
        examples = map(unquote, result[3].split('&'))
        return {
                'result':True,
                'word':word,
                'soundmark':soundmark,
                'definition':definition,
                'examples':examples
                }
    else:
        return {
                'result':False,
                'word':word,
                'soundmark':[],
                'definition':[],
                'examples':[]
                }

def searchall():
    # query database
    try:
        db = sql.connect(dbfile)
    except:
        print("fail to connect the local database")
        exit(-1)

    cursor = db.cursor()
    cursor.execute('select * from dict')
    result = cursor.fetchall()
    db.close()
    if result:
        result = [[j.encode('ascii') for j in i] for i in result]
        return [
                {
                    'result':True,
                    'word':unquote(i),
                    'soundmark':map(unquote, j.split('&')),
                    'definition':map(unquote, k.split('&')),
                    'examples':map(unquote, l.split('&'))
                }
                for i,j,k,l in result
            ]
    else:
        return []

def save(dic):
    # [word, soundmark, definition, examples]
    word = quote(dic['word'])
    soundmark = '&'.join(map(quote, dic['soundmark']))
    definition = '&'.join(map(quote, dic['definition']))
    examples = '&'.join(map(quote, dic['examples']))

    # connect to the database and execute corresponding operations
    db = sql.connect(dbfile)
    cursor = db.cursor()
    cursor.execute('insert into dict values ("{}", "{}", "{}", "{}")'.format(word, soundmark, definition, examples))
    db.commit()
    db.close()
