import os
import nltk
import string
import time
import sys
import pandas as pd
import numpy as np
import pickle


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


class emotion():
    """docstring for emotion"""
    def __init__(self):
        self.read_data()
        self.remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)


        self.lr  = LogisticRegression()
        self.dtc = DecisionTreeClassifier()
        self.svc = LinearSVC(
            C=1.0, class_weight=None, dual=True,
            loss='squared_hinge', max_iter=1000,
            multi_class='ovr', penalty='l2')
        self.knn = KNeighborsClassifier(
            n_neighbors=10, algorithm='auto')
        self.mnb = MultinomialNB(alpha=1.0, class_prior=None, fit_prior=True)


        self.block1()
        self.block2()



    def read_data(self):
        self.data = pd.read_csv('/home/ahmed/Desktop/collegeProjects/bot/emotion/emo/ise_processed_2.csv', header=None)
        self.data.columns = ['emotion', 'text']
        
    def tokenize(self, text):
        lowers = text.lower()
        no_punctuation = lowers.translate(self.remove_punctuation_map)
        tokens = nltk.word_tokenize(no_punctuation)
        return tokens

    def predict_fn(self, data, pipeline):
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


    def block1(self):
        classifier_df = pd.DataFrame()
        trained_pipelines = {}
        for clf, name in [
            (self.lr, 'Logistic Regression'),
            (self.dtc, 'Decision Tree Classifier'),
            (self.svc, 'SVM'),
            (self.knn, 'KNN'),
            (self.mnb, 'Multinomial Naive Bayes')]:
            
            iter_pipeline = Pipeline([
                ('vectorizer',  TfidfVectorizer(tokenizer=self.tokenize, stop_words='english')),
                ('classifier',  clf)])
            
            ret_data = self.predict_fn(self.data, iter_pipeline)
            trained_pipelines[name] = ret_data['pipeline']
            ret_df = pd.DataFrame(ret_data['output'], index={name}, columns=ret_data['output'].keys())
            if (name=="Logistic Regression"):
                classifier_df = ret_df
            else:
                classifier_df = classifier_df.append(ret_df)
            # print name
            sys.stdout.flush()
        classifier_df.to_csv("FinalOutput.csv")

        # # Production Code
    def block2(self):
        self.count_vect = CountVectorizer(tokenizer=self.tokenize, stop_words='english')
        data_train_counts = self.count_vect.fit_transform(self.data.text)
        self.tfidfvec = TfidfTransformer().fit(data_train_counts)
        text_tfidf = self.tfidfvec.transform(data_train_counts)


        # In[9]:

        self.trained_clfs = {}
        for clf, name in [
            (self.lr, 'Logistic Regression'),
            (self.svc, 'SVM'),
            (self.mnb, 'Multinomial Naive Bayes')]:
            
            clf.fit(text_tfidf, self.data.emotion)
            self.trained_clfs[name] = clf
            # print name
            sys.stdout.flush()

    def get_emotion(self, t):
        t0 = time.time()
        result = []
        for name in [
            'Logistic Regression',
            'SVM',
            'Multinomial Naive Bayes']:
            docs_new = [t]
            t_new_counts = self.count_vect.transform(docs_new)
            t_new_tfidf = self.tfidfvec.transform(t_new_counts)
            
            clf = self.trained_clfs[name]
            predicted = clf.predict(t_new_tfidf)
            r1 = (name, predicted)
            result.append(r1)
            sys.stdout.flush()
        time_iter = (time.time() - t0)
        return result
        # i = 0
        # while i in range(10):
        #     t = raw_input("")
        #     t0 = time.time()
        #     for name in [
        #         'Logistic Regression',
        #         'SVM',
        #         'Multinomial Naive Bayes']:
        #         docs_new = [t]
        #         t_new_counts = count_vect.transform(docs_new)
        #         t_new_tfidf = tfidfvec.transform(t_new_counts)
                
        #         clf = trained_clfs[name]
        #         predicted = clf.predict(t_new_tfidf)
        #         # print name, predicted
        #         sys.stdout.flush()
        #     time_iter = (time.time() - t0)
        #     # print time_iter
        #     i+=1


# In[10]:

# i = 0
# while i in range(10):
#     t = raw_input("")
#     t0 = time.time()
#     for name in [
#         'Logistic Regression',
#         'SVM',
#         'Multinomial Naive Bayes']:
#         docs_new = [t]
#         t_new_counts = count_vect.transform(docs_new)
#         t_new_tfidf = tfidfvec.transform(t_new_counts)
        
#         clf = trained_clfs[name]
#         predicted = clf.predict(t_new_tfidf)
#         # print name, predicted
#         sys.stdout.flush()
#     time_iter = (time.time() - t0)
#     # print time_iter
#     i+=1



# In[ ]:
emo = emotion()
print emo.get_emotion('heeeeeey')
