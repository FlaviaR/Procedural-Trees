import numpy as np
import math as math

# Assumes SolidPython is in site-packages or elsewhwere in sys.path
from solid import *
from solid.utils import *

class RecTree():
	
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

	def rn(self, aa, bb):
		'''A Normal random variable generator that takes a range, like
			random.uniform, instead of mean and standard deviation.'''

		return np.random.normal((bb+aa)/2., (bb-aa)/4.)

	ru = np.random.uniform

	ri = np.random.randint

	## Create a stem and leaf
	def stemAndLeaf(self):
		# Radius and height of the stem
		stemR = self.rn(.9, 1.1)
		stemH = self.rn(8, 12)

		# Radius and height of the leaf
		leafR = self.rn(4, 6)
		leafH = self.rn(.8, 1.2)

		# The stem will be represented by a cylynder with radius = stemR and height = stemH
		# Note that a small number of fragments are used to model the cylinder
		cylStem = cylinder(r = stemR, h = stemH)
		cylStem.add_param('$fn', self.ri(4, 8))

		# The leaf will be represented by a cylynder with radius = leafR and height = leafH
		# Note that the leaf height is very short, and only a small number of fragments
		# are used to model the cylinder - giving the leaves their "pentagon" shape
		cylLeaf = cylinder(r = leafR, h = leafH)
		cylLeaf.add_param('$fn', self.ri(4, 8))

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
	def addBranches(self, numIter = 5, scaleFactor = 0.7, xRot = 15):
		# Calculate the number of new branches to be atteched to the last generated branch
		numBranches = self.ri(3, 5)

		# Radius and height of the stem
		stemR = self.rn(.9, 1.1)
		stemH = self.rn(8, 12)

		# Branch scaling factor
		scaleFactor = self.rn(.6, .8)

		# Append the 'base' stem to the nodes list
		nodes = []
		nodes.append(cylinder(r = stemR, h = stemH))

		# For each of the children branches, calculate a random position
		branchPos = [self.ru(.4, 1) for i in range(numBranches)]
		maxBP = max(branchPos)

		# Transform each branch position to be the ratio of the
		# current branch position : the position of the farthest branch
		branchPos = [branchPos[i] / maxBP for i in range(numBranches)]
		for i in range(numBranches):
			# Generate a random x-axis rotation
			xRot = self.rn(35, 55)
			# Prevent branches from being placed too close together
			zRot = i * (360./numBranches)
			# Position in relation to parent
			posIRP = branchPos[i] * stemH * .9
			
			# Append the newly created branch (with its designated position and scale) to the nodes list
			nodes.append(
						 translate([0, 0, posIRP])
						 (scale(scaleFactor)
						 (rotate(a = [xRot, 0, zRot])
						 (self.genTree(numIter - 1, scaleFactor, xRot))))
						 )
		# Perform a union on all branches in the node list
		return union()(nodes)

	def genTree(self, numIter = 4, scaleFactor = .7, xRot = 15):
		# attach a leaf and stem to the end of the branch
		if numIter <= 0:
			return self.stemAndLeaf()
		else:
			return self.addBranches(numIter, scaleFactor, xRot)
