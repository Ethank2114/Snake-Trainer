##matrix
from tabulate import tabulate
import math, random

class matrix:
	def __init__(self, elements = [[1, 0], [0, 1]]): 
		self.elements = elements
		self.m = len(self.elements[0]) #height
		self.n = len(self.elements)	#width

	def __str__(self):
		return tabulate([*zip(*self.elements)])

	def add(self, other):
		return matrix([[self.elements[i][j] + other.elements[i][j] for j in range(self.m)] for i in range(self.n)])

	def subtract(self, other):
		return matrix([[self.elements[i][j] - other.elements[i][j] for j in range(self.m)] for i in range(self.n)])

	def multiply(self, other): #multiply 2 matrix's # other x self
		#[[1, 0, 0], [0, 1, 0], [0, 0, 1]]
		dummy1 = []
		for i in range(self.n): #width
			dummy2 = []
			for j in range(other.m): #height
				counter = 0
				for k in range(self.m):
					counter += self.elements[i][k] * other.elements[k][j]
				dummy2.append(counter)
			dummy1.append(dummy2)
		return matrix(dummy1)

	def scale(self, num): #scale by a constant
		return matrix([[self.elements[i][j] * num for j in range(self.m)] for i in range(self.n)])

	def magnitude(self):
		count = 0
		for i in range(self.m):
			count += self.elements[0][i] ** 2
		return count ** (1/2)

	def norm(self):
		return self.scale(1 / self.magnitude())

	def sigma(self):
		return matrix([[1 / ((math.exp(-1 * self.elements[i][j])) + 1) for j in range(self.m)] for i in range(self.n)])

	def normDist(self, size): #normal distribution curve
		return matrix([[math.exp((-1) * ((random.uniform(-3, 3)) ** 2)) for j in range(size[0])] for i in range(size[1])]) 

	def arcNormHelper(self, x):
		if x < 0:
			return (-1 * math.log(x + 1))**0.5
		elif x >= 0:
			return -1* (-1* math.log(-1*(x-1)))**0.5

	def arcNorm(self, size):
		return matrix([[self.arcNormHelper(random.uniform(-1, 1)) for j in range(size[0])] for i in range(size[1])]) 
