#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 20 08:57:05 2022

@author: Dev
"""

import warnings
import sys
import pandas as pd
import numpy as np
from openpyxl import load_workbook

warnings.simplefilter("ignore")
filename = 'extdata/toyFiles/FROC/frocCr.xlsx'
wb = load_workbook(filename)
ws = wb['TRUTH']
data = ws.values
