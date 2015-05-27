import numpy

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
		self.true_pos = true_pos
		self.true_neg = true_neg

		self.grid = numpy.empty([worldsize, worldsize])
		self.grid.fill(-1)

	# iterate through the new grid
	def update_grid(self, pos, new_grid):
		for x in range(0, len(new_grid)):
			for y in range(0, len(new_grid[x])):
				# print x+pos[0], y+pos[1], new_grid[x][y]
				new_prob = self.probability(x+pos[0], y+pos[1], new_grid[x][y])
				self.grid[x][y] = new_prob

	# update the probability at a specific location
	def probability(self, x, y, occupied):
		priori = self.grid[x][y]
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
	def closest_goal(self, pos_x, pos_y):
		pass

if __name__ == '__main__':
	test_true_pos = 0.97
	test_true_neg = 0.90
	test_worldsize = 6

	gf = GridFilter(test_true_pos, test_true_neg, test_worldsize)
	gf.grid[0][0] = 0.72
	gf.grid[1][0] = 0.63
	print gf.grid

	# new_grid = [[1, 1, 0],[1, 1, 0],[0, 0, 0]]
	new_grid = [[1, 1], [0, 0]]
	new_pos = (0, 0)
	gf.update_grid(new_pos, new_grid)
	print gf.grid
