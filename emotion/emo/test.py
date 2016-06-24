class test(object):
	"""docstring for test"""
	global sub
	def __init__(self):
		self.x=32
		global x
		x=32
	def add(self, n):
		return self.x+n
	def sub(n):
		return x-n
		


t = test()
print t.add(2)
print sub(3)