#!/bin/python
#coding=utf-8

import os, sys, getopt
from getpass import getuser

import ydsearch
import diskcache, dbcache

__version__ = '1.2.3'

def write_to_file(filename, content):
    with open(filename, 'wb+') as fp:
        fp.write(content)

def fetch_initdata():
    try:
        with open('{}/.yd/.info'.format(os.environ['HOME'])) as fp:
            initinfo = fp.read().split('&')[0]
            if initinfo == 'db':
                return dbcache
            elif initinfo == 'disk':
                return diskcache
    except:
        return None

def parse_args():
    help  = "yd [options] word\n"
    help += "\n"
    help += "-s, --save-to=[db|disk] "
    help += "designate the place for local cache\n"
    help += "-u, --user=[name]       "
    help += "set the user to access local database\n"
    help += "-p, --password=[passwd] "
    help += "set the password corresponding to the user name\n"
    help += "-h, --help              "
    help += "display the help and exit\n"
    help += "-v, --version           "
    help += "print version information and exit\n"
    help += "-o, --output=filename   "
    help += "output cached word to file\n"
    help += "--reset                 "
    help += "reset to initial state\n"

    whcache  = ''
    skipinit = False
    username = password = ""
    opts, args = getopt.getopt(sys.argv[1:], "s:u:p:o:hv", ['save-to=', 'user=', 'password=', 'output=', 'help', 'version', 'skip-init', 'reset'])
    for opt,value in opts:
        if opt in ('-h', '--help'):
            print(help)
            exit(0)
        elif opt in ('-v', '--version'):
            print('yd version {}'.format(__version__))
            exit(0)
        elif opt in ('-s', '--save-to'):
            whcache = value
        elif opt in ('-u', '--user='):
            username = value
        elif opt in ('-p', '--password='):
            password = value
        elif opt in ('-o', '--output='):
            output_string='\n\n'.join([output(d, color=('',)*5, stdout=False) for d in dbcache.searchall()])
            write_to_file(value, output_string)
            exit(0)
        elif opt == '--skip-init':
            skipinit = True
        elif opt == '--reset':
            import commands
            commands.getoutput('rm -rf {}/.yd'.format(os.environ['HOME']))
            exit(0)

    #if has inited
    handler = fetch_initdata()
    if skipinit:
        return None, args
    elif handler and not whcache:
        return handler, args

    #haven't init the cache directory
    if whcache != 'disk' and dbcache.init(username, password):
        pass
    else:
        diskcache.init()
    return None, args

def output(dic, color=('\033[0;31m', '\033[0;32m', '\033[0;33m', '\033[0;34m', '\033[0;35m'), stdout=True):
    output_string = ''
    if not dic:
        return None
    if dic[0] == False:
        output_string+="word '{}' not found!".format(dic[1])
        return None
    output_string+='{}{} \033[0m'.format(color[0], dic[1])
    for mark in dic[2]:
        if not mark:continue
        output_string+='{} {}\033[0m'.format(color[1], mark)
    output_string+='\n'
    for item in dic[3]:
        if not item:continue
        output_string+='{} {}\033[0m\n'.format(color[2], item)
    if dic[3]:output_string+='\n'
    count = 0
    for exi in dic[4]:
        count = count + 1
        if not exi:continue
        if (count % 2 != 0):
            output_string+='{} ex.{}\033[0m\n'.format(color[3], exi)
        else:
            output_string+='{}    {}\033[0m\n'.format(color[4], exi)
    if stdout:
        print(output_string)
        return True
    else:
        return output_string

def main():
    handler, args = parse_args()
    if args:
        if not handler or not output(handler.search(args)):
            dictinfo = ydsearch.search(args)
            if output(dictinfo) and handler:
                handler.save(dictinfo)

if __name__ == "__main__":
    main()
