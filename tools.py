import nltk 
from nltk.util import ngrams
from time import time


def contains_numbers(s):
	""" 
	Input: s a string
	returns a boolean variable O: 
	- O = TRUE if s contains a digit 0, 1, ..., 9
	- O = FALSE otherwise 
	"""
	return any(char.isdigit() for char in s)
 
def sentences(textfile):
	""" 
	returns a list of strings. 
	The list contains all sentences from the corpus 'textfile' that
        do not contain a digit. The sentences are returned in a lower
        case format
	"""
	f = open(textfile)
	splitted = f.readlines()
	allSentences = [s.replace('\n','').lower() for s in splitted]
	# discard sentences that contain digits 0, 1, etc ..
	sentences = [s for s in allSentences if not contains_numbers(s)]
	f.close()
	return sentences

def vocabulary(textfile):
	"""
	returns a list of all tokens included in the corpus 'textfile'.
	Tokens may be words or punctuation
	The returned list does not contain repeated elements. 
	The first output of unigrams_bigrams_trigrams function is a list
	of all tokens of the corpus, with repetition
	"""
	S = sentences(textfile)
	vocab = []
	for sentence in S: 
		tokens = nltk.tokenize.word_tokenize(sentence)
		for w in tokens: vocab.append(w)
	return sorted(set(vocab))	



def unigrams_bigrams(corpus):
	bigrams = []
	unigrams = []
	for sentence in corpus:
		tokens = nltk.word_tokenize(sentence)
		for w in tokens: unigrams.append(w)
		bigram = ngrams(tokens,2)
		#bigram = [(tokens[i],tokens[i+1]) for i in range(len(tokens)-1)]
		for couple in bigram: bigrams.append(couple)
	return unigrams,bigrams



def unigrams_bigrams_trigrams(corpus):
	bigrams = []
	trigrams = []
	unigrams = []
	for sentence in corpus:
		tokens = nltk.word_tokenize(sentence)
		for w in tokens: unigrams.append(w)
		bigram = ngrams(tokens,2)
		#bigram = [(tokens[i],tokens[i+1]) for i in range(len(tokens)-1)]
		for couple in bigram: bigrams.append(couple)
		trigram = ngrams(tokens,3)
		#trigram = [(tokens[i],tokens[i+1],tokens[i+2]) for i in range(len(tokens)-2)]
		for tup in trigram: trigrams.append(tup)
	return unigrams,bigrams,trigrams

#def trigrams(corpus):
#	three_grams = []
#	for sentence in corpus:
#		tokens = nltk.word_tokenize(sentence)
#		trigram = nltk.util.ngrams(tokens,3)
#		for tup in trigram: three_grams.append(tup)
#	return three_grams

def learn_discounting_model(unigrams,bigrams,trigrams,beta):
	# compute q2 
	c_star = dict()
	q2 = dict()
	for tup in bigrams:
		c_star[tup] = bigrams.count(tup) - beta
		q2[tup] = c_star[tup]/unigrams.count(tup[0])
	# compute the sets A(v) and B(v) for all tokens/unigrams in the training corpus
	A = dict()
	B = dict()
	for v in unigrams:
		#A[v] = [tup(2) for tup in bigrams if tup(1)==v]
		B[v] = [w for w in unigrams if (v,w) not in bigrams]
	# compute q2D for all bigrams (v,w) such that v and w are tokens from the
	# training corpus (not only bigrams seen in the training corpus)
	q2D = dict()
	for v in unigrams:
		for w in unigrams:
			if (v,w) in bigrams:   
				q2D[(v,w)] = q2[(v,w)]
			else:
				alpha = 1 - sum([q2[tup] for tup in bigrams if tup[0]==v])
				denom = sum([unigrams.count(w_prime) for w_prime in B[v]])
				q2D[(v,w)] = alpha*unigrams.count(w)/denom
	# compute q3D for all trigrams (u,v,w) such that u, v, and w are tokens see in
	# the training corpus (not only trigrams seen in the training corpus) 
	A = dict()
	B = dict()
	for u in unigrams:
		for v in unigrams:
			A[(u,v)] = [w for w in unigrams if (u,v,w) in trigrams]
			B[(u,v)] = [w for w in unigrams if (u,v,w) not in trigrams]
	q3D = dict()
	alpha = dict()
	for u in unigrams:
		for v in unigrams:
			for w in unigrams:
				if w in A[(u,v)]:
					q3D[(u,v,w)] = (trigrams.count((u,v,w)) - beta)/bigrams.count((u,v))

				else:
					alpha = 1 - sum([ ( trigrams.count((u,v,w)) - beta ) / bigrams.count((u,v)) for w in A[(u,v)]])
					denom = sum( [ q2D[(v,w_prime)] for w_prime in B[(u,v)] ] )
					q3D[(u,v,w)] = alpha*q2D[(v,w)]/denom

	return q2D, q3D
	
			

