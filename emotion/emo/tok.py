import string
import nltk
import os

class Tok:
	__module__ = os.path.splitext(os.path.basename(__file__))[0]
	def __init__(self):
		self.remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)
		
	def tokenize(self, text):
	    lowers = text.lower()
	    no_punctuation = lowers.translate(self.remove_punctuation_map)
	    tokens = nltk.word_tokenize(no_punctuation)
	    return tokens