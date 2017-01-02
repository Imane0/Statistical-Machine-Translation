# -*- coding: utf-8 -*-
"""
Created on Sun Dec 25 16:40:32 2016

@author: louati
"""

from import_data import Upload_data
import collections
import decimal
from decimal import Decimal as D
from IBM1 import IBM1_training

# set deciaml context
decimal.getcontext().prec = 4  #Digits of precision 
decimal.getcontext().rounding = decimal.ROUND_HALF_UP


def Count_words(language):
    "Count the total number of words in the language F without repetition"
    Total_words = set()
    for i in range(0,len(language)):
        for f in language[i]:
            if f not in Total_words: 
                Total_words.add(f)
    
    return(Total_words)            
    

class default_key(collections.defaultdict):
    "define a local function for uniform probability initialization"
    def __missing__(self, key):
        if self.default_factory is None:
            raise KeyError(key)
        else:
            result = self[key] = self.default_factory(key)
            return result


'''Import data'''
training_sets=Upload_data(1000)
English=training_sets[0]
French=training_sets[1]

def IBM2_training(French,English,number_of_iterations):
    
    Total_words_in_french=Count_words(French)
    Total_words_in_english=Count_words(English)

    "Initializing t(e|f)"
    t = IBM1_training(French,English,number_of_iterations)            
    
    
    def key_function(key):
        " default_factory function for default_key "
        i, j, l_e, l_f = key
        return D("1") / D(l_f + 1)
    
    a = default_key(key_function)
    itr_max= number_of_iterations ; j=1;
    while j < itr_max:
        j=j+1    
        "initialize counts:"
    
        # variables for estimating t
        count_t = collections.defaultdict(D)
        total_t = collections.defaultdict(D)
        # variables for estimating a
        count_a = collections.defaultdict(D)    
        total_a = collections.defaultdict(D)    
    
        s_total = collections.defaultdict(D)
    
        for i in range(0,len(French)):
            l_f=len(French[i])
            l_e=len(English[i])
            " compute normalization"
            for (j, e) in enumerate(English[i], 1):
                s_total[e] = 0
                for (i, f) in enumerate(French[i], 1):
                    s_total[e] = s_total[e] + D(t[(e, f)]) * a[(i, j, l_e, l_f)]
        
        " collect counts"
        for (j, e) in enumerate(English[i], 1):
            for (i, f) in enumerate(French[i], 1):
                count = D(t[(e, f)]) * a[(i, j, l_e, l_f)] / s_total[e]
                count_t[(e, f)] = count_t[(e,f)] + count
                total_t[f] = total_t[f] + count
                count_a[(i, j, l_e, l_f)] = count_a[(i, j, l_e, l_f)] + count
                total_a[(j, l_e, l_f)] = total_a[(j, l_e, l_f)] + count
 
        for (e, f) in count_t.keys():
            try:
                t[(e, f)] = count_t[(e, f)] / total_t[f]
            
            except decimal.DivisionByZero:
                print(u"e: {e}, f: {f}, count_t[(e, f)]: {ef}, total_t[f]: \
                      {totalf}".format(e=e, f=f, ef=count_t[(e, f)],
                                       totalf=total_t[f]))
                raise
                
        for (i, j, l_e, l_f) in count_a.keys():
            a[(i, j, l_e, l_f)] = count_a[(i, j, l_e, l_f)] / \
            total_a[(j, l_e, l_f)]


    return(t,a)