def learn_discounting_model_(unigrams,bigrams,trigrams,beta):
	# compute counts
	c1 = dict()
	c2 = dict()
	c3 = dict()
	for token in unigrams: c1[token] = unigrams.count(token)
	for tup in bigrams: c2[tup] = bigrams.count(tup)
	for tup in trigrams: c3[tup] = trigrams.count(tup)
	# compute q2
	print "computing q2\n" 
	t0 = time()
	q2 = dict()
	for tup in bigrams:
		q2[tup] = (c2[tup] - beta)/c1[tup[0]]
	print "finished; took ", time()-t0, "seconds"
	# compute the sets A(v) and B(v) for all tokens/unigrams in the training corpus
	print "computing B[v] for all tokens v"
	t0 = time()
	A = dict()
	B = dict()
	for v in unigrams:
		#A[v] = [tup(2) for tup in bigrams if tup(1)==v]
		B[v] = [w for w in unigrams if (v,w) not in bigrams]
	print "finished; took " , time()-t0, " seconds"
	# compute q2D for all bigrams (v,w) such that v and w are tokens from the
	# training corpus (not only bigrams seen in the training corpus)
	print "computing q2D"
	t0 = time()
	q2D = q2
	for v in unigrams:
		denom = sum([c1[w_prime] for w_prime in B[v]])
		alpha = 1 - sum([q2[tup] for tup in bigrams if tup[0]==v])
		for w in B[v]:
			q2D[(v,w)] = alpha*c1[w]/denom
	print "finished; took ", time()-t0, " seconds"
	# compute q3D for all trigrams (u,v,w) such that u, v, and w are tokens seen in
	# the training corpus (not only trigrams seen in the training corpus) 
	print "computing B for all bigrams"
	t0 = time()
#	A = dict()
	B = dict()
	for u in unigrams:
		for v in unigrams:
#			A[(u,v)] = [w for w in unigrams if (u,v,w) in trigrams]
			B[(u,v)] = [w for w in unigrams if (u,v,w) not in trigrams]
	print "finished; took ", time()-t0, " seconds"
	print "computing q3D for all trigrams"
	t0 = time() 
	q3D = dict()
	for tup in trigrams: 
		q3D[tup] = (c3[tup]-beta)/c2[(tup[0],tup[1])]
	for u in unigrams:
		for v in unigrams:
			denom = sum( [ q2D[(v,w_prime)] for w_prime in B[(u,v)] ] )
			alpha = 1 - sum([ ( c3[(u,v,w_prime)] - beta ) / c2[(u,v)] for w_prime in unigrams if (u,v,w_prime) in trigrams])
			for w in B[(u,v)]:
				q3D[(u,v,w)] = alpha*q2D[(v,w)]/denom
	print "finished; took ",time()-t0, " seconds"
	return q2D, q3D

def learn_discounting_bigram_model_(unigrams,bigrams,beta):
	# compute counts
	c1 = dict()
	c2 = dict()
	for token in unigrams: c1[token] = unigrams.count(token)
	for tup in bigrams: c2[tup] = bigrams.count(tup)
	# compute q2
	print "computing q2\n" 
	t0 = time()
	q2 = dict()
	for tup in bigrams:
		q2[tup] = (c2[tup] - beta)/c1[tup[0]]
	print "finished; took ", time()-t0, "seconds"
	# compute the sets A(v) and B(v) for all tokens/unigrams in the training corpus
	print "computing B[v] for all tokens v"
	t0 = time()
	A = dict()
	B = dict()
	for v in unigrams:
		#A[v] = [tup(2) for tup in bigrams if tup(1)==v]
		B[v] = [w for w in unigrams if (v,w) not in bigrams]
	print "finished; took " , time()-t0, " seconds"
	# compute q2D for all bigrams (v,w) such that v and w are tokens from the
	# training corpus (not only bigrams seen in the training corpus)
	print "computing q2D"
	t0 = time()
	q2D = q2
	for v in unigrams:
		denom = sum([c1[w_prime] for w_prime in B[v]])
		alpha = 1 - sum([q2[tup] for tup in bigrams if tup[0]==v])
		for w in B[v]:
			q2D[(v,w)] = alpha*c1[w]/denom
	print "finished; took ", time()-t0, " seconds"
	return q2D

