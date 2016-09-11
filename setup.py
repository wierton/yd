#coding:utf-8

import os
import sys

from setuptools import setup, find_packages

def readme():
    with open('README.md') as f:
        return f.read()

setup(
    name = "yd",
    version = "0.0.3",
    author = "wierton",
    author_email = 'nickouxianfei@gmail.com',
    url = "https://github.com/wierton/dict",
    description = 'A terminal bilingual dictionary',
    long_description = readme(),
    packages=['yd'],
    include_package_data=True,
    entry_points={
        'console_scripts':[
            'yd=yd.yd:main'
            ]
        },
    zip_safe=False,
)
