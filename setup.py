#!/usr/bin/env python
from setuptools import setup, find_packages

setup(name='ironman',
      version='0.1',
      description='SoC Firmware for L1Calo',
      long_description=''.join(open('README.md').readlines()),
      author='Giordon Stark',
      author_email='gstark@cern.ch',
      maintainer='Giordon Stark',
      maintainer_email='gstark@cern.ch',
      license='MIT',
      url='',
      packages=find_packages(),
      classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Topic :: Utilities',
        'Operating System :: POSIX :: Linux',
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License (GPL)'
      ])
