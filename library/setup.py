#!/usr/bin/env python

try:
    import test
except:
    pass

"""
Copyright (c) 2014 Pimoroni

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

try:
    from setuptools import setup, Command
    from setuptools.command.build import build
except ImportError:
    from distutils.core import setup, Command
    from distutils.command.build import build

class BuildWithTests(build):
    def run(self):
        if test is not None and test.test is not None:
            assert test.test() == True, "Automated tests failed!"
            print("notice  all tests passed: OK!")
        else:
            print("notice  automated tests skipped!")

        build.run(self)

class TestCommand(Command):
    description = "Runs Automation HAT tests"
    user_options = []
    def initialize_options(self):
        pass
    def finalize_options(self):
        pass
    def run(self):
        if test is not None and test.test is not None:
            assert test.test() == True, "Automated tests failed!"
            print("notice  all tests passed: OK!")
        else:
            print("notice  automated tests skipped!")

classifiers = ['Development Status :: 5 - Production/Stable',
               'Operating System :: POSIX :: Linux',
               'License :: OSI Approved :: MIT License',
               'Intended Audience :: Developers',
               'Programming Language :: Python :: 2.6',
               'Programming Language :: Python :: 2.7',
               'Programming Language :: Python :: 3',
               'Topic :: Software Development',
               'Topic :: System :: Hardware']

setup(
        name            = 'automationhat',
        version         = '0.0.3',
        author          = 'Philip Howard',
        author_email    = 'phil@pimoroni.com',
        description     = 'Automation HAT Driver',
        long_description= open('README.txt').read() + open('CHANGELOG.txt').read(),
        license         = 'MIT',
        keywords        = 'Raspberry Pi automation controller',
        url             = 'http://www.pimoroni.com',
        classifiers     = classifiers,
        py_modules      = [],
        packages        = ['automationhat'],
        include_package_data = True,
        install_requires= ['RPi.GPIO','sn3218'],
        cmdclass        = {'test': TestCommand, 'testandbuild':BuildWithTests}
)
