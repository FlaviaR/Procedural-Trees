#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
## @package turtle
#
# A 3D turtle graphics implementation.
#
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

## A simple 3D turtle graphics.
#
#  @see https://docs.python.org/3/library/turtle.html
#  @see http://new.math.uiuc.edu/math198/MA198-2015/nwalter2/index.html
#  <br>
class turtle(object):
	__fullDebug__ = False
	__toDebug__ = True

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

		## A list with openscad primitives.
		self.nodes = []

		# Current position.
		self.setPosition(0,  0,  0)

		## Indicates the rotation direction.
		self.dir = None

		# Rotation axis.
		self.setAxis('Z')

		# Put the pen down.
		self.pendown()

		## Holds accumulated rotations.
		self.rotMatrix = matrix.identity()

		## Initial direction.
		self.initialVector = np.array([1, 0, 0, 0])

		## Rotated moving direction.
		self.rotVector = None

		if not t:
		## How to turn in 3D.
			self.turn = self.yaw
			self.turn(0)
		else:
			self.turn = self.__turn

		## Whether coordinate axes should be drawn.
		self.showAxes = False

		## Whether spheres between cylinders should be drawn.
		#  Drawing the spheres makes the render lag quite a bit - only use them in printable models.
		self.useSpheres = False

	## Display spheres according to parameter
	def drawSpheres(self, useSpheres):
		self.useSpheres = useSpheres

	## Control the axis drawing.
	def drawAxes (self, a=True):
		self.showAxes = a

	## Move the current position to (x,y,z).
	def setPosition(self,x,y,z):
		## Current position.
		self.curPoint = np.array([x,  y,  z, 1])

	## Return the current position.
	def position(self):
		return self.curPoint.tolist()[:-1]

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

	## Sets the rotation (intrinsic) axis.
	#
	#  @param dir character identifying a coordinate axis: X, Y or Z.
	#
	def setDirection(self, dir):
		self.dir = dir
		if dir == 'X':
			## Color used to draw.
			self.color = [1,0,0]
		elif dir == 'Y':
			self.color = [0,1,0]
		else:	
			self.color = [0,0,1]

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
		if turtle.__toDebug__:
			print("    turn = %d" % self.h)

	## Draw the intrisic coordinate axes.
	def __drawAxes(self):
			# draw the Z axis.
			c = np.add(self.curPoint, self.h*self.rotVector/2)
			m = matrix.dot(matrix.translate(c[0],c[1],c[2]), self.rotMatrix).tolist()
			self.nodes.append(
				(color([0,0,1]))
				(multmatrix(m) 
   					(cylinder(self.r/8, self.r*3))
				)
			)
			# draw the Y axis.
			m = matrix.dot(self.rotMatrix, matrix.rotate(90,-1,0,0))
			m = matrix.dot(matrix.translate(c[0],c[1],c[2]), m).tolist()
			self.nodes.append(
				(color([0,1,0]))
				(multmatrix(m) 
   					(cylinder(self.r/8, self.r*3))
				)
			)

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
				# move initial cylinder to x axis.
				m = matrix.dot(self.rotMatrix, matrix.rotate(90,0,1,0))
				m = matrix.dot(matrix.translate(t[0],t[1],t[2]), m).tolist()
				self.nodes.append(
					(color(self.color))
					(multmatrix(m) 
					 #(sphere(self.r))
					(cylinder(self.r, self.h))
					)
				)
				if self.showAxes:
					self.__drawAxes()
			else:
				if self.dir == 'Z':
					self.nodes.append(
						(translate(self.position()))
						(rotate(a = [-90, 0, self.curAng]) 	# rotation order: x, y and z
							#(sphere(self.r))
							(cylinder(self.r, self.h))
						)
					)
				else:
					self.nodes.append(
						(translate(self.position()))
						(rotate(a = self.curAng, v = self.axis)	# entering the screen
							#(sphere(self.r))
							(cylinder(self.r, self.h))
						)
					)

		# update current position
		self.curPoint = np.add(self.curPoint, self.h * (self.rotVector if self.rotVector is not None else self.curVector))

		if turtle.__fullDebug__:
			print("curPoint = %s" % self.position())
		if turtle.__toDebug__:
			print("    forward = %d" % self.h)
		

	## Move the turtle backward by distance, opposite to the direction the turtle is headed. 
	#  Do not change the turtle’s heading.
	#
	#  @param distance a number.
	#
	def backward(self, distance):
		self.penup()
		self.yaw(180)
		self.forward(abs(distance))
		self.yaw(180)
		self.pendown()
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
	t.penup();
	t.turnf(90)
	
	t.pendown()
	t.turnf(90)
	t.turnf(90)

	t.penup();
	t.turnf(90)
	t.setAxis('X')
	t.turnf(0)
	t.turnf(-90)

	t.setAxis('Y')
	t.pendown()
	t.turnf(90)
	t.turnf(90)

	t.penup();
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

	len = 25
	# Draws base
	for i in range(4):
		t.forward(len)
		t.turn(90)

	# Moves to top
	t.pitch(90)
	t.forward(len)
	t.pitch(-90);

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

## Main program for testing.
def main(argv=None):
	if argv is None:
		argv = sys.argv

	proc = 0
	funcDict = {0: wireSphere, 1: star, 2: stars, 3: oldCube, 4: gear, 5: cube, 6: cube2}

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
