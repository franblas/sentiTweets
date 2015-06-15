# -*- coding: utf-8 -*-
"""
Created on Mon Jun 15 14:34:40 2015

@author: Paco
"""

import pandas as pd

class SentiWordNetCorpusReader(object):

    _txtfile = ''
    _table = ''
    
    def __init__(self,txt):
        self._txtfile = txt
        self._reader()
    
    def _reader(self):
        try:
            self._table = pd.read_table(self._txtfile,names=['Pos','Id','PosScore','NegScore','SynsetTerms','Gloss'])
            print 'Success loading the Senti table'    
        except:
            print 'Error loading the Senti table'
    
    def senti_synset(self,sen):
        tok = sen.split('.')
        word = tok[0]
        typ = tok[1]
        num = tok[2]
        tmp = self._table[(self._table['SynsetTerms'].str.contains(word+'#'+str(num).replace('0',''))) & (self._table['Pos'].str.contains(typ))] 
        #print sen+' PoScore: '+str(tmp['PosScore'].values.sum())+' NegScore: '+str(tmp['NegScore'].values.sum()) 
        return (sen,tmp['PosScore'].values.sum(),tmp['NegScore'].values.sum())