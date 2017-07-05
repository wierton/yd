#!/bin/python
#coding=utf-8

import os, sys, getopt

import ydsearch
import dbcache

__version__ = '1.3.1'

def write_to_file(filename, content):
    with open(filename, 'wb+') as fp:
        fp.write(content)

def parse_args():
    help  = "yd [options|word]\n"
    help += "\n"
    help += "-h, --help              "
    help += "display the help and exit\n"
    help += "-v, --version           "
    help += "print version information and exit\n"
    help += "--reset                 "
    help += "reset to initial state\n"

    skipinit = False

    opts, args = getopt.getopt(sys.argv[1:], "o:hv", ['output=', 'help', 'version', 'skip-init', 'reset'])
    for opt,value in opts:
        if opt in ('-h', '--help'):
            print(help)
            exit(0)
        elif opt in ('-v', '--version'):
            print('yd version {}'.format(__version__))
            exit(0)
        elif opt in ('-o', '--output='):
            output_string='\n\n'.join([
                sformat(d, color=('',)*6) 
                for d in dbcache.searchall()
            ])
            write_to_file(value, output_string)
            exit(0)
        elif opt == '--reset':
            import commands
            commands.getoutput('rm -rf {}/.yd'.format(os.environ['HOME']))
            exit(0)

    return args


def adjust_encode(dic):
    import locale

    dic = list(dic)

    termial_encoding = locale.getpreferredencoding()

    # word: byte string -> unicode -> target encoding
    dic[1] = dic[1].decode('utf-8').encode(termial_encoding)

    # soundmark
    dic[2] = [s.decode('utf-8').encode(termial_encoding) for s in dic[2]]

    # soundmark
    dic[3] = [s.decode('utf-8').encode(termial_encoding) for s in dic[3]]

    # soundmark
    dic[4] = [s.decode('utf-8').encode(termial_encoding) for s in dic[4]]

    return dic



def sformat(dic, color=('\033[0m', '\033[0;31m', '\033[0;32m', '\033[0;33m', '\033[0;34m', '\033[0;35m')):

    dic = adjust_encode(dic)

    output = ''
    if not dic:
        return None

    # word
    if dic[0] == False:
        return None
    output+='{}{} '.format(color[1], dic[1], color[0])

    # soundmark
    for mark in dic[2]:
        if not mark:continue
        output+='{} {}{}'.format(color[2], mark, color[0])
    output+='\n'

    # definition
    for item in dic[3]:
        if not item or len(item) == 0:
            continue
        output+='{} {}{}\n'.format(color[3], item, color[0])
    if dic[3]:output+='\n'

    # examples
    count = 0
    for exi in dic[4]:
        count = count + 1
        if not exi or len(exi) == 0:continue
        if (count % 2 != 0):
            output+='{} ex.{}{}\n'.format(color[4], exi, color[0])
        else:
            output+='{}    {}{}\n'.format(color[5], exi, color[0])

    return output

def main():
    dbcache.init()

    args = parse_args()

    if not args:
        return

    output = sformat(dbcache.search(args))
    if not output:
        dictinfo = ydsearch.search(args)
        output = sformat(dictinfo)
        if output:
            dbcache.save(dictinfo)
    print output

if __name__ == "__main__":
    main()
