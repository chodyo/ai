import numpy as np
from bzrc import BZRC, Command

class kalmanFilter(object):

	def __init__(self):
		self.deltT = .05
		self.c = 0.01
		self.F = np.array(([1,self.deltT,(self.deltT**2)/2,0,0,0],[0,1,self.deltT,0,0,0],[0,self.c*-1,1,0,0,0],[0,0,0,1,self.deltT,(self.deltT**2)/2],[0,0,0,0,1,self.deltT],[0,0,0,0,self.c*-1,1]))
		self.SumX = np.array(([0.1,0,0,0,0,0],[0,0.1,0,0,0,0],[0,0,5,0,0,0],[0,0,0,0.1,0,0],[0,0,0,0,0.1,0],[0,0,0,0,0,5]))
		self.H = np.array(([1,0,0,0,0,0],[0,0,0,1,0,0]))
		self.SumZ = np.array(([25,0],[0,25]))
		self.SumT = np.array(([100,0,0,0,0,0],[0,0.1,0,0,0,0],[0,0,0.1,0,0,0],[0,0,0,100,0,0],[0,0,0,0,0.1,0],[0,0,0,0,0,0.1]))
		self.utNow = np.array(([0],[0],[0],[0],[0],[0]))
		self.equation = np.dot(np.dot(self.F, self.SumT), self.F.T) + self.SumX
		self.counter = 0
		#self.equation = ((self.F * self.SumT) * self.F.T) + self.SumX
		#print "equation: ",self.equation
		self.future_time = 0
		self.guess_time = -1
		self.real_time = 0
		self.timer = 2.0

	#sets a command to rotate and returns true if me is not within .001 radians of enemy
	def rotate(self, me, enemy):
		target_angle = self.find_angle(me, enemy)
		#1 degree = .017453 radians
		angle_difference = me.angle - target_angle
		#print "AD: ",angle_difference
		return angle_difference*-1

	# TODO: calculate the time difference between the enemy tank getting to firing location and the bullet getting to that same firing location
	# me and enemy are objects that store the tank's attributes, like x, y, angle, etc.
	def fire(self, me, enemy):
		#bullet travels 100 pixels a second
		#distance formula
		distance = ((enemy.x-me.x)**2 + (enemy.y-me.y)**2)**(0.5)
		#print "Distance: ",distance, "  Time:",self.future_time
		if abs(distance/100 - self.future_time) < .1:
			print "Firing at ",enemy.x,enemy.y," to hit in ",self.future_time,"seconds, at",self.future_time+self.real_time
			self.guess_time = self.future_time + self.real_time
			self.future_time -=1.0
			return True
		else:
			return False

	def lead_and_wait(self, me, enemy):
		#bro = self.more_kalman(self.timer)
		self.timer -= .05
		print self.timer
		if self.timer>0:
			return False
		else:
			return True

	def find_angle(self,me,enemy):
		my_result2 = np.arctan2((enemy.y-me.y),(enemy.x-me.x))
		return my_result2

	#does wicked kalman calculations
	def calc_kalman(self, enemy):
		#print "Kalman Time"
		Zt = np.array(([enemy.x],[enemy.y]))
		if self.real_time - self.guess_time < .5:
			print "Z is: ",Zt
		#equation = F*sumT*F*T + SumX
		self.equation = np.dot(np.dot(self.F, self.SumT), self.F.T) + self.SumX

		#KtNow = equation*H*T*(H*(equation)*H*T+sumZ) -1
		'''Step by step dot products of above equation'''
		one =  np.dot(self.equation , self.H.T)
		two = np.dot(self.H , one)
		three = (two + self.SumZ)
		ktNow = np.dot(one, np.linalg.inv(three))
		#                       1           4         2                1           3
		#ktNow = (self.equation * self.H.T) * (self.H * (self.equation * self.H.T) + self.SumZ)^-1
		#print "ktNow: ", ktNow
				
		#utNow = F*utNow +  KtNow*((zt+1) - H*F*utNow)
		'''Step by step dot products of above equation'''
		yi = np.dot(self.F , self.utNow)
		er = np.dot(self.H , self.F)
		san = np.dot(er, self.utNow)
		si = Zt - san
		wu = np.dot(ktNow, si)
		self.utNow = yi + wu
		#                      1            6        5     4          2         3
		#self.utNow = (self.F * self.utNow) + (ktNow * (Zt - ((self.H * self.F) * self.utNow))))
		#print "utNow: ",self.utNow


		#EtNow = (IdentityMatrix - (ktNow)*H)*(equation)
		'''Step by step dot products of above equation'''
		eins = np.dot(ktNow, self.H)
		zwei = (np.identity(6) - eins)
		self.SumT = np.dot(zwei, self.equation)
		#                            2       1         3
		#self.SumT = (np.identity(6) - ktNow * self.H) * self.equation

		#self.future_time -= 2.0
		return self.utNow

	#check an additional .1 seconds into the future
	def more_kalman(self, add_in):
		self.real_time +=.05
		self.future_time += add_in
		self.counter+=1
		#print self.future_time
		tempArray = np.array(([1,self.future_time,(self.future_time**2)/2,0,0,0],[0,1,self.future_time,0,0,0],[0,self.c*-1,1,0,0,0],[0,0,0,1,self.future_time,(self.future_time**2)/2],[0,0,0,0,1,self.future_time],[0,0,0,0,self.c*-1,1]))
		newResult = np.dot(tempArray , self.utNow)
		if add_in == 0.0:
			print "Guess ", float(newResult[0]), float(newResult[3])
		return newResult	


	def main():
		print("Main")
if __name__ == '__main__':
	main()

