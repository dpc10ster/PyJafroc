# ROC data
import foms
import numpy as np
nl = np.array([.1, .2, 3, .4], dtype = np.float32)
ll = np.array([.2, .5, 2, 4, 1], dtype = np.float32)

# k2 = 1:  1 +  0.5 + 0 + 0  =  1.5
# k2 = 2:  1 +  1   + 0 + 1   =  3.0
# k2 = 3:  1 +  1   + 0 + 1   =  3.0
# k2 = 4:  1 +  1 + 1 + 1    =  4.0
# k2 = 5:  1 +  1 + 0 + 1    =  3.0
# sum = 14.5
# divided by 20 gives 0.725

foms.wilcoxon(nl,ll)
0.725


# FROC data
import foms
import numpy as np
negInf = -10e6
K1 = 4
K2 = 5
maxNL = 2
maxLL = 3
nl = np.zeros((K1, maxNL), dtype = np.float32)
ll = np.zeros((K2, maxLL), dtype = np.float32)

nl[0,:] = [.1,  negInf]
nl[1,:] = [.2, .4]
nl[2,:] = [ 3, .7]
nl[3,:] = [.4, .2]

perCase = np.array((1,2,3,1,1), dtype = np.int32)            
# TODO 
# need to check ll[k2] to ensure it does not have more
# finite (non negInf) elements than allowed by perCase
ll[0,:] = [.2, negInf,  negInf]
ll[1,:] = [.5, .3,  negInf ]
ll[2,:] = [ 2,  3,   1  ]
ll[3,:] = [ 4,  negInf,   negInf  ]
ll[4,:] = [ 1,  negInf,   negInf  ]

maxLL = ll.shape[1]
lesWghtDistr = np.zeros((maxLL, maxLL), dtype = np.float32)
for i in range(maxLL):
    lesWghtDistr[i, 0:(i+1)] = 1.0/(i+1)
    
# In [9]: lesWghtDistr
# Out[9]: 
# array([[1.        , 0.        , 0.        ],
#        [0.5       , 0.5       , 0.        ],
#        [0.33333334, 0.33333334, 0.33333334]], dtype=float32)    
    

# In [7]: nl
# Out[7]: 
# array([[ 1.e-01, -1.e+07],
#        [ 2.e-01,  4.e-01],
#        [ 3.e+00,  7.e-01],
#        [ 4.e-01,  2.e-01]], dtype=float32)

# In [8]: ll
# Out[8]: 
# array([[ 2.e-01, -1.e+07, -1.e+07],
#        [ 5.e-01,  3.e-01, -1.e+07],
#        [ 2.e+00,  3.e+00,  1.e+00],
#        [ 4.e+00, -1.e+07, -1.e+07],
#        [ 1.e+00, -1.e+07, -1.e+07]], dtype=float32)


foms.wAfroc(nl,ll,perCase,lesWghtDistr)

# Out[10]: 0.6583333380520344 cython (uses floating point)
# Out[40]: 0.6583333333333334 python (uses double precision)

# SPEED TEST
# Cython
%timeit foms.wAfroc(nl,ll,perCase,lesWghtDistr)
# 1.32 µs ± 8.25 ns per loop (mean ± std. dev. of 7 runs, 1000000 loops each)
# Python
nl12 = np.vstack((nl,ll[:,0:2]))
%timeit FigureOfMerit_ij(nl12, ll, perCase, FOM = "wAfroc")
# 1.11 ms ± 14.4 µs per loop (mean ± std. dev. of 7 runs, 1000 loops each)
# 833x!!
