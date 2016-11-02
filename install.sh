#!/bin/bash

mkdir -p ~/.yd
sudo apt-get install python-mysqldb
sudo python setup.py install --record ~/.yd/.yd_record
