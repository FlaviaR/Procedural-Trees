#! /usr/bin/env python
# -*- coding: UTF-8 -*-
#
## @package tree
#
# Tree generation test - randomized procedural generation
#
# @author Flavia Cavalcanti
# @since 22/02/2018
#

from __future__ import division

import sys
sys.path.append('~/cg/python/OpenPolyhedra')
import numpy as np
import math as math
import matrix
import lSystemObj

# Assumes SolidPython is in site-packages or elsewhwere in sys.path
from solid import *
from solid.utils import *

SEGMENTS = 48

# # ---------------- Rules ------------ ---------------------------------------------------

## Segmentation fault if n > 2 in OpenSCAD
def kochCurve1():
	a = 90
	s = "F-F-F-F"
	i = 2
	r = {'F':"F+FF-FF-F-F+F+FF-F-F+F+FF+FF-F"}
	return lSystemObj.LSysObj(a, s, i, r)

## Will slightly traumatize OpenSCAD
def kochCurve2():
	a = 90
	s = "F-F-F-F"
	i = 4
	r = {'F':"FF-F-F-F-F-F+F"}
	return lSystemObj.LSysObj(a, s, i, r)

# #Ditto
def kochCurve3():
	a = 90
	s = "F-F-F-F"
	i = 4
	r = {'F':"FF-F-F-F-FF"}
	return lSystemObj.LSysObj(a, s, i, r)

def hilbert3D():
	a = 90
	s = "A"
	i = 2
	r = {'A':"B-F+CFC+F-D&F∧D-F+&&CFC+F+B//",\
		'B':"A&F∧CFB∧F∧D∧∧-F-D∧|F∧B|FC∧F∧A//",\
			'C':"|D∧|F∧B-F+C∧F∧A&&FA&F∧C+F+B∧F∧D//",\
		  'D':"|CFB-F+B|FA&F∧A&&FB-F+B|FC//"}
	return lSystemObj.LSysObj(a, s, i, r)

def TwoDTree1():
	a = 25.7
	s = "F"
	i = 5
	r = {'F':"F[+F]F[-F]F"}
	return lSystemObj.LSysObj(a, s, i, r)

def TwoDTree2():
	a = 20
	s = "F"
	i = 5
	r = {'F':"F[+F]F[-F][F]"}
	return lSystemObj.LSysObj(a, s, i, r)

def TwoDTree3():
	a = 25.7
	s = "F"
	i = 4
	r = {'F':"FF-[-F+F+F]+[+F-F-F]"}
	return lSystemObj.LSysObj(a, s, i, r)

def fractalPlant1():
	a = 20
	s = "X"
	i = 7
	r = {'X':"F[+X]F[-X]+X", 'F':"FF"}
	return lSystemObj.LSysObj(a, s, i, r)

def fractalPlant2():
	a = 25.7
	s = "X"
	i = 7
	r = {'X':"F[+X][-X]FX", 'F':"FF"}
	return lSystemObj.LSysObj(a, s, i, r)

def fractalPlant3():
	a = 22.5
	s = "X"
	i = 5
	r = {'X':"F-[[X]+X]+F[+FX]-X", 'F':"FF"}
	return lSystemObj.LSysObj(a, s, i, r)
# # -------//------- Rules ------------ -----------------------///-------------------------

# # ---------------- L-Systems ------------------------------------------------------------

## L-Systems were developed as a mathematical description of plant growth designed to model biological systems.
#  L-Systems can be thought as containing the instructions for how a single cell can grow into a complex organism.
#  They can be used to define the rules for interesting patterns, being particularly useful for fractal creation.
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
def buildLSystem(n, sentence, rules):
	next = ""
	if (n > 0):
		characters = list(sentence)
		
		for c in characters:
			if (c in rules):
				next += buildLSystem(n-1, rules[c], rules);
			else:
				next += c
	else:
		return sentence
	
	return next


