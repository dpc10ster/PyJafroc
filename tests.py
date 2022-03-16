import unittest
import pickle
import numpy as np 
import numpy.testing as nptesting
from DfReadDataFile import DfReadDataFile, DfExtractDataset, DfFroc2Roc
from UtilFigureOfMerit import UtilFigureOfMerit
from StSignificanceTesting import StSignificanceTesting, StSignificanceTestingCadVsRad
import os


class tests(unittest.TestCase):
    def test_df_read(self):
        fileName = "extdata/toyFiles/FROC/frocCr.xlsx"
        dsNow = DfReadDataFile(fileName) 
        fn = os.path.splitext(os.path.basename(fileName))[0]
        save_fn = "goodValues/DfRead/ds_" + fn + ".p"
        if not os.path.exists(save_fn):
            pickle.dump( dsNow, open( save_fn, "wb" ) )
            print("writing good values for test_df_read")            
        else:
            dsGood = pickle.load(open( save_fn, "rb" ))
            for i in range(len(dsNow)):
                self.assertIsNone(nptesting.assert_array_equal(dsNow[i], dsGood[i]))

    def test_df_extract(self):
        fileName = "extdata/Froc.xlsx"
        ds = DfReadDataFile(fileName)
        dsNow = DfExtractDataset(ds, trts= [0], rdrs = [0,1,2,3]) 
        fn = os.path.splitext(os.path.basename(fileName))[0]
        save_fn = "goodValues/DfExtract/ds_" + fn + ".p"
        if not os.path.exists(save_fn):
            pickle.dump( dsNow, open( save_fn, "wb" ) )
            print("writing goodValues for test_df_extract")            
        else:
            dsGood = pickle.load(open( save_fn, "rb" ))
            for i in range(len(dsNow)):
                self.assertIsNone(nptesting.assert_array_equal(dsNow[i], dsGood[i]))

    def test_df_froc_roc(self):
        fileName = "extdata/JT.xlsx"
        ds = DfReadDataFile(fileName)
        dsNow = DfFroc2Roc(ds)
        fn = os.path.splitext(os.path.basename(fileName))[0]
        save_fn = "goodValues/DF2Roc/ds_" + fn + ".p"
        if not os.path.exists(save_fn):
            pickle.dump( dsNow, open( save_fn, "wb" ) )
            print("writing goodValues for test_df_froc_roc")            
        else:
            dsGood = pickle.load(open( save_fn, "rb" ))
            for i in range(len(dsNow)):
                self.assertIsNone(nptesting.assert_array_equal(dsNow[i], dsGood[i]))

    def test_util_fom_Wilcoxon(self):
        # see JT_R_Py_Foms.xlsx for cross check with R code
        fileName = "extdata/JT.xlsx"
        fn = os.path.splitext(os.path.basename(fileName))[0]
        save_fn = "goodValues/foms/Wilcoxon_" + fn + ".p"
        ds = DfReadDataFile(fileName)
        ds = DfFroc2Roc(ds)
        fomNow = UtilFigureOfMerit(ds, FOM = "Wilcoxon") 
        if not os.path.exists(save_fn):
            pickle.dump( fomNow, open( save_fn, "wb" ) )
            print("writing goodValues for test_util_fom_Wilcoxon")            
        else:
            fomGood = pickle.load(open( save_fn, "rb" ))
            for i in range(len(fomNow)):
                self.assertIsNone(nptesting.assert_array_equal(fomNow[i], fomGood[i]))

    def test_util_fom_wAfroc(self):
        # see JT_R_Py_Foms.xlsx for cross check with R code
        fileName = "extdata/JT.xlsx"
        fn = os.path.splitext(os.path.basename(fileName))[0]
        save_fn = "goodValues/foms/wAfroc_" + fn + ".p"
        ds = DfReadDataFile(fileName)
        fomNow = UtilFigureOfMerit(ds, FOM = "wAfroc") 
        if not os.path.exists(save_fn):
            pickle.dump( fomNow, open( save_fn, "wb" ) )
            print("writing goodValues for test_util_fom_wAfroc")            
        else:
            fomGood = pickle.load(open( save_fn, "rb" ))
            for i in range(len(fomNow)):
                self.assertIsNone(nptesting.assert_array_equal(fomNow[i], fomGood[i]))

    def test_util_fom_wAfroc1(self):
        # see JT_R_Py_Foms.xlsx for cross check with R code
        fileName = "extdata/JT.xlsx"
        fn = os.path.splitext(os.path.basename(fileName))[0]
        save_fn = "goodValues/foms/wAfroc1_" + fn + ".p"
        ds = DfReadDataFile(fileName)
        fomNow = UtilFigureOfMerit(ds, FOM = "wAfroc1") 
        if not os.path.exists(save_fn):
            pickle.dump( fomNow, open( save_fn, "wb" ) )
            print("writing goodValues for test_util_fom_wAfroc1")            
        else:
            fomGood = pickle.load(open( save_fn, "rb" ))
            for i in range(len(fomNow)):
                self.assertIsNone(nptesting.assert_array_equal(fomNow[i], fomGood[i]))

    def test_st_significance_cad_roc(self):
        fileName = "extdata/NicoRadRoc.xlsx"
        fn = os.path.splitext(os.path.basename(fileName))[0]
        save_fn = "goodValues/stCad/Wilcoxon_" + fn + ".p"
        ds = DfReadDataFile(fileName)
        stNow = StSignificanceTestingCadVsRad(ds, FOM = "Wilcoxon") 
        if not os.path.exists(save_fn):
            pickle.dump( stNow, open( save_fn, "wb" ) )
            print("writing goodValues for test_st_significance_cad_roc")            
        else:
            stGood = pickle.load(open( save_fn, "rb" ))
            x = np.array(stNow)[0,:]
            y = np.array(stGood)[0,:]
            self.assertIsNone(nptesting.assert_allclose(x, y))
                
    def test_st_significance_cad_froc(self):
        fileName = "extdata/CadFrocData.xlsx"
        fn = os.path.splitext(os.path.basename(fileName))[0]
        save_fn = "goodValues/stCad/wAfroc_" + fn + ".p"
        ds = DfReadDataFile(fileName, DataType = "FROC")
        stNow = StSignificanceTestingCadVsRad(ds, FOM = "wAfroc") 
        if not os.path.exists(save_fn):
            pickle.dump( stNow, open( save_fn, "wb" ) )
            print("writing goodValues for test_st_significance_cad_froc")            
        else:
            stGood = pickle.load(open( save_fn, "rb" ))
            x = np.array(stNow)[0,:]
            y = np.array(stGood)[0,:]
            self.assertIsNone(nptesting.assert_allclose(x, y))
                
    def test_st_significance_test_equality_foms(self):
        ds = DfReadDataFile("extdata/CadFrocData.xlsx", DataType = "FROC")
        ds1 = DfFroc2Roc(ds)
        fom1 = UtilFigureOfMerit(ds1, FOM = "Wilcoxon")
        ds = DfReadDataFile("extdata/NicoRadRoc.xlsx")
        fom = UtilFigureOfMerit(ds, FOM = "Wilcoxon")
        self.assertIsNone(nptesting.assert_allclose(fom1, fom))
                
    def test_st_significance(self):
        fileName = "extdata/JT.xlsx"
        fn = os.path.splitext(os.path.basename(fileName))[0]
        save_fn = "goodValues/st/ds_" + fn + ".p"
        ds = DfReadDataFile(fileName)
        stNow = StSignificanceTesting(ds, FOM = "wAfroc") 
        if not os.path.exists(save_fn):
            pickle.dump( stNow, open( save_fn, "wb" ) )
            print("writing goodValues for test_st_significance")            
        else:
            stGood = pickle.load(open( save_fn, "rb" ))
            strtests = ["foms", "trtMeans", "trtMeanDiffs"]
            for i in range(len(strtests)):
                self.assertIsNone(nptesting.assert_allclose(\
                                                                stNow[0][strtests[i]], \
                                                                stGood[0][strtests[i]]))
            #strtests = ["TRAnova", "VarCom", "IndividualTrt", "IndividualRdr"]
            strtests = ["TRAnova", "IndividualTrt", "IndividualRdr"]
            for i in range(len(strtests)):
                self.assertIsNone(nptesting.assert_allclose(\
                                                                stNow[1][strtests[i]], \
                                                                stGood[1][strtests[i]]))
# core/numeric.py", line 2362, in isclose
#     xfin = isfinite(x)
# TypeError: ufunc 'isfinite' not supported for the input types, 
# and the inputs could not be safely coerced to any supported types 
# according to the casting rule ''safe''                    
# blank cells in 2nd column creates above problem; so I just compare the first column containing 
# var and cov1, cov2, cov3
            self.assertIsNone(nptesting.assert_allclose(\
                                                            stNow[1]["VarCom"]["Estimates"], \
                                                            stGood[1]["VarCom"]["Estimates"]))
                
            strtests = ["FTests", "ciDiffTrt", "ciAvgRdrEachTrt"]
            for i in range(len(strtests)):
                self.assertIsNone(nptesting.assert_allclose(\
                                                                stNow[2][strtests[i]], \
                                                                stGood[2][strtests[i]]))


if __name__ == '__main__':
    unittest.main()


