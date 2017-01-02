from import_data import *
from tools import *
from random import seed, sample
import numpy as np
from IBM1 import *
from IBM2 import *

seed(10)

'''Import data'''
database = Upload_data(5200)

english_train= database[1][0:5000]
french_train= database[0][0:5000]

english_dev= database[1][5000:5200]

##################################################
# language model
##################################################
unigrams = []
bigrams = []
for sentence in english_train:
	# sentence = ['I','ate','an','apple']
	for e in sentence: unigrams.append(e)
	bigram = [(sentence[i],sentence[i+1]) for i in range(len(sentence)-1)] 
	for b in bigram: bigrams.append(b)
print len(unigrams), len(bigrams)

dev_unigrams = []
dev_bigrams = []
for sentence in english_dev:
	# sentence = ['I','ate','an','apple']
	for e in sentence: dev_unigrams.append(e)
	bigram = [(sentence[i],sentence[i+1]) for i in range(len(sentence)-1)] 
	for b in bigram: dev_bigrams.append(b)
print len(dev_unigrams), len(dev_bigrams)


#### learn model
beta =0.45
q2D = learn_discounting_bigram_model_(unigrams,bigrams,beta)


### evaluation of the language model
p = dict()
for ind,sentence in enumerate(english_train):
    sentence_unigrams = sentence	
    sentence_bigrams = [(sentence[i],sentence[i+1]) for i in range(len(sentence)-1)] 
    p[ind] = 1
    for b in sentence_bigrams:
        p[ind] *= q2D[b]
print "average training likelihood: ", np.mean(p.values()) 
 
##################################################
# translation model
##################################################
nb_iterations = 10  
t_IBM1 = IBM1.IBM1_training(french_train, english_train,nb_iterations)
t_IBM2,a = IBM2_training(french_train, english_train,nb_iterations)

''' used for translation in training sets'''
translation_probas = collections.defaultdict(D)
for k in range(len(english_train)):
    I= len(english_train[k])
    J= len(french_train[k])
    S = 0
    for en_word in english_train[k]:
        term = 1
        for fr_word in french_train[k]:
		term *= t[(en_word,fr_word)] 	
        term /= I**J
        S += term	
    en_sen=' '.join(english_train[k])
    fr_sen=' '.join(french_train[k])
    translation_probas[en_sen,fr_sen]=S 	
norm = sum(translation_probas.values())
for k in range(0,len(english_train)):
    en_sen=' '.join(english_train[k])
    fr_sen=' '.join(french_train[k])
    translation_probas[en_sen,fr_sen] /= norm 	
	 

##################################################
# translation
##################################################

fr_s = ' '.join(french_train[8])
best_en_translation = ''
v_prev = 0
for k , en_s in enumerate(english_train):
    en_sen=' '.join(english_train[k])
    fr_sen=' '.join(french_train[k])
    v =  float(p[k]) * float(translation_probas[en_sen,fr_s])
    if v > v_prev: 
        print 'az'
        v_prev = v 
        print en_s,k
        best_en_translation = en_s

print fr_s, '\n', best_en_translation

def word_translation(word,unigrams,t):
    word_translate=[]
    for en_word in unigrams:
        if (en_word,word) in t.keys():
            word_translate.append(en_word)
    return(word_translate)
    
def translate_IBM1(fr_sen,t,q2D):
    
    from itertools import combinations
    translation_probas = collections.defaultdict(D)
    fr_sen_list=fr_sen.lower().split() 
    J= len(fr_sen_list)
    list_word=[]
    for fr_word in fr_sen_list:  
        L = word_translation(fr_word,unigrams,t)
        m=0            
        for e in L:
            if t[(e,fr_word)] > m:
                e_star = e
                m=t[(e,fr_word)]
        list_word.append(e_star)
    sentences= list(combinations(list_word,J))    
    language_evaluation = []    
    for sentence in sentences:
        S = 0
        local_bigrams=[(sentence[i],sentence[i+1]) for i in range(len(sentence)-1)]
        lm = 1
        for b in local_bigrams: 
            lm=lm*q2D[b]
        for en_word in sentence:
            term=1
            for fr_word in fr_sen_list:        
                term *= float(t[(en_word,fr_word)]) 	
            term /= J**J
            S += term
            
        language_evaluation.append(S*lm)
    print sentences    
    ind = np.argmax(language_evaluation)
    print ind
    best_en_translation = sentences[int(ind)]
    print sentences[ind]
    return best_en_translation



def translate_IBM2(fr_sen,t,a,q2D):
    
    from itertools import combinations
    translation_probas = collections.defaultdict(D)
    fr_sen_list=fr_sen.lower().split() 
    J= len(fr_sen_list)
    list_word=[]
    for fr_word in fr_sen_list: 
        L = word_translation(fr_word,unigrams,t)
        m=0      
        for e in L:
            if t[(e,fr_word)] > m:
                e_star = e
                m=t[(e,fr_word)]
        list_word.append(e_star)
    sentences= list(combinations(list_word,J))    
    language_evaluation = []    
    for sentence in sentences:
        S = 0
        local_bigrams=[(sentence[i],sentence[i+1]) for i in range(len(sentence)-1)]
        lm = 1
        for b in local_bigrams: 
            lm=lm*q2D[b]
        for i,en_word in enumerate(sentence):
            term=1
            for j,fr_word in enumerate(fr_sen_list):        
                term = term *float(t[(en_word,fr_word)])*float(a[(i,j,J,J)]) 	
            S += term
        language_evaluation.append(S*lm)
        
    print sentences    
    ind = np.argmax(language_evaluation)
    print ind
    best_en_translation = sentences[int(ind)]
    print sentences[ind]
    return best_en_translation