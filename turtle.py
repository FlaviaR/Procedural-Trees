#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
## @package turtle
#
# A 3D turtle graphics implementation.
# It produces a list of nodes to be loaded by openscad.
#
# Therefore, there have to be installed some packages:
# - On <A HREF="https://start.fedoraproject.org">Fedora</A>:
# -# sudo dnf install openscad-MCAD
# - On <A HREF="https://www.ubuntu.com/desktop">Ubuntu</A>:
# -# sudo apt-get install openscad-mcad
# - On MacOS (using <A HREF="https://www.macports.org">macports</A>):
# -# sudo port install OpenSCAD
# - sudo pip install solidpython <br>
# or for python3:
# - sudo pip3 install solidpython
#
# To see the created model:
# - python turtle.py \<example_number\>
# - openscad turtle.scad &
#
#
# @see http://www.openscad.org/
# @see https://github.com/SolidCode/SolidPython
#
# @author Flavia Cavalcanti
# @since 22/02/2018
#

from __future__ import division

import sys
import math
import matrix
import numpy as np

# Assumes SolidPython is in site-packages or elsewhere in sys.path
from solid import *
from solid.utils import *

SEGMENTS = 48

## Rotate the given vector about the x axis.
#
#  @param array given vector.
#  @param a rotation angle in degrees.
#
def xAxisRot(array, a):
	a = np.deg2rad(a)
	c = cos(a)
	s = sin(a)
	x = [	[1, 0,  0, 0], \
			[0, c, -s, 0], \
			[0, s,  c, 0], \
			[0, 0,  0, 1]	]
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
	y = [	[ c, 0, s, 0], \
			[ 0, 1, 0, 0], \
			[-s, 0, c, 0], \
			[ 0, 0, 0, 1]	]

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
	z = [	[c, -s, 0, 0], \
			[s,  c, 0, 0], \
			[0,  0, 1, 0], \
			[0,  0, 0, 1]	]
	return np.dot(array, z)

## A nice color table.
colors = {"green":          (0.0,1.0,0.0),
          "white":          (1.0,1.0,1.0),
          "red":            (1.0,0.0,0.0),
          "yellow":         (1.0,1.0,0.0),
          "blue":           (0.0,0.0,1.0),
          "magenta":        (1.0,0.0,1.0),
          "cyan":           (0.0,1.0,1.0),
          "pastel pink":    (0.98,0.4,0.7),
          "pumpkin orange": (0.98,0.625,0.12),
          "brown":          (0.6,0.4,0.12),
          "light gray":     (0.75,0.75,0.75),
          "barney purple":  (0.6,0.4,0.7), 
          "dark gray":      (0.25,0.25,0.25),
          "medium orchid":  (0.729,0.333,0.827),
          "dark khaki":     (0.741,0.718,0.420),
          "light yellow":   (1.000,1.000,0.878),
          "orange red":     (1.0,0.271,0.0)}

