# from spacy.en import English
# import json

# class Ner(object):
# 	"""docstring for Ner"""
# 	def __init__(self):
# 		self.file_path = "ner.json"
# 		fo = open(self.file_path, "rw+")
# 		fo.truncate()
# 		fo.write("{\"0\":[]}")
# 		fo.close()
# 	def record(self, sent):
# 		parser = English(parser= False)
# 		#example = "APPLE'S STOCK DROPPED DRAMATICALLY AFTER THE DEATH OF STEVE JOBS IN OCTOBER"
# 		# example = "Apple's stocks dropped dramatically after the death of Steve Jobs in October."
# 		sent = unicode(sent,encoding="utf-8")
# 		parsedEx = parser(sent)

# 		fo = open(self.file_path, "rw+")
# 		entities = json.load(fo)
# 		i = len(entities)
# 		fo.seek(0)
# 		fo.truncate()
# 		# if you just want the entities and nothing else, you can do access the parsed examples "ents" property like this:
# 		ents = list(parsedEx.ents)
# 		entities [i] = ents
# 		print type(ents)
# 		# json_m = json.dumps(entities, sort_keys=True, indent=4, separators=(',', ': '))

# 		# fo.write(json_m)
# 		# fo.close()
# 		for entity in ents:
# 		    # print(entity.label, entity.label_, ' '.join(t.orth_ for t in entity))
# 		    print( entity.label_, ' '.join(t.orth_ for t in entity))

