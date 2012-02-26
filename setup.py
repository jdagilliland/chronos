#!/usr/bin/env python

from distutils.core import setup

setup(
    name='chronos',
    version='0.2',
    description='An ncurses stopwatch/timer.',
    long_description=open('README.rst').read() + "\n\n" + open('HISTORY.rst').read(),
    author='Nick Sinopoli',
    author_email='nsinopoli@gmail.com',
    url='http://git.io/chronos',
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
    packages=['chronos', 'test'],
    entry_points={
        'console_scripts': [
            'chronos = chronos.main:main',
        ],
    }
)
