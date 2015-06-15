

class ValueIteration:

	def __init__(self):

		# states
		self.states = ["s1", "s2", "s3", "s4"]
		self.actions = ["n", "p"]

		# instant reward
		self.R = {}
		self.R["s1"] = 50		# c++ h++
		self.R["s2"] = 0		# c++ h--
		self.R["s3"] = 100		# c-- h++
		self.R["s4"] = 10		# c-- h--


		# discount factor
		self.gamma = 1

		self.P = {}

		self.P[("s1", "n")] = [("s1", 0.5), ("s2", 0.5)]
		self.P[("s1", "p")] = [("s3", 1)]

		self.P[("s2", "n")] = [("s1", 0.5), ("s2", 0.5)]
		self.P[("s2", "p")] = [("s4", 1)]

		self.P[("s3", "n")] = [("s1", 1)]
		self.P[("s3", "p")] = [("s3", 0.5), ("s4", 0.5)]

		self.P[("s4", "n")] = [("s2", 0.5), ("s3", 0.5)]
		self.P[("s4", "p")] = [("s4", 1)]

		# future reward
		self.U = {}
		self.U["s1"] = 0
		self.U["s2"] = 0
		self.U["s3"] = 0
		self.U["s4"] = 0


	def iterate(self):
		# hold the current iteration's values
		temp = {}

		for state in self.states:
			# no chemo
			n = self.P[(state, "n")]
			n_val = 0
			for future_state,future_prob in n:
				n_val += future_prob * self.U[future_state]

			# yes chemo 
			p = self.P[(state, "p")]
			p_val = 0
			for future_state,future_prob in p:
				p_val += future_prob * self.U[future_state]

			best = self.R[state] + self.gamma*max(n_val, p_val)
			temp[state] = best

		self.U = temp

if __name__ == '__main__':
	v = ValueIteration()
	for i in range(0, 1000):
		v.iterate()
	print v.U