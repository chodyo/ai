#!/usr/bin/env python

import matplotlib.pyplot as plt
import numpy as np

from potentialField import PotentialField


fig = plt.figure()
ax = fig.add_subplot(111)
 
# generate grid
x=np.linspace(-2, 2, 32)
y=np.linspace(-1.5, 1.5, 24)
x, y=np.meshgrid(x, y)
# calculate vector field
vx=-y/np.sqrt(x**2+y**2)*np.exp(-(x**2+y**2))
vy= x/np.sqrt(x**2+y**2)*np.exp(-(x**2+y**2))

# plot vecor field
ax.quiver(x, y, vx, vy, pivot='middle', color='r', headwidth=4, headlength=6)
ax.set_xlabel('x')
ax.set_ylabel('y')
plt.show()
#plt.savefig('visualization_quiver_demo.png')