#import warnings
import sys
import pandas as pd
from openpyxl import load_workbook
#warnings.simplefilter("ignore")


def myExit(sheetNames, expectedNames, msg):
    check = all(item in sheetNames for item in expectedNames)
    if not check:
        sys.exit(msg)


def DfReadDataFile(FileName):
    wb = load_workbook(FileName)
    ws = wb['TRUTH']
    data = ws.values
    columnNames = next(data)[0:]
    dfTruth = pd.DataFrame(data, columns=columnNames)
    dfTruth["TruthID"] = (dfTruth["LesionID"] > 0).astype(int)
    pass


FileName = "extdata/JT.xlsx"
DfReadDataFile(FileName)