## Rotate the given vector about the x axis.
#
#  @param array given vector.
#  @param a rotation angle in degrees.
#
def xAxisRot(array, a):
	a = np.deg2rad(a)
	c = cos(a)
	s = sin(a)
	x = [[1, 0,  0, 0], \
		 [0, c, -s, 0], \
		 [0, s,  c, 0], \
		 [0, 0,  0, 1]]
	return np.dot(array, x)

## Rotate the given vector about the y axis.
#
#  @param array given vector.
#  @param a rotation angle in degrees.
#
def yAxisRot(array, a):
	a = np.deg2rad(a)
	c = cos(a)
	s = sin(a)
	y = [[ c, 0, s, 0], \
		 [ 0, 1, 0, 0], \
		 [-s, 0, c, 0], \
		 [ 0, 0, 0, 1]]
	return np.dot(array, y)

## Rotate the given vector about the z axis.
#
#  @param array given vector.
#  @param a rotation angle in degrees.
#
def zAxisRot(array, a):
	a = np.deg2rad(a)
	c = cos(a)
	s = sin(a)
	z = [[c, -s, 0, 0], \
		 [s,  c, 0, 0], \
		 [0,  0, 1, 0], \
		 [0,  0, 0, 1]]
	return np.dot(array, z)


## A simple 3D turtle graphics.
#
#  @see https://docs.python.org/3/library/turtle.html#turtle.right
#  @see http://new.math.uiuc.edu/math198/MA198-2015/nwalter2/index.html
#  <br>
class turtle(object):
	## Constructor.
	#
	#  The cylinder in openscad is centered about the z axis.
	#  @see https://en.wikibooks.org/wiki/OpenSCAD_User_Manual/The_OpenSCAD_Language#cylinder
	#
	#  @param r Cylinder radius.
	#  @param h Cylinder height.
	#
	def __init__(self, r=2, h=10):
		## Cylinder radius.
		self.r = r
		
		## Cylinder height.
		self.h = h
		
		## A list with openscad primitives.
		self.nodes = []
		
		## Current position.
		self.curPoint = np.array([0,  0,  0, 1])
		
		## Rotation axis.
		self.axis = [0,  0,  -1]
		self.rotFunc = zAxisRot
		self.curVector = np.array([0, self.h, 0, 0])
		self.Z = True
		self.curAng = 0
	
	## Sets the rotation axis.
	#
	#  @param axis character identifying a coordinate axis.
	#
	def setAxis(self, axis):
		## Indicates rotations about Z axis.
		self.Z = False
		
		## Current angle.
		# self.curAng = 0
		if axis == 'X':
			if (self.axis != [-1, 0, 0]):
				## Rotation axis.
				self.axis  = [-1,  0,  0]
				## Points to the function that rotates about the chosen axis.
				self.rotFunc = xAxisRot
				## Current direction.
				self.curVector = np.array([0, 0, self.h, 0])
		elif axis == 'Y':
			if (self.axis != [0, -1, 0]):
				self.axis = [0,  -1,  0]
				self.rotFunc = yAxisRot
				self.curVector = np.array([0, 0, self.h, 0])
		else:
			self.Z = True
			
			if (self.axis != [0, 0, -1]):
				self.curAng = 0
				self.axis = [0,  0,  -1]
				self.rotFunc = zAxisRot
				self.curVector = np.array([0, self.h, 0, 0])
