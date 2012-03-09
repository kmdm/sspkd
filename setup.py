#!/usr/bin/env python
import os
import sys

from distutils.core import setup

sys.path.insert(0, 'src')
from sspkd import __sspkd_version__

setup(
    name='sspkd',
    version=__sspkd_version__,
    description='Secure SSH Public Key Distribution',
    author='Kenny Millington',
    author_email='kenny@kennynet.co.uk',
    url='http://github.com/kmdm/sspkd.git',
    packages=['sspkd'],
    package_dir={'sspkd' : 'src/sspkd'},
    scripts=['src/sspkd-shell', 'src/sspkd-fetch', 'src/sspkd-push',
             'src/sspkd-setup']
)
