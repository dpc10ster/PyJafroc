#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 27 16:14:20 2022

@author: Dev
"""

from DfReadDataFile import *
from UtilFigureOfMerit import UtilFigureOfMerit


def UtilPseudoValues (ds, FOM = "WAfroc"):
    NL = ds[0]
    LL = ds[1]
    maxNL = len(NL[0,0,0,:])
    maxLL = len(LL[0,0,0,:])
    I = len(NL[:,0,0,0])
    J = len(NL[0,:,0,0])
    K = len(NL[0,0,:,0])
    K2 = len(LL[0,0,:,0])
    K1 = K - K2
    perCase = ds[2]
    
    fom = UtilFigureOfMerit(ds)
    jkFomValues = np.full((I,J,K), 0.0)
    jkPseudoValues = np.full((I,J,K), 0.0)

    if FOM == "Wilcoxon":
        pass
    
    for i in range(I):
        for j in range(J):
            for k in range(K):
                if k < K1:
                    nlij_jk = pd.DataFrame(NL[i,j,:,:]).drop(k)
                    nlij_jk = np.array(nlij_jk).reshape(1,1,K-1,maxNL)
                    llij_jk = pd.DataFrame(LL[i,j,:,:])
                    llij_jk = np.array(llij_jk).reshape(1,1,K2,maxLL)
                    perCase_jk = perCase
                else:
                    nlij_jk = pd.DataFrame(NL[i,j,:,:]).drop(k)
                    nlij_jk = np.array(nlij_jk).reshape(1,1,K-1,maxNL)
                    llij_jk = pd.DataFrame(LL[i,j,:,:]).drop(k-K1)
                    llij_jk = np.array(llij_jk).reshape(1,1,K2-1,maxLL)
                    perCase_jk = perCase.drop(k-K1)
                    perCase_jk = pd.Series(list(perCase_jk))
                dsjk = [nlij_jk, llij_jk, perCase_jk, ds[3], ds[4]]
                jkFomValues[i, j, k] = UtilFigureOfMerit(dsjk)[0,0]
                jkPseudoValues[i, j, k]  = (fom[i, j] * K - jkFomValues[i, j, k] * (K-1))
                pass
    return [jkFomValues, jkPseudoValues]


def FOMijk2VarCov (resampleFOMijk):
        
    I = len(resampleFOMijk[:,0,0])
    J = len(resampleFOMijk[0,:,0])
    K = len(resampleFOMijk[0,0,:])

    covMatrix = np.full((I,I,J,J), 0.0)

    for i in range(I):
        for ip in range(I):
            for j in range(J):
                for jp in range(J):
                    covMatrix[i, ip, j, jp] = np.cov(resampleFOMijk[i, j, :], resampleFOMijk[ip, jp, :])[0,1]
    Var = 0.0
    count = 0
    I = len(covMatrix[:,0,0,0])
    J = len(covMatrix[0,0,:,0])
    for i in range(I):
        for j in range(J):
            Var = Var + covMatrix[i, i, j, j]
            count = count + 1
    if count > 0: 
        Var = Var/count
    else: Var = 0
  
    Cov1 = 0
    count = 0
    for i in range(I):
        for ip in range(I):
            for j in range(J):
               if ip != i:
                   Cov1 = Cov1 + covMatrix[i, ip, j, j]
                   count = count + 1
    if count > 0: 
        Cov1 = Cov1/count 
    else: 
        Cov1 = 0
  
    Cov2 = 0
    count = 0
    for i in range(I):
        for j in range(J):
            for jp in range(J):
                if j != jp:
                    Cov2 = Cov2 + covMatrix[i, i, j, jp]
                    count = count + 1
    if count > 0: 
        Cov2 = Cov2/count 
    else: 
        Cov2 = 0
  
    Cov3 = 0
    count = 0
    for i in range(I):
        for ip in range(I):
            if i != ip:
                for j in range(J):
                    for jp in range(J):
                        if j != jp:
                            Cov3 = Cov3 + covMatrix[i, ip, j, jp]
                            count = count + 1
    if count > 0: 
        Cov3 = Cov3/count 
    else: 
        Cov3 = 0
  
    Var *=  (K - 1)**2 /K  # see paper by Efron and Stein 
    Cov1 *= (K - 1)**2 /K
    Cov2  *= (K - 1)**2 /K
    Cov3 *= (K - 1)**2 /K

    pass

    return ([Var, Cov1, Cov2, Cov3])
  


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
    
    TRanova = pd.DataFrame({"SS": ssArray, "DF": dfArray, "MS": msArray})
    TRanova.index = ["T", "R", "TR"]
    
    resampleFOMijk = UtilPseudoValues(ds)[0]
    CovTemp = FOMijk2VarCov(resampleFOMijk)
    
    
# BEGIN    
# TODO later
# pending implementation of DfExtractDataset            
# single treatment msR_i 
# if J > 1:
#     msR_i = np.full(I, 0.0)
#     for i in range(I):
#         for j in range(J):
#             msR_i[i] += (foms[i,j] - fomsMeansEchMod[i]) ** 2
#         msR_i[i] /= (J-1)
#  else: msR_i[i] = 0.0    
# cov2EachTrt = vector(length = I)
# varEachTrt = vector(length = I)
# for (i in 1:I) {
#   dsi = DfExtractDataset(dataset, trts = i)
#   ret = OrVarCovMatrixFactorial(dsi, FOM, FPFValue, nBoots, covEstMethod, seed)
#   varEachTrt[i] = ret$Var
#   cov2EachTrt[i] = ret$Cov2
# }

# modID = as.vector(dataset$descriptions$modalityID)
# IndividualTrt = data.frame(DF = rep(J-1, I), 
#                             msREachTrt = msR_i, 
#                             varEachTrt = varEachTrt, 
#                             cov2EachTrt = cov2EachTrt, 
#                             row.names = paste0("trt", modID),
#                             stringsAsFactors = FALSE)    
# TODO later
# pending implementation of DfExtractDataset
# # single reader msT_j ###############################################################
# if (I > 1) {
#   msT_j = array(0, dim = J)
#   for (j in 1:J) {
#     for (i in 1:I) {
#       msT_j[j] = msT_j[j] + (mean(Foms[i, j]) -  mean(Foms[,j]))**2 
#     }
#     msT_j[j] = msT_j[j]/(I - 1)
#   }
# } else msT_j = NA

# varEachRdr = vector(length = J)
# cov1EachRdr = vector(length = J)
# for (j in 1:J) {
#   dsj = DfExtractDataset(dataset, rdrs = j)
#   ret = OrVarCovMatrixFactorial(dsj, FOM, FPFValue, nBoots, covEstMethod, seed)
#   varEachRdr[j] = ret$Var
#   cov1EachRdr[j] = ret$Cov1
# }

# rdrID = as.vector(dataset$descriptions$readerID)
# if (I > 1) {
#   IndividualRdr = data.frame(DF = rep(I-1, J), 
#                               msTEachRdr = msT_j, 
#                               varEachRdr = varEachRdr, 
#                               cov1EachRdr = cov1EachRdr, 
#                               row.names = paste0("rdr", rdrID),
#                               stringsAsFactors = FALSE)
# } else IndividualRdr = NA         
# END    
    return [fomsMeansEchRdr, fomsMeansEchMod]

#FileName = "extdata/JT.xlsx"
FileName = "extdata/toyFiles/FROC/frocCr.xlsx"
ds = DfReadDataFile(FileName)
pv = UtilPseudoValues(ds)
covMatrix = UtilORVarComponentsFactorial(ds)
#fomMeans = UtilORVarComponentsFactorial(ds)    