#exit("Invalid rotation axis")


	## Make a turn by a given angle onto plane:
	#  - xz (rotation about y axis)
	#  - yz (rotation about x axis)
	#  - xy (rotation about z axis)
	#
	#  according to what has been set in #setAxis.
	#
	#  Add a new object (cylinder plus sphere) to the model and update the current position.
	#
	#  @param ang deviation from the previous direction.
	#
	def turn(self,ang):
		self.curAng += ang
		if self.Z:
			self.nodes.append(
							  (translate(self.curPoint.tolist()[:-1]))	# remove fourth coordinate
							  (rotate(a = [-90, 0, self.curAng]) 		# rotation order: x, y and z
							   #(sphere(self.r))
							   (cylinder(self.r, self.h))))
		else:
			self.nodes.append(
							  (translate(self.curPoint.tolist()[:-1]))	# remove fourth coordinate
							  (rotate(a = self.curAng, v = self.axis)		# entering the screen
							   #(sphere(self.r))
							   (cylinder(self.r, self.h))))
		
		if True:
			if self.Z: ang = -ang
			self.curVector = self.rotFunc(self.curVector, ang )
		else:
			if not self.Z: ang = -ang
			mat = matrix.rotate(ang, self.axis[0], self.axis[1], self.axis[2])
			mat = mat.tolist()
			self.curVector = np.dot (self.curVector, mat)
			# update current position
		self.curPoint = np.add(self.curPoint, self.curVector)

	#print("curPoint = %s" % self.curPoint)
	#print("curVector = %s" % self.curVector)
	#print("curAng = %f\n" % self.curAng)

	## Return the nodes created so far.
	#  @return a union with the node list.
	#
	def getNodes(self):
		return union()(self.nodes)


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
#  - [ Push current drawing to stack
#  - ] Pop current drawing from stack
#  @param lSentence - the L-System string returned by buildLSystem
#  @param angle - angle of rotation
#  @param d - length d
def draw(lSentence, angle, d):
	characters = list(lSentence)
	stack = []
	a = 0
	t = turtle(h=d)
	
	for c in characters:
		if (c == 'F'):
			t.turn(a)
			a = 0
		#elif (c == 'f'):
		elif (c == '+'):
			a = angle
			t.setAxis('Z')
		elif (c == '-'):
			a = -angle
			t.setAxis('Z')
		elif (c == '&'):
			a = angle
			t.setAxis('Y')
		elif (c == '^'):
			a = -angle
			t.setAxis('Y')
		elif (c == "\\"):
			a = angle
			t.setAxis('X')
		elif (c == '/'):
			a = -angle
			t.setAxis('X')
		elif (c == '|'):
			a = 180
			t.setAxis('X')
		elif (c == '['):
			tup = (t.curPoint, t.curVector, t.curAng)
			stack.append(tup)
		elif (c == ']'):
			val = stack.pop()
			t.curPoint = val[0]
			t.curVector = val[1]
			t.curAng = val[2]
		else:
			continue

	return t.getNodes()


## Generate and draw the fractal resulting from the following parameters
#  @param n - recursion height
#  @param sentence -  initial sentence - base for the rule applications
#  @param a - angle
#  @param d - step distance
#  @param rules - a dictionary containing an axiom:rule key:value pair, they're both expected to be strings
def lSystem(n, sentence, a, d, rules):
	lSentence = buildLSystem(n, sentence, rules)
	return draw(lSentence, a, d)

# # ------//-------- L-Systems ----------------------///------------------------------------

# ---------------- Recursive Definition ----------------------------------------------------

## The tree is represented completely by cylinders
# <pre>
#           add Stem and Leaf,                                                      if n <= 0
#         /
# Tree (n)
#         \ translate([0, 0, (position of branch in relation to its parent)])       if n > 0
#           (scale(scaleFactor)(rotate(a = [xRot, 0, (angle of rot - around parent's circumference)])
#           (genTree(numIter - 1, scaleFactor, xRot))))
#
#           ~xRot and scaleFactor are randomely selected values~
#
# </pre>
# @see https://github.com/yosinski/OpenSCAD-playground/blob/master/tree.py

def rn(aa, bb):
	'''A Normal random variable generator that takes a range, like
		random.uniform, instead of mean and standard deviation.'''
	
	return np.random.normal((bb+aa)/2., (bb-aa)/4.)

ru = np.random.uniform

ri = np.random.randint

