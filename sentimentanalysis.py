# -*- coding: utf-8 -*-
"""
Created on Fri Jun 05 09:09:09 2015

@author: Paco
"""

import pandas as pd
import nltk as nltk
from nltk.corpus import wordnet as wn
from sentiwordnet import SentiWordNetCorpusReader
from negmod import NegMod

#data import
data = pd.read_csv('testdata.manual.2009.06.14.csv',names=['popularity','id','date','request','user','text'])
dicoslang = pd.read_table('SlangLookupTable.txt',names=['abrev','expr'])

'''
Remove ponctuation from a text
'''
def remove_ponctuation(text):
    temp = text
    ponctuation = [',',';','?','!',':','.','^','*','-','(',')','/','=','_','[',']','{','}','"']
    for p in ponctuation:
        temp = temp.replace(p,'') 
    temp = temp.replace("'",'')    
    return temp    

def is_url(text):
    if text.startswith('http'):
        return True
    else:
        return False

def is_hashtag(text):
    if text.startswith('#'):
        return True
    else:
        return False

def is_tweeter_user(text):
    if text.startswith('@'):
        return True
    else:
        return False

def is_retweet(text):
    if text.lower() == 'rt':
        return True
    else:
        return False

def is_empty(text):
    if text == '':
        return True
    else:
        return False    

def is_special_chara(text):
    if text.startswith('&') or text.startswith('$'):
        return True
    else:
        return False

def replace_abrev(text,tokens):
    temp = dicoslang['abrev'].tolist()
    for ab in temp:
        if text.lower() == ab:
            exp = dicoslang['expr'][temp.index(ab)]
            exp = exp.replace("'",' ')
            arr = exp.split(' ')
            indice = tokens.index(text)
            for a in reversed(arr):
                tokens.insert(indice+1,a)
            tokens.pop(indice)    
    return tokens            
    
def drop_stuff(tokens):
    temp = tokens
    for t in tokens:
        t.replace('&amp','')
        if (is_retweet(t) or is_special_chara(t) or is_url(t) or is_hashtag(t) or is_tweeter_user(t) or is_empty(t)):
            temp[temp.index(t)]=''
        temp = replace_abrev(t,temp)    
    temp = filter(lambda a: a != '', temp)
    return temp        

#Algo 1
def preProcessed(data):
    temp = data['text'].tolist()
    res = list()
    for text in temp:
        #remove ponctuation
        text_1 = remove_ponctuation(text)
        #tokenize
        tokens = text_1.split(' ')  
        #clean text
        tokens_1 = drop_stuff(tokens)
        #add it to final list
        res.append(tokens_1)
    return res
        
# Algo 2
def etiqGrama(preProData):
    res = list()
    for d in preProData:
        taggedData = nltk.pos_tag(d)
        res.append(taggedData)
    return res    

# Algo 3            
def scores(preProData,emot,sentifile='SentiWordNet_3.0.0_20130122.txt'):
    swn = SentiWordNetCorpusReader(sentifile)
    res = list()
    bar = 0.0
    nm = NegMod()
    for tweet,emo in zip(preProData,emot):
        print bar / float(len(preProData))
        tweetneg = 0.0
        tweetpos = 0.0
        c = 0
        for word in tweet:
            try:
                w = str(wn.synsets(word)[0].name())
                temp = swn.senti_synset(w)
                plop = 0.0
                plopp = 0.0
                # Negation et modifieurs
                if c != 0:
                    if nm.neg_it(tweet[c-1]):#negation
                        tweetpos = temp[2]
                        tweetneg = temp[1]
                        break
                    if nm.mod_multiply(tweet[c-1]):#modifier
                        plop = temp[1]*2
                        plopp = temp[2]*2
                    else:
                        plop = temp[1]
                        plopp = temp[2]   
                else:
                    plop = temp[1]
                    plopp = temp[2]
                tweetpos = tweetpos + plop
                tweetneg = tweetneg + plopp
            except:
                pass
            c = c + 1 
        # Add emot feeling        
        tweetpos = tweetpos + emo[0]
        tweetneg = tweetneg + emo[1]
        res.append((tweetpos,tweetneg))
        bar = bar + 1.0
    return res    