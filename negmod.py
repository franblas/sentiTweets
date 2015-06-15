# -*- coding: utf-8 -*-
"""
Created on Mon Jun 15 16:18:04 2015

@author: Paco
"""

import pandas as pd

class NegMod(object):

    _txtfile = ''
    _txtfile2 = ''
    _table = '' 
    _table2 = ''    
    
    def __init__(self,txt='NegatingWordList.txt',txt2='BoosterWordList.txt'):
        self._txtfile = txt
        self._txtfile2 = txt2
        self._reader()
        
    def _reader(self):
        self._table = pd.read_table(self._txtfile,names=['neg'])
        self._table2 = pd.read_table(self._txtfile2,names=['boost','score'])
    
    def mod_multiply(self,precword):
        yo = self._table2[self._table2['boost'].str.contains(precword)]
        if(len(yo)!=0):
            return True
        else:
            return False
     
    def neg_it(self,precword):
        yo = self._table[self._table['neg'].str.contains(precword)]
        if(len(yo)!=0):
            return True
        else:
            return False
