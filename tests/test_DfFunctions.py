import unittest
import pickle
import numpy.testing as nptesting
from Py.DfReadDataFile import DfReadDataFile
from Py.DfReadDataFile import DfExtractDataset
import os


class TestDfFunctions(unittest.TestCase):
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
            print("writing good values for extracted dataset")            
        else:
            dsGood = pickle.load(open( save_fn, "rb" ))
            for i in range(len(dsNow)):
                self.assertIsNone(nptesting.assert_array_equal(dsNow[i], dsGood[i]))

if __name__ == '__main__':
    unittest.main()


