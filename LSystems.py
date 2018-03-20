#! /usr/bin/env python
# -*- coding: UTF-8 -*-
#
## @package Tree
#
# Draws the resulting model based on the received LSystem rule.  
# See the draw function for more information regarding the character interpretations. 
#
# @author Flavia Cavalcanti
# @since 22/02/2018
#

import matrix
import numpy as np
import random
# Assumes SolidPython is in site-packages or elsewhwere in sys.path
from solid import *
from solid.utils import *
from turtle import turtle

class LSystem():
	
	def __init__(self):
		self.stochastic = False
		self.spheres = False
		self.debug = False
		self.turtle = turtle()
	
	def printDebug(self, state):
		self.debug = state
	
	def useStochastic(self, state):
		self.stochastic = state
	
	def useSpheres(self, state):
		self.spheres = state

	## L-Systems were developed as a mathematical description of plant growth designed to model biological systems.
	#  L-Systems can be thought as containing the instructions for how a single cell can grow into a complex organism.
	#  They can be used to define the rules for interesting patterns, being particularly useful for fractal creation.s
	#
	#  Example usage:
	#  - A       - Axiom
	#  - A -> B  - Rule 1 Change A to B
	#  - B -> AB - Rule 2 Change B to AB
	#  @see - http://interactivepython.org/courselib/static/thinkcspy/Strings/TurtlesandStringsandLSystems.html
	#  @param n - height of tree
	#  @param sentence - initial sentence - base for the rule applications
	#  @param rules - a dictionary containing an axiom:rule key:value pair, they're both expected to be strings
	#  @return the resulting L-System based off of the given axioms and rules
	def buildLSystem(self, n, sentence, rules, sRules):
		next = ""
		
		if (n > 0):
			characters = list(sentence)
			
			for c in characters:
				if (not self.stochastic and c in rules):
					next += self.buildLSystem(n-1, rules[c], rules, sRules)
				elif (self.stochastic and c in sRules):
					arr = sRules[c]
					#						half = int(len(rule)/2)
					#						ruleH1 = rule[0:half + 1]
					#						ruleH2 = rule[(half):]
					
					sel = random.randint(0, len(arr) - 1)
					#						arr = [rule, ruleH1, ruleH2]
					selectedRule = arr[sel]
					
					next += self.buildLSystem(n-1, selectedRule, rules, sRules)
				else:
					next += c

		else:
			return sentence
		
		return next


	## Interpret a given sentence and draw the result.
	#
	#  - F move forward a step of length d
	#  - f Move forward a step of length d without drawing a line
	#  - + Turn left by angle a
	#  - - Turn right by angle a
	#  - & Pitch down by angle a
	#  - ^ Pitch up by angle a
	#  - \ Roll left by angle a
	#  - / Roll right by angle a
	#  - | Turn arund (180 deg)
	#  - > Decrement cylinder thickness by percent constant
	#  - < Increment cylinder thickness by percent constant
	#  - [ Push current drawing to stack
	#  - ] Pop current drawing from stack
	#  @param lSentence - the L-System string returned by buildLSystem
	#  @param angle - angle of rotation
	#  @param d - length d
	def draw(self, col, lSentence, angle, d):
		characters = list(lSentence)
		stack = []
		
		a = 0
		accumAngle = ""
		finishedAccumAng = False
		
		t = turtle(h=d)
		# Set whether to add spheres between cylinders
		t.setRounded(rd = self.spheres)
		# Set whether to print the debug log
		t.setDebug(self.debug)
		# Set a pencolor
		if col is not "":
			t.pencolor(col);
		# Percentage of cylinder reduction
		percent = 0.20
		
		for c in characters:
			a = int(accumAngle) if (accumAngle is not '') else angle
			
			if (c == 'F' or c == 'f'):
				t.forward(d)
				a = 0

			if (finishedAccumAng):
				accumAngle = ""

			if (c.isdigit()):
				accumAngle = accumAngle + c
			
			elif (c == '('):
				finishedAccumAng = False
			
			elif (c == ')'):
				finishedAccumAng = True
			
			elif (c == 'L'):
				t.addLeaf(r = 1)

			elif (c == '+'):
				t.yaw(a)
			
			elif (c == '-'):
				t.yaw(-a)
			
			elif (c == '&'):
				t.pitch(a)
			
			elif (c == '^'):
				t.pitch(-a)
			
			elif (c == "\\"):
				t.roll(a)
			
			elif (c == '/'):
				t.roll(-a)
			
			elif (c == '|'):
				a = 180
				t.yaw(a)
			
			elif (c == ">"):
				t.r -= percent * t.r
			
			elif (c == "<"):
				t.r += (percent * t.r)
			
			elif (c == '['):
				tup = (t.curPoint, t.rotVector, t.rotMatrix, t.r)
				stack.append(tup)
			
			elif (c == ']'):
				val = stack.pop()
				t.penup()
				t.setposition(val[0][0], val[0][1], val[0][2])
				t.pendown()
				t.rotVector = val[1]
				t.rotMatrix = val[2]
				t.r = val[3]

			else:
				continue

		return t.getNodes()


	## Generate and draw the fractal resulting from the following parameters
	#  @param n - recursion height
	#  @param sentence -  initial sentence - base for the rule applications
	#  @param a - angle
	#  @param d - step distance
	#  @param rules - a dictionary containing an axiom:rule key:value pair, they're both expected to be strings
	def lSystem(self, col, n, sentence, a, d, rules, sRules):

		lSentence = self.buildLSystem(n, sentence, rules, sRules)
		print (lSentence)
		return self.draw(col, lSentence, a, d)

## Silly test that draws a bunch of cylinders.
def test(d):
	t = turtle(h=d)
		
	t.turn(0)
	t.turn(30)
	t.turn(0)
	
	t.setAxis('X')
	
	t.turn(30)
	t.turn(30)
	
	t.setAxis('Y')
	
	t.turn(-90)
	t.turn(-90)
	t.turn(90)
	t.turn(0)
	t.turn(90)
	
	return t.getNodes()
