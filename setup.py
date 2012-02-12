#!/usr/bin/env python

from distutils.core import setup

setup(name='trigger',
      version='0.1',
      description='An ncurses stopwatch/timer.',
      author='Nick Sinopoli',
      author_email='nsinopoli@gmail.com',
      home_page='git.io/trigger',
      license='BSD',
      scripts=['bin/trigger'],
      packages=['trigger'])
