#!/usr/bin/env python

import matplotlib.pyplot as plt
import numpy as np
from potentialFieldForDrawing import PotentialField
from bzrc import BZRC, Command


class Misc(object):
	pass


bzrc = BZRC("localhost", 45207)
constants = bzrc.get_constants()

obstacles = bzrc.get_obstacles()
worldsize = constants['worldsize']
mytanks = bzrc.get_mytanks()
mycolor = mytanks[0].callsign[:-1]
bases = bzrc.get_bases()
mybase = None
for base in bases:
	if base.color == mycolor:
		mybase = base

mytanks, othertanks, flags, shots = bzrc.get_lots_o_stuff()
myflags = flags

flag=flags[2]
aTank=mytanks[0]
tempFields = PotentialField(obstacles, worldsize, mybase)
goal = Misc()
goal.x = flag.x
goal.y = flag.y
goal.r = 0
print "x is:",aTank.x
print "y is:",aTank.y
tempFields.set_goal(goal)


fig = plt.figure()
ax = fig.add_subplot(111)

# generate grid
x=np.linspace(-400, 400, 50)
y=np.linspace(-400, 400, 50)
x, y=np.meshgrid(x, y)

aTank.x=x
aTank.y=y
# calculate vector field
print "x is:",aTank.x
print "y is:",aTank.y
vx, vy = tempFields.get_vector(aTank)
print vx
# plot vecor field
ax.quiver(x, y, vx, vy, pivot='middle', color='r', headwidth=4, headlength=6)
ax.set_xlabel('x')
ax.set_ylabel('y')
plt.show()


#plt.savefig('visualization_quiver_demo.png')

