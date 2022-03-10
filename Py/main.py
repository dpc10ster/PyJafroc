from DfReadDataFile import DfReadDataFile, DfFroc2Roc, DfExtractDataset, DfRatings2Dataset
from StSignificanceTesting import StSignificanceTesting, StSignificanceTestingCadVsRad
from UtilFigureOfMerit import UtilFigureOfMerit
from UtilFigureOfMerit import UtilLesionWeightsDistr
from UtilORVarComponents import testJackKnife, UtilPseudoValues, UtilORVarComponents
import numpy as np



#ds1 = DfFroc2Roc(ds)
# val = UtilFigureOfMerit(ds, "wAfroc")
# ds = StSignificanceTesting("extdata/JT.xlsx")
# relWeights = [0.2, 0.3, 0.5]
# relWeights = 0
# lesWghtDistr = UtilLesionWeightsDistr(3, relWeights)
#FileName = "extdata/toyFiles/FROC/frocCr.xlsx"
# ds = DfReadDataFile("extdata/JT.xlsx")
# pv = UtilPseudoValues(ds, FOM = "wAfroc")
# # varCom = UtilORVarComponents(ds)
# #fomMeans = UtilORVarComponents(ds)
# st = StSignificanceTesting(ds)
# ste = StSignificanceTesting(ds)
# fom = UtilFigureOfMerit(ds, FOM = "wAfroc")
# fom1 = UtilFigureOfMerit(ds1, FOM = "Wilcoxon")
# jkFomValuesds1 = testJackKnife(ds, FOM = "wAfroc")
# jkFomValuesds2 = testJackKnife(ds1, FOM = "Wilcoxon")
# jkFomValuesds3 = testJackKnife(ds1, FOM = "wAfroc")
# pv = UtilPseudoValues(ds, FOM = "wAfroc")
# ds = DfReadDataFile("extdata/JT.xlsx")




## test1
#ds = DfReadDataFile("extdata/JT.xlsx")
#st = StSignificanceTesting(ds)

## test2
# ds = DfReadDataFile("extdata/NicoRadRoc.xlsx", DataType="ROC")
# dse = DfExtractDataset(ds, rdrs = [0,1,2,3])
# Stats = StSignificanceTestingCadVsRad(dse, FOM = "Wilcoxon")

## test 3
# ds = DfReadDataFile("extdata/JT2Rdrs.xlsx")
# st = StSignificanceTesting(ds)

## test4
# ds = DfReadDataFile("extdata/NicoRadRoc.xlsx", DataType="ROC")
# Stats = StSignificanceTestingCadVsRad(ds, FOM = "Wilcoxon")

## test5 c interface to fom functions
# ds = DfReadDataFile("extdata/toyFiles/ROC/rocCr.xlsx", DataType="ROC")
# fom = UtilFigureOfMerit(ds, "Wilcoxon")


## test6 check c fom function with NicoRad dataset
#ds = DfReadDataFile("extdata/NicoRadRoc.xlsx", DataType="ROC")
#dse = DfExtractDataset(ds, rdrs = [0,1,2,3])
#Stats = StSignificanceTestingCadVsRad(ds, FOM = "Wilcoxon")


## test7 check c fom function with froc dataset
#ds = DfReadDataFile("extdata/Froc.xlsx")
#pv = UtilPseudoValues(ds, FOM = "wAfroc")
#dse = DfExtractDataset(ds, trts= [0], rdrs = [0,1,2,3])
#dse[0].flags['C_CONTIGUOUS'] # check if array is C-contiguous
#fom = UtilFigureOfMerit(dse, FOM = "wAfroc")
#st = StSignificanceTesting(ds)
#fom = UtilFigureOfMerit(ds, "wAfroc")


## test8 adding DfRatings2Dataset function
# NL = np.array([30, 19,  8,  2,  1])
# LL = np.array([5,  6,  5, 12, 22])
# ds = DfRatings2Dataset(NL, LL, InputIsCountsTable =True)
# fom1 = UtilFigureOfMerit(ds, FOM = "Wilcoxon")
# NL = np.array([1,2,3,2,1])
# LL = np.array([1,2,3,2,1,4,5])
# ds = DfRatings2Dataset(NL, LL, perCase = np.ones(7, dtype=int))
# fom2 = UtilFigureOfMerit(ds, FOM = "wAfroc")


## test9 after changes to DfRead.. function
#ds = DfReadDataFile("extdata/toyFiles/FROC/frocCr.xlsx")
#ds = DfReadDataFile("extdata/toyFiles/ROC/rocCr.xlsx", DataType="ROC")
#ds = DfReadDataFile('extdata/toyFiles/FROC/bad/frocCr-01.xlsx') # unordered TRUTH
#ds = DfReadDataFile('extdata/toyFiles/FROC/bad/frocCr-02.xlsx') # unordered TRUTH
#ds = DfReadDataFile('extdata/toyFiles/FROC/bad/frocCr-03.xlsx') # incorrect sheet names
#ds = DfReadDataFile('extdata/toyFiles/FROC/bad/frocCr-04.xlsx') # normal case in LL
#ds = DfReadDataFile('extdata/toyFiles/FROC/bad/frocCr-05.xlsx') # do: numeric format
#ds = DfReadDataFile('extdata/toyFiles/FROC/bad/frocCr2BlankRows.xlsx')
#ds = DfReadDataFile('extdata/toyFiles/FROC/bad/frocCrNonCharInReaderID.xlsx')
#ds = DfReadDataFile('extdata/toyFiles/FROC/bad/incorrectCaseIDsInLL.xlsx') #why missing?
#ds = DfReadDataFile('extdata/toyFiles/FROC/bad/incorrectCaseIDsInLL2.xlsx')
#ds = DfReadDataFile("extdata/toyFiles/FROC/bad/incoCaseIDsInTP.xlsx")
#ds = DfReadDataFile("extdata/JT.xlsx")
#ds = DfReadDataFile("extdata/Froc.xlsx")
#st = StSignificanceTesting(ds)


#ds = DfReadDataFile("extdata/toyFiles/FROC/frocCr.xlsx")
#pv = UtilPseudoValues(ds, FOM = "wAfroc")
#dse = DfExtractDataset(ds, trts= [0], rdrs = [0,1,2,3])


ds = DfReadDataFile("../Py/extdata/JT.xlsx")
stNow = StSignificanceTesting(ds, FOM = "wAfroc")


# ds = DfReadDataFile("extdata/JT.xlsx")
# foms = UtilFigureOfMerit(ds, "wAfroc1")
