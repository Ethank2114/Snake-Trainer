##snakeDisplay

import pygame, sys
from snake import snake, apple, game, board, dna
from matrix import matrix

class colour:
	def __init__(self):
		self.white = (255, 255, 255)
		self.green = (0, 255, 0)
		self.red = (255, 0, 0)
colour = colour()

class display:
	def __init__(self, width, height, games):
		self.width = width
		self.height = height
		self.games = games

		self.window = window = pygame.display.set_mode((self.width, self.height))
		pygame.init()

		while True:
			window.fill(colour.white)

			for game in games:
				widthRatio = self.width / game.board.width
				heightRatio = self.height / game.board.height
				for i in game.snake.body:
					pygame.draw.rect(window, colour.green, ((i[0] - 1) * widthRatio, (i[1] - 1) * heightRatio, widthRatio, heightRatio))
				pygame.draw.rect(window, colour.red, ((game.apple.x - 1) * widthRatio, (game.apple.y - 1) * heightRatio, widthRatio, heightRatio))

			pygame.display.update()

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
					break 

				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_SPACE:
						self.games[0].step()

'''
testBoard = board(10,10)
testDna = dna([matrix().arcNorm([8, 32]), matrix().arcNorm([8, 8]), matrix().arcNorm([4, 8])], [matrix().arcNorm([8, 1]), matrix().arcNorm([8, 1]), matrix().arcNorm([4, 1]).scale(1/10)])
testgame = game(snake([[4, 3], [4, 4], [4, 5]], testDna), apple(7, 3), testBoard)

testDisplay = display(500, 500, [testgame])'''

'''
window = pygame.display.set_mode((500, 500))
pygame.init()

while True:
	window.fill(colour.white)

	pygame.draw.rect(window, (255, 0, 0), ((testgame.apple.x - 1) * 500 / 10, (testgame.apple.y - 1) * 500 / 10, 500 / 10, 500 / 10)) #draw apple
	for i in testgame.snake.body: #draw snake
		pygame.draw.rect(window, (0, 255, 0), ((i[0] - 1) * 500 / 10, (i[1] - 1) * 500 / 10, 500 / 10, 500 / 10))
	
	pygame.display.update()

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
			break

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE:
				testgame.step()

			if event.key == pygame.K_UP:
				testgame.snake.direction = matrix([[0, -1]])
				testgame.step()
			if event.key == pygame.K_DOWN:
				testgame.snake.direction = matrix([[0, 1]])
				testgame.step()
			if event.key == pygame.K_LEFT:
				testgame.snake.direction = matrix([[-1, 0]])
				testgame.step()
			if event.key == pygame.K_RIGHT:
				testgame.snake.direction = matrix([[1, 0]])
				testgame.step()
'''