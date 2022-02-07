Python 3.9.7 (default, Sep 16 2021, 08:50:36) 
Type "copyright", "credits" or "license" for more information.

IPython 7.29.0 -- An enhanced Interactive Python.

runfile('/Users/Dev/GitHub/PyJafroc/Py/main1.py', wdir='/Users/Dev/GitHub/PyJafroc/Py')

%timeit df.apply(lambda x: integrate_f(x["a"], x["b"], x["N"]), axis=1)
122 ms ± 902 µs per loop (mean ± std. dev. of 7 runs, 10 loops each)

%prun -l 4 df.apply(lambda x: integrate_f(x["a"], x["b"], x["N"]), axis=1)
          629653 function calls (629635 primitive calls) in 0.219 seconds

   Ordered by: internal time
   List reduced from 200 to 4 due to restriction <4>

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
     1000    0.120    0.000    0.180    0.000 main1.py:27(integrate_f)
   555729    0.060    0.000    0.060    0.000 main1.py:21(f)
     3000    0.005    0.000    0.025    0.000 series.py:928(__getitem__)
     3000    0.003    0.000    0.017    0.000 series.py:1034(_get_value)

%load_ext Cython

%%cython

def f_plain(x):

    return x * (x - 1)

def integrate_f_plain(a, b, N):

    s = 0

    dx = (b - a) / N

    for i in range(N):

        s += f_plain(a + i * dx)

    return s * dx
    

%timeit df.apply(lambda x: integrate_f_plain(x["a"], x["b"], x["N"]), axis=1)
72 ms ± 1.1 ms per loop (mean ± std. dev. of 7 runs, 10 loops each)

%%cython

cdef double f_typed(double x) except? -2:

    return x * (x - 1)

cpdef double integrate_f_typed(double a, double b, int N):

    cdef int i

    cdef double s, dx

    s = 0

    dx = (b - a) / N

    for i in range(N):

        s += f_typed(a + i * dx)

    return s * dx
    

%timeit df.apply(lambda x: integrate_f_typed(x["a"], x["b"], x["N"]), axis=1)
21.6 ms ± 753 µs per loop (mean ± std. dev. of 7 runs, 10 loops each)

%prun -l 4 df.apply(lambda x: integrate_f_typed(x["a"], x["b"], x["N"]), axis=1)
          73924 function calls (73906 primitive calls) in 0.041 seconds

   Ordered by: internal time
   List reduced from 199 to 4 due to restriction <4>

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
     3000    0.005    0.000    0.026    0.000 series.py:928(__getitem__)
     3000    0.004    0.000    0.018    0.000 series.py:1034(_get_value)
     3000    0.002    0.000    0.006    0.000 base.py:5174(_get_values_for_loc)
     3000    0.002    0.000    0.008    0.000 base.py:3317(get_loc)

%%cython

cimport numpy as np

import numpy as np

cdef double f_typed(double x) except? -2:

    return x * (x - 1)

cpdef double integrate_f_typed(double a, double b, int N):

    cdef int i

    cdef double s, dx

    s = 0

    dx = (b - a) / N

    for i in range(N):

        s += f_typed(a + i * dx)

    return s * dx

cpdef np.ndarray[double] apply_integrate_f(np.ndarray col_a, np.ndarray col_b,

                                           np.ndarray col_N):

    assert (col_a.dtype == np.float_

            and col_b.dtype == np.float_ and col_N.dtype == np.int_)

    cdef Py_ssize_t i, n = len(col_N)

    assert (len(col_a) == len(col_b) == n)

    cdef np.ndarray[double] res = np.empty(n)

    for i in range(len(col_a)):

        res[i] = integrate_f_typed(col_a[i], col_b[i], col_N[i])

    return res
    
