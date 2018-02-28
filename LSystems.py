import matrix
import numpy as np
# Assumes SolidPython is in site-packages or elsewhwere in sys.path
from solid import *
from solid.utils import *

## Rotate the given vector about the x axis.
#
#  @param array given vector.
#  @param a rotation angle in degrees.
#
def xAxisRot(array, a):
	a = np.deg2rad(a)
	c = cos(a)
	s = sin(a)
	x = [[1, 0,  0, 0], \
		 [0, c, -s, 0], \
		 [0, s,  c, 0], \
		 [0, 0,  0, 1]]
	return np.dot(array, x)
	
## Rotate the given vector about the y axis.
#
#  @param array given vector.
#  @param a rotation angle in degrees.
#
def yAxisRot(array, a):
	a = np.deg2rad(a)
	c = cos(a)
	s = sin(a)
	y = [[ c, 0, s, 0], \
		 [ 0, 1, 0, 0], \
		 [-s, 0, c, 0], \
		 [ 0, 0, 0, 1]]
	return np.dot(array, y)

## Rotate the given vector about the z axis.
#
#  @param array given vector.
#  @param a rotation angle in degrees.
#
def zAxisRot(array, a):
	a = np.deg2rad(a)
	c = cos(a)
	s = sin(a)
	z = [[c, -s, 0, 0], \
		 [s,  c, 0, 0], \
		 [0,  0, 1, 0], \
		 [0,  0, 0, 1]]
	return np.dot(array, z)


## A simple 3D turtle graphics.
#
#  @see https://docs.python.org/3/library/turtle.html#turtle.right
#  @see http://new.math.uiuc.edu/math198/MA198-2015/nwalter2/index.html
#  <br>
class turtle(object):
	## Constructor.
	#
	#  The cylinder in openscad is centered about the z axis.
	#  @see https://en.wikibooks.org/wiki/OpenSCAD_User_Manual/The_OpenSCAD_Language#cylinder
	#
	#  @param r Cylinder radius.
	#  @param h Cylinder height.
	#
	def __init__(self, r=2, h=10):
		## Cylinder radius.
		self.r = r
		
		## Cylinder height.
		self.h = h
		
		## A list with openscad primitives.
		self.nodes = []
		
		## Current position.
		self.curPoint = np.array([0,  0,  0, 1])
		
		# Indicates the rotation direction.
		self.dir = None
		
		## Rotation axis.
		self.setAxis('Z')

		## Whether to add spheres in between cylinder connections
		self.useSpheres = False
	
	
	## Sets the rotation axis.
	#
	#  @param dir character identifying a coordinate axis: X, Y or Z.
	#
	def setAxis(self, dir):
		if dir == self.dir :
			return # nothing has changed
		
		## Current angle.
		self.curAng = 0
		self.dir = dir
		
		if dir == 'X':
			## Rotation axis.
			self.axis  = [-1,  0,  0]
			## Points to the function that rotates about the chosen axis.
			self.rotFunc = xAxisRot
			## Current direction.
			self.curVector = np.array([0, 0, self.h, 0])
		elif dir == 'Y':
			self.axis = [0,  -1,  0]
			self.rotFunc = yAxisRot
			self.curVector = np.array([0, 0, self.h, 0])
		else:
			self.axis = [0,  0,  -1]
			self.rotFunc = zAxisRot
			self.curVector = np.array([0, self.h, 0, 0])
	#exit("Invalid rotation axis")



	## Make a turn by a given angle onto plane:
	#  - xz (rotation about y axis)
	#  - yz (rotation about x axis)
	#  - xy (rotation about z axis)
	#
	#  according to what has been set in #setAxis.
	#
	#  Add a new object (cylinder plus sphere) to the model and update the current position.
	#
	#  @param ang deviation from the previous direction.
	#
	def turn(self,ang):
		self.curAng += ang
		print (self.useSpheres)
		if self.dir == 'Z':
			if self.useSpheres:
				self.nodes.append(
								  (translate(self.curPoint.tolist()[:-1]))	# remove fourth coordinate
								  (rotate(a = [-90, 0, self.curAng]) 		# rotation order: x, y and z
								  (sphere(self.r))
								  (cylinder(self.r, self.h))))
			else:
				self.nodes.append(
								  (translate(self.curPoint.tolist()[:-1]))	# remove fourth coordinate
								  (rotate(a = [-90, 0, self.curAng]) 		# rotation order: x, y and z
								  (cylinder(self.r, self.h))))
		else:
			if self.useSpheres:
				self.nodes.append(
								  (translate(self.curPoint.tolist()[:-1]))	# remove fourth coordinate
								  (rotate(a = self.curAng, v = self.axis)		# entering the screen
								  (sphere(self.r))
								  (cylinder(self.r, self.h))))
			else:
				self.nodes.append(
								  (translate(self.curPoint.tolist()[:-1]))	# remove fourth coordinate
								  (rotate(a = self.curAng, v = self.axis)		# entering the screen
								  (cylinder(self.r, self.h))))

		if True:
			if self.dir == 'Z': ang = -ang
			self.curVector = self.rotFunc(self.curVector, ang )
		else:
			if not self.dir == 'Z': ang = -ang
			mat = matrix.rotate(ang, self.axis[0], self.axis[1], self.axis[2])
			mat = mat.tolist()
			self.curVector = np.dot (self.curVector, mat)
			# update current position
		self.curPoint = np.add(self.curPoint, self.curVector)

	#print("curPoint = %s" % self.curPoint)
	#print("curVector = %s" % self.curVector)
	#print("curAng = %f\n" % self.curAng)

	## Return the nodes created so far.
	#  @return a union with the node list.
	#
	def getNodes(self):
		return union()(self.nodes)

