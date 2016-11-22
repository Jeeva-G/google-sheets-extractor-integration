"""
Handles the building of python package
"""
from setuptools import setup
from newsdriver.version import __version__

setup(
    name='newsdriver',
    version=__version__,
    url='http://github.io/import.io/postsales_news-driver',
    author='David Gwartney',
    author_email='david.gwartney@import.io',
    packages=['newsdriver', ],
    entry_points={
        'console_scripts': [
            'newsdriver = newsdriver.main:main',
        ],
    },
    description='Web extraction solution for NewsDriver',
    long_description=open('README.txt').read(),
    install_requires=[
        'requests >= 2.11.1',
    ],
)
