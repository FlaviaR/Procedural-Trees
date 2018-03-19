#! /usr/bin/env python
# -*- coding: UTF-8 -*-
#
## @package Tree
# Interface to control the user inputs to generate the recursive models. 
#
# @author Flavia Cavalcanti
# @since 22/02/2018
#

import sys
import subprocess
from BuildTree import BuildTree
from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit, QComboBox, QPushButton,
							 QCheckBox, QTextEdit, QGridLayout, QApplication)


class Example(QWidget):
	
	def __init__(self):
		super().__init__()
		self.treeBuilder = BuildTree()
		self.buildRec = False
		self.ruleDict = self.treeBuilder.rules.fetchRules()
		self.axisList = ["Orientation", "+X", "+Y", "+Z", "-X", "-Y", "-Z"]
		self.diameterList = ["Base Diameter - Default 6", "6", "20", "35", "45", "60", "75"]
		self.func = self.treeBuilder.rules.kochCurve1()
		self.initUI()
		
		
	def initUI(self):
		rulesTitle = QLabel('----------L-System Rules-----------')
		rules = QLabel("F - Move forward a step of length d\n+ - Turn left by angle a\n- - Turn right by angle a\n& - Pitch down by angle a\n^ - Pitch up by angle a\n\ - Roll left by angle a\n/ - Roll right by angle a\n| - Turn arund (180 deg)\n[ - Push current drawing to stack\n] - Pop current drawing from stack")

		pre_Rules = QLabel('----------Pre-made Rules----------')
		combo = QComboBox(self)
		for key in self.ruleDict:
			combo.addItem(key)
		combo.activated[str].connect(self.onActivated)

		options = QLabel('---------------Options---------------')
		
		stochastic = QCheckBox('Stochastic L-Systems', self)
		stochastic.stateChanged.connect(self.setStochastic)
		
		orientation = QComboBox(self)
		for axis in self.axisList:
			orientation.addItem(axis)
		orientation.activated[str].connect(self.onActivatedOri)
		
		diameter = QComboBox(self)
		for d in self.diameterList:
			diameter.addItem(d)
		diameter.activated[str].connect(self.onActivatedDiameter)
		
		spheres = QCheckBox('Add Spheres', self)
		spheres.stateChanged.connect(self.setSpheres)
		base = QCheckBox('Add Base To Model', self)
		base.stateChanged.connect(self.setBase)
		debug = QCheckBox('Set Debug', self)
		debug.stateChanged.connect(self.setDebug)
		rec = QCheckBox('No L-System - Recursive Tree', self)
		rec.stateChanged.connect(self.setRec)

		own_Rules = QLabel('--------Make Your Own Rules--------')
		self.ownAngle = QLineEdit()
		self.ownNum = QLineEdit()
		self.ownSentence = QLineEdit()
		self.ownRules = QLineEdit()

		build = QPushButton('Build Tree!', self)
		build.clicked.connect(self.on_click)

		grid = QGridLayout()
		grid.setSpacing(10)
		
		interfaceComponents = [rulesTitle, rules, pre_Rules, combo, options, stochastic, orientation, spheres, base, diameter, debug, rec, own_Rules, self.ownAngle, self.ownNum, self.ownSentence, self.ownRules, build]

		i = 0
		for component in interfaceComponents:
			grid.addWidget(component, i, 1)
			i += 1

		self.setLayout(grid)
		
#		self.setGeometry(300, 300, 350, 300)
		self.setWindowTitle('Tree Builder')
		self.show()

	def onActivated(self, text):
		self.func = self.ruleDict[text]

	def onActivatedOri(self, axis):
		if ("Orientation" not in axis):
			self.treeBuilder.axis = axis

	def onActivatedDiameter(self, d):
		if (d.isdigit()):
			self.treeBuilder.diameter = float(d)

	## Allows a user to create their own tree according to their given L-System rules and parameters.
	def buildOwnTree(self):
		angle = self.ownAngle.text()
		num = self.ownNum.text()
		sentence = self.ownSentence.text()
		rules = self.ownRules.text()
		
		if (not angle):
			return None
		else:

			angle = float(angle)
			num = int(num)

			rules = rules.split(',')
			d = {}
			i = 0
			while i < len(rules) - 1:
				key = rules[i]
				val = rules[i+1]
				if key is not "" and val is not "":
					d[key] = val
				i += 2
			return self.treeBuilder.rules.createCustomRule(angle, sentence, num, d)

	## When the 'Build Tree" button is pressed, a tree model is generated according to the
	#  selected options in the interface.
	def on_click(self):
		rules = self.func
		
		if self.buildRec:
			self.treeBuilder.draw(rec = True)
			subprocess.call(["open", "BuildTree.scad"])
			return
		
		if self.buildOwnTree() is not None:
			rules = self.buildOwnTree()
		
		self.treeBuilder.draw(rule = rules)
		subprocess.call(["open", "BuildTree.scad"])

	def setStochastic(self, state):
		self.treeBuilder.useStochastic(state)
	
	## Sets treeBuilder to add spheres in between cylinders according to the 'state' param.
	def setSpheres(self, state):
		self.treeBuilder.useSpheres(state)

	## Sets treeBuilder to print the debug log according to the 'state' param.
	def setDebug(self, state):
		self.treeBuilder.printDebug(state)

	## Sets treeBuilder to add a base to the tree model according to the 'state' param.
	def setBase(self, state):
		self.treeBuilder.useBase(state)

	## Sets the buildRec variable - if this variable is set, then the tree built will be
	#  purely recursive and will not use the L-System rules.
	def setRec(self, state):
		self.buildRec = not self.buildRec

if __name__ == '__main__':
	
	app = QApplication(sys.argv)
	ex = Example()
	sys.exit(app.exec_())
