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
		self.addSphere = False
		self.ruleDict = self.treeBuilder.rules.fetchRules()
		self.func = self.treeBuilder.rules.kochCurve1()
		self.initUI()
		
		
	def initUI(self):
		rulesTitle = QLabel('L-System Rules')
		rules = QLabel("F - Move forward a step of length d\n+ - Turn left by angle a\n- - Turn right by angle a\n& - Pitch down by angle a\n^ - Pitch up by angle a\n\ - Roll left by angle a\n/ - Roll right by angle a\n| - Turn arund (180 deg)\n[ - Push current drawing to stack\n] - Pop current drawing from stack")

		pre_Rules = QLabel('Pre-made Rules')
		combo = QComboBox(self)
		for key in self.ruleDict:
			combo.addItem(key)
		combo.activated[str].connect(self.onActivated)

		own_Rules = QLabel('Make Your Own Rules')
		self.ownAngle = QLineEdit()
		self.ownNum = QLineEdit()
		self.ownSentence = QLineEdit()
		self.ownRules = QLineEdit()
		
		spheres = QCheckBox('Add Spheres', self)
		spheres.stateChanged.connect(self.setSpheres)

		rec = QCheckBox('Gen Recursive Trees', self)
		rec.stateChanged.connect(self.setRec)

		build = QPushButton('Build Tree!', self)
		build.clicked.connect(self.on_click)

		grid = QGridLayout()
		grid.setSpacing(10)

		grid.addWidget(pre_Rules, 3, 2)
		grid.addWidget(combo, 4, 2)

		grid.addWidget(own_Rules, 5, 2)
		grid.addWidget(self.ownAngle, 6,2)
		grid.addWidget(self.ownNum, 7,2)
		grid.addWidget(self.ownSentence, 8,2)
		grid.addWidget(self.ownRules, 9,2)

		grid.addWidget(rulesTitle, 1, 3)
		grid.addWidget(rules, 2, 3)
		grid.addWidget(build, 3, 3)

		grid.addWidget(spheres, 3, 4)
		grid.addWidget(rec, 4, 4)

		self.setLayout(grid)
		
#		self.setGeometry(300, 300, 350, 300)
		self.setWindowTitle('Tree Builder')
		self.show()

	def onActivated(self, text):
		self.func = self.ruleDict[text]

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

	def on_click(self):
		rules = self.func
		
		if self.buildRec:
			self.treeBuilder.draw(rec = True)
			subprocess.call(["open", "BuildTree.scad"])
			return
		
		if self.buildOwnTree() is not None:
			rules = self.buildOwnTree()
		
		self.treeBuilder.useSpheres(self.addSphere)
		self.treeBuilder.draw(rule = rules)
		subprocess.call(["open", "BuildTree.scad"])

	def setSpheres(self, state):
		self.addSphere = not self.addSphere

	def setRec(self, state):
		self.buildRec = not self.buildRec

if __name__ == '__main__':
	
	app = QApplication(sys.argv)
	ex = Example()
	sys.exit(app.exec_())
