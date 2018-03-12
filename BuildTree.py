#! /usr/bin/env python
# -*- coding: UTF-8 -*-
#
## @package Tree
#
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

	def draw(self, rec = False, rule = None, addBase = False):
		if rec:
			lTree = self.recTree.genTree()
		elif not rec and rule is not None:
			lTree = self.lSys.lSystem(rule.iterations, rule.sentence, rule.angle, 4, rule.rules)
		if addBase:
			lTree = self.treeWithBase(lTree)
		
		scad_render_to_file(lTree, file_header='$fn = %s;' % self.SEGMENTS, include_orig_code=True)

	def useBase(self, state):
		self.base = state

	def printDebug(self, state):
		self.lSys.printDebug(state)
	
	def useSpheres(self, state):
		self.lSys.useSpheres(state)
	
	## Given a union of nodes, return the union of the tree with a base
	#  @param tree - a union of nodes that composes the tree
	def treeWithBase(self, tree):
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
	tree = BuildTree()
	
	tree.draw(rule = tree.rules.kochCurve2())

