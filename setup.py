from os.path import join, dirname

from setuptools import setup, find_packages

setup(
    name='Road To The Dream',
    version='1.0',
    packages=find_packages(),
    long_description=open(join(dirname(__file__), 'README.md')).read(),
    install_requires=[
        'jsonpickle==0.9.6',
        'python-dateutil==2.6.1'
    ],
    entry_points={
       'console_scripts': [
           'rtd = console_interface.console:main',
        ]
    },
    test_suite='tests.lib_tests'
)
