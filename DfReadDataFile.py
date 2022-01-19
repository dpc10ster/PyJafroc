import warnings
import sys
import pandas as pd
import numpy as np
from openpyxl import load_workbook

warnings.simplefilter("ignore")


def DfReadDataFile(filename):
    """
    Parameters
    ----------
    filename : JAFROC format Excel input file

    Returns
    -------
    dataset object

    """

    wb = load_workbook(filename=filename)
    sheetnames = wb.sheetnames
    correctNames = ["NL", "LL", "TRUTH"]
    check = all(item in sheetnames for item in correctNames)
    if not check:
        sys.exit("Excel workbook is missing at least one of NL, LL or "
                 "TRUTH worksheets.")

    ws = wb['TRUTH']
    data = ws.values

# Get the first line in file as a header line
    columns = next(data)[0:]
    correctNames = ['CaseID', 'LesionID', 'Weight']
    check = all(item in columns for item in correctNames)
    if not check:
        sys.exit(("Excel workbook TRUTH sheet has missing or incorrect " 
            "required column names. These are the correct names: "
            " 'CaseID', 'LesionID', 'Weight'"))

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
    normalCases = df.loc[df['LesionID'] == 0]
    K1=len(normalCases)
    abnormalCases = df.loc[df['LesionID'] == 1]
    K2=len(abnormalCases)
    K = K1 + K2
    
    
    
    return(df)
