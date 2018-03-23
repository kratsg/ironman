#!/usr/bin/env python
from __future__ import print_function
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
import io, os, sys

import ironman

here = os.path.abspath(os.path.dirname(__file__))

def read(*filenames, **kwargs):
    encoding = kwargs.get('encoding', 'utf-8')
    sep = kwargs.get('sep', '\n')
    buf = []
    for filename in filenames:
        with io.open(filename, encoding=encoding) as f:
            buf.append(f.read())
    return sep.join(buf)

long_description = read(os.path.join(here, 'README.rst'))#, 'CHANGES.txt')

class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = ['--strict', '--verbose', '--tb=long', 'tests']
        self.test_suite = True

    def run_tests(self):
        import pytest
        errno = pytest.main(self.test_args)
        sys.exit(errno)

setup(name='ironman',
      version=ironman.__version__,
      url='https://github.com/kratsg/ironman',
      license='MIT',
      description='SoC Firmware for L1Calo',
      long_description=long_description,
      author='Giordon Stark',
      author_email='gstark@cern.ch',
      maintainer='Giordon Stark',
      maintainer_email='gstark@cern.ch',
      tests_require=['pytest'],
      install_requires=['Twisted>=15.4.0',
                        'zope.interface==4.1.3',
                        'construct==2.9.39',
                        'PyYAML==3.11'],
      cmdclass={'test': PyTest},
      packages=find_packages(),
      test_suite='ironman.test.test_ironman',
      classifiers=[
        'Programming Language :: Python',
        'Development Status :: 4 - Beta',
        'Natural Language :: English',
        'Operating System :: POSIX :: Linux',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License (GPL)'
      ],
      extras_require={
        'testing': ['pytest'],
      },
      data_files=[('workbench', ['workbench/gFEXTest.py', 'workbench/xadc.yml'])],
)
