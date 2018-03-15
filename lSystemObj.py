class LSysObj:

	angle = 0.0
	sentence = ""
	iterations = 0
	color = ""
	rules = {}

	## This object keeps track of the rules required to execute the L system
	# @param color - color to be used in the model
	# @param angle - of rotation
	# @param sentence - base sentence used to apply the rules
	# @param iterations - number of iterations for the recursive function
	# @param rules - dictionary of rules -> axiom:rules
	def __init__(self, angle, sentence, iterations, rules, color=None):
		
		if color is not None:
			self.color = color
		self.angle = angle
		self.sentence = sentence
		self.iterations = iterations
		self.rules = rules

