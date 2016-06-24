class op(object):
	"""docstring for op"""
	
	def add(self, inp):
		if(inp==''):
			inp = 9

		n = int(inp)
		n = n+1
		return n
operations = op()