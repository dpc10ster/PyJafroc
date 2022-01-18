import warnings
import sys
import pandas as pd
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
    requiredNames = ["NL", "LL", "TRUTH"]
    check = all(item in sheetnames for item in requiredNames)
    if not check:
        sys.exit("Excel workbook is missing at least one of NL, LL or "
                 "TRUTH worksheets.")

    ws = wb['TRUTH']
    data = ws.values

# Get the first line in file as a header line
    columns = next(data)[0:]

# Create a DataFrame based on the second and subsequent lines of data
    df = pd.DataFrame(data, columns=columns)
    # df.sort_values(by=[""])
    return(df)
