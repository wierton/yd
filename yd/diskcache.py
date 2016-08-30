#!/bin/python
#coding=utf-8

from getpass import getuser

yd_dir = '/home/{}/.yd'.format(getuser())
cache_file = yd_dir + '/.cache'
info_file = yd_dir + './.info'

def init():
    import os, commands
    if not os.path.exists(yd_dir):
        os.makedirs(yd_dir)
    status, output = commands.getstatusoutput('echo >{}'.format(cache_file))
    if status != 0:
        print 'something error!'
        exit(-1)

    commands.getoutput('echo "isfile&" >{}'.format(info_file))
