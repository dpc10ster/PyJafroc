from DfReadDataFile import DfReadDataFile, DfFroc2Roc, DfExtractDataset
from StSignificanceTesting import StSignificanceTesting, StSignificanceTestingCadVsRad
from UtilFigureOfMerit import UtilFigureOfMerit
from UtilFigureOfMerit import UtilLesionWeightsDistr
from UtilORVarComponents import testJackKnife, UtilPseudoValues, UtilORVarComponents



#ds = DfReadDataFile("extdata/toyFiles/FROC/frocCr.xlsx")
#ds = DfReadDataFile("extdata/toyFiles/ROC/rocCr.xlsx")
#ds = DfReadDataFile("extdata/Froc.xlsx")
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
# FileName = "extdata/JT.xlsx"
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
ds = DfReadDataFile("extdata/Froc.xlsx")
#pv = UtilPseudoValues(ds, FOM = "wAfroc")
dse = DfExtractDataset(ds, trts= [0], rdrs = [0,1,2,3])
#dse[0].flags['C_CONTIGUOUS'] # check if array is C-contiguous
fom = UtilFigureOfMerit(dse, FOM = "wAfroc")
#varCom = UtilORVarComponents(ds)
#st = StSignificanceTesting(ds)
#fom = UtilFigureOfMerit(ds, "wAfroc")