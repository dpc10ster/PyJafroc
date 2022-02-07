import cython
import numpy as np
import pandas as pd

df = pd.DataFrame(

    {

        "a": np.random.randn(1000),

        "b": np.random.randn(1000),

        "N": np.random.randint(100, 1000, (1000)),

        "x": "x",

    }

)

def f(x):

    return x * (x - 1)



def integrate_f(a, b, N):

    s = 0

    dx = (b - a) / N

    for i in range(N):

        s += f(a + i * dx)

    return s * dx



