
# coding: utf-8

# In[1]:

import os
import nltk
import string
import time
import sys
import pandas as pd
import numpy as np
import dill



# machine learning
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import f1_score, recall_score, precision_score
from sklearn.pipeline import Pipeline
from sklearn.cross_validation import KFold, train_test_split

# NLP
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer, TfidfTransformer, CountVectorizer

# from tok import Tok

# tok = Tok()
# theTokenizer = tok.tokenize
# In[2]:

data = pd.read_csv(
    '/home/ahmed/Desktop/collegeProjects/bot/emotion/emo/ise_processed_2.csv', 
    header=None)
data.columns = ['emotion', 'text']
data.head(10)


# In[3]:
global tokenize
def tokenize(text):
    import string
    import nltk
    remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)
    lowers = text.lower()
    no_punctuation = lowers.translate(remove_punctuation_map)
    tokens = nltk.word_tokenize(no_punctuation)
    return tokens


# In[4]:

def predict_fn(data, pipeline):
    k_fold = KFold(n=len(data), n_folds=6)
    fscores = []
    pscores = []
    rscores = []
    t0 = time.time()
    for train_indices, test_indices in k_fold:
        train_text = data.iloc[train_indices]['text'].values
        train_y = data.iloc[train_indices]['emotion'].values

        test_text = data.iloc[test_indices]['text'].values
        test_y = data.iloc[test_indices]['emotion'].values

        pipeline.fit(train_text, train_y)
        predictions = pipeline.predict(test_text)

        fscore = f1_score(test_y, predictions, average='weighted')
        fscores.append(fscore)
        rscore = recall_score(test_y, predictions, average='weighted')
        rscores.append(rscore)
        pscore = precision_score(test_y, predictions, average='weighted')
        pscores.append(pscore)
    time_iter = (time.time() - t0)
    output = {"F1": sum(fscores)/len(fscores),
              "Precision": sum(pscores)/len(pscores),
              "Recall": sum(rscores)/len(rscores),
              "Time": time_iter}
    ret = {
        "output": output,
        "pipeline": pipeline
    }
    return ret


# In[5]:

lr  = LogisticRegression()
dtc = DecisionTreeClassifier()
svc = LinearSVC(
    C=1.0, class_weight=None, dual=True,
    loss='squared_hinge', max_iter=1000,
    multi_class='ovr', penalty='l2')
knn = KNeighborsClassifier(
    n_neighbors=10, algorithm='auto')
mnb = MultinomialNB(alpha=1.0, class_prior=None, fit_prior=True)


# In[6]:

classifier_df = pd.DataFrame()
trained_pipelines = {}
for clf, name in [
    (lr, 'Logistic Regression'),
    (dtc, 'Decision Tree Classifier'),
    (svc, 'SVM'),
    (knn, 'KNN'),
    (mnb, 'Multinomial Naive Bayes')]:
    
    iter_pipeline = Pipeline([
        ('vectorizer',  TfidfVectorizer(tokenizer=tokenize, stop_words='english')),
        ('classifier',  clf)])
    
    ret_data = predict_fn(data, iter_pipeline)
    trained_pipelines[name] = ret_data['pipeline']
    ret_df = pd.DataFrame(ret_data['output'], index={name}, columns=ret_data['output'].keys())
    if (name=="Logistic Regression"):
        classifier_df = ret_df
    else:
        classifier_df = classifier_df.append(ret_df)
    print name
    sys.stdout.flush()
classifier_df.to_csv("FinalOutput.csv")


# In[7]:






# # Production Code

# In[8]:

count_vect = CountVectorizer(tokenizer=tokenize, stop_words='english')
data_train_counts = count_vect.fit_transform(data.text)
tfidfvec = TfidfTransformer().fit(data_train_counts)
text_tfidf = tfidfvec.transform(data_train_counts)


# In[9]:

trained_clfs = {}
for clf, name in [
    (lr, 'Logistic Regression'),
    (svc, 'SVM'),
    (mnb, 'Multinomial Naive Bayes')]:
    
    clf.fit(text_tfidf, data.emotion)
    trained_clfs[name] = clf
    print name
    sys.stdout.flush()


# In[10]:


file_Name1 = "/home/ahmed/Desktop/collegeProjects/bot/emotion/emo/count_vect.txt"
file_Name2 = "/home/ahmed/Desktop/collegeProjects/bot/emotion/emo/tfidfvec.txt"
# open the file for writing
fileObject1 = open(file_Name1,'wb') 
fileObject2 = open(file_Name2,'wb') 

# this writes the object a to the
# file named 'testfile'
dill.dump(count_vect,fileObject1)   
dill.dump(tfidfvec,fileObject2)   

# here we close the fileObject
fileObject1.close()
fileObject2.close()





i = 0
while i in range(10):
    t = raw_input("hi")
    t0 = time.time()
    for name in [
        'Logistic Regression',
        'SVM',
        'Multinomial Naive Bayes']:
        docs_new = [t]
        t_new_counts = count_vect.transform(docs_new)
        t_new_tfidf = tfidfvec.transform(t_new_counts)
        
        clf = trained_clfs[name]
        predicted = clf.predict(t_new_tfidf)
        print name, predicted
        sys.stdout.flush()
    time_iter = (time.time() - t0)
    print time_iter
    i+=1


# In[ ]:



