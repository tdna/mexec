#!/usr/bin/env python

from os.path import exists

from setuptools import setup


setup(name='mexec',
      version='0.1',
      description='Execute commands inside docker containers run by marathon',
      url='http://github.com/tdna/mexec',
      maintainer='Andras Toth',
      maintainer_email='ta1986@gmail.com',
      license='BSD',
      keywords='marathon docker',
      packages=['mexec'],
      long_description=(open('README.rst').read() if exists('README.rst')
                        else ''),
      install_requires=['docker-py'],
      zip_safe=False)
