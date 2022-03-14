import sys
import pandas as pd
from UtilFigureOfMerit import UtilFigureOfMerit, DfExtractDataset
from UtilORVarComponents import UtilORVarComponents, UtilPseudoValues, FOMijk2VarCov
import math
import numpy as np
from scipy.stats import f, t
import statistics




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
                            "MS": (TRAnova["MS"]["T"], msDen), \
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
    stdErr1T = [0] * I
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
        stdErr1T[i] = math.sqrt(msDenSingle[i]/J) # Eqn. 25
        CISingle[i][0] = trtMeans[i] - t.ppf(1 - alpha/2, dfSingle[i]) * stdErr1T[i] 
        CISingle[i][1] = trtMeans[i] + t.ppf(1 - alpha/2, dfSingle[i]) * stdErr1T[i] # Eqn. 25
        ci = ci.append({"Estimate": trtMeans[i], 
                   "StdErr": stdErr1T[i], 
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
    sys.exit("FRRC not yet implemented")
    pass



def ORSummaryRRFC(ds, FOMs, ANOVA, alpha, diffTRName):
    sys.exit("RRFC not yet implemented")
    pass



def StSignificanceTesting(ds, FOM = "wAfroc", analysisOption = "RRRC", alpha = 0.05):
    """
    Parameters
    ----------
    ds : list
        dataset object
        
    FOM: str
        The figure of merit, default "wAfroc" for FROC data, or "wAfroc1" 
        (for FROC dataset with mainly diseased cases) or "Wilcoxon", 
        for ROC dataset.

    analysisOption : str
        The desired generalization: random reader random case
        "RRRC" (default), random reader fixed case "RRFC" or 
        fixed reader random case "FRRC"
        
    alpha : float
        The significance level of the test, 0.05 (default)    

    Returns
    -------
    List containing FOMs, ANOVA and RRRC, where 
    FOMs contains the treatment reader foms,
    TODO

    """
    
    I = len(ds[0][:,0,0,0])
    J = len(ds[0][0,:,0,0])
    # https://www.tutorialsteacher.com/python/python-list-comprehension
    trtNames = ["trt" + s for s in ds[5]]
    rdrNames = ["rdr" + s for s in ds[6]]
    DataType = ds[4]
    if (DataType == "ROC") & (FOM != "Wilcoxon"):
        sys.exit("ROC dataset requires Wilcoxon FOM")    
    if (DataType == "FROC") & (FOM == "Wilcoxon"):
        sys.exit("FROC dataset cannot have Wilcoxon FOM")    
    if J == 1:
        analysisOption = "FRRC" 
    elif I == 1: 
        analysisOption = "RRFC"
    pass

    foms = UtilFigureOfMerit(ds, FOM)
    foms = pd.DataFrame(foms, index = trtNames, columns = rdrNames)
    fomsMeansEchMod = foms.mean(axis=1) # row means
    trtMeans = pd.DataFrame({"Estimate": fomsMeansEchMod}, index = trtNames)
    
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



# def MyVar(x):
#     avgx = np.mean(x)
#     var = 0.0
#     N = len(x)
#     for i in range(N):
#         var += (x[i] - avgx) ** 2
#     var /=  (N - 1)
#     return var
    
    

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
        The figure of merit: "wAfroc" (default) or "Wilcoxon". 
    alpha : float, optional
        The significance level of the test, 0.05 (default)

    Returns
    -------
    TODO
    Implements SingleModalityRRRC(dataset, FOM, alpha) in R-Code
    """
    
    J = len(ds[0][0,:,0,0])
    dsCad = DfExtractDataset(ds, trts = [0], rdrs = [0])
    dsRad = DfExtractDataset(ds, trts = [0], rdrs = list(range(1,J)))
    
    jkFomValuesCad = UtilPseudoValues(dsCad, FOM)[0]
    jkFomValuesRad = UtilPseudoValues(dsRad, FOM)[0]
    
    jkDiffFomValues = jkFomValuesRad - jkFomValuesCad
    varCov = FOMijk2VarCov(jkDiffFomValues)
    Var = varCov[0]
    Cov2 = varCov[2]
    thetajc = UtilFigureOfMerit(ds, FOM)
    Psijc = thetajc[0][list(range(1,J))] - thetajc[0][0]
    Cad = thetajc[0][0]
    avgRad = np.mean(thetajc[0][list(range(1,J))])
    avgPsijc = np.mean(Psijc)
    
    J1 = (J-1) # number of radiologists
    # numpy variance function is incorrect
    # https://stackoverflow.com/questions/11236951/output-values-differ-between-r-and-python#comment14763812_11236993
    x = thetajc[0][list(range(1,J))]
    #varRad = np.var(x) * J1/(J1-1) # uses incorrect definition
    #varRad = MyVar(x) # my implementation
    varRad = statistics.stdev(x)**2 # this uses correct definition of stdev
                       
    
    MSR = 0 # 1st un-numbered equation on page 607
    avgDiffFom = np.mean(Psijc)
    for j in range(J1):
        MSR += (Psijc[j] - avgDiffFom) ** 2
    MSR /= (J1 - 1)
    
    # Compared to equations in 2013 Hillis paper, in paragraph following Table I
    # OK; 10/14/19
    MSden1T = MSR + max(J1 * Cov2, 0) #  # 2nd un-numbered equation on page 607
    stdErr1T = math.sqrt(MSden1T/J1)
    ddf1T = MSden1T ** 2 / (MSR ** 2 / (J1 - 1))  # 3rd un-numbered equation on page 607
    TstatStar = avgDiffFom / np.sqrt(MSden1T/J1) # in-text equation on line 1 on page 607
    # BUT with theta0 = 0
    pval = 2 * (1 - t.cdf(abs(TstatStar), ddf1T))
    # Equation 25 on page 607
    ciDiffTrt_lo = avgPsijc - t.ppf(1 - alpha/2, ddf1T) * stdErr1T
    ciDiffTrt_hi = avgPsijc + t.ppf(1 - alpha/2, ddf1T) * stdErr1T
    
    RadMinusCadStats = pd.DataFrame({"Rad": [avgRad], \
                                "CAD": [Cad], \
                                "Rad-CAD": [np.mean(Psijc)], \
                                "VarRad": [varRad], \
                                "VarError": [Var], \
                                "Cov2": [Cov2], \
                                "MSden1T": [MSden1T], \
                                "stdErr1T": [stdErr1T], \
                                "ddf1T": [ddf1T], \
                                "Tstat": [TstatStar], \
                                "p val": [pval], \
                                "CI_lo": [ciDiffTrt_lo], \
                                "CI_hi": [ciDiffTrt_hi]})
            
    return RadMinusCadStats



