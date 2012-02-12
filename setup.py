#!/usr/bin/env python

from distutils.core import setup

setup(
    name='trigger',
    version='0.1',
    description='An ncurses stopwatch/timer.',
    long_description=open('README.rst').read() + "\n\n" + open('HISTORY.rst').read(),
    author='Nick Sinopoli',
    author_email='nsinopoli@gmail.com',
    url='http://git.io/trigger',
    license='BSD',
    classifiers=(
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Environment :: Console :: Curses',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Science/Research',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2'
    ),
    packages=['trigger', 'test']
)
