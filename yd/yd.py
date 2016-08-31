#!/bin/python
#coding=utf-8

import ydsearch
import sys, getopt
import diskcache, dbcache
from getpass import getuser

def fetch_initdata():
    try:
        with open('/home/{}/.yd/.info'.format(getuser())) as fp:
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
    help += "output version information and exit\n"
    help += "--reset                 "
    help += "reset to initial state\n"

    whcache  = ''
    skipinit = False
    username = password = ""
    opts, args = getopt.getopt(sys.argv[1:], "s:u:p:hv", ['save-to=', 'user=', 'password=', 'help', 'version', 'skip-init', 'reset'])
    for opt,value in opts:
        if opt in ('-h', '--help'):
            print help
            exit(0)
        elif opt in ('-v', '--version'):
            print 'yd version 0.0.2'
            exit(0)
        elif opt in ('-s', '--save-to'):
            whcache = value
        elif opt in ('-u', '--user='):
            username = value
        elif opt in ('-p', '--password='):
            password = value
        elif opt == '--skip-init':
            skipinit = True
        elif opt == '--reset':
            import commands
            commands.getoutput('rm -rf /home/{}/.yd'.format(getuser()))
            exit(0)

    #if has inited
    handler = fetch_initdata()
    if handler and not whcache:
        return handler, args
    elif skipinit:
        return None, args

    #haven't init the cache directory
    if whcache != 'disk' and dbcache.init(username, password):
        pass
    else:
        diskcache.init()
    return None, args

def output(dic):
    if not dic:
        return None
    print '\033[0;31m', dic[0],
    for mark in dic[1]:
        print '\033[0;32m', mark,
    print ''
    for item in dic[2]:
        print '\033[0;33m', item
    print ''
    count = 0
    for exi in dic[3]:
        count = count + 1
        if (count % 2 != 0):
            print '\033[0;34m', 'ex.', exi
        else:
            print '\033[0;35m', '   ', exi
    print '\033[0m'
    return True

if __name__ == "__main__":
#   search here means fetch data and output relative info
    handler, args = parse_args()
    if args:
        if not handler or not output(handler.search(args)):
            dictinfo = ydsearch.search(args)
            output(dictinfo)
            if handler:
                handler.save(dictinfo)
