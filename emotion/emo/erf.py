import os
import string
import time
import sys
import pandas as pd
import numpy as np
import dill

class Emotion(object):
    def __init__(self):
        file_Name = "/home/ahmed/Desktop/collegeProjects/bot/emotion/emo/modelfile.txt"
        file_Name1 = "/home/ahmed/Desktop/collegeProjects/bot/emotion/emo/count_vect.txt"
        file_Name2 = "/home/ahmed/Desktop/collegeProjects/bot/emotion/emo/tfidfvec.txt"
        # we open the file for reading
        fileObject = open(file_Name,'r')  
        fileObject1 = open(file_Name1,'r')  
        fileObject2 = open(file_Name2,'r')  
        # load the object from the file into var b
        global trained_clfs
        global count_vect
        global tfidfvec
        trained_clfs = dill.load(fileObject) 
        count_vect = dill.load(fileObject1) 
        tfidfvec = dill.load(fileObject2) 

    def get_emotion(self, t):
        result = []
        for name in ['Logistic Regression', 'SVM', 'Multinomial Naive Bayes']:
            docs_new = [t]
            t_new_counts = count_vect.transform(docs_new)
            t_new_tfidf = tfidfvec.transform(t_new_counts)
            clf = trained_clfs[name]
            predicted = clf.predict(t_new_tfidf)
            r1 = {'name':name, 'emotion':predicted[0]}
            result.append(r1)
            sys.stdout.flush()
        return result
