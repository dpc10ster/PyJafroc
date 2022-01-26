#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 24 17:30:32 2022

@author: Dev
"""

from DfReadDataFile import *
from StSignificanceTesting import StSignificanceTesting
from UtilFigureOfMerit import UtilFigureOfMerit
from UtilFigureOfMerit import UtilLesionWeightsDistr



# ds = DfReadDataFile("extdata/toyFiles/FROC/frocCr.xlsx")
# ds = DfReadDataFile("extdata/Froc.xlsx")
ds = DfReadDataFile("extdata/JT.xlsx")
val = UtilFigureOfMerit(ds, "wAfroc")
# ds = StSignificanceTesting("extdata/JT.xlsx")

# relWeights = [0.2, 0.3, 0.5]
# relWeights = 0
# lesWghtDistr = UtilLesionWeightsDistr(3, relWeights)