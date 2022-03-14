import foms
import numpy as np
import pandas as pd
from DfReadDataFile import DfReadDataFile, DfExtractDataset
import sys



def UtilLesionWeightsDistr(maxLL, relWeights=0):
    """
    Parameters
    ----------
    maxLL : int
        The maximum number of lesions per case in the dataset

    relWeights: float
        The vector containing the relative weights of the lesions; The default
        is 0, meaning equal weights assigned to lesions

    Returns
    -------
    The lower triangular lesion weights distribution square matrix:
    """
    lesWghtDistr = np.zeros((maxLL, maxLL))
    if relWeights == 0:
        for i in range(maxLL):
            lesWghtDistr[i, 0:(i+1)] = 1./(i+1)
        pass
    else:
        relWeights = np.array(relWeights)
        for i in range(maxLL):
            lesWghtDistr[i, 0:(i+1)] = relWeights[0:(i+1)] / sum(relWeights[0:(i+1)])

    pass
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


def FigureOfMerit_ij(nl, ll, perCase, FOM):
    if FOM == "Wilcoxon":
        nl = nl[:,0]
        ll = ll[:,0]
        nl = np.where(nl == -np.inf, -1e7, nl) 
        ll = np.where(ll == -np.inf, -1e7, ll) 
        return foms.wilcoxon(nl,ll)
    elif FOM == "wAfroc":
        nl = np.where(nl == -np.inf, -1e7, nl) 
        ll = np.where(ll == -np.inf, -1e7, ll) 
        maxLL = len(ll[0][:])
        lesWghtDistr = UtilLesionWeightsDistr(maxLL)
        return foms.wAfroc(nl,ll,np.array(perCase),lesWghtDistr)
    elif FOM == "wAfroc1":
        nl = np.where(nl == -np.inf, -1e7, nl) 
        ll = np.where(ll == -np.inf, -1e7, ll) 
        maxLL = len(ll[0][:])
        lesWghtDistr = UtilLesionWeightsDistr(maxLL)
        return foms.wAfroc1(nl,ll,np.array(perCase),lesWghtDistr)
    else: 
        sys.exit("unsupported value of FOM")



def UtilFigureOfMerit(ds, FOM):
    """
    Parameters
    ----------
    FileName : list
        JAFROC dataset list object created by DfReadDataFile()

    FOM: str
        The figure of merit or measure of performance, the
        default is "wAFROC", "wAFROC1", or "Wilcoxon"

    Returns
    -------
    A dataframe with I rows and J columns, corresponding to treatments and
    readers, respectively, containing the FOM values
    """
    DataType = ds[4]

    if not FOM in ["wAfroc", "wAfroc1", "Wilcoxon"]:
        sys.exit('FOM NOT in ["wAfroc", "wAfroc1", "Wilcoxon"]')

    if (FOM != "Wilcoxon") & (DataType == "ROC"):
        sys.exit("ROC dataset requires FOM = 'Wilcoxon'")
    if (FOM not in ["wAfroc", "wAfroc1"]) & (DataType == "FROC"):
        sys.exit("FROC dataset requires FOM = 'wAfroc' or 'wAfroc1'")
        
    NL = ds[0]
    LL = ds[1]
    perCase = ds[2]
    I = len(NL[:, 0, 0, 0])
    J = len(NL[0, :, 0, 0])
    maxNL = len(NL[0, 0, 0, :])
    maxLL = len(LL[0, 0, 0, :])
    if (maxNL > 1) & (DataType != "FROC"):
        sys.exit("Only FROC data can have more than one NL per case")
    if (maxLL > 1) & (DataType != "FROC"):
        sys.exit("Only FROC data can have more than one lesion per case")

# =============================================================================
# TODO: control # of decimal places shown and add row and column names
# =============================================================================
    fom = np.full((I, J), 0.0)
    for i in range(I):
        for j in range(J):            
            fom[i, j] = FigureOfMerit_ij(NL[i,j,:,:], \
                                         LL[i,j,:,:], \
                                         perCase, \
                                         FOM)

    return fom