## A simple 3D turtle graphics.
#
#  @see https://docs.python.org/3/library/turtle.html
#  @see http://new.math.uiuc.edu/math198/MA198-2015/nwalter2/index.html
#  <br>
class turtle(object):
	__fullDebug__ = False
	__toDebug__ = False

	## Constructor.
	#
	#  The cylinder in openscad is centered about the z axis.
	#
	#  @param r Cylinder radius.
	#  @param h Cylinder height.
	#  @param t When False, use yaw, pitch and roll.
	#  @see https://en.wikibooks.org/wiki/OpenSCAD_User_Manual/The_OpenSCAD_Language#cylinder
	#  <br>
	def __init__(self, r=2, h=10, t=False):
		## Cylinder radius.
		self.r = r

		## Cylinder height.
		self.h = h

		## Create rounded cylinders.
		self.round = True
	
		## Whether pencolor has been called before.
		self.controlColor = False

		if not t:	
			self.mode ("standard")
		else:
			self.mode ("world")

		## Whether coordinate axes should be drawn.
		self.showAxes = False

	## Turn debugging on or off.
	def setDebug(self, state=True):
		self.__toDebug__ = state

	## Delete the turtle’s drawings from the screen, 
	#  re-center the turtle and set variables to the default values.
	#
	def reset(self):
		## A list with openscad primitives.
		self.nodes = []

		# Set default position and orientation.
		self.home()

		# Put the pen down.
		self.pendown()

		## Rotated moving direction.
		self.rotVector = None

		if self.__mode != "world":
			if self.__mode == "standard":
				## How to turn in 3D.
				self.turn = self.yaw
			else:
				self.turn = self.roll
			self.turn(0)
		else:
			self.turn = self.__turn

	## Set turtle mode (“standard”, “logo” or “world”) and perform reset. 
	#  If mode is not given, current mode is returned.
	#  - Mode “standard” is compatible with old turtle. 
	#  - Mode “logo” is compatible with most Logo turtle graphics. 
	#  - Mode “world” uses user-defined “world coordinates”. <br>
	#    Attention: in this mode angles appear distorted if x/y unit-ratio doesn't equal 1.
	#  @param mode   Turtle Mode 
	#  <PRE>
	#       Mode             Initial turtle heading     positive angles
	#       “standard”       to the right (east)        counterclockwise
	#       “logo”           upward (north)             clockwise
	#  </PRE>
	def mode(self,mode=None):
		if mode is None:
			return self.__mode
		elif mode in ("standard", "logo", "world"):
			## Turtle mode.
			self.__mode = mode
			if mode == "standard":
				## Initial direction. Does not change.
				self.initialVector = np.array([1, 0, 0, 0])
			elif mode == "logo":
				self.initialVector = np.array([0, 0, 1, 0])

			self.reset()

	## Control the axis drawing.
	def drawAxes (self, a=True):
		self.showAxes = a

	## Move the current position to (x,y,z).
	#
	#  Move turtle to an absolute position. 
	#  If the pen is down, draw line. 
	#  Do not change the turtle’s orientation.
	#
	def setposition(self,x,y,z):
		if not self.controlColor:
			self.pencolor("pumpkin orange")

		Z = np.array([0,  0,  1])
		v = np.array([x,  y,  z])

		# norm of vector v
		norm = lambda v: math.sqrt(v[0]*v[0] + v[1]*v[1] + v[2]*v[2])

		# vector from current position to (x,y,z)
		v = np.subtract(v, self.position())

		# distance from current position to (x,y,z)
		dist = norm(v)
		if dist > 0:
			v = (1.0/dist) * v
		else:
			# (x,y,z) is at current position
			return
		self.h = dist

		axis = np.cross(Z, v)
		naxis = norm(axis)
		if naxis == 0:
			# parallel to Z axis
			axis = [0, 0, 1]
		else:
			axis = (1.0/naxis) * axis

		ang = np.rad2deg(math.acos(np.clip(np.dot(Z, v),-1,1)))

		if self.isdown():
			self.addNode2(ang, axis.tolist())

		## Current position.
		self.curPoint = np.array([x,  y,  z, 1])

		# restore color
		self.setDirection(self.dir)

	## Return the current position.
	def position(self):
		return self.curPoint.tolist()[:-1]

	## Return the turtle’s current heading (value depends on the turtle mode, see #mode()).
	def heading(self):
		return self.rotVector if self.rotVector is not None else self.curVector

	## Move turtle to the origin – coordinates (0,0,0) – 
	#  and set its heading to its start-orientation 
	#  (which depends on the mode, see #mode()).
	def home(self):
		## Indicates the rotation direction.
		self.dir = None

		## Current position.
		self.curPoint = np.array([0,  0,  0, 1])

		## Holds accumulated rotations.
		self.rotMatrix = matrix.identity()

		# Rotation axis.
		self.setAxis('Z')

	## Return the absolute coordinates of the current position.
	def abspos(self):
		# remove fourth coordinate
		return np.fabs(self.curPoint).tolist()[:-1]

	## Pull the pen up – no drawing when moving.
	def penup(self):
		## Pen state: up or down.
		self.down = False
	
	## Pull the pen down – drawing when moving.
	def pendown(self):
		self.down = True

	## Return or set the pencolor.
	def pencolor(self, color=None):
		self.controlColor = True
		if color is None:
			return self.color
		elif isinstance(color, str):
			self.color = colors[color.lower()]
		elif isinstance(color, collections.Sequence):
			self.color = color
	
	## Set the line thickness to width or return it.
	def pensize(self, width):
		if width is None:
                        return self.r
		elif isinstance(width, float):
			self.r = width

	## Return True if pen is down, False if it’s up.
	def isdown(self):
		return self.down

	## Rotate around Z axis.
	#
	#  The rotation is intrinsic.
	#
	#  @param ang rotation angle in degrees.
	#
	def yaw(self, ang):
		self.setDirection('Z')
		self.rotMatrix = matrix.dot(self.rotMatrix, matrix.rotate(ang,0,0,1))
		self.rotVector = np.dot (self.initialVector, self.rotMatrix.T.tolist())
		if turtle.__toDebug__:
			print ("yaw(%d)" % ang)

	## Rotate around Y axis.
	#
	#  The rotation is intrinsic.
	#
	#  @param ang rotation angle in degrees.
	#
	def pitch(self, ang):
		self.setDirection('Y')
		self.rotMatrix = matrix.dot(self.rotMatrix, matrix.rotate(ang,0,1,0))
		self.rotVector = np.dot (self.initialVector, self.rotMatrix.T.tolist())
		if turtle.__toDebug__:
			print ("pitch(%d)" % ang)

	## Rotate around X axis.
	#
	#  The rotation is intrinsic.
	#  This is the symmetry axis of the cylinder.
	#
	#  @param ang rotation angle in degrees.
	#
	def roll(self, ang):
		self.setDirection('X')
		self.rotMatrix = matrix.dot(self.rotMatrix, matrix.rotate(ang,1,0,0))
		self.rotVector = np.dot (self.initialVector, self.rotMatrix.T.tolist())
		if turtle.__toDebug__:
			print ("roll(%d)" % ang)

	## Sets the rotation (intrinsic) axis color.
	#  - X red.
	#  - Y green.
	#  - Z blue.
	#
	#  @param dir character identifying a coordinate axis: X, Y or Z.
	#
	def setDirection(self, dir):
		self.dir = dir
		if self.controlColor:
			return

		if dir == 'X':
			## Color used to draw.
			self.color = colors["red"]
		elif dir == 'Y':
			self.color = colors ["green"]
		else:	
			self.color = colors ["blue"]

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

		self.setDirection(dir)

		if dir == 'X':
			## Rotation axis.
			self.axis  = [-1,  0,  0]
			## Points to the function that rotates about the chosen axis.
			self.rotFunc = xAxisRot
			## Current direction.
			self.curVector = np.array([0, 0, 1, 0])
		elif dir == 'Y':
			self.axis = [0,  -1,  0]
			self.rotFunc = yAxisRot
			self.curVector = np.array([0, 0, 1, 0])
		else:
			self.axis = [0,  0,  -1]
			self.rotFunc = zAxisRot
			self.curVector = np.array([0, 1, 0, 0])

	## Make a turn and step forward.
	#  
	#  @param ang deviation from the previous direction.
	#  @param d amount to go forward.
	#
	def turnf(self,ang,d=None):
		if d is None: d = self.h
		self.turn(ang)
		self.forward(d)

	## Make a turn by a given angle onto plane:
	#  - xz (rotation about y axis)
	#  - yz (rotation about x axis)
	#  - xy (rotation about z axis)
	#
	#  according to what has been set in #setAxis.
	#
	#  The initial cylinder must be aligned to an axis perpendicular to the rotation axis.
	#  - Rotation about x,y -> z,
	#  - Rotation about z -> y.
	#
	#  @param ang deviation from the previous direction.
	#
	def __turn(self,ang):
		self.rotVector = None
		self.curAng += ang

		if True:
			if self.dir == 'Z': ang = -ang
			self.curVector = self.rotFunc(self.curVector, ang )
		else:
			if self.dir != 'Z': ang = -ang
			mat = matrix.rotate(ang, self.axis[0], self.axis[1], self.axis[2])
			mat = mat.tolist()
			self.curVector = np.dot (self.curVector, mat)

		if turtle.__fullDebug__: 
			print("curVector = %s" % self.curVector)
			print("curAng = %f\n" % self.curAng)

	## Controls the shape of cylinder extremities.
	#
	#  @param rd True for rounded cylinders.
	#
	def setRounded(self, rd=True):
		self.round = rd

	## Add a new node to the openscad tree.
	#
	#  @param m node transformation.
	#  @param c node color.
	#  @param r cylinder radius.
	#  @param h cylinder height.
	#  @param rd whether to create rounded cylinders.
	#
	def addNode(self, m, c=None, r=None, h=None, rd=None):
		if c is None:
			c = self.color
		if r is None:
			r = self.r
		if h is None:
			h = self.h
		if rd is None:
			rd = self.round
		
		if rd:
			self.nodes.append(
				(color(c))
				(multmatrix(m)
					(sphere(r))
					(cylinder(r, h))
				)
			)
		else:
			self.nodes.append(
				(color(c))
				(multmatrix(m)
					(cylinder(r, h))
				)
			)

	## Add a new node to the openscad tree.
	#
	#  @param ang rotation angle.
	#  @param axis rotation axis.
	#  @param c node color.
	#  @param r cylinder radius.
	#  @param h cylinder height.
	#  @param rd whether to create rounded cylinders.
	#
	def addNode2(self, ang=None, axis=None, c=None, r=None, h=None, rd=None):
		if ang is None:
			ang = self.curAng
		if axis is None:
			axis = self.axis
		if c is None:
			c = self.color
		if r is None:
			r = self.r
		if h is None:
			h = self.h
		if rd is None:
			rd = self.round
		
		if rd:
			self.nodes.append(
				(translate(self.position()))
				(rotate(a = ang, v = axis)
					(color(c)
						(sphere(self.r))
						(cylinder(r, h))
					)
				)
			)
		else:
			self.nodes.append(
				(translate(self.position()))
				(rotate(a = ang, v = axis)
					(color(c)
						(cylinder(r, h))
					)
				)
			)

	## Add a leaf node.
	def addLeaf(self, ang=None, axis=None, c=colors["pastel pink"], r=None):
		if ang is None:
			ang = self.curAng
		if axis is None:
			axis = self.axis
		if c is None:
			c = self.color
		if r is None:
			r = self.r
		
		pos = self.position()
		pos[1] += 1
		
		self.nodes.append(
			(translate(pos))
				(rotate(a = ang, v = axis)
					(color(c)
						(sphere(r))
					)
				)
		)

	## Draw the intrisic coordinate axes.
	def __drawAxes(self):
			r = self.r/8
			if self.__mode == "standard":
				hx = self.h*0.8
				hy = self.r*3
				hz = self.r*3
			else:
				hx = self.r*3
				hy = self.r*3
				hz = self.h*0.8
				
			# draw the Z axis.
			c = np.add(self.curPoint, self.h*self.rotVector/2)
			m = matrix.dot(matrix.translate(c[0],c[1],c[2]), self.rotMatrix).tolist()
			self.addNode(m, [0,0,1], r, hz, False)
			# draw the Y axis.
			m = matrix.dot(self.rotMatrix, matrix.rotate(90,-1,0,0))
			m = matrix.dot(matrix.translate(c[0],c[1],c[2]), m).tolist()
			self.addNode(m, [0,1,0], r, hy, False)
			# draw the X axis.
			m = matrix.dot(self.rotMatrix, matrix.rotate(90,0,1,0))
			m = matrix.dot(matrix.translate(c[0],c[1],c[2]), m).tolist()
			self.addNode(m, [1,0,0], r, hx, False)

	## Move the turtle forward by the specified distance, in the direction the turtle is headed. 
	#
	#  Add a new object (cylinder plus sphere) to the model and update the current position.
	#
	#  @param distance amount to go forward.
	#
	def forward(self,distance):
		if distance <= 0:
			return

		self.h = distance
		if self.down:
			if self.rotVector is not None:
				t = self.position()
				m = self.rotMatrix
				if self.__mode == "standard":
					# move initial cylinder to x axis.
					m = matrix.dot(m, matrix.rotate(90,0,1,0))
				m = matrix.dot(matrix.translate(t[0],t[1],t[2]), m).tolist()
				self.addNode(m)

				if self.showAxes:
					self.__drawAxes()
			else:
				if self.dir == 'Z':
					self.addNode2(ang = [-90, 0, self.curAng])
				else:
					self.addNode2()

		# update current position
		self.curPoint = np.add(self.curPoint, self.h * self.heading())

		if turtle.__fullDebug__:
			print("curPoint = %s" % self.position())
		if turtle.__toDebug__:
			print("    forward = %d -> heading = %s" % (self.h, self.heading().tolist()[:-1]))
		

	## Move the turtle backward by distance, opposite to the direction the turtle is headed. 
	#  Do not change the turtle’s heading.
	#
	#  @param distance a number.
	#
	def backward(self, distance):
		pendown = self.isdown()
		self.penup()
		self.yaw(180)
		self.forward(abs(distance))
		self.yaw(180)
		if pendown: self.pendown()
		if turtle.__toDebug__:
			print("    backward = %d" % self.h)

	## Return the nodes created so far.
	#  @return a union with the node list.
	#
	def getNodes(self):
		return union()(self.nodes)

