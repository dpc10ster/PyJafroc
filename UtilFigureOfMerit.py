#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 25 08:52:01 2022

@author: Dev
"""

import numpy as np
from DfReadDataFile import *

def UtilLesionWeightsDistr(maxLL, relWeights = 0):
    """
    Parameters
    ----------
    maxLL : int
        The maximum number of lesions per case in the dataset

    relWeights: float
        The default is 0, the vector containing the relative
        weights of the lesions

    Returns
    -------
    The lesion weights distribution 2D matrix
    """
    lesWghtDistr = np.full((maxLL, maxLL), -np.inf)
    if relWeights == 0:
        for i in range(maxLL):
            lesWghtDistr[i,0:(i+1)] = 1./(i+1)
    else:
        relWeights = np.array(relWeights, float)
        for i in range(maxLL):
            lesWghtDistr[i,0:(i+1)] = relWeights[0:(i+1)] / sum(relWeights[0:(i+1)])
      
    
    return (lesWghtDistr)
    

def Psi(x, y):
    """
    
    The famous Psi function in the definition of the Wilcoxon statistic
    
    Parameters
    ----------
    x and y: num
        ratings: float or integer


    Returns
    ----------
    1 if x < y, 0.5 if x = y or 0 if x > y
    
    """
    ret = 0.
    if x < y:
        ret = 1.
    elif x == y:
        ret = 0.5
    return ret


def UtilFigureOfMerit(ds, FOM):
    """
    Parameters
    ----------
    FileName : ds
        JAFROC dataset object created by DfReadDataFile()

    FOM: str
        The figure of merit, i.e., measure of performance,
        default is "wAFROC", or "Wilcoxon"

    Returns
    -------
    A dataframe with I rows and J columns, corresponding to treatments and
    readers, respectively, containing the FOM values
    """
    NL = ds[0]
    LL = ds[1]
    perCase = ds[2]
    relWeights = ds[3]
    DataType = ds[4]
    pass

    if not FOM in ["wAfroc", "Wilcoxon"]:
        myExit('FOM NOT in ["wAfroc", "Wilcoxon"]')
        
    K = len(NL[0,0,:,0])
    K2 = len(LL[0,0,:,0])
    K1 = K - K2
    maxNL = len(NL[0,0,0,:])
    maxLL = len(LL[0,0,0,:])
    lesWghtDistr = UtilLesionWeightsDistr(maxLL)
    
    ret = 0.0
    for k1 in range(K1):
        fp = -np.inf
        for l1 in range(maxNL):
            if NL[0,0,k1,l1] > fp: # capture the highest value
                fp = NL[0,0,k1,l1]
        for k2 in range(K2):
            for l2 in range(perCase[k2+1]):
                ret += lesWghtDistr[perCase[k2+1]-1,l2] * Psi(fp, LL[0,0,k2,l2])
    
    ret /= (K1*K2)
    return ret


ds = DfReadDataFile("extdata/JT.xlsx")
val = UtilFigureOfMerit(ds, "wAfroc")
