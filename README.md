# PyJafroc

This repository is for converting some of the `RJafroc` functions to `Python`.




## Added UtilORVarComponentsFactorial 01/30/22
compared to R code


## Added FOMijk2VarCov 01/29/22
compared to R code


## Added UtilPseudoValue 01/29/22
Checked with "extdata/toyFiles/FROC/frocCr.xlsx" in Python and fileName <- system.file("extdata", "/toyFiles/FROC/frocCrEqWts.xlsx",
package = "RJafroc", mustWork = TRUE) in `RJafroc` RStudio.

Checked with "extdata/toyFiles/FROC/frocCr.xlsx" in Python and dataset05 in RStudio.

A major sticking point was the following (the second line took some figuring out):
perCase_jk = perCase.drop(k-K1)
perCase_jk = pd.Series(list(perCase_jk))

The second line is needed as otherwise the index variable is the case number, not the desired offset into abnormal cases.

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