## Draw a sphere. 
#
#  @see http://new.math.uiuc.edu/math198/MA198-2015/nwalter2/index.html
#  <br>
def wireSphere():	
	movelength = 0.5
	angle = 10

	t = turtle(r=0.1,h=movelength)

	for i in range(18):
		for j in range(36):
			if j == 0:
				t.forward(movelength/2)
			else:
				t.forward(movelength)
			t.pitch(angle)

		t.forward(movelength/2)
		t.turn(angle)

	return t.getNodes()

t0 = turtle(t=False)
## Draw a star. 
def star():	

	for i in range(5):
		t0.turn(144 if i > 0 else 0)
		t0.forward(30)

	return t0.getNodes()

## Draw three stars.
def stars():
	# we can draw on any plane...
	t0.pitch(45)

	star()
	t0.setAxis('X')
	star()
	t0.setAxis('Y')
	star()

	return t0.getNodes()

## Draw a cube in the old way.
def oldCube():
	t = turtle(t=True)
	t.setRounded(False)

	t.setAxis('Y')
	t.turnf(90)
	t.turnf(90)
	t.turnf(90)
	t.turnf(90)
	
	t.setAxis('X')
	t.turnf(-90)
	t.turnf(-90)
	t.turnf(-90)

	t.setAxis('Z')
	t.penup()
	t.turnf(90)
	
	t.pendown()
	t.turnf(90)
	t.turnf(90)

	t.penup()
	t.turnf(90)
	t.setAxis('X')
	t.turnf(0)
	t.turnf(-90)

	t.setAxis('Y')
	t.pendown()
	t.turnf(90)
	t.turnf(90)

	t.penup()
	t.turnf(180)

	t.setAxis('X')
	t.pendown()
	t.turnf(90)

	return t.getNodes()

