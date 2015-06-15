# -*- coding: utf-8 -*-
"""
Created on Mon Jun 15 16:50:56 2015

@author: Paco
"""

import pandas as pd

class Emot(object):

    _txtfile = ''
    _table = ''
    
    def __init__(self,txt='EmoticonLookupTable.txt'):
        self._txtfile = txt
        self._reader()        
        
        
    def _reader(self):
        self._table = pd.read_table(self._txtfile,names=['emot','score'])

    def _escape(self,em):
        res = em
        res = res.replace('^','\^')
        res = res.replace('*','\*')
        res = res.replace('(','\(')
        res = res.replace(')','\)')
        res = res.replace('/','\/')
        return res
    
    def emot_it(self,tweet):
        posres = 0
        negres = 0
        for em in self._table['emot']:
            if em in tweet:
                emem = self._escape(em)
                tmp = self._table[self._table['emot'].str.contains(emem)]['score'].values[0]
                if tmp == 1:
                    posres = posres + 1
                elif tmp == -1:
                    negres = negres + 1
                else:
                    pass
        return posres,negres        
     