#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 25 08:52:01 2022

@author: Dev
"""

def UtilFigureOfMerit(ds, FOM):
    """
    Parameters
    ----------
    FileName : ds
        JAFROC dataset object created by DfReadDataFile()

    FOM: str
        The figure of merit, i.e., measure of performance,
        default is "wAFROC", or "Wilcoxon"

    Returns
    -------
    A dataframe with I rows and J columns, corresponding to treatments and
    readers, respectively, containing the FOM values
    """
    NL = ds[0]
    LL = ds[1]
    perCase = ds[2]
    relWeights = ds[3]
    DataType = ds[4]
    
    