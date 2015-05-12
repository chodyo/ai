class PotentialField(object):

	def __init__(self, obstacles, bases, flags):
		self.obstacles = obstacles
		self.bases = bases
		self.flags = flags

	def set_obstacles(self, obstacles):
		self.obstacles = obstacles

	def set_bases(self, bases):
		self.bases = bases

	def set_flags(self, flags):
		self.flags = flags

	def set_goal(self, coords):
		self.goal = coords