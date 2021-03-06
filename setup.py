#!/usr/bin/env python3
""" Nullpynter - The Nullpointer Uploader Service Interface

BSD 3-Clause License

Copyright (c) 2021, Ian Santopietro
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its
   contributors may be used to endorse or promote products derived from
   this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

#pylint: skip-file
# We don't need to check these in setup

import os
import subprocess
from setuptools import setup, find_packages, Command

NAME = "nullpynter"

def get_version():
    """ Get the program version. """
    #pylint: disable=exec-used
    # Just getting the version.
    version = {}
    with open(os.path.join(NAME, '__version__.py')) as fp:
        exec(fp.read(), version)
    return version['__version__']

with open("README.md", "r") as fh:
    long_description = fh.read()

classifiers = [
    'Environment :: Console',
    'Environment :: X11 Applications :: GTK',
    'Intended Audience :: End Users/Desktop',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: BSD License'
    'Natural Language :: English',
    'Operating System :: POSIX :: Linux',
    'Programming Language :: Python :: 3',
    'Topic :: Communications :: File Sharing',
    'Topic :: Internet'
]

class Release(Command):
    """ Generate a release and push it to git."""
    description = "Generate a release and push it to git."

    user_options = [
        ('dry-run', None, 'Skip the actual release and do a dry run instead.'),
        ('skip-deb', None, 'Skip doing a debian update for this release.'),
        ('skip-git', None, 'Skip committing to git at the end.'),
        ('prerelease=', None, 'Release a pre-release version (alpha,beta,rc)'),
        ('increment=', None, 'Manually specify the desired increment (MAJOR, MINOR, PATCH)')
    ]

    def initialize_options(self):
        self.dry_run = False
        self.skip_deb = False
        self.skip_git = False
        self.prerelease = None
        self.increment = None

    def finalize_options(self):
        pass

    def run(self):
        cz_command = ['cz', 'bump', '--yes']
        ch_command = ['dch']
        git_command = ['git', 'add', '.']

        def capture_version(sp_complete):
            output = sp_complete.stdout.decode('UTF-8').split('\n')
            print('\n'.join(output))
            for line in output:
                if 'tag to create' in line:
                    version_line = line

            try:
                return version_line.split()[-1].replace('v', '')
            except UnboundLocalError:
                stderr = sp_complete.stderr.decode('UTF-8')
                print("WARNING: Couldn't get updated version! Using current.")
                print(stderr)
                return get_version()

        if self.dry_run:
            print('Dry run: Not making actual changes')
            cz_command.append('--dry-run')

        if self.prerelease:
            if self.prerelease.lower() not in ['alpha', 'beta', 'rc']:
                raise Exception(
                    f'{self.prerelease} is not a valid prerelease type. Please '
                    'use one of "alpha", "beta", or "rc".'
                )
            cz_command.append('--prerelease')
            cz_command.append(self.prerelease.lower())

        if self.increment:
            if self.increment.upper() not in ['MAJOR', 'MINOR', 'PATCH']:
                raise Exception(
                    f'{self.increment} is not a valid increments. Please use '
                    'one of MAJOR, MINOR, or PATCH.'
                )
            cz_command.append('--increment')
            cz_command.append(self.increment.upper())

        # We need to get the new version from CZ, as the file hasn't been
        # updated yet.
        version_command = cz_command.copy()
        version_command.append('--dry-run')
        version_complete = subprocess.run(version_command, capture_output=True)

        version = capture_version(version_complete)
        print(f'Old Version: {get_version()}')
        print(f'New version: {version}')

        ch_command.append(f'-v{version}')
        if not self.skip_deb:
            print(ch_command)
            if not self.dry_run:
                subprocess.run(ch_command)
                subprocess.run(['dch', '-r', '""'])

        if not self.skip_git:
            print(git_command)
            if not self.dry_run:
                subprocess.run(git_command)

        print(' '.join(cz_command))
        if not self.dry_run:
            subprocess.run(cz_command)

class Test(Command):
    """ Run pyflakes and pytest"""
    description = 'Run pyflakes, pytest, and pylint'

    user_options = [
        ('run-flakes', None, 'Run pyflakes'),
        ('skip-test', None, 'Skip running pytest'),
        ('skip-lint', None, 'Skip running pylint')
    ]

    def initialize_options(self):
        self.run_flakes = True
        self.skip_test = False
        self.skip_lint = False

    def finalize_options(self):
        pass

    def run(self):
        pytest_command = ['pytest-3']
        flakes_command = ['pyflakes3', 'repolib']
        lint_command = ['pylint', 'repolib']

        if not self.skip_test:
            subprocess.run(pytest_command)

        if not self.run_flakes:
            subprocess.run(flakes_command)

        if not self.skip_lint:
            subprocess.run(lint_command)

setup(
    name=NAME,
    version=get_version(),
    author='Ian Santopietro',
    author_email='ian@system76.com',
    url='https://github.com/pop-os/nullpy',
    description='Simple Command-line and GTK Interface for the Nullpointer file bucket and URL Shortener Service',
    download_url='https://github.com/isantop/nullpy/releases',
    long_description=long_description,
    tests_require=['pytest'],
    license='BSD',
    packages=['nullpynter', 'nullpynter/gui'],
    cmdclass={'release': Release, 'test': Test},
    scripts=['bin/npy'],
    data_files=[]
)
