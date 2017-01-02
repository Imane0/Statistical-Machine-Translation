from import_data import *
from tools import *
from random import seed, sample
import numpy as np


seed(10)


##################################################
# language model
##################################################
'''Import data'''
database = Upload_data(10)
english_train= database[0][0:8]
english_dev = database[0][8:]
french_train= database[1][0:8]
#french_dev = database[1][80:]


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
dev_logliks = dict()
q2D = dict()
for beta in linspace(0.1,1,10):
	print "learning model for beta = ",beta
        t_start = time()
        q2D[beta] = learn_discounting_bigram_model_(unigrams,bigrams,beta)
	print "execution time for learn_discounting_model_:" ,time()-t_start
        print "finished learning"
        dev_loglik = 0
        for u in unigrams:
                for v in unigrams:
                        if u!=v:
                                tup = (u,v)
				dev_loglik = dev_loglik + dev_bigrams.count(tup)*log(q2D[beta][tup])
	dev_logliks[beta] = dev_loglik
max_loglik = max(dev_logliks.values())
for key,value in dev_logliks.iteritems():
	if value == max_loglik:
		print "beta yielding the maximum log-loglikelihood on the dev set is: %f" % key
		beta_star = key
q2D = q2D[key]

### evaluation of the language model
p = dict()
for sentence in english_train:
	sentence_unigrams = sentence	
	sentence_bigrams = [(sentence[i],sentence[i+1]) for i in range(len(sentence)-1)] 
	p[sentence] = 1
	for b in sentence_bigrams:
		p[sentence] *= q2D[b]
print "average training perplexity: ", np.mean(p.values) 
 
##################################################
# translation model
##################################################
nb_iterations = 10
t = IBM1_training(french_train, english_train,nb_iterations)
translation_probas = dict()
for k in range(len(english_train)):
	I= len(english_train[k])
	J= len(french_train[k])
	S = 0
	for en_word in english_train[k]:
		term = 1
		for fr_word in french_train[K]:
			term *= t[(en_word,fr_word)] 	
		term /= I**J
		S += term	
	translation_probas[(english_train[k],french_train[k])] = S 	
norm = sum(translation_probas.values)
for k in translation_probas.keys:
	translation_probas[k] /= norm

##################################################
# translation
##################################################
fr_s = french_train[2]
best_en_translation = english_train[0]
v_prev = 0
for en_s in english_train:
	v =  p[en_s] * translation_probas[(en_s,fr_s)]
	if v > v_prev: 
		v_prev = v 
		best_en_translation = en_s

print fr_s, '\n', best_en_translation
