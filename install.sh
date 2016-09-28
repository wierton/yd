#!/bin/bash

mkdir -p ~/.yd
apt-get install python-mysqldb
python setup.py install --record ~/.yd/.yd_record
