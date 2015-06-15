# -*- coding: utf-8 -*-
"""
Created on Mon Jun 15 17:15:43 2015

@author: Paco
"""

from emot import Emot
from sentimentanalysis import data, preProcessed, scores

# get Emot scores
em = Emot()
emot_score = list()
for d in data['text']:
    emot_score.append(em.emot_it(d))

# Pre processed tweets    
preprodata = preProcessed(data)    
    
# Get scores    
tweets_score = scores(preprodata,emot_score)    
    