import math

class PotentialField(object):

	def __init__(self, obstacles, worldsize, mybase):
		self.obstacles = obstacles
		self.worldsize = worldsize
		self.mybase = mybase
		self.home_x = (mybase.corner1_x+mybase.corner2_x+mybase.corner3_x+mybase.corner4_x)/4
		self.home_y = (mybase.corner1_y+mybase.corner2_y+mybase.corner3_y+mybase.corner4_y)/4

		self.attractive_strength = 2
		self.repulsive_strength = 1
		self.tangential_strength = 1

		self.get_flag = True

	# only one goal, it will be the only attractive field
	def set_goal(self, goal):
		self.goal = goal


	def get_vector(self, coords):
		'''Returns <x,y> of the sum of fields at coords'''
		ret_x = 0
		ret_y = 0
		# attractive field on the goal
		x, y = self.get_attractive(self.goal, coords, self.attractive_strength)
		ret_x += x
		ret_y += y
		
		# tangential fields on obstacles
		for ob in self.obstacles:
			x, y = self.get_tangential(ob, coords, self.tangential_strength)
			ret_x += x
			ret_y += y

		# repulsive field on the base if seeking flag
		if self.get_flag:
			x, y = self.get_repulsive(self.mybase, coords, self.repulsive_strength)
			ret_x += x
			ret_y += y

		# print ret_x, ret_y
		return ret_x, ret_y

	# obj is a variable that must hold the x and y coordinates of a goal, 
	# and a radius with the size of the goal. for example, a flag has a radius of 0
	def get_attractive(self, obj, coords, strength):
		'''Returns <x,y> of the sum of fields at coords'''
		g = obj
		r = float(g.r)
		s = 0 # float(self.worldsize)/16				# this value needs to be adjusted based on experimentation

		d = math.sqrt((g.x-coords.x)**2+(g.y-coords.y)**2)
		theta = math.atan2((g.y-coords.y),(g.x-coords.x))

		x = 0
		y = 0
		if d < r:
			pass
		elif r <= d and d <= s+r:
			x = strength*(d-r)*math.cos(theta)	
			y = strength*(d-r)*math.sin(theta)
		elif d >= s+r:
			x = strength*s*math.cos(theta)
			y = strength*s*math.sin(theta)
		return x, y

	# obj is a variable that must hold the x and y coordinates of the corners of
	# an obstacle.
	def get_repulsive(self, obj, coords, strength):
		'''Returns <x,y> of the sum of fields at coords'''
		o = Misc()
		o.x = (obj.corner1_x+obj.corner2_x+obj.corner3_x+obj.corner4_x)/4
		o.y = (obj.corner1_y+obj.corner2_y+obj.corner3_y+obj.corner4_y)/4

		r = math.fabs(o.x-obj.corner1_x)
		s = float(self.worldsize) / 4				# this value needs to be adjusted based on experimentation

		d = math.sqrt((o.x-coords.x)**2+(o.y-coords.y)**2)
		theta = math.atan2((o.y-coords.y),(o.x-coords.x))

		x = 0
		y = 0
		if d < r:
			x = -1 * self.sign(math.cos(theta)) * float('inf')
			y = -1 * self.sign(math.sin(theta)) * float('inf')
		elif r <= d and d <= s+r:
			x = -1 * strength * (s+r-d) * math.cos(theta)
			y = -1 * strength * (s+r-d) * math.sin(theta)
		elif d >= s+r:
			pass
		return x, y

	def get_tangential(self, obj, coords, strength):
		'''Returns <x,y> of the sum of fields at coords'''
		o = Misc()
		o.x = (obj[0][0]+obj[1][0]+obj[2][0]+obj[3][0])/4
		o.y = (obj[0][1]+obj[1][1]+obj[2][1]+obj[3][1])/4

		r = math.fabs(o.x-obj[0][0])
		s = r*1.5				# this value needs to be adjusted based on experimentation

		d = math.sqrt((o.x-coords.x)**2+(o.y-coords.y)**2)
		theta = math.atan2((o.y-coords.y),(o.x-coords.x))
		# THIS IS THE ONLY REAL DIFFERENCE BETWEEN TANGENTIAL AND REPULSIVE
		theta += math.pi / 2

		x = 0
		y = 0
		if d < r:
			x = -1 * self.sign(math.cos(theta)) * float('inf')
			y = -1 * self.sign(math.sin(theta)) * float('inf')
		elif r <= d and d <= s+r:
			x = -1 * strength * (s+r-d) * math.cos(theta)
			y = -1 * strength * (s+r-d) * math.sin(theta)
		elif d >= s+r:
			pass
		return x, y


	# Utility
	def sign(self, value):
		if value < 0:
			return -1
		elif value >= 0:
			return 1

class Misc(object):
    pass