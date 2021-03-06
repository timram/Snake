import pygame, random, os, inputbox, time
from Objects import *
from Walls import *
from snakeMenu import *

pygame.init()

class Game(object):
	width = 800
	high = 600
	screen = pygame.display.set_mode([width, high])

	background = (198, 202, 204)
	
	clock = pygame.time.Clock()
	
	font = pygame.font.Font(None, 25)
	fontGameOver = pygame.font.Font(None, 75)

	snake = Snake()

	walls = BlockWall()

	fallBlocks = FallBlock()

	result = {"best":0}

	if os.path.exists("Result.txt"):
		file = open("Result.txt", 'r')
		for line in file:
			line = line.split(' ')
			result[line[0]] = int(line[1])
			print(line)
		file.close()

	name = inputbox.ask(screen, "Your name", background)
	if name not in result:
		result[name] = 0

	myMenu = Menu(screen, clock, background)

	def __init__(self):

		self.fallBlocks.snake = []
		self.snake.__init__()
		self.walls.__init__()

		self.speed  = 20

		self.speedX = self.speed
		self.speedY = 0

		self.score = 0
		self.addScore = 1

		self.food = [Food() for i in range(3)]
		for i in range(3):
			self.food[i].create(self.snake, self.food)

		self.gameover = False

		self.moveSpeed = 0

		self.timeSinceTap = self.snake.speed
		self.timeToDie = 20
		self.startTime = self.endTime = time.time()
		self.pouseTimeStart = self.pouseTime = 0

	def mainGame(self):
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					return
				if event.type == pygame.KEYDOWN and self.timeSinceTap >= self.snake.speed:
					if event.key == pygame.K_UP and self.speedY != self.speed:
						self.speedX = 0; self.speedY = -self.speed
					elif event.key == pygame.K_DOWN and self.speedY != -self.speed:
						self.speedX = 0; self.speedY = self.speed
					elif event.key == pygame.K_LEFT and self.speedX != self.speed:
						self.speedX = -self.speed; self.speedY = 0
					elif event.key == pygame.K_RIGHT and self.speedX != -self.speed:
						self.speedX = self.speed; self.speedY = 0
					elif event.key == pygame.K_RETURN and self.gameover:
						self.__init__()
					elif event.key == pygame.K_ESCAPE:
						if not self.gameover:
							self.pouseTimeStart = time.time()
							choice = self.myMenu.menu(True, self.result, self.name)
							if not choice:
								print("END")
								return
							self.pouseTime += time.time() - self.pouseTimeStart
						else:
							choice = self.myMenu.menu(False, self.result, self.name)
							if not choice:
								print("END")
								return
							self.__init__()
					self.timeSinceTap = 0

			self.screen.fill(self.background)

			self.walls.draw(self.screen)

			self.fallBlocks.draw(self.screen)

			if len(self.fallBlocks.snake) > 0:
				self.fallBlocks.move()

			if len(self.snake.snake) > 0:
				self.snake.draw(self.screen)

			text = self.font.render("%d"%(self.score), True, (255,0,0))
			text1 = self.font.render("Best score: %d"%(self.result['best']), True, (255,0,0))
			text2 = self.font.render("Your best score: %d"%(self.result[self.name]), True, (255,0,0))
			text3 = self.font.render("%.2f"%(self.endTime - self.startTime), True, (255,0,0))
			self.screen.blit(text, [25,25])
			self.screen.blit(text1, [25,75])
			self.screen.blit(text2, [25,50])
			self.screen.blit(text3, [300,25])

			for i in range(3):
				self.food[i].draw(self.screen)

			if self.snake.gameover(self.width, self.high) or self.walls.isTouchWall(self.snake.snake[0], self.snake.size):
				self.gameover = True
				if self.score > self.result['best']:
					self.result['best'] = self.score
				if self.score > self.result[self.name]:
					self.result[self.name] = self.score

			if not self.gameover:
				self.endTime = time.time() - self.pouseTime

				if self.endTime - self.startTime >= self.timeToDie:
					self.gameover = True

				track = self.snake.snake[-1]
				
				self.moveSpeed += 1

				self.addScore = len(self.snake.snake)

				self.score += self.addScore

				if self.moveSpeed >= self.snake.speed:
					
					self.moveSpeed = 0

					for i in range(3):
						if self.snake.snake[0].x in range(self.food[i].x-self.snake.size, self.food[i].x + 20) and \
						self.snake.snake[0].y in range(int(self.food[i].ys)-self.snake.size, int(self.food[i].ys) + 20):
							self.startTime = self.endTime
							self.snake.snake.append(Block(track.x, track.y, track.color, track.nextColor))
							self.snake.speed -= self.food[i].typ
							self.score += self.food[i].addPoint
							self.snake.resize(self.food[i].typ)
							self.fallBlocks.size = self.snake.size
							self.speed -= self.food[i].typ*5
							if self.speed != 0:
								if self.speedX != 0:
									self.speedX -= int(((self.food[i].typ*5)/abs(self.speedX) * self.speedX))
								else:
									self.speedY -= int(((self.food[i].typ*5)/abs(self.speedY) * self.speedY))
								self.food[i].create(self.snake, self.food)
							else:
								self.gameover = True
								if self.score > self.result['best']:
									self.result['best'] = self.score
								if self.score > self.result[self.name]:
									self.result[self.name] = self.score
							break
					self.snake.move(self.speedX, self.speedY)

				touchID = self.walls.isWallTouch(self.snake.snake,self.snake.size)

				if touchID != None:
					self.fallBlocks.speed = touchID[1]+5
					for i in range(len(self.snake.snake)-1, touchID[0]-1, -1):
						self.fallBlocks.snake.append(self.snake.snake[i])
						self.snake.snake.remove(self.snake.snake[i])
					self.score -= len(self.fallBlocks.snake)*100

				self.walls.move()

			else:
				text = self.fontGameOver.render("GAME OVER", True, (255,0,0))
				textSuppot =self.font.render("For continue tap ENTER", True, (0,0,0))
				textSuppot1 =self.font.render("For exit tap ESCAPE", True, (0,0,0))
				self.screen.blit(text, [275, 200])
				self.screen.blit(textSuppot, [335, 275])
				self.screen.blit(textSuppot1, [335, 300])


			self.timeSinceTap += 1
			self.clock.tick(30)

			pygame.display.flip()

def main():
	game = Game()
	print(game.name)
	choice = game.myMenu.menu(False, game.result, game.name)
	if not choice:
		print("END")
		return

	game.__init__()
	game.mainGame()

	file = open("Result.txt", 'w')
	for key in game.result:
		file.write(key + " " + str(game.result[key])+' \n')
	file.close()

main()

pygame.quit()