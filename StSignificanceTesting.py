#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 24 09:26:41 2022

@author: Dev
"""
from DfReadDataFile import DfReadDataFile
from UtilFigureOfMerit import UtilFigureOfMerit

def StSignificanceTesting(FileName, DataType="FROC",
                          analysisOption = "RRRC"):
    """
    Parameters
    ----------
    FileName : str
        JAFROC format Excel input file name

    DataType : str
        The type of data: "FROC" (default) or "ROC"

    analysisOption : str
        The desired generalization: RRRC" (default) 
        or "RRFC" or "FRRC"

    Returns
    -------
    significanceTesting object st

    """
    ds = DfReadDataFile(FileName)
    I = len(ds[0][:,0,0,0])
    J = len(ds[0][0,:,0,0])
    
    if J == 1:
        analysisOption = "FRRC" 
    elif I == 1: 
        analysisOption = "RRFC"
    pass

    foms = UtilFigureOfMerit(ds, "wAfroc")

    return foms


FileName = "extdata/JT.xlsx"
#ds = DfReadDataFile(FileName)
# val = UtilFigureOfMerit(ds, "wAfroc")
st = StSignificanceTesting(FileName)