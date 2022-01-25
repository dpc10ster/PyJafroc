# PyJafroc

This repository is for converting some of the `RJafroc` files to `Python`.

## cython_tutorial
https://docs.cython.org/en/latest/src/tutorial/cython_tutorial.html


## Create setup.py
from setuptools import setup
from Cython.Build import cythonize

setup(
    ext_modules = cythonize("helloworld.pyx")
)

## Create helloworld.pyx
def say_hello_to(name):
    print("Hello my crap name is %s!" % name)


## At Terminal
python setup.py build_ext --inplace


## In new iPython Console
import helloworld
helloworld.say_hello_to("Dev")
