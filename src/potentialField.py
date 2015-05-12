class PotentialField(object):

	def __init__(self, obstacles):
		self.obstacles = obstacles

		self.repulsive_strength = 1
		self.attractive_strength = 1
		self.tangential_strength = 1

	def set_obstacles(self, obstacles):
		self.obstacles = obstacles

	def set_mybase(self, mybase):
		self.mybase = mybase


	# only one goal, will be the only attractive field
	def set_goal(self, coords):
		self.goal = coords


	def get_vector(self, coords):
		'''Returns radian, magnitude of the sum of fields at coords'''
		for ob in self.obstacles:
			get_tangential(ob, coords, tangential_strength)


	def get_repulsive(self, obj, coords, strength):
		'''Returns radian, magnitude of the sum of fields at coords'''
		pass

	def get_attractive(self, obj, coords, strength):
		'''Returns radian, magnitude of the sum of fields at coords'''
		pass

	def get_tangential(self, obj, coords, strength):
		'''Returns radian, magnitude of the sum of fields at coords'''
		pass