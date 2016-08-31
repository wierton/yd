import sys
import getpass
import commands
import MySQLdb as sql
from urllib import quote, unquote

select_priv = 1<<4
insert_priv = 1<<3
update_priv = 1<<2
delete_priv = 1<<1
create_priv = 1<<0

yd_dir = '/home/{}/.yd'.format(getpass.getuser())
info_file = yd_dir + '/.info'

def check_privilege(username, password, privilege=31):
    try:
        db = sql.connect('localhost', username, password, "")
    except:
        print 'Bad username or password!'
        exit(-1)
    cursor = db.cursor()
    cursor.execute('select Select_priv, Insert_priv, Update_priv, Delete_priv, Create_priv from mysql.user where user="{}"'.format(username))
    arr = cursor.fetchone()
    db.close()

    if not arr[0] in ('Y', 'y'):
        print 'can\'t access the database'
        privilege = privilege & 0xf
    elif not arr[1] in ('Y', 'y'):
        print 'can\'t insert item into the database'
        privilege = privilege & 0x17
    elif not arr[2] in ('Y', 'y'):
        print 'can\'t update old value in the database'
        privilege = privilege & 0x1b
    elif not arr[3] in ('Y', 'y'):
        print 'can\'t delete error value in database'
        privilege = privilege & 0x1d
    elif not arr[4] in ('Y', 'y'):
        print 'can\'t create table for caching'
        privilege = privilege & 0x1e
    return privilege

def init(username="", password=""):
    # query username and password to connect local database
    if username == '' or password == '':
        print 'To cache the search history, we need access permission for your local database'
        sys.stdout.write('Username: ')
        username = raw_input()
        password = getpass.getpass()

    #check if has access permission to database
    privilege = check_privilege(username, password)

    #base on the create privilege
    if privilege & create_priv:
        db = sql.connect('localhost', username, password, '')
        cursor = db.cursor()
        cursor.execute('drop database if exists yd_cache')
        cursor.execute('create database yd_cache')
        cursor.execute('use yd_cache')
        cursor.execute('create table dict (\
                word varchar(255) not null default \'\',\
                soundmark varchar(1023) not null,\
                definition varchar(1023) not null,\
                examples varchar(4095) not null,\
                primary key(word))')
        db.commit()
        db.close()
    else:
        print 'fail to create database "yd_cache"'
        return False

    # record info in .info
    commands.getoutput('echo "db&{}&{}" > {}'.format(username, password, info_file))
    return True

def search(args):
    # fetch username and password
    with open(info_file) as fp:
        text = fp.read().split('&')
        username = text[1]
        password = text[2]
        print username, password

    # query database
    word = args[0]
    qword = quote(word)
    db = sql.connect('localhost', username, password, '')
    cursor = db.cursor()
    cursor.execute('use yd_cache')
    cursor.execute('select * from dict where word="{}"'.format(qword))
    result = cursor.fetchone()
    db.close()
    if result:
        soundmark = map(unquote, result[1].split('&'))
        definition = map(unquote, result[2].split('&'))
        examples = map(unquote, result[3].split('&'))
        return word, soundmark, definition, examples

def save(dic):
    # [word, soundmark, definition, examples]
    print '***'
    word = quote(dic[0])
    soundmark = '&'.join(map(quote, dic[1]))
    definition = '&'.join(map(quote, dic[2]))
    examples = '&'.join(map(quote, dic[3]))

    db = sql.connect('localhost', user, passwd, "yd_cache")
    cursor = db.cursor()
    cursor.execute('insert into cache values ("{}", "{}", "{}", "{}")'.format(word, soundmark, definition, examples))
    db.commit()
    db.close()
