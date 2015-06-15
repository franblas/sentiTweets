# -*- coding: utf-8 -*-
"""
Created on Mon Jun 15 17:45:23 2015

@author: Paco
"""

class Classifier(object):
    
    _table = ''   
    _score_classif = 0.0
    
    def __init__(self,data):
        self._table = data
    
    def _compare(self,pos,neg):
        if(pos>neg):
            return 4
        elif(neg>pos):
            return 0
        elif(pos==neg):
            return 2
        else:
            return 2
    
    # score = (pos,neg)  
    def process(self,tweets_score=[]):
        res = 0.0
        sen = [p for p in self._table['popularity']]
        for t,s in zip(tweets_score,sen):
            if self._compare(t[0],t[1])==s:
                res = res + 1.0
            else:
                pass
        self._score_classif =  (res / len(sen))*100    
        print 'Tweets detection success : '+str(int(self._score_classif))+' %'