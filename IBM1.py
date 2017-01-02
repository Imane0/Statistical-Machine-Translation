# -*- coding: utf-8 -*-

"""
Created on Thu Dec  1 22:53:22 2016

@author: louati
"""

from import_data import Upload_data
import collections
from decimal import Decimal as D

def _uniform_distribution(value):
    "define a local function for uniform probability initialization"
    return lambda: value

def Count_words(language):
    "Count the total number of words in the language F without repetition"
    Total_words = set()
    for i in range(0,len(language)):
        for f in language[i]:
            if f not in Total_words: 
                Total_words.add(f)
    
    return(Total_words)            
    
'''Import data'''
training_sets=Upload_data(10000)
English=training_sets[1]
French=training_sets[0]
Total_words_in_french=Count_words(French)
Total_words_in_english=Count_words(English)

def IBM1_training(French,English,number_of_iterations):
    Total_words_in_french=Count_words(French)
    Total_words_in_english=Count_words(English)

    "Initializing t(e|f)"
    L=len(Total_words_in_french)
    E=len(Total_words_in_english)    
    t = collections.defaultdict(_uniform_distribution(D(1./L)))
    
    for i in range(0,len(French)):    
        for e in English[i]:
            for f in French[i]:
                t[(e,f)]= 1./(L+1)
            
    itr_max=number_of_iterations ; j=1;
    while j < itr_max:
        j=j+1    
        "initialize counts:"
        count = collections.defaultdict(D)
        total = collections.defaultdict(D)
        s_total = collections.defaultdict(D)
    
        for i in range(0,len(French)):
            for f in French[i]:
                total[f]=0
                for e in English[i]:            
                    count[(e,f)] = 0
                    
        for i in range(0,len(French)):
            "compute normalization" 
            for  e in English[i] :
                s_total[e] = 0
                for f in French[i]:
                    s_total[e] = s_total[e] + t[(e,f)]
                    
        for i in range(0,len(French)):                            
            "collect counts:"  
            for e in English[i]:
                for f in French[i]:
                    if s_total[e]!=0 :
                        count[(e,f)] = count[(e,f)] + t[(e,f)]/s_total[e]
                        total[f] = total[f] + t[(e,f)]/s_total[e]
                        
        "estimate probabilities:"
        for i in range(0,len(French)):      
            for f in French[i]:
                for  e in English[i]:
                    t[(e,f)] = count[(e,f)]/total[f]    
                    
    return(t)
        

def IBM1_test(IBM1_train_model,English_sentence,Total_words):
    French_sentence= ''
    t= IBM1_train_model
    e_s=English_sentence.split()
    for e in e_s:
        M=0
        for f in Total_words:
            if t[(e,f)] > M:
                M=t[(e,f)]
                _f = f
        French_sentence=French_sentence + _f + ' '
    return (French_sentence)
    
#for (e, f), val in t.items():
 #   if val > 0.98:
  #      print("{} {}\t{}".format(e, f, val))
        

    
    
    
    
    
    
    
    
    

