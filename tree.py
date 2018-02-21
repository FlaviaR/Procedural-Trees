# Tree generation test - randomized procedural generation

#! /usr/bin/env python
# -*- coding: UTF-8 -*-
from __future__ import division
import os
import sys
import re
from numpy import array, random, cross


# Assumes SolidPython is in site-packages or elsewhwere in sys.path
from solid import *
from solid.utils import *

SEGMENTS = 48

# # ---------------- L-Systems ------------------------------------------------------------

# L-Systems were developed as a mathematical description of plant growth designed to model biological systems.
# L-Systems can be thought as containing the instructions for how a single cell can grow into a complex organism.
# They can be used to define the rules for interesting patterns, being particularly useful for fractal creation.
# Example usage:
# A	      - Axiom
# A -> B  - Rule 1 Change A to B
# B -> AB - Rule 2 Change B to AB
# @see - http://interactivepython.org/courselib/static/thinkcspy/Strings/TurtlesandStringsandLSystems.html


# F move forward a step of length d
# f Move forward a step of length d without drawing a line
# + Turn left by angle a
# - Turn right by angle a
# & Pitch down by angle a
# ^ Pitch up by angle a
# \ Roll left by angle a
# / Roll right by angle a
# | Turn arund (180 deg)
#def draw(n, a, d, axiom, rule):
def draw(n, sentence):
	next = ""
	if (n > 0):
		characters = list(sentence)

		for c in characters:
			if (c == 'X'):
				next += draw(n-1, "F-[[X]+X]+F[+FX]-X");
			elif (c == 'F'):
				next += draw(n-1, "FF");
			else:
				next += c
	else:
		next = sentence

	return next

# Generate the L-System string based off of the following parameters
# @param a - angle
# @param d - step distance
# @param axiom
# @param rule - rule descriptor
# def lSystem(n, a, d, axiom, rule):


# # ------//-------- L-Systems ----------------------///------------------------------------


# ---------------- Recursive Definition ----------------------------------------------------

# The tree is represented completely by cylinders
#           add Stem and Leaf,														if n <= 0
#		  /
# Tree (n)
#         \ translate([0, 0, (position of branch in relation to its parent)])		if n > 0
#			(scale(scaleFactor)(rotate(a = [xRot, 0, (angle of rot - around parent's circumference)])
#			(genTree(numIter - 1, scaleFactor, xRot))))
#
#			~xRot and scaleFactor are randomely selected values~
#
# Expanded from https://github.com/yosinski/OpenSCAD-playground/blob/master/tree.py

def rn(aa, bb):
	'''A Normal random variable generator that takes a range, like
	random.uniform, instead of mean and standard deviation.'''
    
	return random.normal((bb+aa)/2., (bb-aa)/4.)

ru = random.uniform

ri = random.randint

# Create a stem and leaf
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

# Recursive method to generate more branches in the tree
# @param scaleFactor - branch scale factor 
# @param xRot - x-axis angle of rotation
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

def treeWithBase():
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
		genTree(5),                  
	)

# -------//------- Recursive Definition -----------------------///-------------------------

if __name__ == '__main__':
	# n = 5, angle = 25.7
	# Axiom - F
	# Rule  - F[+F]F[-F]F
	print(draw(3, 'X'))
	#a = treeWithBase()
	#scad_render_to_file(a, file_header='$fn = %s;' % SEGMENTS, include_orig_code=True)
