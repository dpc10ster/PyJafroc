import time
from DfReadDataFile import *
from UtilFigureOfMerit import UtilFigureOfMerit, FigureOfMerit_ij


def JackKnifeList(x, y, z, FOM):
    # x = NL; x1 = corresponding jackknife value
    # y = LL; y1 = corresponding jackknife value
    # z = perCase; z1 = corresponding jackknife value
    K = len(x)
    K2 = len(y)
    K1 = K - K2

    jkFomValues = [0] * K
    for k in range(K):
        if k < K1:
            if k == 0:  # first case is special
                x1 = x[1:][:]
            else:
                x1 = x[0:k][:] + x[(k+1):][:]
            y1 = y
            z1 = z
        else:
            if k == (K-1):  # last case is also special
                x1 = x[0:(K-1)][:]  # drop last abnormal case nl rationg
                y1 = y[0:(K2-1)][:]  # drop last abnormal case ll rating
                z1 = z[0:(K2-1)]
            else:
                x1 = x[0:k][:] + x[(k+1):][:]
                y1 = y[0:(k-K1)][:] + y[(k-K1+1):][:]
                z1 = z[0:(k-K1)] + z[(k-K1+1):]
        jkFomValues[k] = FigureOfMerit_ij(x1, y1, z1, FOM)

    return jkFomValues


def JackKnifeArr(x, y, z, FOM):
    # x = NL; x1 = corresponding jackknife value
    # y = LL; y1 = corresponding jackknife value
    # z = perCase; z1 = corresponding jackknife value
    K = len(x)
    K2 = len(y)
    K1 = K - K2
    z = np.array(z)  # otherwise np.delete (see below) fails

    jkFomValues = [0] * K
    for k in range(K):
        if k < K1:
            x1 = np.delete(x, k, axis=0)
            y1 = y
            z1 = z
        else:
            x1 = np.delete(x, k, axis=0)
            y1 = np.delete(y, k-K1, axis=0)
            z1 = np.delete(z, k-K1, axis=0)
        jkFomValues[k] = FigureOfMerit_ij(x1, y1, z1, FOM)

    return jkFomValues


def testJackKnife(ds, FOM):
    NL = ds[0]
    LL = ds[1]
    maxNL = len(NL[0, 0, 0, :])
    maxLL = len(LL[0, 0, 0, :])
    I = len(NL[:, 0, 0, 0])
    J = len(NL[0, :, 0, 0])
    K = len(NL[0, 0, :, 0])
    K2 = len(LL[0, 0, :, 0])
    K1 = K - K2
    perCase = ds[2]

# =============================================================================
# TODO: check that correct FOM is passed
# does it make a difference? r
# ran JT dataset with Wilcoxon with no error??
# =============================================================================
    jkFomValues = np.full((I, J, K), 0.0)
    #jkFomValues = [[[0 for k in range(K)] for j in range(J)] for i in range(I)]

    for i in range(I):
        for j in range(J):
            # Loop time is 2.6164 seconds using pure Python without drop method
            # JT dataset; using array indexing
            # Loop time is 1.7576 seconds using list indexing
            x = NL[i, j, :, :]
            y = LL[i, j, :, :]
            tic = time.perf_counter()
            # jkFomValues[i][j][:] = JackKnife(Listlist(x), \
            #                                 list(y), \
            #                                 list(perCase), \
            #                                 FOM)
            jkFomValues[i, j, :] = JackKnifeArr(x, y, perCase, FOM)
            toc = time.perf_counter()
            if (i == 0) & (j == 0):
                print(f"Loop time is {toc - tic:0.4f} seconds")
            pass

    return jkFomValues


