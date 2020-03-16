# coding: utf-8
import sys
from os.path import join, dirname

from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand

class Tox(TestCommand):

    user_options = TestCommand.user_options + [
        ('environment=', 'e', "Run 'test_suite' in specified environment")
    ]
    environment = None

    def finalize_options(self):
        super(Tox, self).finalize_options()
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import tox
        if self.environment:
            self.test_args.append('-e{0}'.format(self.environment))

        errno = tox.cmdline(self.test_args)
        sys.exit(errno)


setup(
    name='events_manager',
    version='1.2.0',
    description='Event Source Implementation',
    author='BRMED',
    author_email='desenvolvimento@grupobrmed.com.br',
    url='https://github.com/brmed/events_manager.git',
    packages=find_packages(),
    install_requires=['Django>=1.9', 'python-dateutil==2.6.1', 'attrs==18.2.0'],
    tests_require=['tox>=3.14.0', 'virtualenv>=1.11.2'],
    cmdclass = {'test': Tox},
)
