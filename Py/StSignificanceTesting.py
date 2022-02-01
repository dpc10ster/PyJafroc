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
from scipy.stats import f
from scipy.stats import t




def ORSummaryRRRC(ds, FOMs, ANOVA, alpha, diffTRName):
    I = len(ds[0][:,0,0,0])
    J = len(ds[0][0,:,0,0])

    trtMeans =  FOMs[1]
    trtMeanDiffs  =  FOMs[2]
    
    TRanova = ANOVA[0]
    VarCom = ANOVA[1]
    
    # a) Test for H0: Treatments have the same AUC
    msDen = TRanova['MS']['TR'] + \
        max(J * (VarCom['Estimates']['Cov2'] \
        - VarCom['Estimates']['Cov3']), 0)
    f_ = TRanova["MS"]["T"]/msDen
    ddf = msDen ** 2/(TRanova['MS']['TR'] ** 2 / ((I - 1) * (J - 1)))
    #https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.f.html
    p = 1 - f.cdf(f_, I-1, ddf)
    
    RRRC = {"FTests": [], "ciDiffTrt": []}
    RRRC["FTests"].append(pd.DataFrame({"DF": (I-1,ddf), \
                            "MS": (TRanova["MS"]["T"], TRanova["MS"]["TR"]), \
                            "FStat": (f_, np.NAN), \
                            "PValue": (p, np.NAN)}).round(4))
        
    stdErr = math.sqrt(2 * msDen/J)
    tStat = []
    PrGTt = []
    CI = np.zeros((len(trtMeanDiffs["Estimate"]), 2), dtype=float)
    for i in range(len(trtMeanDiffs["Estimate"])):
        tStat.append(trtMeanDiffs["Estimate"][i] / stdErr)
        # 1 - t.pdf is AUC above the observed value of t
        # the factor of 2 counts both upper and lower tails
        # the absolute value counts equally both positive and negative
        # excursions from zero
        PrGTt.append(2 * (1 - t.cdf(abs(tStat[i]), ddf)))
        CI[0][0] = trtMeanDiffs["Estimate"] - t.ppf(1 - alpha/2, ddf) * stdErr
        CI[0][1] = trtMeanDiffs["Estimate"] + t.ppf(1 - alpha/2, ddf) * stdErr 
    # *** ValueError: If using all scalar values, you must pass an index
    RRRC["ciDiffTrt"].append(pd.DataFrame({"Estimate": trtMeanDiffs.values[0][0], \
                            "StdErr": [stdErr], \
                            "DF": [ddf], \
                            "t": [tStat[0]], \
                            "PrGTt": [PrGTt[0]], \
                            "CI_Lo": [CI[0][0]], \
                            "CI_hi": [CI[0][1]]}).round(4))
    pass
    return RRRC
# =============================================================================
# TODO this code needs to pass the FED 5-modality dataset
# =============================================================================



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
    # fomsMeansEchRdr = foms.values.mean(axis=0) # col means
    fomsMeansEchMod = foms.values.mean(axis=1) # row means
    # fomsMean = foms.values.mean() # mean over all values ? NO see TBA
    trtMeans = pd.DataFrame({"Estimate": fomsMeansEchMod})
    
    ret = UtilORVarComponentsFactorial(ds)
    TRAnova = ret[0]
    VarCom = ret[1]
    
    ANOVA = [TRAnova, VarCom]
    
    trtMeanDiffs = np.full(math.comb(I,2), 0.0)
    # in following dtype=object is needed to hold variable length strings
    diffTRName = np.ndarray([math.comb(I,2)], dtype=object) 
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
    
    FOMs = [foms, trtMeans, trtMeanDiffs]
    
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
    
    pass




#FileName = "extdata/JT.xlsx"
FileName = "extdata/toyFiles/FROC/frocCr.xlsx"
ds = DfReadDataFile(FileName)
# pv = UtilPseudoValues(ds)
# varCom = UtilORVarComponentsFactorial(ds)
#fomMeans = UtilORVarComponentsFactorial(ds)
st = StSignificanceTesting(ds)