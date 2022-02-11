from DfReadDataFile import DfReadDataFile, DfFroc2Roc, DfExtractDataset
from StSignificanceTesting import StSignificanceTesting, StSignificanceTestingCadVsRad
from UtilFigureOfMerit import UtilFigureOfMerit
from UtilFigureOfMerit import UtilLesionWeightsDistr
from UtilORVarComponents import testJackKnife, UtilPseudoValues



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




# tests passed 2/10/22
# tests passed 2/10/22
# tests passed 2/10/22
## test1
#ds = DfReadDataFile("extdata/JT.xlsx")
#st = StSignificanceTesting(ds)


## test2
# ds = DfReadDataFile("extdata/NicoRadRoc.xlsx", DataType="ROC")
# dse = DfExtractDataset(ds, rdrs = [0,1,2,3])
# Stats = StSignificanceTestingCadVsRad(dse, FOM = "Wilcoxon")


## test 3
ds = DfReadDataFile("extdata/JT2Rdrs.xlsx")
st = StSignificanceTesting(ds)
