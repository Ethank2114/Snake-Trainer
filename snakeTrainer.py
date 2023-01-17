##snake trainer

from snake import snake, apple, game, board, dna
from matrix import matrix
from snakeDisplay import display
import random



class trainer:
	def __init__(self, games = []):
		self.games = games

	def display(self, width, height):
		display(width, height, self.games)

	def newPop(self, popSize):
		for i in range(popSize):
			self.games.append(game().new())

	def completeGames(self):
		for game in self.games:
			game.completeGame()

		def findFitness(x):
			return x.snake.fitness
		self.games.sort(key = findFitness, reverse = True)

	def nextGeneration(self):

		self.completeGames()

		aSet = set()
		while len(aSet) <= 80:
			aSet.add(round(100*(-(1-(random.uniform(0, 1))**6)**(1/2) + 1)))

		#print(aSet)

		newGames = [self.games[i] for i in aSet]

		for i in range(0, 20, 2):
			newGames.append(game(newGames[i].snake.breed(newGames[i + 1].snake), apple(7, 3), board(10, 10)))

		for i in range(10):
			newGames.append(game().new())

		for i in range(len(newGames)):
			newGames[i].snake.dna.mutate(1 / self.games[0].snake.fitness)
			newGames[i].snake.reset()

		self.games = newGames.copy()

		

'''
testBoard = board(10,10)
testDna = dna([matrix().arcNorm([8, 32]), matrix().arcNorm([8, 8]), matrix().arcNorm([4, 8])], [matrix().arcNorm([8, 1]), matrix().arcNorm([8, 1]), matrix().arcNorm([4, 1]).scale(1/10)])
testgame = game(snake([[4, 3], [4, 4], [4, 5]], testDna), apple(7, 3), testBoard)

testDisplay = display(500, 500, [testgame])'''

testTrainer = trainer()
testTrainer.newPop(100)
testTrainer.completeGames()



for i in range(100):
	testTrainer.nextGeneration()
	testTrainer.completeGames()
	print([game.snake.fitness for game in testTrainer.games])
	

	
	input("next?")