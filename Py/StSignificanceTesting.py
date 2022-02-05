#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 24 09:26:41 2022

@author: Dev
"""
import pandas as pd
from UtilFigureOfMerit import UtilFigureOfMerit, DfExtractDataset
from UtilORVarComponents import UtilORVarComponents
import math
import numpy as np
from scipy.stats import f, t




def ORSummaryRRRC(ds, FOMs, ANOVA, alpha, diffTRName):
    I = len(ds[0][:,0,0,0])
    J = len(ds[0][0,:,0,0])

    trtMeanDiffs = FOMs[list(FOMs.keys())[2]]
    
    TRAnova = ANOVA["TRAnova"]
    VarCom = ANOVA["VarCom"]
    #
    # a) Test for H0: Treatments have the same AUC
    #
    msDen = TRAnova['MS']['TR'] + \
        max(J * (VarCom['Estimates']['Cov2'] \
        - VarCom['Estimates']['Cov3']), 0)
    f_ = TRAnova["MS"]["T"]/msDen
    ddf = msDen ** 2/(TRAnova['MS']['TR'] ** 2 / ((I - 1) * (J - 1)))
    #https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.f.html
    p = 1 - f.cdf(f_, I-1, ddf)
    
    RRRC = {"FTests": [], "ciDiffTrt": [], "ciAvgRdrEachTrt": []}
    ftests = pd.DataFrame({"DF": (I-1,ddf), \
                            "MS": (TRAnova["MS"]["T"], TRAnova["MS"]["TR"]), \
                            "FStat": (f_, np.NAN), \
                            "PValue": (p, np.NAN)}).round(4)
    ftests.index = ["Treatment", "Error"]        
    RRRC["FTests"].append(ftests)
    #
    # b) 1-alpha confidence intervals and hypothesis tests (H0: difference = 0)
    # for same treatment AUC differences
    #
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
    trtdiffs = pd.DataFrame({"Estimate": trtMeanDiffs.values[0][0], \
                            "StdErr": [stdErr], \
                            "DF": [ddf], \
                            "t": [tStat[0]], \
                            "PrGTt": [PrGTt[0]], \
                            "CI_lo": [CI[0][0]], \
                            "CI_hi": [CI[0][1]]})
# =============================================================================
# TODO generalize to more than 2 treatments
# =============================================================================
    trtdiffs.index = ["trt0 - trt1"]
    trtdiffs = trtdiffs.round(4)
    RRRC["ciDiffTrt"].append(trtdiffs)    
    #
    # c) Single-treatment 95% confidence intervals
    # (Each analysis is based only on data for the specified treatment, i.e., 
    # on the treatment-specific reader ANOVA of AUCs and Cov2 estimates.)
    #
    dfSingle = [0] * I
    msDenSingle = [0] * I
    stdErrSingle = [0] * I
    CISingle = np.zeros((I,2))
    # alternate way of getting the key variables of dictionary data type
    trtMeans = FOMs[list(FOMs.keys())[0]]
    trtMeans = trtMeans.mean(axis = 1)
    ci = pd.DataFrame({"Estimate": [],
                       "StdErr": [], 
                       "DF": [],
                       "CI_lo": [], 
                       "CI_hi": [],
                       "Cov2": []})
    for i in range(I):
        # Hillis 2007 5.3. Single test inference using only corresponding data
        trtStr = "trt" + str(i)
        msDenSingle[i] = ANOVA["IndividualTrt"]["msREachTrt"][trtStr] + \
            max(J * ANOVA["IndividualTrt"]["cov2EachTrt"][trtStr], 0)
        dfSingle[i] = (msDenSingle[i] ** 2) / (ANOVA["IndividualTrt"]["msREachTrt"][trtStr] ** 2) * (J - 1)
        stdErrSingle[i] = math.sqrt(msDenSingle[i]/J) # Eqn. 25
        CISingle[i][0] = trtMeans[i] - t.ppf(1 - alpha/2, dfSingle[i]) * stdErrSingle[i] 
        CISingle[i][1] = trtMeans[i] + t.ppf(1 - alpha/2, dfSingle[i]) * stdErrSingle[i] # Eqn. 25
        ci = ci.append({"Estimate": trtMeans[i], 
                   "StdErr": stdErrSingle[i], 
                   "DF": dfSingle[i],
                   "CI_lo": CISingle[i][0], 
                   "CI_hi": CISingle[i][1],
                   "Cov2": ANOVA["IndividualTrt"]["cov2EachTrt"][trtStr]}, 
                   ignore_index=True)
# =============================================================================
# TODO generalize to more than 2 treatments
# =============================================================================
    ci.index = ["trt0", "trt1"]
    RRRC["ciAvgRdrEachTrt"] = ci
        
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
    List containing FOMs, ANOVA and RRRC, where 
    FOMs contains the treatment reader foms,
    TODO

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
    
    ANOVA = UtilORVarComponents(ds)
    
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
    
    FOMs = {"foms": foms, "trtMeans": trtMeans, "trtMeanDiffs": trtMeanDiffs}
    
    pass

# list(FOMs.keys())[0]
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



def StSignificanceTestingCadVsRad(ds, FOM = "wAfroc", alpha = 0.05):
    """
    Compares standalone CAD to average of radiologists interpreting the same 
    cases; standalone CAD means all the designer-level mark-rating pairs 
    generated by the CAD algorithm are available to the analyst, not just the 
    one or two marks per case displayed to the radiologist: the latter are 
    marks whose ratings exceed a pre-selected threshold.
        
    Parameters
    ----------
    ds : list
        dataset.
    FOM : str, optional
        The figure of merit: "wAfroc" or "Wilcoxon". The default is "wAfroc".
    alpha : float, optional
        The significance level of the test. The default is 0.05.

    Returns
    -------
    TODO.
    """
    pass


def DiffFomVarCov2(ds):
    J = len(ds[0][0,:,0,0])
    K = len(ds[0][0,0,:,0])
    dsCad = DfExtractDataset(ds, trts = [0], rdrs = [0])
    dsRad = DfExtractDataset(ds, trts = [0], rdrs = [1,2,3,4,5,6,7,8,9])

