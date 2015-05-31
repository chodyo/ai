#!/usr/bin/env python

import matplotlib.pyplot as plt
import numpy as np
from potentialFieldForDrawing import PotentialField
from bzrc import BZRC, Command

bzrc = BZRC("localhost", 60307)
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

flag=flags[1]
aTank=mytanks[0]
tempFields = PotentialField(obstacles, worldsize, mybase)

goal = tempFields.myMisc
goal.x = -267
goal.y = -267
goal.r = 0
tempFields.add_goal(goal)




#for flag in myflags:
#	tempFields.resetMisc()
#	goal = tempFields.myMisc
#	if flag.color == mycolor:
#		continue
 #        	          
#	else:
#		goal = tempFields.myMisc
#		goal.x = flag.x
#		goal.y = flag.y
#		goal.r = 0

#	tempFields.add_goal(goal)






fig = plt.figure()
ax = fig.add_subplot(111)

# generate grid
x=np.linspace(-400, 400, 80)
myx = x
y=np.linspace(400, -400, 80)
myy = y
x, y=np.meshgrid(x, y)

# calculate vector field
vx, vy = tempFields.get_vector(aTank, myx, myy)

# plot vecor field
ax.quiver(x, y, vx, vy, pivot='middle', color='r', headwidth=4, headlength=6)
ax.set_xlabel('x')
ax.set_ylabel('y')
#plt.show()


plt.savefig('visualization_quiver_demo.png')
