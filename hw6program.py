from random import randrange

ex = " is executed."
par = " is pardoned."

def Guard(executed):
	temp = randrange(0, 3)
	while temp == executed or temp == 0:
		temp = randrange(0, 3)
	return temp

def Execution():

	e = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

	for i in range(1, 100000):

		executed = randrange(0, 3)
		pardoned = Guard(executed)

		e[executed][pardoned] += 1

	print "A is executed:", e[0], "\nB is executed:", e[1], "\nC is executed:", e[2]

if __name__ == '__main__':
	Execution()
