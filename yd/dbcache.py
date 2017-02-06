import os, sys
import getpass
import commands
import _MySQLdb as sql
from urllib import quote, unquote
from Crypto.PublicKey import RSA 

select_priv = 1<<4
insert_priv = 1<<3
update_priv = 1<<2
delete_priv = 1<<1
create_priv = 1<<0

yd_dir = '{}/.yd'.format(os.environ['HOME'])
info_file = yd_dir + '/.info'

global_username = ''
global_password = ''
key = RSA.importKey('''-----BEGIN RSA PRIVATE KEY-----
MIIEowIBAAKCAQEAqEsPBgxV7vxFL9lVy4RuOIr+SJcXXzbnnLo1YUnlMePeob5y
ApOeNM6Cmh8hOi+ZoTMQH4qQ5s+5TEh2L20ZxRCyD3aQHuriNVFZIovlQrmsQWHI
+GaLb1YJqIb91q8uKdvzCBTeg/l09peIXnvwdxC8i3DbKE2HKUHO2/DSIbdb78NQ
z6ETzWPuT5eRUaKL1BzZwkl+5LsMJrdWip5gjQ+YOe5cAQGtlKBS918TcWgJkXUW
NzJ/xF6Uc7gRuFIJ4nP/AzQiqs9sPx+8LeF46+uq2EvNOvItlH2Ns3mt5vFHgRYZ
6rUZbd/M6jFYCxN1uaEUNoAEXeo/ggUL9Z8tDwIDAQABAoIBAFBt9tMkKBmcNRCm
JMusEeUyAE7+7quRmOWdVI+XelL6nVbdpq02kYCZRW+U+xNM1nZk6gq49YFpuxwK
8Xi/AnbdAMxFFKHCDbP/mcLZ6wqVpA5nRl343CCslNcXFM96T2yv8pllJ+cY3F5R
k1ncj9LHi+R0XjkHvFXqXotcr4Bu07BI8CfqP8x+BTJT7aB0CfPpp3gqOMTo6wy/
aI+uuNMV3E23kdfier6c5A/f/M/M0J4r2ygzp5ii8PBxBdJ32ry61U87sHYTWc4x
Oa7XM9PifbjcU1WIjpA1rxGSsnX4Aw8H2nPzsMXHrmZVVE5LpaHZAfRAAn0+pRpZ
tunl9ZECgYEAy3rvu6Nq4Bl2s3dcG35KOeu5+oOWqxbpIyfhGLcoflZepqReb8s3
0kRLvzXi6u2koKp44LbZfbC+MvfLv1V/dYAQHHw9IgKyecr5vU+PMcE9bZDG4/P6
VP+ciI4OtwsVfEJwLvtU/LWo6ED2wjcT/crcHtB7QXQ74SwrJbczuNkCgYEA07se
/LcEjPu7U1AkxWxpW7VF1j9YxeZgIM5uGe+M3Pnd+eI64bpiJ74mzOodXYmYEiId
t6V7KqF/GiB8voIhJBW156jaFmRKnwXnqoBzU20YZisM/TSHn8Dsb6TTwWx1gurt
qxX4HZ98cIAJd0VOe0vNYxNegf07GpxAGyELpCcCgYAr57nkte0wr63iKYYRVJ21
g7ycZlpTTl09vbQfPh4ZrI89y8eovaOs1hm2B22QHXjhRgdRDYM+UK2pl7g577vR
4bEYRGJ4fTZ/eyGKDKmsJbMYeh3AP/uq7YCcInLgYh7fsgI80PRUlun8O1BDNdk1
cNkwOPHvfKITAxHIUJBzeQKBgGdZsXh+BZSj0/6I4koT7yG6zEoWRcjj+QxKd2fl
jIbY2Md+7Gr+xabMpLfll0vvO/GuAX+BISvgBODF9t4vOuoYRuC7hSjk75/MDBcn
+CNC32QPo5l9KK6MR1z/wfVqcbnj3vtiD+i1ztJDTVuQ0wxQJgM0ky80YsNMfeZA
LSSFAoGBALfuvDs5Bck0fqwdKR0qaIQ9OKl6FoUGfpkXuxdTCsjXl0sAC1ei5e+y
5Fhuq1Fh6tDwYjtewPUMnMu6AbhAckqGuvv3bI42ZqfxlJwYV6GT45dU8g9l5y/l
a7RQfd6zRRyrsUzjHj7V9n0S7+yuQskOymtlc7HsRC1CO2rT/AuH
-----END RSA PRIVATE KEY-----
''')

def fetch_loginfo():
    # fetch username and password

    # if has decrypted
    global global_username, global_password
    if global_username != '' and global_password != '':
        return global_username, global_password

    # read and decrypt for login info
    with open(info_file) as fp:
        text = fp.read().split('&')
        encrypt_username = unquote(text[1])
        encrypt_password = unquote(text[2])
    global_username = key.decrypt(encrypt_username)
    global_password = key.decrypt(encrypt_password)
    return global_username, global_password

def check_privilege(username, password, privilege=31):
    try:
        db = sql.connect('localhost', username, password, "")
    except:
        print 'Bad username or password!'
        return False
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

    # if ret value is False, return False
    if not privilege:
        return False

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

    encrypt_username = quote(key.encrypt(username, 20)[0])
    encrypt_password = quote(key.encrypt(password, 20)[0])

    # record info in .info
    if not os.path.exists(yd_dir):
        os.makedirs(yd_dir)
    commands.getoutput('echo "db&{}&{}&" > {}'.format(encrypt_username, encrypt_password, info_file))
    return True

def search(args):
    #fetch username and password
    username, password = fetch_loginfo()

    # query database
    word = args[0]
    qword = quote(word)
    try:
        db = sql.connect('localhost', username, password, "yd_cache")
    except:
        print("fail to connect the local database")
        exit(-1)
    cursor = db.cursor()
    cursor.execute('select * from dict where word="{}"'.format(qword))
    result = cursor.fetchone()
    db.close()
    if result:
        soundmark = map(unquote, result[1].split('&'))
        definition = map(unquote, result[2].split('&'))
        examples = map(unquote, result[3].split('&'))
        return word, soundmark, definition, examples

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
    #fetch username and password
    username, password = fetch_loginfo()

    # [word, soundmark, definition, examples]
    word = quote(dic[0])
    soundmark = '&'.join(map(quote, dic[1]))
    definition = '&'.join(map(quote, dic[2]))
    examples = '&'.join(map(quote, dic[3]))

    # connect to the database and execute corresponding operations
    db = sql.connect('localhost', username, password, "yd_cache")
    cursor = db.cursor()
    cursor.execute('insert into dict values ("{}", "{}", "{}", "{}")'.format(word, soundmark, definition, examples))
    db.commit()
    db.close()
