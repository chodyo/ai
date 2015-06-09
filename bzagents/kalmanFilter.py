import numpy as np

class KalmanFilter(object):

	def __init__(self):
		self.F = np.array([1,deltT,(deltT*deltT)/2,0,0,0],[0,1,deltT,0,0,0],[0,-c,1,0,0,0],[0,0,0,1,deltT,(deltT*deltT)/2],[0,0,0,0,1,deltT],[0,0,0,0,-c,1])
		self.SumX = np.array([0.1,0,0,0,0,0],[0,0.1,0,0,0,0],[0,0,100,0,0,0],[0,0,0,0.1,0,0],[0,0,0,0,0.1,0],[0,0,0,0,0,100])
		self.H = np.array([1,0,0,0,0,0],[0,0,0,1,0,0])
		self.SumZ = np.array([25,0],[0,25])
		self.fDOTt = np.dot(F,0.5)
		self.hDOTt = np.dot(H, 0.5)
		self.SumT = np.array([100,0,0,0,0,0],[0,0.1,0,0,0,0],[0,0,0.1,0,0,0],[0,0,0,100,0,0],[0,0,0,0,0.1,0],[0,0,0,0,0,0.1])
		self.utNow = np.array([0],[0],[0],[0],[0],[0])
		self.x_velocity = 0
		self.y_velocity = 0

	# TODO: use the kalman filter to determine if i am facing a direction where the enemy tank will eventually travel
	# me and enemy are objects that store the tank's attributes, like x, y, angle, etc.
	def rotate(self, me, enemy):
		return true

	# TODO: calculate the time difference between the enemy tank getting to firing location and the bullet getting to that same firing location
	# me and enemy are objects that store the tank's attributes, like x, y, angle, etc.
	def fire(self, me, enemy):
		return true

	def calc_kalman(self, enemy, time):
		deltT = 0.5
		c = 0.01
		Zt = np.array([enemy.x],[enemy.y])
		#initialize matrix
		XT = np.array([enemy.x],[enemy.vx],[(self.x_velocity-enemy.vx)/0.5],[enemy.y],[enemy.vy],[(self.y_velocity-enemy.vy)/0.5])

		#		equation = F*sumT*F*T + SumX
		equation = np.dot(np.dot(self.F,self.SumT),self.fDOTt) + self.SumX

		ktNow = np.dot(np.dot(equation,self.hDOTt),(np.dot(np.dot(self.H,equation),self.hDOTt))+self.SumZ) - 1
		#		KtNow = equation*H*T*(H*(equation)*H*T+sumZ) -1

		self.utNow = np.dot(self.F,self.utNow) + np.dot(ktNow,(Zt - np.dot(self.H,np.dot(self.F,self.utNow))))
		#		utNow = F*utNow +  KtNow*((zt+1) - H*F*utNow)

		self.SumT = np.dot(np.identity(6) - (np.dot(ktNow,self.H)),equation)
		#		ΣtNow = (IdentityMatrix - (ktNow)*H)*(equation)

	def main():
		print("Main")
if __name__ == '__main__':
	main()
