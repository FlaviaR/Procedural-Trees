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
		rules = QLabel("F - Move forward a step of length d\nf  - Move forward a step of length d without drawing a line\n+ - Turn left by angle a\n- - Turn right by angle a\n& - Pitch down by angle a\n^ - Pitch up by angle a\n\ - Roll left by angle a\n/ - Roll right by angle a\n| - Turn arund (180 deg)\n[ - Push current drawing to stack\n] - Pop current drawing from stack")

		pre_Rules = QLabel('Preset Rules')
		combo = QComboBox(self)
		for key in self.ruleDict:
			combo.addItem(key)
		combo.activated[str].connect(self.onActivated)

		own_Rules = QLabel('Make Your Own Rules')
		rulesEdit = QLineEdit()
		
		spheres = QCheckBox('Add Spheres', self)
		spheres.stateChanged.connect(self.setSpheres)

		rec = QCheckBox('Gen Recursive Trees', self)
		rec.stateChanged.connect(self.setRec)

		build = QPushButton('Build Tree!', self)
		build.clicked.connect(self.on_click)

		grid = QGridLayout()
		grid.setSpacing(10)
		
		grid.addWidget(rulesTitle, 1, 0)
		grid.addWidget(rules, 1, 1)

		grid.addWidget(pre_Rules, 2, 0)
		grid.addWidget(combo, 2, 1)

		grid.addWidget(own_Rules, 3, 0)
		grid.addWidget(rulesEdit, 3,1)

		grid.addWidget(spheres, 4, 0)
		grid.addWidget(rec, 4, 1)
		grid.addWidget(build, 4, 2)

		self.setLayout(grid)
		
		self.setGeometry(300, 300, 350, 300)
		self.setWindowTitle('Tree Builder')
		self.show()

	def onActivated(self, text):
		self.func = self.ruleDict[text]

	def on_click(self):
		if self.buildRec:
			self.treeBuilder.draw(rec = True)
			subprocess.call(["open", "BuildTree.scad"])
			return
				
		self.treeBuilder.useSpheres(self.addSphere)
		self.treeBuilder.draw(rule = self.func)
		subprocess.call(["open", "BuildTree.scad"])

	def setSpheres(self, state):
		self.addSphere = not self.addSphere

	def setRec(self, state):
		self.buildRec = not self.buildRec

if __name__ == '__main__':
	
	app = QApplication(sys.argv)
	ex = Example()
	sys.exit(app.exec_())
