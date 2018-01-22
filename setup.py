import os
import sys

from setuptools import setup
from yd.version import __version__

def readme():
    with open('README.md') as f:
        return f.read()

setup(
    name = "yd",
    version = __version__,
    author = "wierton",
    author_email = 'nickouxianfei@gmail.com',
    url = "https://github.com/wierton/dict",
    description = 'A terminal bilingual dictionary',
    long_description = readme(),
    packages=['yd'],
    include_package_data=True,
    #install_requires=['MySQL'],
    entry_points={
        'console_scripts':[
            'yd=yd.yd:main'
            ]
        },
    zip_safe=False,
)