## Draw a "gear".
def gear():
	t = turtle()
	while True:
		t.forward(200)
		t.turn(170)
		if max(t.abspos()) < 1:
			break

	return t.getNodes()

## Draw a cube.
#
#  @see http://new.math.uiuc.edu/math198/MA198-2015/nwalter2/index.html
#  <br>
def cube():
	t = turtle()
	t.drawAxes()
	t.setRounded(False)

	len = 25
	# Draws base
	for i in range(4):
		t.forward(len)
		t.turn(90)

	# Moves to top
	t.pitch(90)
	t.forward(len)
	t.pitch(-90)

	# Draws top edges and lines connecting top and base
	for i in range(4):
		t.forward(len)
		t.pitch(-90)
		t.forward(len)
		t.backward(-len)
		t.pitch(90)
		t.turn(90)

	return t.getNodes()

## Draw another cube.
def cube2():
	t = turtle()
	t.drawAxes()
	
	t.pitch(0)	
	#t.roll(0)	
	#t.yaw(0)
	t.forward(10)
	t.forward(10)
	t.pitch(90)
	t.forward(10)
	t.forward(10)
	t.pitch(90)
	t.forward(10)
	t.forward(10)
	t.pitch(90)
	t.forward(10)
	t.forward(10)

	t.yaw(90)
	t.forward(10)
	t.forward(10)
	t.pitch(90)
	t.forward(10)
	t.forward(10)
	t.pitch(90)
	t.forward(20)

	t.backward(20)
	t.yaw(90)
	t.forward(20)
	t.pitch(90)
	t.forward(20)
	t.pitch(90)
	t.forward(20)

	t.backward(20)	
	t.yaw(-90)
	t.forward(20)

	t.penup()
	t.pitch(90)
	t.forward(20)
	t.pendown()
	t.pitch(90)
	t.forward(20)
	
	return t.getNodes()

