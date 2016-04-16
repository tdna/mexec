#!/usr/bin/env python

from os.path import exists

from setuptools import setup


setup(name='mexec',
      version='0.1.0',
      description='Execute commands inside docker containers run by mesos',
      url='http://github.com/tdna/mexec',
      scripts=['bin/mexec'],
      maintainer='Andras Toth',
      maintainer_email='ta1986@gmail.com',
      license='BSD',
      keywords='mesos docker',
      packages=['mexec'],
      long_description=(open('README.md').read() if exists('README.md')
                        else ''),
      install_requires=['docker-py', 'requests'],
      tests_require=['pytest-mock', 'pytest'],
      setup_requires=['pytest-runner'],
      zip_safe=False)
