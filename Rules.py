#! /usr/bin/env python
# -*- coding: UTF-8 -*-
#
## @package Tree
#
# A series of rules to be used in the LSystem.
# Each rule returns an LSystem object containing an angle, a recursion depth, a base sentence, and a list of substitution rules.  
#
# @author Flavia Cavalcanti
# @since 22/02/2018
#

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
		rs = {'F':["F+FF-FF-F-F+F+FF-F-F+F+FF+FF-F", "F+FF-FF-F-F+F+F", "F-F-F+F+FF+FF-F"]}
		return lSystemObj.LSysObj(a, s, i, r, rs)

	## Will slightly traumatize OpenSCAD
	def kochCurve2(self):
		a = 90
		s = "F-F-F-F"
		i = 4
		r = {'F':"FF-F-F-F-F-F+F"}
		rs = {'F':["FF-F-F-F-F-F+F", "FF-F-F-F", "F-F-F+F"]}
		return lSystemObj.LSysObj(a, s, i, r, rs)

	# #Ditto
	def kochCurve3(self):
		a = 90
		s = "F-F-F-F"
		i = 4
		r = {'F':"FF-F-F-F-FF"}
		rs = {'F':["FF-F-F-F-FF", "FF-F-F", "F-F-FF"]}
		return lSystemObj.LSysObj(a, s, i, r, rs)

	def hilbert3D(self):
		a = 90
		s = "X"
		i = 5
		r = {'X':"-F^//XFX&F+//XFX-F/X-/"}
		rs = {}

			#r = {'A':"B-F+CFC+F-D&F∧D-F+&&CFC+F+B//",\
			#'B':"A&F∧CFB∧F∧D∧∧-F-D∧|F∧B|FC∧F∧A//",\
			#'C':"|D∧|F∧B-F+C∧F∧A&&FA&F∧C+F+B∧F∧D//",\
			#'D':"|CFB-F+B|FA&F∧A&&FB-F+B|FC//"}
		return lSystemObj.LSysObj(a, s, i, r, rs)

	def TwoDTree1(self):
		a = 25.7
		s = "F"
		i = 5
		r = {'F':"F[+F]F[-F]F"}
		rs = {'F':["F[+F]F[-F]F", "F[+F]F", "F[-F]F"]}
		return lSystemObj.LSysObj(a, s, i, r, rs)

	def TwoDTree2(self):
		a = 20
		s = "F"
		i = 5
		r = {'F':"F[+F]F[-F][F]"}
		rs = {'F':["F[+F]F[-F][F]", "F[+F]F", "F[-F][F]"]}
		return lSystemObj.LSysObj(a, s, i, r, rs)

	def TwoDTree3(self):
		a = 25.7
		s = "F"
		i = 4
		r = {'F':"FF-[-F+F+F]+[+F-F-F]"}
		rs = {'F':["FF-[-F+F+F]+[+F-F-F]", "FF-[-F+F+F]", "F+[+F-F-F]"]}

		return lSystemObj.LSysObj(a, s, i, r, rs)

	def fractalPlant1(self):
		a = 20
		s = "X"
		i = 7
		r = {'X':"F[+X]F[-X]+X", 'F':"FF"}
		rs = {'X':["F[+X]F[-X]+X", "F[+X]F", "F[-X]+X"], 'F':["FF", "F", "F"]}
		return lSystemObj.LSysObj(a, s, i, r, rs)

	def fractalPlant2(self):
		a = 25.7
		s = "X"
		i = 7
		r = {'X':"F[+X][-X]FX", 'F':"FF"}
		rs = {'X':["F[+X][-X]FX", "F[+X]", "[-X]FX"], 'F':["FF", "F", "F"]}
		return lSystemObj.LSysObj(a, s, i, r, rs)

	def fractalPlant3(self):
		a = 22.5
		s = "X"
		i = 5
		r = {'X':"F-[[X]+X]+F[+FX]-X", 'F':"FF"}
		rs = {'X':["F-[[X]+X]+F[+FX]-X", "F-[[X]+X]", "+F[+FX]-X"],'F':["FF", "F", "F"]}
		return lSystemObj.LSysObj(a, s, i, r, rs)

	def ugly3DTree(self):
		a = 25
		s = "FA"
		i = 8
		r = {'A':"&FFB\\B\\\\\B", 'B':"[&&FF\\\\\\A]"}
		rs = {'A':["&FFB\\B\\\\\B", "&FFB\\", "B\\\\\B"], 'B':["[&&FF\\\\\\A]"]}
		return lSystemObj.LSysObj(a, s, i, r, rs)
	
	def seaweed3D(self):
		c = "orange red"
		a = 22
		s = "F"
		i = 4
		r = {"F":"FF-[&F^F^F]+[^F&F&F][>^F^F&F]"}
		rs = {'F':["FF-[&F^F^F]+[^F&F&F][>^F^F&F]", "FF-[&F^F^F]+", "[^F&F&F][>^F^F&F]"]}
		return lSystemObj.LSysObj(a, s, i, r, rs, color=c)
	
	def pinetree3D(self):
		c = "green"
		a = 37
		s = "ffffA"
		i = 15
		r = {"A":"ff[(90)&TP++P++P++P++P]fAB", "P":"[(10)^fZ]", "Z":"fBZ", "B":"[(80)^[f][(70)+[f](100)+[>f]] [(80)-f]]", "T":"(20)+T"}
		rs = {}
		return lSystemObj.LSysObj(a, s, i, r, rs, color=c)

	def skeletalTree3D(self):
		c = "brown"
		a = 20
		s = "A"
		i = 10
		r = {"A":"[B]////[B]////[B]", "B":"FF&>FFFAL"}
		rs = {"A":["[B]////[B]////[B]","[B]////","[B]////[B]"], "B":["FF&>FFFAL", "FF&>FFFA", "F&>FFFAL"]}
		return lSystemObj.LSysObj(a, s, i, r, rs, color=c)

	def birdNest3D(self):
		c = "brown"
		a = 15
		s = "F"
		i = 3
		r = {"F":"[-&>G][>++&G]||F[--&<G][+&G]FF-[-F+F+F]-[^>F-F-F&<]", "G":"F[+G][-G]F[+G][-G]FG"}
		rs = {}
		return lSystemObj.LSysObj(a, s, i, r, rs, color=c)

	
	def createCustomRule (self, angle, sentence, num, dict):
		a = angle
		s = sentence
		i = num
		r = dict
		return lSystemObj.LSysObj(a, s, i, r, rs)

	def fetchRules(self):
		return {"kochCurve1":self.kochCurve1(), "kochCurve2":self.kochCurve2(), "kochCurve3":self.kochCurve3(), "hilbert3D":self.hilbert3D(), "TwoDTree1":self.TwoDTree1(), "TwoDTree2":self.TwoDTree2(), "TwoDTree3":self.TwoDTree3(), "fractalPlant1":self.fractalPlant1(), "fractalPlant2":self.fractalPlant2(), "fractalPlant3":self.fractalPlant3(), "Tree With Arthritis":self.ugly3DTree(), "3D Seaweed" : self.seaweed3D(), "3D Pine Tree":self.pinetree3D(), "3D Skeletal Tree":self.skeletalTree3D(), "3D Birds Nest":self.birdNest3D()}
