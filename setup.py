# coding: utf-8
import sys
from os.path import join, dirname

from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand


setup(
    name='event_sourcing',
    version='1.0.0',
    description='Event Source Implementation',
    author='BRMED',
    author_email='desenvolvimento@',
    url='https://github.com/brmed/event_sourcing.git',
    packages=find_packages(),
    install_requires=['Django>=1.5.3', 'python-dateutil==2.6.1', 'attrs==18.2.0', 'typing==3.6.2'],
    tests_require=['tox>=1.6.1', 'virtualenv>=1.11.2'],
    cmdclass = {'test': Tox},
)
