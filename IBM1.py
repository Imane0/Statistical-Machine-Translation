# -*- coding: utf-8 -*-

"""
Created on Thu Dec  1 22:53:22 2016

@author: louati
"""

import collections
from decimal import Decimal as D


def _uniform_distribution(value):
    '''define a local function for uniform probability initialization'''
    return lambda: value

"Initializing t(e|f)"
L=len(Total_words_in_french);
t = collections.defaultdict(_uniform_distribution(1/L));

for i in range(0,len(French)):    
    for f in French.iloc[i]:
        for e in English.iloc[i]:
            t[(e,f)]= 1./L
            
convergence= 'false'
itr_max=10 ; j=1;
while j < itr_max:
    j=j+1    
    "initialize counts:"
    count = collections.defaultdict(D)
    total = collections.defaultdict(D)
    s_total = collections.defaultdict(D)
    
    for i in range(0,len(French)):
        for f in French.iloc[i]:
            total[f]=0
            for e in English.iloc[i]:            
                count[(e,f)] = 0 
    for i in range(0,len(French)):
        "compute normalization" 
        for  e in English.iloc[i] :
            s_total[e] = 0
            for f in French.iloc[i]:
                s_total[e] = s_total[e] + t[(e,f)]
    for i in range(0,len(French)):                            
        "collect counts:"   
        for  e in English.iloc[i]:
            for  f in French.iloc[i]:
                count[(e,f)] =count[(e,f)] + t[(e,f)]/s_total[e]
                total[f] = total[f] + t[(e,f)]/s_total[e]
    "estimate new probabilities:"
    for i in range(0,len(French)):      
        for f in French.iloc[i]:
            for  e in English.iloc[i]:
                if e=='None' or f=='None':
                    t[(e,f)]=0
                else:    
                    t[(e,f)] = count[(e,f)]/total[f]              
    "Show tuples with probability greater than 0.9 :"
    for (e, f), val in t.items():
        if val > 0.9:
            print("{} {}\t{}".format(e, f, val))
