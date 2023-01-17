##Network
from matrix import matrix

class network:
	def __init__(self, weights, biases):
		self.weights = weights #list of matrix
		self.biases = biases #list of matrix
		self.layers = len(self.weights) + 1 

	def propagate(self, inp):
		current = inp
		for i in range(self.layers - 1):
			current = current.multiply(self.weights[i]).add(self.biases[i]).sigma()
		#print(current)
		return current

'''testNetwork = network([matrix().normDist([2, 2]), matrix().normDist([2, 2])], [matrix().normDist([2, 1]), matrix().normDist([2, 1])])

print(testNetwork.propagate(matrix([[1, 0]])))'''