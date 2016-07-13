#coding:utf-8

import os
import sys

from setuptools import setup, find_packages

setup(
    name = "yd",
    version = "0.0.1",
    author = "wierton",
    author_email = '2980493052@qq.com',
    url = "",
    description = 'A terminal bilingual dictionary',

    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    include_package_data=True,
    zip_safe=False,
    entry_points={
        'console_scripts':[
            'yd = yd.yd:main'
            ]
        }
)
