#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  2 14:15:41 2022

@author: Dev
"""

def myFunction(): 
    print ('The value of __name__ is ' + __name__)

def main(): 
    myFunction()
    if __name__ == '__main__':    main()


myFunction()