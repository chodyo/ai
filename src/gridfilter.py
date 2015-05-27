import numpy

# The main piece of this class is the self.grid item.
# self.grid has three states:
# -1 = NO DATA
#  0 = NOT OCCUPIED
#  1 = OCCUPIED

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
				print x+pos[0], y+pos[1], new_grid[x][y]
				self.probability(x+pos[0], y+pos[1], new_grid[x][y])

	# update the probability at a specific location
	def probability(self, x, y, occupied):
		self.grid[x][y] = occupied

	# returns the closest location that needs to be explored
	def closest_goal(self, pos_x, pos_y):
		pass

def main():
	test_true_pos = 0.97
	test_true_neg = 0.90
	test_worldsize = 6

	gf = GridFilter(test_true_pos, test_true_neg, test_worldsize)

	print gf.grid

	new_grid = [[1, 1, 0],[1, 1, 0],[0, 0, 0]]
	new_pos = (3, 3)
	gf.update_grid(new_pos, new_grid)

	print gf.grid

	print "Main not implemented yet."

if __name__ == '__main__':
    main()