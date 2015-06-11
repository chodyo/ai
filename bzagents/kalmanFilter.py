import numpy as np

class KalmanFilter(object):

	def __init__(self):
		self.deltT = 0.01
		self.c = 0.01
		self.F = np.array([1,self.deltT,(self.deltT*self.deltT)/2,0,0,0],[0,1,self.deltT,0,0,0],[0,-self.c,1,0,0,0],[0,0,0,1,self.deltT,(self.deltT*self.deltT)/2],[0,0,0,0,1,self.deltT],[0,0,0,0,-self.c,1])
		self.SumX = np.array([0.1,0,0,0,0,0],[0,0.1,0,0,0,0],[0,0,5,0,0,0],[0,0,0,0.1,0,0],[0,0,0,0,0.1,0],[0,0,0,0,0,5])
		self.H = np.array([1,0,0,0,0,0],[0,0,0,1,0,0])
		self.SumZ = np.array([25,0],[0,25])
		self.SumT = np.array([100,0,0,0,0,0],[0,0.1,0,0,0,0],[0,0,0.1,0,0,0],[0,0,0,100,0,0],[0,0,0,0,0.1,0],[0,0,0,0,0,0.1])
		self.utNow = np.array([0],[0],[0],[0],[0],[0])

	#sets a command to rotate and returns true if me is not within .001 radians of enemy
	def rotate(self, me, enemy):
		target_angle = self.find_angle(me, enemy)
		#1 degree = .017453 radians
		if np.absolute(me.angle - target_angle) > 0.001:
			command = Command(me.index, 0, 1, False)
        		me.commands.append(command)
			return True
		return False

	# TODO: calculate the time difference between the enemy tank getting to firing location and the bullet getting to that same firing location
	# me and enemy are objects that store the tank's attributes, like x, y, angle, etc.
	def fire(self, me, enemy):
		return true

	def find_angle(self,me,enemy):
		x = np.array([enemy.y-me.y])
		y = np.array([enemy.x-me.x])
		my_result = np.arctan2(y,x)
		return my_result[0]

	#does wicked kalman calculations
	def calc_kalman(self, enemy, time):
		Zt = np.array([enemy.x],[enemy.y])

		#equation = F*sumT*F*T + SumX
		equation = (self.F * sumT * self.F.T) + self.SumX

		#KtNow = equation*H*T*(H*(equation)*H*T+sumZ) -1
		ktNow = (equation * self.H.T) * (self.H * equation * self.H.T + self.SumZ) - 1
		
		#utNow = F*utNow +  KtNow*((zt+1) - H*F*utNow)
		self.utNow = (F * self.utNow) + (ktNow * (Zt - self.H * self.F * self.utNow))
		
		#ΣtNow = (IdentityMatrix - (ktNow)*H)*(equation)
		self.SumT = (np.identity(6) - ktNow * H) * equation

		#future stuff is just self.utNow = self.F * utNow

	#check an additional .01 seconds into the future
	def more_kalman(self):
		self.utNow = self.F * utNow

	def main():
		print("Main")
if __name__ == '__main__':
	main()
