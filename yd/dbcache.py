import MySQLdb as sql
from urllib import quote, unquote

user       = ""
passwd     = ""
priviledge = 0
select_priv = 1<<4
insert_priv = 1<<3
update_priv = 1<<2
delete_priv = 1<<1
create_priv = 1<<0

def check_priviledge():
    try:
        db = sql.connect('localhost', user, passwd, "")
    except:
        print 'Bad username or password!'
        return
    cursor = db.cursor()
    cursor.execute('select Select_priv, Insert_priv, Update_priv, Delete_priv, Create_priv from mysql.user where user="{}"'.format(user))
    arr = cursor.fetchone()
    if not arr[0] in ('Y', 'y'):
        print 'can\'t access the database'
        priviledge = priviledge & 0xf
    if not arr[1] in ('Y', 'y'):
        print 'can\'t insert item into the database'
        priviledge = priviledge & 0x17
    if not arr[2] in ('Y', 'y'):
        print 'can\'t update old value in the database'
        priviledge = priviledge & 0x1b
    if not arr[3] in ('Y', 'y'):
        print 'can\'t delete error value in database'
        priviledge = priviledge & 0x1d
    if not arr[4] in ('Y', 'y'):
        print 'can\'t create table for caching'
        priviledge = priviledge & 0x1e
    db.close()

def init(username="", password=""):
    print 'To cache the search history, we need access permission for your local database'
    if username == '' or password == '':
        sys.stdout.write('user:')
        user = raw_input()
        sys.stdout.write('password:')
        passwd = raw_input()
    else:
        user = username
        passwd = password

    #check if has access permission to database
    check_priviledge()

    if priviledge & create_priv:
        db = sql.connect('localhost', user, passwd, '')
        cursor = db.cursor()
        cursor.execute('create database yd_cache')
        cursor.execute('use yd_cache')
        cursor.execute('create table dict (\
                word varchar(255) not null default \'\',\
                soundmark varchar(255) not null,\
                definition varchar(255) not null,\
                examples varchar(1023) not null,\
                primary key(word))')
        db.commit()
    else:
        print 'fail to create database "yd_cache"'

def search(args):
    word = args[0]
    qword = quote(word)
    db = sql.connect('localhost', user, passwd, 'yd_cache')
    cursor = db.cursor()
    cursor.execute('select * from dict where word="{}"'.format(qword))
    result = cursor.fetchone()
    db.close()
    if result:
        soundmark = map(unquote, result[1].split('&'))
        definition = map(unquote, result[2].split('&'))
        examples = map(unquote, result[3].split('&'))
        return word, soundmark, definition, examples

def save(dic):
#   [word, soundmark, definition, examples]
    word = quote(dic[0])
    soundmark = '&'.join(map(quote, dic[1]))
    definition = '&'.join(map(quote, dic[2]))
    examples = '&'.join(map(quote, dic[3]))

    db = sql.connect('localhost', user, passwd, "yd_cache")
    cursor = db.cursor()
    cursor.execute('insert into cache values ("{}", "{}", "{}", "{}")'.format(dic.words soundmark, definition, examples))
    db.commit()
    db.close()
