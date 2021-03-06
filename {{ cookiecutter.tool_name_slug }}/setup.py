# -*- coding: utf-8 -*-
#
# {{ cookiecutter.tool_name }}
#
# Redistribution and use in source and binary forms, with or without modification, are permitted provided that the
# following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this list of conditions and the
# following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the
# following disclaimer in the documentation and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote
# products derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
# INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

import re
import os
import sys
import codecs

from os.path import dirname, join
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand


if sys.version_info < (3, 5,):
    raise RuntimeError("{{ cookiecutter.tool_name }} requires Python 3.5.0+")


#
# Get version software version
#
version_file = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), "{{ cookiecutter.tool_name_slug }}")), '__init__.py')
with codecs.open(version_file, 'r', 'latin1') as fp:
    try:
        version = re.findall(r"^__version__ = ['\"]([^']+)['\"]\r?$",
                             fp.read(), re.M)[0]
    except IndexError:
        raise RuntimeError('Unable to determine version.')
    
    
with open(join(dirname(__file__), 'requirements.txt')) as f:
    required = f.read().splitlines()
    
with open(join(dirname(__file__), 'requirements-performance.txt')) as f:
    required_performance = f.read().splitlines()

with open(join(dirname(__file__), 'requirements-runtest.txt')) as f:
    required_test = f.read().splitlines()

with open(join(dirname(__file__), 'README.md')) as f:
    long_description = f.read()


class PyTest(TestCommand):
    user_options = []
    
    def run(self):
        import subprocess
        import sys
        errno = subprocess.call([sys.executable, '-m', 'pytest', '--cov-report', 'html', '--cov-report', 'term', '--cov', '{{ cookiecutter.tool_name_slug }}/'])
        raise SystemExit(errno)


setup(
    name='{{ cookiecutter.tool_name_slug }}',
    version=version,
    install_requires=required,
    url='{{ cookiecutter.project_site }}',
    license='BSD',
    author='{{ cookiecutter.author }}',
    author_email='{{ cookiecutter.author_mail }}',
    packages=find_packages(),
    include_package_data=True,
    extras_require={
        'performance':  required_performance
    },
    entry_points={'console_scripts': [
        '{{ cookiecutter.tool_name_slug | replace("_", "-") }} = {{ cookiecutter.tool_name_slug }}.actions.default.cli:cli',
    ]},
    description='{{ cookiecutter.brief_description }}',
    long_description=long_description,
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Other Audience',
        'License :: OSI Approved :: BSD License',
        'Operating System :: MacOS',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 3.5',
        'Topic :: Security',
    ],
    tests_require=required_test,
    cmdclass=dict(test=PyTest)
)

