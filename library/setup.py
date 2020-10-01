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


setup(
        cmdclass        = {'test': TestCommand, 'testandbuild':BuildWithTests}
)
