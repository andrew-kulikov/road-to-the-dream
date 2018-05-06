from setuptools import setup, find_packages
from os.path import join, dirname

setup(
    name='tasochki',
    version='1.0',
    packages=find_packages(),
    long_description=open(join(dirname(__file__), 'README.md')).read(),
    install_requires=[
        'jsonpickle==0.9.6'
    ],
    entry_points={
       'console_scripts': [
           'rd = console_interface.console:main',
           ]
       }
)
