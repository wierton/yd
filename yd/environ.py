#!/bin/python


import os
import locale


preferred_encoding = locale.getpreferredencoding()

homedir = ''
if 'HOME' in os.environ:
    homedir = os.environ['HOME']
elif 'USERPROFILE' in os.environ:
    homedir = os.environ['USERPROFILE']
else:
    print("home directory is not found")
    exit(-1)
