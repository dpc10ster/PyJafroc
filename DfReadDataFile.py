import warnings
import sys
import pandas as pd
import numpy as np
from openpyxl import load_workbook

warnings.simplefilter("ignore")


def myExit(sheetNames, expectedNames, msg):
    check = all(item in sheetNames for item in expectedNames)
    if not check:
        sys.exit(msg)


def testDfReadDataFile(filename):
    DfReadDataFile(filename)


def DfCheck(filename):

# =============================================================================
# Tested with 1 good and 2 bad files
# filename = 'extdata/toyFiles/FROC/frocCr.xlsx'
# filename = 'extdata/toyFiles/FROC/bad/frocCr-01.xlsx' unordered TRUTH
# filename = 'extdata/toyFiles/FROC/bad/frocCr-02.xlsx' unordered TRUTH
# filename = 'extdata/toyFiles/FROC/bad/frocCr-03.xlsx' unexpected case
# filename = 'extdata/toyFiles/FROC/bad/frocCr-04.xlsx' normal case in LL
# filename = 'extdata/toyFiles/FROC/bad/frocCr-05.xlsx' do: numeric format
# filename = 'extdata/toyFiles/FROC/bad/frocCr2BlankRows.xlsx'
# filename = 'extdata/toyFiles/FROC/bad/frocCrNonCharInReaderID.xlsx'
# filename = 'extdata/toyFiles/FROC/bad/incorrectCaseIDsInTP.xlsx' why missing?
# filename = 'extdata/toyFiles/FROC/bad/incorrectCaseIDsInTP2.xlsx'
# filename = "extdata/toyFiles/FROC/bad/incoCaseIDsInTP.xlsx"
# fn = ['extdata/toyFiles/FROC/frocCr.xlsx',
# 'extdata/toyFiles/FROC/bad/frocCr-01.xlsx',
# 'extdata/toyFiles/FROC/bad/frocCr-02.xlsx',
# 'extdata/toyFiles/FROC/bad/frocCr-03.xlsx',
# 'extdata/toyFiles/FROC/bad/frocCr-04.xlsx']
# =============================================================================

    wb = load_workbook(filename)
    sheetNames = wb.sheetnames
    expectedNames = ["NL", "LL", "TRUTH"]
    msg = ("Excel workbook has missing or incorrectly named sheets. "
           "These are the correct names: ") + ", ".join(expectedNames)
    myExit(sheetNames, expectedNames, msg)

    ws = wb['TRUTH']
    data = ws.values
    columnNames = next(data)[0:]

    expectedNames = ['CaseID', 'LesionID', 'Weight']
    msg = ("Excel worksheet TRUTH has missing or incorrect "
           "required column names. "
           "These are the correct names: ") + ", ".join(expectedNames)
    myExit(columnNames, expectedNames, msg)

    dfTruth = pd.DataFrame(data, columns=columnNames)
    # Check for missing cells
    if dfTruth.isnull().values.any():
        sys.exit("Missing cell(s) encountered in TRUTH worksheet")

    ws = wb['NL']
    data = ws.values
    columnNames = next(data)[0:]
    # Extract the data minus the column names
    dfNL = pd.DataFrame(data, columns=columnNames)

    expectedNames = ['ReaderID', 'ModalityID', 'CaseID', 'NLRating']
    msg = ("Excel worksheet NL has missing or incorrect "
           "required column names. "
           "These are the correct names: ") + ", ".join(expectedNames)
        
    if dfNL.isnull().values.any():
        sys.exit("Missing cell(s) encountered in NL worksheet")

    ws = wb['LL']
    data = ws.values
    columnNames = next(data)[0:]
    # Extract the data minus the column names
    dfLL = pd.DataFrame(data, columns=columnNames)
    

    if dfLL.isnull().values.any():
        sys.exit("Missing cell(s) encountered in LL worksheet")


def DfReadDataFile(filename):
    """
    Parameters
    ----------
    filename : JAFROC format Excel input file

    Returns
    -------
    dataset object

    """
# =============================================================================
# Check the Excel file
# Load the Excel file
# =============================================================================
    DfCheck(filename)
    wb = load_workbook(filename)

# =============================================================================
# Load the TRUTH worksheet
# Exract the columns
# =============================================================================
    ws = wb['TRUTH']
    data = ws.values
    columnNames = next(data)[0:]
    # Extract the data minus the column names
    dfTruth = pd.DataFrame(data, columns=columnNames)


    dfTruth["TruthID"] = (dfTruth["LesionID"] > 0).astype(int)
    # sort on "TruthID" & "CaseID" fields, putting non-diseased cases first
    dfTruth = dfTruth.sort_values(["TruthID", "CaseID"])
    truthCaseIDCol = dfTruth["CaseID"]
    truthLesionIDCol = dfTruth["LesionID"]
    dfTruth['Weight'] = dfTruth['Weight'].astype(float, errors = 'raise')
    weightCol = dfTruth["Weight"]
    L = len(truthCaseIDCol)
    allCases = np.unique(np.array(dfTruth["CaseID"]))
    normalCases = dfTruth.loc[dfTruth['LesionID'] == 0]["CaseID"]
    K1 = len(normalCases)
    abnormalCases = dfTruth.loc[dfTruth['LesionID'] == 1]["CaseID"]
    K2 = len(abnormalCases)
    K = K1 + K2

    # calculate lesion perCase
    x = pd.Series(dfTruth["CaseID"])
    x = x.isin(abnormalCases)
    x = pd.Series(dfTruth["CaseID"][x])
    x = x.value_counts()
    perCase = x.sort_index()

    maxLL = max(perCase)
    relWeights = [1/maxLL] * maxLL
 
# =============================================================================
# Load the NL sheet
# Exract the columns
# =============================================================================
    ws = wb['NL']
    data = ws.values
    columnNames = next(data)[0:]
    # Extract the data minus the column names
    dfNL = pd.DataFrame(data, columns=columnNames)

    nlReaderIDCol = dfNL["ReaderID"]
    nlModalityIDCol = dfNL["ModalityID"]
    nlCaseIDCol = dfNL["CaseID"]
    nlRatingsCol = dfNL["NLRating"]

# =============================================================================
# Load the LL sheet
# Exract the columns
# =============================================================================
    ws = wb['LL']
    data = ws.values
    columnNames = next(data)[0:]
    # Extract the data minus the column names
    dfLL = pd.DataFrame(data, columns=columnNames)
    

    llReaderIDCol = dfLL["ReaderID"]
    llModalityIDCol = dfLL["ModalityID"]
    llCaseIDCol = dfLL["CaseID"]
    llLesionIDCol = dfLL["LesionID"]
    llRatingsCol = dfLL["LLRating"]
       
    modalities = (llModalityIDCol.append(nlModalityIDCol)).unique()
    I = len(modalities)

    readers = (llReaderIDCol.append(nlReaderIDCol)).unique()
    J = len(readers)
    
    maxNL = dfNL.groupby(['ReaderID',
                          'ModalityID', 
                          'CaseID']).transform(len).max()[0]
    
    maxLL = max(perCase)
    
    NegInf = -2000
    NL = np.full((I,J,K,maxNL), NegInf)
    LL = np.full((I,J,K,maxLL), NegInf)
    
    return(dfTruth)


