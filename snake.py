##Snake 

'''
network
	weights
	biases
	input
	output

board
	game
		Snake
			location
			fitness
			DNA (ai)
		apple
			location

trainer
	calculate fitness/display rounds
	procceed generation
		kill off weak
		breed
		mutate

'''

import random, math
from matrix import matrix
from network import network

class dna:
	def __init__(self, weights = None, biases = None):
		self.weights = weights
		self.biases = biases

	def mutate(self, rate):
		for x in range(len(self.weights)):
			for i in range(len(self.weights[x].elements)):
				for j in range(len(self.weights[x].elements[i])):
					if random.randint(0, round(rate ** (-1))) == 0:
						#print("utated")
						self.weights[x].elements[i][j] += matrix().arcNormHelper(random.uniform(-1, 1))

		for x in range(len(self.biases)):
			for j in range(len(self.biases[x].elements[0])):
				if random.randint(0, round(rate ** (-1))) == 0:
					self.biases[x].elements[0][j] += matrix().arcNormHelper(random.uniform(-1, 1))

		

	def combine(self, other):
		for x in range(len(self.weights)):
			for i in range(len(self.weights[x].elements)):
				for j in range(len(self.weights[x].elements[i])): 
					self.weights[x].elements[i][j] = (self.weights[x].elements[i][j] + other.weights[x].elements[i][j]) / 2

		return self

	def new(self):
		return dna([matrix().arcNorm([8, 32]), matrix().arcNorm([8, 8]), matrix().arcNorm([4, 8])], [matrix().arcNorm([8, 1]), matrix().arcNorm([8, 1]), matrix().arcNorm([4, 1]).scale(1/10)])


class snake: 
	def __init__(self, body = None, dna = None):
		self.body = body
		self.direction = matrix([[1, 0]]) #vector
		
		self.apples = 0
		self.steps = 0
		self.hunger = 0
		self.full = 0
		self.alive = True
		self.fitness = None

		self.dna = dna

	def die(self):
		self.alive = False
		self.calcFitness()

	def move(self, apple, board):
		
		outLayer = network(self.dna.weights, self.dna.biases).propagate(matrix([self.see(apple, board)])).elements[0]
		direction = (math.pi / 2) * outLayer.index(sorted(outLayer)[-1])
		unit = matrix([[round(math.cos(direction)), round(math.sin(direction))]])

		newHead = matrix([self.body[-1]]).add(unit).elements[0]

		#print(outLayer)
		#print(unit.elements)

		if newHead in self.body or newHead[0] > board.width or newHead[0] < 1 or newHead[1] > board.height or newHead[1] < 1:
			self.die()
		else:
			self.body.append(newHead)
			self.steps += 1
			self.hunger += 1
			if self.hunger > 100:
				self.die()
			if self.full == 0:
				self.body.pop(0) 
			else:
				self.full -= 1

	def eat(self):
		pass


	def see(self, apple, board):
		headDirection = matrix([self.body[-2]]).subtract(matrix([self.body[0]])).elements[-1]
		tailDirection = matrix([self.body[1]]).subtract(matrix([self.body[0]])).elements[0]

		hd = [0, 0, 0, 0]
		hd[(headDirection[0] + headDirection[1] * 2) % 4 - 1 if headDirection[1] != -1 else 3] = 1

		td = [0, 0, 0, 0]
		td[(tailDirection[0] + tailDirection[1] * 2) % 4 - 1 if tailDirection[1] != -1 else 3] = 1

		#apple direction
		#wall direction
		#body direction
		a = [] #apples
		appleHeading = matrix([[apple.x, apple.y]]).subtract(matrix([self.body[-1]]))
		for i in range(8): #apples
			if [round(appleHeading.norm().elements[0][0], 10), round(appleHeading.norm().elements[0][1], 10)] == [round(math.cos((math.pi * i) / 4), 10), round(math.sin((math.pi * i) / 4), 10)]:
				a.append(1 - (appleHeading.magnitude() / ((2 ** (1/2)) ** (i % 2)) - 1 ) / ((board.width + board.height) / 2))
			else:
				a.append(0)

		b = [] #body
		for i in range(8): #body (all)
			unit = [math.cos(math.pi * i / 4) * ((2**(1/2)) ** (i % 2)), math.sin(math.pi * i / 4) * ((2**(1/2)) ** (i % 2))]
			current = self.body[-1]
			dummy = 0
			for j in range(int((board.width + board.height) / 2)):
				current = [current[x] + unit[x] for x in range(2)]
				if current in self.body:
					dummy = 1 - (round((matrix([current]).subtract(matrix([self.body[-1]])).magnitude() / ((2**(1/2)) ** (i % 2)) - 1) / ((board.width + board.height) / 2), 5))
					break
			b.append(dummy)


		w = [] #walls
		for i in range(8):
			unit = [round(math.cos(math.pi * i / 4) * ((2**(1/2)) ** (i % 2))), round(math.sin(math.pi * i / 4) * ((2**(1/2)) ** (i % 2)))]
			current = self.body[-1]
			counter = 0
			while True:
				if current[0] == board.width or current[0] == 1 or current[1] == board.height or current[1] == 1:
					w.append(round(1 - (counter / int((board.width + board.height) / 2)), 8))
					break
				current = [current[x] + unit[x] for x in range(2)]
				counter += 1

		#print(hd + td + a + b + w)
		return hd + td + a + b + w

	def calcFitness(self):

		a = self.apples
		s = self.steps
		self.fitness = s + ((2 ** a) + (500 * (a ** 2.1))) - (a ** 1.2) * ((0.25 * s)**1.3 )

	def new(self):
		return snake([[4, 3], [4, 4], [4, 5]], dna().new())

	def breed(self, other):
		self.dna = self.dna.combine(other.dna)
		return self

	def reset(self):
		self.apples = 0
		self.steps = 0
		self.hunger = 0
		self.full = 0
		self.alive = True
		




class apple:
	def __init__(self, x = 1, y = 1):
		self.x = x
		self.y = y

	def new(self, board):
		self.x = random.randint(1, board.width)
		self.y = random.randint(1, board.height)
		return self

class board:
	def __init__(self, width, height):
		self.width = width
		self.height = height

class game:
	def __init__(self, snake = None, apple = None, board = None):
		self.snake = snake
		self.apple = apple
		self.board = board

	def step(self):
		#print(self.snake.body)
		if self.snake.alive:
			self.snake.move(self.apple, self.board) 
			while [self.apple.x, self.apple.y] in self.snake.body:
			#print("eat")
				self.apple.x = random.randint(1, self.board.width)
				self.apple.y = random.randint(1, self.board.height)
				self.snake.apples += 1
				self.snake.full += 1
		else:
			print("dead")

	def completeGame(self):
		while self.snake.alive:
			self.step()

	def new(self):
		return game(snake().new(), apple(7, 3), board(10, 10))
		
'''
testBoard = board(5,5)
testDna = dna([matrix().normDist([8, 32]), matrix().normDist([8, 8]), matrix().normDist([4, 8])], [matrix().normDist([8, 1]), matrix().normDist([8, 1]), matrix().normDist([4, 1])])
testgame = game(snake([[2, 5], [2,4], [2,3]], testDna), apple(4, 5), testBoard)

testgame.step()'''