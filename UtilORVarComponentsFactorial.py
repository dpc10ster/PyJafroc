#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 27 16:14:20 2022

@author: Dev
"""

from DfReadDataFile import *
from UtilFigureOfMerit import UtilFigureOfMerit

def UtilORVarComponentsFactorial(ds, FOM = "wAfroc"):

    NL = ds[0]
    LL = ds[1]
    if not FOM in ["wAfroc", "Wilcoxon"]:
        myExit('FOM NOT in ["wAfroc", "Wilcoxon"]')
        
    I = len(NL[:,0,0,0])
    J = len(NL[0,:,0,0])
    K = len(NL[0,0,:,0])
    
    foms = UtilFigureOfMerit(ds)
    fomsMeansEchRdr = foms.mean(axis=0) # row means
    fomsMeansEchMod = foms.mean(axis=1) # row means
    fomsMean = foms.mean() # row means
    
    if I > 1:
        msT = 0.0
        for i in range(I):
            msT += (fomsMeansEchMod[i] - fomsMean) ** 2
        msT *= J/(I - 1) 
    else: msT = 0
    
    if J > 1:
        msR = 0.0
        for j in range(J):
            msR += (fomsMeansEchRdr[j] - fomsMean) ** 2
        msR *= I / (J - 1)
    else: msR = 0
  
    if ((I > 1) & (J > 1)):
        msTR = 0.0
        for i in range(I):
            for j in range(J):
                msTR += (foms[i, j] - fomsMeansEchMod[i] - fomsMeansEchRdr[j] + fomsMean) ** 2
        msTR /= ((J - 1) * (I - 1))
    else: msTR = 0
    
    msArray = [msT, msR, msTR]
    dfArray = [I - 1, J - 1, (I - 1) * (J - 1)]
    ssArray = [a * b for a, b in zip(msArray, dfArray)]
    
    return [fomsMeansEchRdr, fomsMeansEchMod]
    
FileName = "extdata/JT.xlsx"
ds = DfReadDataFile(FileName)
fomMeans = UtilORVarComponentsFactorial(ds)    