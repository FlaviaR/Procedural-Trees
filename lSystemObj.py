#! /usr/bin/env python
# -*- coding: UTF-8 -*-
#
## @package Tree
#
# An LSysObj is a container to keep track of individual rule information including the
# angle, recursion depth, base sentence, model color, and substitution rules. 
#
# @author Flavia Cavalcanti
# @since 22/02/2018
#

class LSysObj:

	angle = 0.0
	sentence = ""
	iterations = 0
	color = ""
	rules = {}
	rulesStochastic = {}

	## This object keeps track of the rules required to execute the L system
	# @param color - color to be used in the model
	# @param angle - of rotation
	# @param sentence - base sentence used to apply the rules
	# @param iterations - number of iterations for the recursive function
	# @param rules - dictionary of rules -> axiom:rules
	def __init__(self, angle, sentence, iterations, rules, rulesStochastic, color=None):
		
		if color is not None:
			self.color = color
		self.angle = angle
		self.sentence = sentence
		self.iterations = iterations
		self.rules = rules
		self.rulesStochastic = rulesStochastic

