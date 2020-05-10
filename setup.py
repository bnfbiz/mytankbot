import os, sys, re

# from realpython/lessons/installable-single-package

from pirobot import __version__ as version

readme = os.path.join(os.path.dirname(__file__), "README.md")
long_description = open(readme).read()

SETUP_ARGS = dict(
    name='pirobot',
    version=version,
    description=('Pi based robot modules and robot code'),
    url='https://github.com/bnfbiz/mytankbot',
    author='Brian Farrell',
    author_email='',
    license='GPLv3',
    include_package_data=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Raspberry Pi Robot',
        'Intended Audience :: Raspberry Pi Robot Users',
        'Operating System :: Raspberry Pi',
        'Programming Language :: Python :: 3.7',
    ],
    py_modules = ['pirobot',],
    install_requires = [
        'evdev >= 1.3.0',
        'time',
        'rpi.GPIO >= 0.7.0',
    ]
)

if __name__ == '__main__':
    from setuptools import setup, find_packages

