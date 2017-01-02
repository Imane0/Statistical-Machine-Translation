# -*- coding: utf-8 -*-

"""
Created on Thu Dec  1 17:50:39 2016

@author: louati
"""
def Upload_data(length_training):
    
    import re
    
    " Open files:"
    languageE = open('europarl-v7.fr-en.en', 'r+')
    languageF = open('europarl-v7.fr-en.fr', 'r+')

    "Split files into sentences:"
    SentencesE = languageE.readlines()
    SentencesF = languageF.readlines()


    "Select length of training set:"
    M =length_training ; SentencesE_train=[];SentencesF_train=[];
    SentencesE_train[0:M]=SentencesE[0:M]
    SentencesF_train[0:M]=SentencesF[0:M]

    "Presere letters only for each line: "
    "Split words in each sentence:"
    for i in range(len(SentencesE_train)):
        SentencesE_train[i]= SentencesE_train[i].replace('\n','')
        SentencesF_train[i]= SentencesF_train[i].replace('\n','')
        SentencesE_train[i] = re.sub("[^a-zA-Z1-9éèàâêîôûç']", " ", SentencesE_train[i])    
        SentencesF_train[i] = re.sub("[^a-zA-Z1-9éèàâêîôûç']", " ", SentencesF_train[i])
        SentencesE_train[i]= SentencesE_train[i].lower().split() 
        SentencesF_train[i]= SentencesF_train[i].lower().split() 
    
    return [SentencesF_train,SentencesE_train]
    