def UtilPseudoValues(ds, FOM):

    NL = ds[0]
    LL = ds[1]
    maxNL = len(NL[0, 0, 0, :])
    maxLL = len(LL[0, 0, 0, :])
    I = len(NL[:, 0, 0, 0])
    J = len(NL[0, :, 0, 0])
    K = len(NL[0, 0, :, 0])
    K2 = len(LL[0, 0, :, 0])
    K1 = K - K2
    perCase = ds[2]

    fom = UtilFigureOfMerit(ds, FOM)

    jkFomValues = np.full((I, J, K), 0.0)
    jkPseudoValues = np.full((I, J, K), 0.0)
    # jkFomValues = [[[0 for k in range(K)] for j in range(J)] for i in range(I)]
    # kPseudoValues = [[[0 for k in range(K)] for j in range(J)] for i in range(I)]

    for i in range(I):
        for j in range(J):
            x = NL[i, j, :, :]
            y = LL[i, j, :, :]
            tic = time.perf_counter()
            #jkFomValues[i][j][:] = JackKnifeList(list(x), list(y), list(perCase), FOM)
            jkFomValues[i, j, :] = JackKnifeArr(x, y, perCase, FOM)
            toc = time.perf_counter()
            if (i == 0) & (j == 0):
                print(f"Loop time is {toc - tic:0.4f} seconds")
            # for k in range(K):
            #     jkPseudoValues[i][j][k]  = (fom.values[i, j] * K - jkFomValues[i][j][k] * (K-1))
            jkPseudoValues[i, j, :] = (
                fom.values[i, j] * K - jkFomValues[i, j, :] * (K-1))
            pass
    return [jkFomValues, jkPseudoValues]


def FOMijk2VarCov(resampleFOMijk):

    I = len(resampleFOMijk[:, 0, 0])
    J = len(resampleFOMijk[0, :, 0])
    K = len(resampleFOMijk[0, 0, :])

    covMatrix = np.full((I, I, J, J), 0.0)

    for i in range(I):
        for ip in range(I):
            for j in range(J):
                for jp in range(J):
                    covMatrix[i, ip, j, jp] = \
                        np.cov(resampleFOMijk[i, j, :],
                               resampleFOMijk[ip, jp, :])[0, 1]
    Var = 0.0
    count = 0
    I = len(covMatrix[:, 0, 0, 0])
    J = len(covMatrix[0, 0, :, 0])
    for i in range(I):
        for j in range(J):
            Var = Var + covMatrix[i, i, j, j]
            count = count + 1
    if count > 0:
        Var = Var/count
    else:
        Var = 0

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

    Var *= (K - 1)**2 / K  # see paper by Efron and Stein
    Cov1 *= (K - 1)**2 / K
    Cov2 *= (K - 1)**2 / K
    Cov3 *= (K - 1)**2 / K

    pass

    return ([Var, Cov1, Cov2, Cov3])


