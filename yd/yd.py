#!/bin/python
#coding=utf-8

import environ
import os, sys, getopt

import ydsearch
import dbcache

from version import __version__

preferred_encoding = environ.preferred_encoding

default_colors = {
            'reset'        :'\033[0m',
            'word'         :'\033[31m',
            'soundmark'    :'\033[32m',
            'definition'   :'\033[33m',
            'examples_odd' :'\033[34m',
            'examples_even':'\033[35m',
        }

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

    opts, args = getopt.getopt(sys.argv[1:], "o:hv", ['output=', 'help', 'version', 'reset'])
    for opt,value in opts:
        if opt in ('-h', '--help'):
            print(help)
            exit(0)
        elif opt in ('-v', '--version'):
            print('yd version {}'.format(__version__))
            exit(0)
        elif opt in ('-o', '--output='):
            output_string='\n\n'.join([
                sformat(d, color={
                    'word':'', 'soundmark':'', 'definition':'',
                    'examples_odd':'', 'examples_even':'',
                    'reset':''
                    }) 
                for d in dbcache.searchall()
            ])
            write_to_file(value, output_string)
            exit(0)
        elif opt == '--reset':
            import commands
            commands.getoutput('rm -rf {}/.yd'.format(environ.homedir))
            exit(0)

    return [s.decode(preferred_encoding).encode('utf-8') for s in args]


def adjust_encode(dic):
    ret_dic = {'result':dic['result']}

    # word: byte string -> unicode -> target encoding
    ret_dic['word'] = dic['word'].decode('utf-8').encode(preferred_encoding)

    for key in dic:
        if type(dic[key]) != type([]):
            continue
        ret_dic[key] = [s.decode('utf-8').encode(preferred_encoding, errors='ignore') for s in dic[key]]

    return ret_dic



def sformat(byte_dic, color=default_colors):
    
    if not byte_dic:
        return None

    dic = adjust_encode(byte_dic)

    if not dic['result']:
        return "word '{}' not found".format(dic['word'])

    output = '{}{} '.format(color['word'], dic['word'], color['reset'])

    # soundmark
    for mark in dic['soundmark']:
        if not mark:continue
        output+='{} {}{}'.format(color['soundmark'], mark, color['reset'])
    output+='\n'

    # definition
    for item in dic['definition']:
        if not item or len(item) == 0:
            continue
        output+='{} {}{}\n'.format(color['definition'], item, color['reset'])
    if dic['definition']:output+='\n'

    # examples
    count = 0
    for exi in dic['examples']:
        count = count + 1
        if not exi or len(exi) == 0:continue
        if (count % 2 != 0):
            output+='{} ex.{}{}\n'.format(color['examples_odd'], exi, color['reset'])
        else:
            output+='{}    {}{}\n'.format(color['examples_even'], exi, color['reset'])

    return output

def main():
    dbcache.init()

    args = parse_args()
    if not args: return

    word = ' '.join(args)
    
    dictinfo = dbcache.search(word)
    output = sformat(dictinfo)
    if not dictinfo['result']:
        dictinfo = ydsearch.search(word)
        output = sformat(dictinfo)
        if dictinfo['result']:
            dbcache.save(dictinfo)
    print output

if __name__ == "__main__":
    main()
