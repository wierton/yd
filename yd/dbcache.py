import os, sys
import getpass
import commands
import sqlite3 as sql
from urllib import quote, unquote


yd_dir = '{}/.yd'.format(os.environ['HOME'])
dbfile = '{}/dict.db'.format(yd_dir)


def init():
    # record info in .info
    if not os.path.exists(yd_dir):
        os.makedirs(yd_dir)
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

def search(args):
    # query database
    word = args[0]
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
        return True, word, soundmark, definition, examples

def searchall():
    #fetch username and password
    username, password = fetch_loginfo()

    # query database
    try:
        db = sql.connect('localhost', username, password, "yd_cache")
    except:
        print("fail to connect the local database")
        exit(-1)
    cursor = db.cursor()
    cursor.execute('select * from dict;')
    result = cursor.fetchall()
    db.close()
    if result:
        return [(unquote(i), map(unquote, j.split('&')), map(unquote, k.split('&')), map(unquote, l.split('&'))) for i,j,k,l in result]

def save(dic):
    # [word, soundmark, definition, examples]
    word = quote(dic[1])
    soundmark = '&'.join(map(quote, dic[2]))
    definition = '&'.join(map(quote, dic[3]))
    examples = '&'.join(map(quote, dic[4]))

    # connect to the database and execute corresponding operations
    db = sql.connect(dbfile)
    cursor = db.cursor()
    cursor.execute('insert into dict values ("{}", "{}", "{}", "{}")'.format(word, soundmark, definition, examples))
    db.commit()
    db.close()
