# PyJafroc

This repository is a works-in-progress project for converting some of the `RJafroc` functions to `Python`. The converted functions are those judged essential for analyzing ROC/FROC datasets. Functions in `RJafroc` that are of research interest to me are not converted.


## Cython code introduced 2/22/22
* The Python code implementation of `StCadVsRad` for Nico ROC dataset was incredibly slow.
* Spent about 10 days wading through tutorials on `Cython`.
* Added `Cython` function `foms.pyx` which currently implements `Wilcoxon` and `wAfroc` FOMs. 
* Checked vs. `RJafroc` implementation
* An issue is that the `Cython` code does not easily implement -`Inf`. So the ratings have to be filtered to replace all such ratings with -10^6.
* At this time check vs. `RJafroc` only applies to `Wilcoxon` FOM.


## Workflow for using Cython 2/22/22
* Note `setup.py` and `foms.pyx` files
* Open Terminal and navigate to ~/GitHub/PyJafroc/Py directory.
* `python setup.py build_ext -if`
* `ipython`
* Copy code from test-foms-roc.py to ipython windos and hit return
* One can now work in Spyder. 
* If any changes are made to foms.pyx one must recompile and restart ipython/spyder kernel.


## Work on significance testing 2/11/22
* Implemented `StSignificanceTestingCadVsRad`, only `RRRC` analysis and checked vs. `R`
* Discovered error in `Numpy` variance function, which does not yield unbiased estimate
* Replaced `np.var` with `MyVar()` in `StSignificanceTestingCadVsRad`
* Checked all values for `$FTests` below; OK


## Work on significance testing 2/4/22
* `FOMijk2VarCov` to be renamed to `FOMijk2CovMatrix`

## JT2Rdr.xlsx
* All readers except 1 and 3 removed
* check into MS error; should be: OK, see note above on 2/11/22
```
$FTests
                 DF            MS     FStat          p
Treatment 1.0000000 0.00326627112 3.5955149 0.12348145
Error     4.4561033 0.00090842931        NA         NA
```

## Working on StSignificanceTesting 01/30/22
* Need to add `modalityID` and `readerID` fields to dataset object; done 2/1/22


## Added UtilORVarComponentsFactorial 01/30/22
* compared to R code; OK


## Added FOMijk2VarCov 01/29/22
* compared to R code
* unlike R code, at this point Python code is restricted to equal weights
* this has often caused confusion
* when comparing R code using `frocCr.xlsx`, which has unequal weights, will get different results that with Python code using the same file
* **MUST compare R code using `frocCrEqWts.xlsx` with Python code using `frocCr.xlsx`**


## Added UtilPseudoValue 01/29/22
Checked with "extdata/toyFiles/FROC/frocCr.xlsx" in Python and fileName <- system.file("extdata", "/toyFiles/FROC/frocCrEqWts.xlsx",
package = "RJafroc", mustWork = TRUE) in `RJafroc` RStudio.

Checked with "extdata/toyFiles/FROC/frocCr.xlsx" in Python and dataset05 in RStudio.

A major sticking point was the following (the second line took some figuring out):
```
perCase_jk = perCase.drop(k-K1)
perCase_jk = pd.Series(list(perCase_jk))
```

The second line is needed as otherwise the index variable is the case number, not the desired offset into abnormal cases.

## cython_tutorial (converting Python code to Cpp)
https://docs.cython.org/en/latest/src/tutorial/cython_tutorial.html


## Create setup.py
```
from setuptools import setup
from Cython.Build import cythonize
setup(
    ext_modules = cythonize("helloworld.pyx")
)
```

## Create helloworld.pyx
```
def say_hello_to(name):
    print("Hello my crap name is %s!" % name)
```

## At Terminal
```
python setup.py build_ext --inplace
```

## In new iPython Console
```
import helloworld
helloworld.say_hello_to("Dev")
```
