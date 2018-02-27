class LSysObj:

	angle = 0.0
	sentence = ""
	iterations = 0	
	rules = {}

	# @param angle - of rotation
	# @param sentence - base sentence used to apply the rules
	# @param iterations - number of iterations for the recursive function
	# @param rules - dictionary of rules -> axiom:rules
	def __init__(self, angle, sentence, iterations, rules):
		self.angle = angle
		self.sentence = sentence
		self.iterations = iterations
		self.rules = rules

