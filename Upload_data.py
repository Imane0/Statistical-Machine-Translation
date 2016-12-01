# -*- coding: utf-8 -*-
"""
Created on Thu Dec  1 17:50:39 2016

@author: louati
"""
import pandas as pd
import numpy as np
import re

" Open files:"
languageE = open('europarl-v7.fr-en.en', 'r+')
languageF = open('europarl-v7.fr-en.fr', 'r+')

"Split files into sentences:"
SentencesE = languageE.readlines()
SentencesF = languageF.readlines()

"Select length of training set:"
length_training =1000 ; SentencesE_train=[];SentencesF_train=[];
SentencesE_train[0:length_training]=SentencesE[0:length_training]
SentencesF_train[0:length_training]=SentencesF[0:length_training]

"Delete the '\n' characters from each line: "
"Split words in each sentence:"
for i in range(len(SentencesE_train)):
    SentencesE_train[i]= SentencesE_train[i].replace('\n','')
    SentencesF_train[i]= SentencesF_train[i].replace('\n','')
    SentencesE_train[i]= SentencesE_train[i].split()
    SentencesF_train[i]= SentencesF_train[i].split()

length_E=[] ; length_F=[];
"Define dataframes for two languages:"
for i in range(len(SentencesE_train)):
    length_E.append(len(SentencesE_train[i]))
    length_F.append(len(SentencesF_train[i]))

"Define length of longest sentence for each language:"    
L=np.max(length_E) 
M=np.max(length_F)

"Define data frames:"
French=pd.DataFrame(SentencesE_train)
English=pd.DataFrame(SentencesF_train)






