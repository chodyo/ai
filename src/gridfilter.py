import numpy
import math
import drawgridfilter

# The main piece of this class is the self.grid item.
# quick reference:
# -1 = NO DATA
#  0 = NOT OCCUPIED
#  1 = OCCUPIED
# most of the time the grid is a probabilistic value between 0 and 1.
# the grid stores the P(S=True), or the probability the state is occupied

# This constant is the confidence threshold. Once the algorithm determines the occupancy probability is higher than this, 
# it will determine that is is occupied.
CONFIDENCE = 0.5

class GridFilter(object):

	# true_pos and true_neg are obtained by the server as part of the response to the "constraints" command
	# worldsize is the width/height of a square world. the default from what we've been using is 800x800
	def __init__(self, true_pos, true_neg, worldsize=800):
		self.worldsize = worldsize
		self.true_pos = true_pos
		self.true_neg = true_neg

		self.grid = numpy.empty([worldsize, worldsize])
		self.grid.fill(-1)

	# iterate through the new grid
	def update_grid(self, pos, new_grid):
		start_x = pos[0]
		start_y = pos[1]
		for x in range(0, len(new_grid)):
			for y in range(0, len(new_grid[x])):
				# print x+pos[0], y+pos[1], new_grid[x][y]
				priori = self.grid[x+start_x][y+start_y]
				self.grid[x+start_x][y+start_y] = self.probability(priori, new_grid[x][y])

	# prepare the grid for drawing
	def get_grid(self):
		outgrid = numpy.empty([self.worldsize, self.worldsize])
		for x in range(0, self.worldsize):
			for y in range(0, self.worldsize):
				# unexplored
				if self.grid[x][y] == -1:
					outgrid[x][y] = 0.5
				# not occupied
				elif self.grid[x][y] < CONFIDENCE:
					# white
					outgrid[x][y] = 1
				# occupied
				else:
					# black
					outgrid[x][y] = 0
		return outgrid


	# update the probability at a specific location
	def probability(self, priori, occupied):
		if priori == -1:
			priori = 0.5
		inv_priori = 1 - priori

		# if occupied
		A = self.true_pos
		B = 1 - self.true_neg

		if not occupied:
			A = 1 - self.true_pos
			B = self.true_neg

		alpha = 1 / (priori*A + inv_priori*B)
		return alpha*A*priori

	# returns the closest location that needs to be explored
	# this is not very efficient, just a brute force algorithm. don't spam this method.
	def closest_goal(self, pos_x, pos_y):
		closest_dist = self.worldsize**2
		closest_x = pos_x
		closest_y = pos_y
		for x in range(0, len(self.grid)):
			for y in range(0, len(self.grid)):
				if (self.grid[x][y] == -1):
					dist = numpy.sqrt((x-pos_x)**2 + (y-pos_y)**2)
					if dist < closest_dist:
						closest_dist = dist
						closest_x = x
						closest_y = y
		return closest_x, closest_y

if __name__ == '__main__':
	test_true_pos = 0.97
	test_true_neg = 0.90
	test_worldsize = 800

	gf = GridFilter(test_true_pos, test_true_neg, test_worldsize)
	gf.grid[4][4] = 0.72
	gf.grid[4][5] = 0.45
	gf.grid[5][4] = 0.63
	# gf.grid[1][1] = 0.90
	# print gf.grid

	# new_grid = [[1, 1, 0],[1, 1, 0],[0, 0, 0]]
	new_grid = [[1, 1], [0, 0]]
	new_pos = (4, 4)
	gf.update_grid(new_pos, new_grid)
	# print gf.grid

	# print gf.closest_goal(5, 4)

	# this needs to be converted to the agent's code
	drawgridfilter.init_window(gf.worldsize, gf.worldsize)
	while 1:
		drawgridfilter.update_grid(gf.get_grid())
		drawgridfilter.draw_grid()