## Create a stem and leaf
def stemAndLeaf():
	# Radius and height of the stem
	stemR = rn(.9, 1.1)
	stemH = rn(8, 12)
	
	# Radius and height of the leaf
	leafR = rn(4, 6)
	leafH = rn(.8, 1.2)
	
	# The stem will be represented by a cylynder with radius = stemR and height = stemH
	# Note that a small number of fragments are used to model the cylinder
	cylStem = cylinder(r = stemR, h = stemH)
	cylStem.add_param('$fn', ri(4, 8))
	
	# The leaf will be represented by a cylynder with radius = leafR and height = leafH
	# Note that the leaf height is very short, and only a small number of fragments
	# are used to model the cylinder - giving the leaves their "pentagon" shape
	cylLeaf = cylinder(r = leafR, h = leafH)
	cylLeaf.add_param('$fn', ri(4, 8))
	
	# Perform a union on the stem and leaf cylinders
	# Make sure the stems are halfway through the leaves
	return union()(
				   cylStem,
				   translate([0, 0, stemH - (leafH)/2.])(cylLeaf),
				   )


## Recursive method to generate more branches in the tree
#  @param numIter - number of iterations
#  @param scaleFactor - branch scale factor
#  @param xRot - x-axis angle of rotation
def addBranches(numIter = 3, scaleFactor = 0.7, xRot = 15):
	# Calculate the number of new branches to be atteched to the last generated branch
	numBranches = ri(3, 5)
		
	# Radius and height of the stem
	stemR = rn(.9, 1.1)
	stemH = rn(8, 12)
	
	# Branch scaling factor
	scaleFactor = rn(.6, .8)
	
	# Append the 'base' stem to the nodes list
	nodes = []
	nodes.append(cylinder(r = stemR, h = stemH))
	
	# For each of the children branches, calculate a random position
	branchPos = [ru(.4, 1) for i in range(numBranches)]
	maxBP = max(branchPos)
	
	# Transform each branch position to be the ratio of the
	# current branch position : the position of the farthest branch
	branchPos = [branchPos[i] / maxBP for i in range(numBranches)]
	for i in range(numBranches):
		# Generate a random x-axis rotation
		xRot = rn(35, 55)
		# Prevent branches from being placed too close together
		zRot = i * (360./numBranches)
		# Position in relation to parent
		posIRP = branchPos[i] * stemH * .9
		
		# Append the newly created branch (with its designated position and scale) to the nodes list
		nodes.append(
					 translate([0, 0, posIRP])
					 (scale(scaleFactor)(rotate(a = [xRot, 0, zRot])
										 (genTree(numIter - 1, scaleFactor, xRot))))
					 )
	# Perform a union on all branches in the node list
	return union()(nodes)

def genTree(numIter = 3, scaleFactor = .7, xRot = 15):
	# attach a leaf and stem to the end of the branch
	if numIter <= 0:
		return stemAndLeaf()
	else:
		return addBranches(numIter, scaleFactor, xRot)

# -------//------- Recursive Definition -----------------------///-------------------------


## Given a union of nodes, return the union of the tree with a base
#  @param tree - a union of nodes that composes the tree
def treeWithBase(tree):
	base = cylinder(r = 6, h = .75)
	base.add_param('$fn', 40)
	
	trunk1 = cylinder(r1 = 3.5, r2 = 0, h = 2)
	trunk1.add_param('$fn', 5)
	
	trunk2 = cylinder(r1 = 2, r2 = 0, h = 4)
	trunk2.add_param('$fn', 5)
	
	return union()(
				   base,
				   trunk1,
				   trunk2,
				   tree,
				   )

if __name__ == '__main__':
	
	#recTree = treeWithBase(genTree(5))
	
	lSysO = fractalPlant2()
	lTree = lSystem(lSysO.iterations, lSysO.sentence, lSysO.angle, 4, lSysO.rules)
	
	scad_render_to_file(lTree, file_header='$fn = %s;' % SEGMENTS, include_orig_code=True)

