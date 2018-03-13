import matrix
import numpy as np
# Assumes SolidPython is in site-packages or elsewhwere in sys.path
from solid import *
from solid.utils import *
from turtle import turtle

class LSystem():
	
	def __init__(self):
		self.spheres = False
		self.debug = False
		self.turtle = turtle()
	
	def printDebug(self, state):
		self.debug = state
	
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
	def buildLSystem(self, n, sentence, rules):
		next = ""
		if (n > 0):
			characters = list(sentence)
			
			for c in characters:
				if (c in rules):
					next += self.buildLSystem(n-1, rules[c], rules);
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
	def draw(self, lSentence, angle, d):
		characters = list(lSentence)
		stack = []
		a = 0
		t = turtle(h=d)
		t.setRounded(rd = self.spheres)
		t.setDebug(self.debug)

		percent = 0.35
		accumAngle = 0;
		
		for c in characters:
			if (c == 'F' or c == 'f'):
				t.forward(d)
				a = 0
			elif (c == '+'):
				a = angle
				t.yaw(a)
			elif (c == '-'):
				a = -angle
				t.yaw(a)
			elif (c == '&'):
				a = angle
				t.pitch(a)
			elif (c == '^'):
				a = -angle
				t.pitch(a)
			elif (c == "\\"):
				a = angle
				t.roll(a)
			elif (c == '/'):
				a = -angle
				t.roll(a)
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
				t.setposition(val[0][0], val[0][1], val[0][2])
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
	def lSystem(self, n, sentence, a, d, rules):
		lSentence = self.buildLSystem(n, sentence, rules)
		return self.draw(lSentence, a, d)

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
