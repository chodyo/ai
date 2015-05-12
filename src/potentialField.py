class PotentialField(object):

	def __init__(self, obstacles):
		self.obstacles = obstacles

		self.attractive_strength = 1
		self.repulsive_strength = 1
		self.tangential_strength = 1

		self.get_flag = True

	def set_obstacles(self, obstacles):
		self.obstacles = obstacles

	def set_mybase(self, mybase):
		self.mybase = mybase


	# only one goal, will be the only attractive field
	def set_goal(self, coords):
		self.goal = coords


	def get_vector(self, coords):
		'''Returns <x,y> of the sum of fields at coords'''
		ret_x = 0
		ret_y = 0
		# attractive field on the goal
		ret_x, ret_y += get_attractive(self.goal, coords, self.attractive_strength)
		# tangential fields on obstacles
		for ob in self.obstacles:
			ret_x, ret_y += get_tangential(ob, coords, self.tangential_strength)
		# repulsive field on the base if seeking flag
		if self.get_flag:
			ret_x, ret_y += get_repulsive(self.mybase, coords, self.repulsive_strength)

	def get_attractive(self, obj, coords, strength):
		'''Returns <x,y> of the sum of fields at coords'''
		pass

	def get_repulsive(self, obj, coords, strength):
		'''Returns <x,y> of the sum of fields at coords'''
		pass

	def get_tangential(self, obj, coords, strength):
		'''Returns <x,y> of the sum of fields at coords'''
		pass