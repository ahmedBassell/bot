# from practnlptools.tools import Annotator
# import json


# class srl(object):
# 	"""docstring for srl"""
# 	def __init__(self):
# 		self.file_path = "srl.json"
# 		fo = open(self.file_path, "rw+")
# 		fo.truncate()
# 		fo.write("{\"0\":[]}")
# 		fo.close()

# 	def record(self, sent):
# 		annotator=Annotator()
# 		fo = open(self.file_path, "rw+")
# 		predicates = json.load(fo)
# 		i = len(predicates)
# 		# while(1):
# 			# predicates = json.load(fo)
			
# 			# sent = raw_input()
# 			# if(sent == "bye"):
# 			# 	fo.close()
# 			# 	break
# 		# fo = open(self.file_path, "rw+")
# 		fo.seek(0)
# 		fo.truncate()
# 		l=annotator.getAnnotations(sent)['srl']
# 		predicates[i] = l
# 		json_m = json.dumps(predicates, sort_keys=True, indent=4, separators=(',', ': '))

# 		fo.write(json_m)
# 		fo.close()
# 			# i+=1