## Draw an spiral.
#
#  @see https://michael0x2a.com/blog/turtle-examples
#  <br>	
def spiral():
	painter = turtle()

	painter.pensize(0.2)

	painter.pencolor("Blue")
	for i in range(50):
    		painter.forward(50)
    		painter.turn(123) # Let's go counterclockwise this time 
    
	painter.pencolor("Red")
	for i in range(50):
    		painter.forward(100)
    		painter.turn(123)
    
	return painter.getNodes()

## Draw some knots.
#
#  @see http://new.math.uiuc.edu/math198/MA198-2015/nwalter2/files/project/src/turtle_scripts/parametric_line.js
#  <br>
def knot():
	TMIN = 0
	TMAX = 2 * math.pi
	TSTEPS = 300

	TSTEP = (TMAX - TMIN) / TSTEPS

	td = turtle()
	td.setRounded(True)

	td.pensize(0.2)

	#td.setMoveSpeed(1000)
	#td.setTurnSpeed(1000)
	td.reset()

	## Return a point onto the surface.
	#
	#  @paran n surface type (0, 1, or 2).
	#  @paran t parametric value
	#
	def pos (n, t):
		if n==0:
			# TREFOIL KNOT
			x = math.sin(t) + 2 * math.sin(2 * t)
			y = math.cos(t) - 2 * math.cos(2 * t)
			z = -math.sin(3 * t)
		elif n==1:
			# TOROUS KNOT
			# T: [0, 2pi]
			# Good pairs of (p, q): (5, 2), (3, 10)
			p = 3
			q = 10
			x = math.cos(q*t)*(5+math.cos(p*t))
			y = math.sin(q*t)*(5+math.cos(p*t))
			z = math.sin(p*t)
		else:
			# CINQUEFOIL KNOT
			# T: [-5, 5]
			x = (1/50)*(math.pow(t, 5) - 36*math.pow(t, 3) + 260*t)
			y = (1/20)*(math.pow(t, 4) - 24*math.pow(t, 2))
			z = (1/1000)*(math.pow(t, 7) - 31*math.pow(t, 5) + 164*math.pow(t, 3) + 560*t)
		return x, y, z

	n = 0
	t = TMIN
	position = pos(n,t)
	td.penup()
	td.setposition(position[0], position[1], position[2])
	td.pendown()
	while t <= TMAX:
		position = pos(n,t)
		td.setposition(position[0], position[1], position[2])
		t += TSTEP

	return td.getNodes()

