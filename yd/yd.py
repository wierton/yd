#!/bin/python
#coding=utf-8

import os, sys, getopt

import ydsearch
import dbcache

__version__ = '1.2.3'


def parse_args():
    help  = "yd [options|word]\n"
    help += "\n"
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

    opts, args = getopt.getopt(sys.argv[1:], "o:hv", ['output=', 'help', 'version', 'skip-init', 'reset'])
    for opt,value in opts:
        if opt in ('-h', '--help'):
            print(help)
            exit(0)
        elif opt in ('-v', '--version'):
            print('yd version {}'.format(__version__))
            exit(0)
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
    if skipinit:
        return args
    elif not whcache:
        return args

    return args

def test_output(dic, color=('\033[0;31m', '\033[0;32m', '\033[0;33m', '\033[0;34m', '\033[0;35m'), stdout=True):
    output_string = ''
    if not dic:
        return None
    if dic[0] == False:
        print "word '{}' not found!".format(dic[1])
        return None
    print dic[1]
    for mark in dic[2]:
        if not mark:continue
        print mark
    for item in dic[3]:
        if not item:continue
        print item

    count = 0
    for exi in dic[4]:
        count = count + 1
        if not exi:continue
        if (count % 2 != 0):
            print exi
        else:
            print exi

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
    dbcache.init()

    args = parse_args()

    if not args:
        return

    if not output(dbcache.search(args)):
        dictinfo = ydsearch.search(args)
        if output(dictinfo):
            dbcache.save(dictinfo)

if __name__ == "__main__":
    main()
