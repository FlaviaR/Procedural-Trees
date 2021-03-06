#! /usr/bin/env python
# -*- coding: UTF-8 -*-
#
## @package Tree
# Returns a tree model generated by the LSystem file. 
#
# @author Flavia Cavalcanti
# @since 22/02/2018
#

from __future__ import division

import sys
sys.path.append('~/cg/python/OpenPolyhedra')
import numpy as np
import math as math

from LSystems import LSystem
from RecTree import RecTree
from Rules import Rules

# Assumes SolidPython is in site-packages or elsewhwere in sys.path
from solid import *
from solid.utils import *

class BuildTree():

	SEGMENTS = 48
	
	def __init__(self):
		self.recTree = RecTree()
		self.lSys = LSystem()
		self.rules = Rules()
		self.base = False
		self.axis = "+X"
		self.diameter = 6
		self.filepathCounter = 0
	
	## Draws a tree in the orientation defined by the axis class variable.
	#  The tree can be either purely recursive or use l-system rules. A Base can be added to the model.
	def draw(self, rec = False, rule = None):
		if rec:
			# Rotate the tree that is built on the Z axis by the default to alignn to the X axis
			lTree = rotate(a = 90, v = [0,1,0])(self.recTree.genTree())
		if not rec and rule is not None:
			lTree = self.lSys.lSystem(rule.color, rule.iterations, rule.sentence, rule.angle, 4, rule.rules, rule.rulesStochastic)

		rot = self.fetchRot()
		lTree = rotate(a = rot[1], v = rot[0])(lTree)

		if self.base:
			lTree = union() (lTree, self.treeWithBase())
		
		self.filepathCounter += 1
		
		scad_render_to_file(lTree, filepath = "lSystemModel" + str(self.filepathCounter) + ".scad", file_header='$fn = %s;' % self.SEGMENTS, include_orig_code=True)
		

	## Defines whether to apply a stochastic interpretation of the rules  to the tree model or not.
	def useStochastic(self, state):
		self.lSys.useStochastic(state)
	
	## Defines whether to add a base to the tree model or not.
	def useBase(self, state):
		self.base = state

	## Defines whether to print out the debugging log or not.
	def printDebug(self, state):
		self.lSys.printDebug(state)
	
	## Defines whether to add spheres between cylinder connections or not.
	def useSpheres(self, state):
		self.lSys.useSpheres(state)
	
	## Returns a tupple containing the rotation axis and angle for the tree as well as the ones for the base
	#  Structure (Rot axis for tree, Rot angle for tree, Rot axis for base, Rot angle for base)
	def fetchRot(self):
		if self.axis == "+X":
			return ([1, 0, 0], 0, [0, 1, 0], 90)
		elif self.axis == "+Y":
			return ([0, 0, 1], 90, [1, 0, 0], -90)
		elif self.axis == "+Z":
			return ([0, 1, 0], -90, [0, 0, 1], 0)
		elif self.axis == "-X":
			return ([0, 1, 0], 180, [0, 1, 0], -90)
		elif self.axis == "-Y":
			return ([0, 0, 1], -90, [1, 0, 0], 90)
		elif self.axis == "-Z":
			return ([0, 1, 0], 90, [0, 1, 0], 180)


	
	## Given a union of nodes, return the union of the tree with a base
	#  @param tree - a union of nodes that composes the tree
	def treeWithBase(self):
		base = cylinder(r = self.diameter, h = 2)
		base.add_param('$fn', 40)
		
		rTrunk1 = 20 if self.diameter >= 35 else 5.5
		hTrunk1 = 10 if self.diameter >= 35 else 5
		trunk1 = cylinder(r1 = rTrunk1, r2 = 0, h = hTrunk1)
		trunk1.add_param('$fn', 5)
		
		trunk2 = cylinder(r1 = 2, r2 = 0, h = 4)
		trunk2.add_param('$fn', 5)
		
		rot = self.fetchRot()
		return union()(
					   rotate(a = rot[3], v = rot[2])
					   (base,
						trunk1,
						trunk2)
					   )

if __name__ == '__main__':
	
	#recTree = treeWithBase(genTree(5))
	tree = BuildTree()
	
	tree.draw(rule = tree.rules.kochCurve2())