## Draw some surfaces.
#
#  @see http://new.math.uiuc.edu/math198/MA198-2015/nwalter2/files/project/src/turtle_scripts/surfaces.js
#  <br>
def surfaces():
	XMIN = -5
	XMAX = 5
	YMIN = -5
	YMAX = 5
	XSTEPS = 20
	YSTEPS = 20

	YSTEP = (YMAX - YMIN) / YSTEPS
	XSTEP = (XMAX - XMIN) / XSTEPS

	t = turtle()
	t.pensize(0.05)

	# t.setMoveSpeed(1000)
	# t.setTurnSpeed(1000)
	t.reset()

	## Return the surface height.
	#
	#  @paran n surface type (0, 1, 2, or 3).
	#  @paran x coordinate.
	#  @paran y coordinate.
	#  @return z value.
	#
	def surface (n, x, y):
		if n ==0:
  			# RIPPLES
  			return math.sin((math.pow(x, 2) + math.pow(y, 2)))
		elif n==1:
  			# SMOOTH RIPPLES
  			return math.sin(math.sqrt(math.pow(x, 2) + math.pow(y, 2)))
		elif n==2:
  			# PYRAMID
  			return 1-abs(x+y)-abs(y-x)
		elif n==3:
  			# CONE
  			return math.pow((math.pow(x, 2) + math.pow(y, 2)), 0.5)

	x = XMIN
	y = YMIN
	n = 0
	increasing = True
	t.penup()
	t.setposition(x, y, surface(n, x, y))
	t.pendown()

	while (x <= XMAX):
  		while (True):
    			t.setposition(x, y, surface(n, x, y))
    			y += YSTEP if increasing else -YSTEP
    			if (increasing and y > YMAX or not increasing and y < YMIN):
      				break
  		y = YMAX if increasing else YMIN
  		increasing = not increasing
  		x += XSTEP

	x = XMIN
	y = YMIN
	increasing = True
	t.penup()
	t.setposition(x, y, surface(n, x, y))
	t.pendown()
	while (y <= YMAX):
  		while (True):
    			t.setposition(x, y, surface(n, x, y))
    			x += XSTEP if increasing else -XSTEP
    			if (increasing and x > XMAX or not increasing and x < XMIN):
      				break
  		x = XMAX if increasing else XMIN
  		increasing = not increasing
  		y += YSTEP

	return t.getNodes()

