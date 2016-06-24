import nltk
import string
import sys
import pandas as pd
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer, TfidfTransformer, CountVectorizer

# global tokenize
remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)
def tokenize(text):
	lowers = text.lower()
	no_punctuation = lowers.translate(remove_punctuation_map)
	tokens = nltk.word_tokenize(no_punctuation)
	return tokens
	

	
class Emotion:
	"""docstring for emotion"""
	global tokenize
	def tokenize(text):
		lowers = text.lower()
		no_punctuation = lowers.translate(remove_punctuation_map)
		tokens = nltk.word_tokenize(no_punctuation)
		return tokens
	def __init__(self):
		global remove_punctuation_map
		remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)
		file_Name = "/home/ahmed/Desktop/collegeProjects/bot/emotion/emo/modelfile.txt"
		# file_Name1 = "/home/ahmed/Desktop/collegeProjects/bot/emotion/emo/count_vect.txt"
		# file_Name2 = "/home/ahmed/Desktop/collegeProjects/bot/emotion/emo/tfidfvec.txt"
		fileObject = open(file_Name,'r')
		# fileObject1 = open(file_Name1,'r')
		# fileObject2 = open(file_Name2,'r')
		global trained_clfs
		trained_clfs = pickle.load(fileObject)
		global count_vect
		# count_vect = pickle.load(fileObject1)
		global tfidfvec
		# tfidfvec = pickle.load(fileObject2)
		data = pd.read_csv('/home/ahmed/Desktop/collegeProjects/bot/emotion/emo/ise_processed_2.csv', header=None)
		data.columns = ['emotion', 'text']

		count_vect = CountVectorizer(tokenizer=tokenize, stop_words='english')
		data_train_counts = count_vect.fit_transform(data.text)
		tfidfvec = TfidfTransformer().fit(data_train_counts)
		text_tfidf = tfidfvec.transform(data_train_counts)
	
	
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
emo = Emotion()
print emo.get_emotion("i feel sad")