def UtilORVarComponents(ds, FOM="wAfroc"):
    """
    Parameters
    ----------
    ds : list
        JAFROC dataset list object created by DfReadDataFile()

    FOM: str
        The figure of merit or measure of performance, the
        default is "wAFROC", or "Wilcoxon"

    Returns
    -------
    TODO dictionary ANOVA

    """
    NL = ds[0]
    LL = ds[1]
    if not FOM in ["wAfroc", "Wilcoxon"]:
        sys.exit('FOM NOT in ["wAfroc", "Wilcoxon"]')

    I = len(NL[:, 0, 0, 0])
    J = len(NL[0, :, 0, 0])
    K = len(NL[0, 0, :, 0])

    foms = UtilFigureOfMerit(ds, FOM)
    fomsMeansEchRdr = foms.mean(axis=0)  # col means
    fomsMeansEchMod = foms.mean(axis=1)  # row means
    fomsMean = foms.mean().mean()  # mean over all values

    if I > 1:
        msT = 0.0
        for i in range(I):
            msT += (fomsMeansEchMod[i] - fomsMean) ** 2
        msT *= J/(I - 1)
    else:
        msT = 0

    if J > 1:
        msR = 0.0
        for j in range(J):
            msR += (fomsMeansEchRdr[j] - fomsMean) ** 2
        msR *= I / (J - 1)
    else:
        msR = 0

    if ((I > 1) & (J > 1)):
        msTR = 0.0
        for i in range(I):
            for j in range(J):
                msTR += (foms.values[i, j] - fomsMeansEchMod[i] -
                         fomsMeansEchRdr[j] + fomsMean) ** 2
        msTR /= ((J - 1) * (I - 1))
    else:
        msTR = 0

    msArray = [msT, msR, msTR]
    dfArray = [I - 1, J - 1, (I - 1) * (J - 1)]
    ssArray = [a * b for a, b in zip(msArray, dfArray)]

    TRAnova = pd.DataFrame({"SS": ssArray, "DF": dfArray, "MS": msArray})
    TRAnova.index = ["T", "R", "TR"]

    # single treatment msR_i
    if J > 1:
        msR_i = [0] * I
        for i in range(I):
            for j in range(J):
                msR_i[i] = msR_i[i] + \
                    (foms.values[i, j] - np.mean(foms.values[i, :])) ** 2
            msR_i[i] /= (J - 1)
    else:
        msR_i = 0

    varEachTrt = [0] * I
    cov2EachTrt = [0] * I
    for i in range(I):
        dsi = DfExtractDataset(ds, trts=[i], rdrs=[0, 1, 2])
        [resampleFOMijk, jkPseudoValues] = UtilPseudoValues(dsi)
        covMatrix = FOMijk2VarCov(resampleFOMijk)
        varEachTrt[i] = covMatrix[0]
        cov2EachTrt[i] = covMatrix[2]

    modID = ds[5]
    IndividualTrt = pd.DataFrame({"DF": [J-1] * I,
                                  "msREachTrt": msR_i,
                                  "varEachTrt": varEachTrt,
                                  "cov2EachTrt": cov2EachTrt})
    IndividualTrt.index = ["trt" + s for s in modID]

    # single reader msT_j
    if I > 1:
        msT_j = [0] * J
        for j in range(J):
            for i in range(I):
                msT_j[j] = msT_j[j] + \
                    (foms.values[i, j] - fomsMeansEchRdr[j]) ** 2
                msT_j[j] /= (I - 1)
    else:
        msT_j < - 0

    varEachRdr = [0] * J
    cov1EachRdr = [0] * J
    for j in range(J):
        dsj = DfExtractDataset(ds, trts=[0, 1], rdrs=[j])
        [resampleFOMijk, jkPseudoValues] = UtilPseudoValues(dsj)
        covMatrix = FOMijk2VarCov(resampleFOMijk)
        varEachRdr[j] = covMatrix[0]
        cov1EachRdr[j] = covMatrix[1]

    rdrID = ds[6]
    if I > 1:
        IndividualRdr = pd.DataFrame({"DF": [I-1] * J,
                                      "msTEachRdr": msT_j,
                                      "varEachRdr": varEachRdr,
                                      "cov1EachRdr": cov1EachRdr})
        IndividualRdr.index = ["rdr" + s for s in rdrID]
    else:
        IndividualRdr = 0

    [resampleFOMijk, jkPseudoValues] = UtilPseudoValues(ds)
    covMatrix = FOMijk2VarCov(resampleFOMijk)
    Var = covMatrix[0]
    Cov1 = covMatrix[1]
    Cov2 = covMatrix[2]
    Cov3 = covMatrix[3]

    if I > 1:
        VarTR = msTR - Var + Cov1 + max(Cov2 - Cov3, 0)
    else:
        VarTR = 0

    VarR = (msR - VarTR - Var + Cov2 - (I-1)*(Cov1 - Cov3))/I

    VarCom = pd.DataFrame({"Estimates": [VarR, VarTR, Var, Cov1, Cov2, Cov3],
                           "rhos": ["", "", "", Cov1/Var, Cov2/Var, Cov3/Var]})
    VarCom.index = ["VarR", "VarTR", "Var", "Cov1", "Cov2", "Cov3"]

# TODO later
# pending implementation of DfExtractDataset
# single treatment msR_i
# # single reader msT_j

    ANOVA = {"TRAnova": TRAnova,
             "VarCom": VarCom,
             "IndividualTrt": IndividualTrt,
             "IndividualRdr": IndividualRdr}

    return ANOVA