## Draw a fractal tree.
#  @see https://rosettacode.org/wiki/Fractal_tree#BBC_BASIC
#  <br>
def tree():
	Spread = 25
	Scale = 0.76
	SizeX = 40
	SizeY = 30
	Depth = 10
	Radius = 10

	t = turtle() 
	t.pensize(Depth/Radius)
	t.penup()
	t.setposition(SizeX,0,0)
	t.pendown()

	#  Draw a stem of the tree at a given position and orientation.
	#
	#  @param x1 x coordinate of stem position.
	#  @param y1 y coordinate of stem position.
	#  @param size length of the stem.
	#  @param angle rotation angle measured from the x axis.
	#  @param depth recursion level.
	#
	def procBranch(x1, y1, size, angle, depth):
		t.pensize(depth/Radius)
		if depth == 1:
			t.pencolor("Green")
		elif depth == 2:
			t.pencolor("pastel pink")
		else:
			t.pencolor("Brown")
		if False:
			a = np.deg2rad(angle)
			x2 = x1 + size * math.cos(a)
			y2 = y1 + size * math.sin(a)
			t.penup()
			t.setposition(x1, y1, 0)
			t.pendown()
			t.setposition(x2, y2, 0)
		else:
			# angle is an absolute value measured from (zero at) the home position
			# and turn is relative to the previous angle
			t.home()
			t.penup()
			t.setposition(x1, y1, 0)
			t.pendown()
			t.turn(angle)
			t.forward(size)
			x2, y2, z2 = t.position()

		if depth > 0:
			procBranch(x2, y2, size * Scale, angle - Spread, depth - 1)
			procBranch(x2, y2, size * Scale, angle + Spread, depth - 1)

	procBranch(SizeX, 0, SizeY*0.5, 90, Depth)
	return t.getNodes()

def test():
	t = turtle()

	t.drawAxes()
	
	if True:
		t.forward(10)
		t.turn(90)
		t.forward(10)
	else:
		t.mode("logo")
		t.forward(10)
		t.turn(90)
		t.forward(10)

	return t.getNodes()

## Main program for testing.
def main(argv=None):
	if argv is None:
		argv = sys.argv

	proc = 0
	funcDict = {0: wireSphere, 1: star, 2: stars, 3: oldCube, 4: gear, 5: cube, 6: cube2, 7: spiral, 8: knot, 9: test, 10: surfaces, 11: tree}

	if len(argv) > 1:
		try:
			proc = int(argv[1])
			proc = max(min(proc,len(funcDict)-1),0)
		except:
			proc = 2

	lTree = funcDict[proc]()

	scad_render_to_file(lTree, file_header='$fn = %s;' % SEGMENTS, include_orig_code=True)

if __name__ == '__main__':
	sys.exit(main())
