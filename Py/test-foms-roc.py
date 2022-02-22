# ROC data
import foms
import numpy as np
# add dummy ll ratings to nl array
nl = np.array([.1, .2, 3, .4, 0, 0, -1, -1, 2], dtype = np.double)
ll = np.array([.2, .5, 2, 4, 1], dtype = np.double)

# k2 = 1:  1 +  0.5 + 0 + 0  =  1.5
# k2 = 2:  1 +  1   + 0 + 1   =  3.0
# k2 = 3:  1 +  1   + 0 + 1   =  3.0
# k2 = 4:  1 +  1 + 1 + 1    =  4.0
# k2 = 5:  1 +  1 + 0 + 1    =  3.0
# sum = 14.5
# divided by 20 gives 0.725

foms.wilcoxon(nl,ll)
0.725


