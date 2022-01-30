#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 24 09:26:41 2022

@author: Dev
"""
from DfReadDataFile import DfReadDataFile
import pandas as pd
from UtilFigureOfMerit import UtilFigureOfMerit
from UtilORVarComponentsFactorial import UtilORVarComponentsFactorial
import math
import numpy as np



def ORSummaryRRRC(ds, FOMs, ANOVA, alpha, diffTRName):
    pass



def ORSummaryFRRC(ds, FOMs, ANOVA, alpha, diffTRName):
    pass



def ORSummaryRRFC(ds, FOMs, ANOVA, alpha, diffTRName):
    pass



def StSignificanceTesting(ds, FOM = "wAfroc", analysisOption = "RRRC", \
                          alpha = 0.05):
    """
    Parameters
    ----------
    ds : list
        dataset list object ds

    FOM : string
        The figure of merit or measure of performance, the
        default is "wAfroc", or "Wilcoxon"
        
    analysisOption : str
        The desired generalization: RRRC" (default) or "RRFC" or "FRRC"
        
    alpha : float
        The significance level of the test, defaults to 0.05    

    Returns
    -------
    TODO significanceTesting object st 

    """
    
    I = len(ds[0][:,0,0,0])
    J = len(ds[0][0,:,0,0])
    
    if J == 1:
        analysisOption = "FRRC" 
    elif I == 1: 
        analysisOption = "RRFC"
    pass

    foms = UtilFigureOfMerit(ds, "wAfroc")
    # fomsMeansEchRdr = foms.mean(axis=0) # col means
    fomsMeansEchMod = foms.mean(axis=1) # row means
    # fomsMean = foms.mean() # mean over all values
    trtMeans = pd.DataFrame({"Estimate": fomsMeansEchMod})
    
    ret = UtilORVarComponentsFactorial(ds)
    TRAnova = ret[0]
    VarCom = ret[1]
    
    ANOVA = [TRAnova, VarCom]
    
    trtMeanDiffs = np.full(math.comb(I,2), 0.0)
    # following is needed to hold variable length strings
    diffTRName = np.array([math.comb(I,2)], dtype=object) 
    ii = 0
    for i in range(I):
        if i == I:
            break
        for ip in range((i+1),I):
            trtMeanDiffs[ii] = trtMeans.Estimate[i] - trtMeans.Estimate[ip]
            diffTRName[ii] = "trt" + str(i) + " - " + "trt" + str(ip)
            ii += 1
    trtMeanDiffs = pd.DataFrame({"Estimate": trtMeanDiffs})
    trtMeanDiffs.index = diffTRName
    
    FOMs = [foms, trtMeans, trtMeans]
    
    pass

    if analysisOption == "RRRC":
        RRRC = ORSummaryRRRC(ds, FOMs, ANOVA, alpha, diffTRName)
        return [FOMs, ANOVA, RRRC]
    
    
    if analysisOption == "FRRC":
        FRRC = ORSummaryFRRC(ds, FOMs, ANOVA, alpha, diffTRName)
        return [FOMs, ANOVA, FRRC]
    
    if analysisOption == "RRFC":
        RRFC = ORSummaryRRFC(ds, FOMs, ANOVA, alpha, diffTRName)
        return [FOMs, ANOVA, RRFC]
    
    




#FileName = "extdata/JT.xlsx"
FileName = "extdata/toyFiles/FROC/frocCr.xlsx"
ds = DfReadDataFile(FileName)
# pv = UtilPseudoValues(ds)
# varCom = UtilORVarComponentsFactorial(ds)
#fomMeans = UtilORVarComponentsFactorial(ds)
st = StSignificanceTesting(ds)