## Done for python 2 and python 3 compatibility
## does nothing on python 3
from __future__ import print_function
from setuptools import setup, find_packages

__version__ = '0.1 dev'
with open('README.md') as readme:
    long_description = readme.read()

exclude = [
        'data',
        ]

classifiers = [
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: System Administrators",
        "Topic :: System :: Systems Administration :: Authentication/Directory",
        ]

print(find_packages(exclude=exclude))
setup(
        name='git-authorized-key',
        description='AuthorizedKeysCommand to get authorized_keys entries from a git repo',
        keywords='System Administration',
        version=__version__,
        url='https://github.com/nixalot/git-authorized-key',
        classifiers=classifiers,
        license='BSD',
        maintainer='Matthew Raspberry',
        maintainer_email='nixalot@nixalot.com',
        long_description=long_description,
        packages=find_packages(exclude=exclude),
        install_requires=['pygit2'],
        entry_points={
            'console_scripts' : [
                'git-authorized-keys = git_authorized_key:main']
            }
        )
