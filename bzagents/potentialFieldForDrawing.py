import math

class PotentialField(object):
	class Misc(object):
		pass
	def __init__(self, obstacles, worldsize, mybase):
		self.obstacles = obstacles
		self.worldsize = worldsize
		self.mybase = mybase
		self.worldCorners = []
		self.loadCorners()
		self.home_x = (mybase.corner1_x+mybase.corner2_x+mybase.corner3_x+mybase.corner4_x)/4
		self.home_y = (mybase.corner1_y+mybase.corner2_y+mybase.corner3_y+mybase.corner4_y)/4
		self.goals = []
		self.attractive_strength = 7
		self.repulsive_strength = 4
		self.tangential_strength = 24
		self.myMisc = self.Misc()
		self.vecX = []
		self.vecY = []

		self.get_flag = True

	# only one goal, it will be the only attractive field
	def set_goal(self, goal):
		self.goal = goal

	def add_goal(self, goal):
		self.goals.append(goal)

	def resetMisc(self):
		self.myMisc = self.Misc()
		
	def loadCorners(self):
		self.topLeft()
		self.topRight()
		self.bottomLeft()
		self.bottomRight()
		
	def topLeft(self):
		base = self.Misc()
		base.corner1_x = -450
		base.corner1_y = 450
		base.corner2_x = -450
		base.corner2_y = 450
		base.corner3_x = -450
		base.corner3_y = 450
		base.corner4_x = -450
		base.corner4_y = 450
		self.worldCorners.append(base)
			
	def topRight(self):
		base = self.Misc()
		base.corner1_x = 450
		base.corner1_y = 450
		base.corner2_x = 450
		base.corner2_y = 450
		base.corner3_x = 450
		base.corner3_y = 450
		base.corner4_x = 450
		base.corner4_y = 450
		self.worldCorners.append(base)	
            
	def bottomLeft(self):
		base = self.Misc()
		base.corner1_x = -450
		base.corner1_y = -450
		base.corner2_x = -450
		base.corner2_y = -450
		base.corner3_x = -450
		base.corner3_y = -450
		base.corner4_x = -450
		base.corner4_y = -450
		self.worldCorners.append(base)     
            
	def bottomRight(self):
		base = self.Misc()
		base.corner1_x = 450
		base.corner1_y = -450
		base.corner2_x = 450
		base.corner2_y = -450
		base.corner3_x = 450
		base.corner3_y = -450
		base.corner4_x = 450
		base.corner4_y = -450
		self.worldCorners.append(base)    	
			
		

	def get_vector(self, coord, arX, arY):
		'''Returns <x,y> of the sum of fields at coords'''
		fret_x = [6401]
		fret_y = [6401]
		
		# attractive field on the goal
		
		for trackerY in arY:
			for trackerX in arX:
				ret_x = 0
				ret_y = 0
				
				coord.x = trackerX
				coord.y = trackerY
				#print " "
				#print coord.x
				#print coord.y
				
				for currentGoal in self.goals:
					
					x, y = self.get_attractive(currentGoal, coord, self.attractive_strength)
					ret_x += x
					ret_y += y
				
				# tangential fields on obstacles
				for ob in self.obstacles:
					x, y = self.get_tangential(ob, coord, self.tangential_strength)
					ret_x += x
					ret_y += y
					#print "tang",ret_x, ret_y
					
				# repulsive field on the base if seeking flag
				for oneCorner in self.worldCorners:
					x, y = self.get_repulsive(oneCorner, coord, self.repulsive_strength)
					ret_x += x
					ret_y += y
					
				if self.get_flag:
					x, y = self.get_repulsive(self.mybase, coord, self.repulsive_strength)
					ret_x += x
					ret_y += y
					#print "repuls",ret_x, ret_y
			
				fret_x.append(ret_x)
				fret_y.append(ret_y)

		#print ret_x, ret_y
		print len(fret_x)
		print len(fret_y)
		self.vecX = fret_x
		self.vecY = fret_y
		return fret_x, fret_y

	# obj is a variable that must hold the x and y coordinates of a goal, 
	# and a radius with the size of the goal. for example, a flag has a radius of 0
	def get_attractive(self, obj, coord, strength):
		'''Returns <x,y> of the sum of fields at coords'''

		g = obj
		r = float(g.r)
		s = float(self.worldsize)*.3				# this value needs to be adjusted based on experimentation

		d = math.sqrt((g.x-coord.x)**2+(coord.y-g.y)**2)
		theta = math.atan2((g.y-coord.y),(g.x-coord.x))

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
			#pass
		return x, y

	# obj is a variable that must hold the x and y coordinates of the corners of
	# an obstacle.
	def get_repulsive(self, obj, coord, strength):
		'''Returns <x,y> of the sum of fields at coords'''
		o = self.Misc()
		o.x = (obj.corner1_x+obj.corner2_x+obj.corner3_x+obj.corner4_x)/4
		o.y = (obj.corner1_y+obj.corner2_y+obj.corner3_y+obj.corner4_y)/4

		r = math.fabs(o.x-obj.corner1_x)
		s = float(self.worldsize) / 2.5				# this value needs to be adjusted based on experimentation

		d = math.sqrt((o.x-coord.x)**2+(coord.y-o.y)**2)
		theta = math.atan2((o.y-coord.y),(o.x-coord.x))

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

	def get_tangential(self, obj, coord, strength):
		'''Returns <x,y> of the sum of fields at coords'''
		o = self.Misc()
		o.x = (obj[0][0]+obj[1][0]+obj[2][0]+obj[3][0])/4
		o.y = (obj[0][1]+obj[1][1]+obj[2][1]+obj[3][1])/4

		r = math.fabs(o.x-obj[0][0])
		s = r*1.5				# this value needs to be adjusted based on experimentation

		d = math.sqrt((o.x-coord.x)**2+(coord.y-o.y)**2)
		theta = math.atan2((o.y-coord.y),(o.x-coord.x))
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

	
