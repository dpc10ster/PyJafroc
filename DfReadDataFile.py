import warnings
import sys
import pandas as pd
import numpy as np
from openpyxl import load_workbook

warnings.simplefilter("ignore")


def myExit(testStr, correctNames, msg):
    check = all(item in testStr for item in correctNames)
    if not check:
        sys.exit(msg)


def DfReadDataFile(filename):
    """
    Parameters
    ----------
    filename : JAFROC format Excel input file

    Returns
    -------
    dataset object

    """

    wb = load_workbook(filename)
    testStr = wb.sheetnames
    correctNames=["NL","LL","TRUTH"]
    msg = "Excel workbook is missing at least one of NL, LL or "
    "TRUTH worksheets."
    myExit(testStr,correctNames,msg)

    ws = wb['TRUTH']
    data = ws.values

# Get the first line in file as a header line
    columns = next(data)[0:]
    correctNames = ['CaseID', 'LesionID', 'Weight']
    msg = ("Excel workbook TRUTH sheet has missing or incorrect "
        "required column names. These are the correct names: "
        " 'CaseID', 'LesionID', 'Weight'")
    myExit(columns,correctNames,msg)

# Create a DataFrame based on the second and subsequent lines of data
    df = pd.DataFrame(data, columns=columns)
    
    if df.isnull().values.any():
        sys.exit("Missing cell(s) encountered in TRUTH worksheet")
        
    # sort on LesionID field, putting non-diseased cases first
    df["TruthID"]=(df["LesionID"] > 0).astype(int)
    caseIDCol = df["CaseID"]
    lesionIDCol = df["LesionID"]
    weightCol = df["Weight"]
    L=len(caseIDCol)
    allCases = np.unique(np.array(df["CaseID"]))
    normalCases = df.loc[df['LesionID'] == 0]["CaseID"]
    K1=len(normalCases)
    abnormalCases = df.loc[df['LesionID'] == 1]["CaseID"]
    K2=len(abnormalCases)
    K = K1 + K2
    
    x=pd.Series(df["CaseID"])
    x=x.isin(abnormalCases)
    x=pd.Series(df["CaseID"][x])
    x=x.value_counts()
    perCase=x.sort_index()
    
    
    return(df)
