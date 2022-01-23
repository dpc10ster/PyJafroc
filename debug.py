import warnings
import sys
import pandas as pd
import numpy as np
from openpyxl import load_workbook
warnings.simplefilter("ignore")

#FileName = "extdata/toyFiles/FROC/frocCr2.xlsx"
FileName = "extdata/Froc.xlsx"

wb = load_workbook(FileName)

ws = wb['TRUTH']
data = ws.values
columnNames = next(data)[0:]
dfTruth = pd.DataFrame(data, columns=columnNames)
# add TruthID column based on cases with 0 or > 0 lesions
dfTruth["TruthID"] = (dfTruth["LesionID"] > 0).astype(int)

dfTruth = dfTruth.sort_values(["TruthID", "CaseID"])
dfTruth['Weight'] = dfTruth['Weight'].astype(float, errors='raise')
# weightCol = dfTruth["Weight"]

AllCases = np.unique(dfTruth["CaseID"])
NormalCases = dfTruth.loc[dfTruth['LesionID'] == 0]["CaseID"]
K1 = len(NormalCases)
AbnormalCases = dfTruth.loc[dfTruth['LesionID'] == 1]["CaseID"]
K2 = len(AbnormalCases)
K = K1 + K2

x = pd.Series(dfTruth["CaseID"])
x = x.isin(AbnormalCases)
x = pd.Series(dfTruth["CaseID"][x])
x = x.value_counts()
perCase = x.sort_index().tolist()

maxLL = max(perCase)
relWeights = [1/maxLL] * maxLL

ws = wb['NL']
data = ws.values
columnNames = next(data)[0:]
dfNL = pd.DataFrame(data, columns=columnNames)

ws = wb['LL']
data = ws.values
columnNames = next(data)[0:]
dfLL = pd.DataFrame(data, columns=columnNames)

modalities = (dfLL["ModalityID"].append(dfNL["ModalityID"])).unique()
I = len(modalities)
readers = (dfLL["ReaderID"].append(dfNL["ReaderID"])).unique()
J = len(readers)
maxNL = dfNL.groupby(['ReaderID',
                      'ModalityID',
                      'CaseID']).transform(len).max()[0]

maxLL = max(perCase)

truthTableStr = np.full((I, J, K, max(maxNL,maxLL)+1), 0)
for indxCsId in range(len(dfTruth["CaseID"])):
    c = (AllCases == dfTruth["CaseID"][indxCsId])
    l = dfTruth["LesionID"][indxCsId]
    truthTableStr[:, :, c, l] = 1

NL = np.full((I, J, K, maxNL), -np.inf)

#for indxNl in range(14):
for indxNl in range(len(dfNL["ModalityID"])):
    i = (modalities == dfNL["ModalityID"][indxNl])
    j = (readers == dfNL["ReaderID"][indxNl])
    c = (AllCases == dfNL["CaseID"][indxNl])

    multipleMarks = ((dfNL["CaseID"] == dfNL["CaseID"][indxNl]) &
                  (dfNL["ModalityID"] == dfNL["ModalityID"][indxNl]) &
                  (dfNL["ReaderID"] == dfNL["ReaderID"][indxNl]))
    for l in range(sum(multipleMarks)):
        if NL[i, j, c, l] == -np.inf:
            NL[i, j, c, l] = dfNL["NLRating"][indxNl + l]
        if truthTableStr[i, j, c, l] == 0:
            truthTableStr[i, j, c, l] = 1

LL = np.full((I, J, K2, maxLL), -np.inf)
for indxLl in range(len(dfLL["ModalityID"])):
    i = (modalities == dfLL["ModalityID"][indxLl])
    j = (readers == dfLL["ReaderID"][indxLl])
    c = (AbnormalCases == dfLL["CaseID"][indxLl])

    matchCount = ((dfLL["CaseID"] == dfLL["CaseID"][indxLl]) &
                  (dfLL["ModalityID"] == dfLL["ModalityID"][indxLl]) &
                  (dfLL["ReaderID"] == dfLL["ReaderID"][indxLl]))
    for l in range(sum(matchCount)):
        if LL[i, j, c, l] == -np.inf:
            LL[i, j, c, l] = dfLL["LLRating"][indxLl + l]
        truthTableStr[i, j, np.append([False]*K1, c), l] = 1

    ds = [NL, LL, perCase, relWeights, "FROC"]