class LSystem():
	
	def __init__(self):
		self.spheres = False
	
	def useSpheres(self, state):
		self.spheres = state
	
	## L-Systems were developed as a mathematical description of plant growth designed to model biological systems.
	#  L-Systems can be thought as containing the instructions for how a single cell can grow into a complex organism.
	#  They can be used to define the rules for interesting patterns, being particularly useful for fractal creation.
	#
	#  Example usage:
	#  - A       - Axiom
	#  - A -> B  - Rule 1 Change A to B
	#  - B -> AB - Rule 2 Change B to AB
	#  @see - http://interactivepython.org/courselib/static/thinkcspy/Strings/TurtlesandStringsandLSystems.html
	#  @param n - height of tree
	#  @param sentence - initial sentence - base for the rule applications
	#  @param rules - a dictionary containing an axiom:rule key:value pair, they're both expected to be strings
	#  @return the resulting L-System based off of the given axioms and rules
	def buildLSystem(self, n, sentence, rules):
		next = ""
		if (n > 0):
			characters = list(sentence)
			
			for c in characters:
				if (c in rules):
					next += self.buildLSystem(n-1, rules[c], rules);
				else:
					next += c
		else:
			return sentence
		
		return next


	## Interpret a given sentence and draw the result.
	#
	#  - F move forward a step of length d
	#  - f Move forward a step of length d without drawing a line
	#  - + Turn left by angle a
	#  - - Turn right by angle a
	#  - & Pitch down by angle a
	#  - ^ Pitch up by angle a
	#  - \ Roll left by angle a
	#  - / Roll right by angle a
	#  - | Turn arund (180 deg)
	#  - [ Push current drawing to stack
	#  - ] Pop current drawing from stack
	#  @param lSentence - the L-System string returned by buildLSystem
	#  @param angle - angle of rotation
	#  @param d - length d
	def draw(self, lSentence, angle, d):
		characters = list(lSentence)
		stack = []
		a = 0
		t = turtle(h=d)
		t.useSpheres = self.spheres
		
		for c in characters:
			if (c == 'F'):
				t.turn(a)
				a = 0
			#elif (c == 'f'):
			elif (c == '+'):
				a = angle
				t.setAxis('Z')
			elif (c == '-'):
				a = -angle
				t.setAxis('Z')
			elif (c == '&'):
				a = angle
				t.setAxis('Y')
			elif (c == '^'):
				a = -angle
				t.setAxis('Y')
			elif (c == "\\"):
				a = angle
				t.setAxis('X')
			elif (c == '/'):
				a = -angle
				t.setAxis('X')
			elif (c == '|'):
				a = 180
				t.setAxis('X')
			elif (c == '['):
				tup = (t.curPoint, t.curVector, t.curAng)
				stack.append(tup)
			elif (c == ']'):
				val = stack.pop()
				t.curPoint = val[0]
				t.curVector = val[1]
				t.curAng = val[2]
			else:
				continue

		return t.getNodes()


	## Generate and draw the fractal resulting from the following parameters
	#  @param n - recursion height
	#  @param sentence -  initial sentence - base for the rule applications
	#  @param a - angle
	#  @param d - step distance
	#  @param rules - a dictionary containing an axiom:rule key:value pair, they're both expected to be strings
	def lSystem(self, n, sentence, a, d, rules):
		lSentence = self.buildLSystem(n, sentence, rules)
		return self.draw(lSentence, a, d)

## Silly test that draws a bunch of cylinders.
def test(d):
	t = turtle(h=d)
		
	t.turn(0)
	t.turn(30)
	t.turn(0)
	
	t.setAxis('X')
	
	t.turn(30)
	t.turn(30)
	
	t.setAxis('Y')
	
	t.turn(-90)
	t.turn(-90)
	t.turn(90)
	t.turn(0)
	t.turn(90)
	
	return t.getNodes()
