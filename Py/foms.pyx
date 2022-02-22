#from cpython.array cimport array
#cimport numpy as np
from libc.stdio cimport printf

def wilcoxon(double [:] fp, double [:] tp):
    cdef: 
        double ret = 0.0
        int K1, K2, k1, k2
  
    K2 = tp.shape[0]
    K1 = fp.shape[0] - K2
    
    for k1 in range(K1):
        for k2 in range(K2):
            if fp[k1] < tp[k2]: 
                ret += 1.0
            elif fp[k1] == tp[k2]:
                ret += 0.5
    ret /= (K1 * K2)
  
    return ret


def wAfroc(double [:,:] nl, double [:,:] ll, int [:] perCase, double [:,:] lesWghtDistr):
    cdef: 
        double ret = 0.0
        double fp
        int K1, K2, k1, k2, maxNL, maxLL, l1, l2
  
    K2    = ll.shape[0]
    maxLL = ll.shape[1]
    K1    = nl.shape[0] - K2
    maxNL = nl.shape[1]
    #printf("K1 = %d, K2 = %d\n", K1, K2)
    #printf("maxNL = %d, maxLL = %d\n", maxNL, maxLL)
    
    for k1 in range(K1):
        fp = -10e6
        for l1 in range(maxNL):
            #printf("k1 = %d, l1 = %d, nl[k1][l1] = %f\n", k1, l1, nl[k1][l1])
            if nl[k1][l1] > fp:  # capture the highest value
                fp = nl[k1][l1]
        for k2 in range(K2):
            for l2 in range(perCase[k2]):
                #printf("k2 = %d, perCase[k2] = %d, l2 = %d, ll[k2][l2] = %f, lesWghtDistr[perCase[k2]-1, l2] = %f\n", k2, perCase[k2], l2, ll[k2][l2], lesWghtDistr[perCase[k2]-1, l2])
                if fp < ll[k2,l2]: 
                    ret += lesWghtDistr[perCase[k2]-1, l2]
                elif fp == ll[k2,l2]:
                    ret += (0.5*lesWghtDistr[perCase[k2]-1, l2])
    ret /= (K1 * K2)
  
    return ret
