import unittest
import pickle
import numpy.testing as nptesting
from DfReadDataFile import DfReadDataFile, DfExtractDataset
from UtilFigureOfMerit import UtilFigureOfMerit
from StSignificanceTesting import StSignificanceTesting
import os


class tests(unittest.TestCase):
    def test_df_read(self):
        fileName = "../Py/extdata/toyFiles/FROC/frocCr.xlsx"
        fn = os.path.splitext(os.path.basename(fileName))[0]
        save_fn = "goodValues/DfRead/ds_" + fn + ".p"
        dsNow = DfReadDataFile(fileName) 
        if not os.path.exists(save_fn):
            pickle.dump( dsNow, open( save_fn, "wb" ) )
            print("writing good value ds file for frocCr.xlsx")            
        else:
            dsGood = pickle.load(open( save_fn, "rb" ))
            for i in range(len(dsNow)):
# https://stackoverflow.com/questions/3302949/best-way-to-assert-for-numpy-array-equality
                self.assertIsNone(nptesting.assert_array_equal(dsNow[i], dsGood[i]))

    def test_df_extract(self):
        fileName = "../Py/extdata/Froc.xlsx"
        fn = os.path.splitext(os.path.basename(fileName))[0]
        save_fn = "goodValues/DfExtract/ds_" + fn + ".p"
        ds = DfReadDataFile(fileName)
        dsNow = DfExtractDataset(ds, trts= [0], rdrs = [0,1,2,3]) 
        if not os.path.exists(save_fn):
            pickle.dump( dsNow, open( save_fn, "wb" ) )
            print("writing goodValues for extracted dataset")            
        else:
            dsGood = pickle.load(open( save_fn, "rb" ))
            for i in range(len(dsNow)):
                self.assertIsNone(nptesting.assert_array_equal(dsNow[i], dsGood[i]))

    def test_util_fom(self):
        fileName = "../Py/extdata/Froc.xlsx"
        fn = os.path.splitext(os.path.basename(fileName))[0]
        save_fn = "goodValues/foms/ds_" + fn + ".p"
        ds = DfReadDataFile(fileName)
        fomNow = UtilFigureOfMerit(ds, FOM = "wAfroc") 
        if not os.path.exists(save_fn):
            pickle.dump( fomNow, open( save_fn, "wb" ) )
            print("writing ggoodValues for figures of merit")            
        else:
            fomGood = pickle.load(open( save_fn, "rb" ))
            for i in range(len(fomNow)):
                self.assertIsNone(nptesting.assert_array_equal(fomNow[i], fomGood[i]))

    def test_st_significance(self):
        fileName = "../Py/extdata/JT.xlsx"
        fn = os.path.splitext(os.path.basename(fileName))[0]
        save_fn = "goodValues/st/ds_" + fn + ".p"
        ds = DfReadDataFile(fileName)
        stNow = StSignificanceTesting(ds, FOM = "wAfroc") 
        if not os.path.exists(save_fn):
            pickle.dump( stNow, open( save_fn, "wb" ) )
            print("writing goodValues for st_significance")            
        else:
            stGood = pickle.load(open( save_fn, "rb" ))
            strtests = ["foms", "trtMeans", "trtMeanDiffs"]
            for i in range(len(strtests)):
                self.assertIsNone(nptesting.assert_array_equal(\
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


