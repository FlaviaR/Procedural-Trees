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
		orientation = QComboBox(self)
		for axis in self.axisList:
			orientation.addItem(axis)
		orientation.activated[str].connect(self.onActivatedOri)
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

		grid.addWidget(rulesTitle, 1, 1)
		grid.addWidget(rules, 2, 1)

		grid.addWidget(pre_Rules, 3, 1)
		grid.addWidget(combo, 4, 1)

		grid.addWidget(options, 5, 1)
		grid.addWidget(orientation, 6, 1)
		grid.addWidget(spheres, 7, 1)
		grid.addWidget(base, 8, 1)
		grid.addWidget(debug, 9, 1)
		grid.addWidget(rec, 10, 1)

		grid.addWidget(own_Rules, 11, 1)
		grid.addWidget(self.ownAngle, 12,1)
		grid.addWidget(self.ownNum, 13,1)
		grid.addWidget(self.ownSentence, 14,1)
		grid.addWidget(self.ownRules, 15,1)

		grid.addWidget(build, 16, 1)


		self.setLayout(grid)
		
#		self.setGeometry(300, 300, 350, 300)
		self.setWindowTitle('Tree Builder')
		self.show()

	def onActivated(self, text):
		self.func = self.ruleDict[text]

	def onActivatedOri(self, axis):
		if (axis is not "Orientation"):
			self.treeBuilder.axis = axis

	## Allows a user to create their own tree according to their given L-System rules and parameters.
	def buildOwnTree(self):
		angle = self.ownAngle.text()
		num = self.ownNum.text()
		sentence = self.ownSentence.text()
		rules = self.ownRules.text()
		
		if (angle is '' or num is '' or sentence is '' or rules is ''):
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