In file included from /Users/Dev/.ipython/cython/_cython_magic_5063b81dd83f9d43b51b2481cb4da689.c:643:
In file included from /Users/Dev/opt/anaconda3/lib/python3.9/site-packages/numpy/core/include/numpy/arrayobject.h:4:
In file included from /Users/Dev/opt/anaconda3/lib/python3.9/site-packages/numpy/core/include/numpy/ndarrayobject.h:12:
In file included from /Users/Dev/opt/anaconda3/lib/python3.9/site-packages/numpy/core/include/numpy/ndarraytypes.h:1944:
/Users/Dev/opt/anaconda3/lib/python3.9/site-packages/numpy/core/include/numpy/npy_1_7_deprecated_api.h:17:2: warning: "Using deprecated NumPy API, disable it with "          "#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION" [-W#warnings]
#warning "Using deprecated NumPy API, disable it with " \
 ^
1 warning generated.

%timeit apply_integrate_f(df["a"].to_numpy(), df["b"].to_numpy(), df["N"].to_numpy())
1.02 ms ± 12.5 µs per loop (mean ± std. dev. of 7 runs, 1000 loops each)

%timeit apply_integrate_f(df["a"].to_numpy(), df["b"].to_numpy(), df["N"].to_numpy())
1.01 ms ± 8.3 µs per loop (mean ± std. dev. of 7 runs, 1000 loops each)

%prun -l 4 apply_integrate_f(df["a"].to_numpy(), df["b"].to_numpy(), df["N"].to_numpy())
          76 function calls in 0.001 seconds

   Ordered by: internal time
   List reduced from 24 to 4 due to restriction <4>

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    0.001    0.001    0.001    0.001 {built-in method _cython_magic_5063b81dd83f9d43b51b2481cb4da689.apply_integrate_f}
        1    0.000    0.000    0.001    0.001 {built-in method builtins.exec}
        3    0.000    0.000    0.000    0.000 frame.py:3418(__getitem__)
        3    0.000    0.000    0.000    0.000 base.py:412(to_numpy)

%%cython

cimport cython

cimport numpy as np

import numpy as np

cdef double f_typed(double x) except? -2:

    return x * (x - 1)

cpdef double integrate_f_typed(double a, double b, int N):

    cdef int i

    cdef double s, dx

    s = 0

    dx = (b - a) / N

    for i in range(N):

        s += f_typed(a + i * dx)

    return s * dx

@cython.boundscheck(False)

@cython.wraparound(False)

cpdef np.ndarray[double] apply_integrate_f_wrap(np.ndarray[double] col_a,

                                                np.ndarray[double] col_b,

                                                np.ndarray[int] col_N):

    cdef int i, n = len(col_N)

    assert len(col_a) == len(col_b) == n

    cdef np.ndarray[double] res = np.empty(n)

    for i in range(n):

        res[i] = integrate_f_typed(col_a[i], col_b[i], col_N[i])

    return res
    
In file included from /Users/Dev/.ipython/cython/_cython_magic_95402377153af7930e33031c504ba541.c:644:
In file included from /Users/Dev/opt/anaconda3/lib/python3.9/site-packages/numpy/core/include/numpy/arrayobject.h:4:
In file included from /Users/Dev/opt/anaconda3/lib/python3.9/site-packages/numpy/core/include/numpy/ndarrayobject.h:12:
In file included from /Users/Dev/opt/anaconda3/lib/python3.9/site-packages/numpy/core/include/numpy/ndarraytypes.h:1944:
/Users/Dev/opt/anaconda3/lib/python3.9/site-packages/numpy/core/include/numpy/npy_1_7_deprecated_api.h:17:2: warning: "Using deprecated NumPy API, disable it with "          "#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION" [-W#warnings]
#warning "Using deprecated NumPy API, disable it with " \
 ^
1 warning generated.

%timeit apply_integrate_f_wrap(df["a"].to_numpy(), df["b"].to_numpy(), df["N"].to_numpy())
Traceback (most recent call last):

  File "/var/folders/d1/mx6dcbzx3v39r260458z2b200000gn/T/ipykernel_59802/4244180358.py", line 1, in <module>
    get_ipython().run_line_magic('timeit', 'apply_integrate_f_wrap(df["a"].to_numpy(), df["b"].to_numpy(), df["N"].to_numpy())')

  File "/Users/Dev/opt/anaconda3/lib/python3.9/site-packages/IPython/core/interactiveshell.py", line 2351, in run_line_magic
    result = fn(*args, **kwargs)

  File "/Users/Dev/opt/anaconda3/lib/python3.9/site-packages/decorator.py", line 232, in fun
    return caller(func, *(extras + args), **kw)

  File "/Users/Dev/opt/anaconda3/lib/python3.9/site-packages/IPython/core/magic.py", line 187, in <lambda>
    call = lambda f, *a, **k: f(*a, **k)

  File "/Users/Dev/opt/anaconda3/lib/python3.9/site-packages/IPython/core/magics/execution.py", line 1169, in timeit
    time_number = timer.timeit(number)

  File "/Users/Dev/opt/anaconda3/lib/python3.9/site-packages/IPython/core/magics/execution.py", line 169, in timeit
    timing = self.inner(it, self.timer)

  File "<magic-timeit>", line 1, in inner

  File "_cython_magic_95402377153af7930e33031c504ba541.pyx", line 32, in _cython_magic_95402377153af7930e33031c504ba541.apply_integrate_f_wrap

ValueError: Buffer dtype mismatch, expected 'int' but got 'long'

