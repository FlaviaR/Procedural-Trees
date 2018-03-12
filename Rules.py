import lSystemObj

## Rules taken or modified from:
# @see https://github.com/abiusx/L3D/tree/master/L
# @see http://algorithmicbotany.org/papers/abop/abop.pdf

class Rules():
	
	## Segmentation fault if n > 2 in OpenSCAD
	def kochCurve1(self):
		a = 90
		s = "F-F-F-F"
		i = 2
		r = {'F':"F+FF-FF-F-F+F+FF-F-F+F+FF+FF-F"}
		return lSystemObj.LSysObj(a, s, i, r)

	## Will slightly traumatize OpenSCAD
	def kochCurve2(self):
		a = 90
		s = "F-F-F-F"
		i = 4
		r = {'F':"FF-F-F-F-F-F+F"}
		return lSystemObj.LSysObj(a, s, i, r)

	# #Ditto
	def kochCurve3(self):
		a = 90
		s = "F-F-F-F"
		i = 4
		r = {'F':"FF-F-F-F-FF"}
		return lSystemObj.LSysObj(a, s, i, r)

	def hilbert3D(self):
		a = 90
		s = "A"
		i = 2
		r = {'A':"B-F+CFC+F-D&F∧D-F+&&CFC+F+B//",\
			'B':"A&F∧CFB∧F∧D∧∧-F-D∧|F∧B|FC∧F∧A//",\
			'C':"|D∧|F∧B-F+C∧F∧A&&FA&F∧C+F+B∧F∧D//",\
			'D':"|CFB-F+B|FA&F∧A&&FB-F+B|FC//"}
		return lSystemObj.LSysObj(a, s, i, r)

	def TwoDTree1(self):
		a = 25.7
		s = "F"
		i = 5
		r = {'F':"F[+F]F[-F]F"}
		return lSystemObj.LSysObj(a, s, i, r)

	def TwoDTree2(self):
		a = 20
		s = "F"
		i = 5
		r = {'F':"F[+F]F[-F][F]"}
		return lSystemObj.LSysObj(a, s, i, r)

	def TwoDTree3(self):
		a = 25.7
		s = "F"
		i = 4
		r = {'F':"FF-[-F+F+F]+[+F-F-F]"}
		return lSystemObj.LSysObj(a, s, i, r)

	def fractalPlant1(self):
		a = 20
		s = "X"
		i = 7
		r = {'X':"F[+X]F[-X]+X", 'F':"FF"}
		return lSystemObj.LSysObj(a, s, i, r)

	def fractalPlant2(self):
		a = 25.7
		s = "X"
		i = 7
		r = {'X':"F[+X][-X]FX", 'F':"FF"}
		return lSystemObj.LSysObj(a, s, i, r)

	def fractalPlant3(self):
		a = 22.5
		s = "X"
		i = 5
		r = {'X':"F-[[X]+X]+F[+FX]-X", 'F':"FF"}
		return lSystemObj.LSysObj(a, s, i, r)

	def ugly3DTree(self):
		a = 25
		s = "FA"
		i = 8
		r = {'A':"&FFB\\B\\\\\B", 'B':"[&&FF\\\\\\A]"}
		return lSystemObj.LSysObj(a, s, i, r)
	
	def seaweed3D(self):
		a = 22
		s = "F"
		i = 4
		r = {"F":"FF-[&F^F^F]+[^F&F&F][^F^F&F]"}
		return lSystemObj.LSysObj(a, s, i, r)
	
	def pinetree3D(self):
		a = 37
		s = "ffffA"
		i = 15
		r = {"A":"ff[&(90)TP++P++P++P++P]fAB", "P":"[^(10)fZ]", "Z":"fBZ", "B":"[^(80)[f][+(70)[f]+(100)[f]] [-(80)f]]", "T":"+(20)T"}
		return lSystemObj.LSysObj(a, s, i, r)

	def skeletalTree3D(self):
		a = 20
		s = "A"
		i = 10
		r = {"A":"[B]////[B]////[B]", "B":"&>FFFA"}
		return lSystemObj.LSysObj(a, s, i, r)

	def birdNest3D(self):
		a = 15
		s = "F"
		i = 3
		r = {"F":"[-&>G][>++&G]||F[--&<G][+&G]FF-[-F+F+F]-[^>F-F-F&<]", "G":"F[+G][-G]F[+G][-G]FG"}
		return lSystemObj.LSysObj(a, s, i, r)

	
	def createCustomRule (self, angle, sentence, num, dict):
		a = angle
		s = sentence
		i = num
		r = dict
		return lSystemObj.LSysObj(a, s, i, r)

	def fetchRules(self):
		return {"kochCurve1":self.kochCurve1(), "kochCurve2":self.kochCurve2(), "kochCurve3":self.kochCurve3(), "hilbert3D":self.hilbert3D(), "TwoDTree1":self.TwoDTree1(), "TwoDTree2":self.TwoDTree2(), "TwoDTree3":self.TwoDTree3(), "fractalPlant1":self.fractalPlant1(), "fractalPlant2":self.fractalPlant2(), "fractalPlant3":self.fractalPlant3(), "Tree With Arthritis":self.ugly3DTree(), "3D Seaweed" : self.seaweed3D(), "3D Pine Tree":self.pinetree3D(), "3D Skeletal Tree":self.skeletalTree3D(), "3D Birds Nest":self.birdNest3D()}
