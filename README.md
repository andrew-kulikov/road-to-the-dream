# Road To The Dream task tracker

Installation package contains library and console application.

Package contains:

1.  Task tracker library 'src': implements basic models and communication interface. For more information see modules documentstion.

2.  'tests' package: contains unit tests for library.

3.  'console_interface' package: console application that uses library.


## Installation

To install this package you need run terminal, go to the package folder and simply enter command:

python setup.py install

All described packages will be installed at your computer.

To work with console application, enter command starts from rd:

```
rd ...
```

To get help enter

```
rd -h
```

## Python library usage

To use rd library in your python program simply import library.

```python
>>> import rd_tracker
>>> help(rd_tracker)
```

In documentation you can get all information about main library instances and classes.

## Library testing

You can test library functionality by running native tests. To run tests, just open the command window and enter command below:

```
python setup.py test
```

You can see test rusults on your screen. You can also add your own tests in file tests/lib_tests.py.