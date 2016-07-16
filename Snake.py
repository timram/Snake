import pygame, random, os
from Objects import *
from Walls import *
from snakeMenu import *

pygame.init()

class Game(object):
	width = 800
	high = 600
	screen = pygame.display.set_mode([width, high])
	
	clock = pygame.time.Clock()
	
	font = pygame.font.Font(None, 25)
	
	snake = Snake()

	walls = BlockWall()

	myMenu = Menu(screen, clock)

	fallBlocks = FallBlock()

	def __init__(self):
		self.best = 0

		if os.path.exists("Result.txt"):
			file = open("Result.txt", 'r')
			self.best = int(file.readline())
			file.close()

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
					elif event.key == pygame.K_ESCAPE and not self.gameover:
						choice = self.myMenu.menu(True)
						if not choice:
							print("END")
							return
					self.timeSinceTap = 0

			self.screen.fill((255,255,255))

			self.walls.draw(self.screen)

			self.fallBlocks.draw(self.screen)

			if len(self.fallBlocks.snake) > 0:
				self.fallBlocks.move()

			self.snake.draw(self.screen)

			text = self.font.render("%d"%(self.score), True, (255,0,0))
			text1 = self.font.render("Best score: %d"%(self.best), True, (255,0,0))
			self.screen.blit(text, [25,25])
			self.screen.blit(text1, [25,50])

			for i in range(3):
				self.food[i].draw(self.screen)

			if self.snake.gameover(self.width, self.high) or self.walls.isTouchWall(self.snake.snake[0], self.snake.size):
				self.gameover = True
				if self.score > self.best:
					file = open("Result.txt", 'w')
					file.write(str(self.score))
					file.close()

			if not self.gameover:
				track = self.snake.snake[-1]
				
				self.moveSpeed += 1

				self.addScore = len(self.snake.snake)

				self.score += self.addScore

				if self.moveSpeed >= self.snake.speed:
					
					self.moveSpeed = 0

					for i in range(3):
						if self.snake.snake[0].x in range(self.food[i].x-self.snake.size, self.food[i].x + 20) and \
						self.snake.snake[0].y in range(int(self.food[i].ys)-self.snake.size, int(self.food[i].ys) + 20):
							self.snake.snake.append(Block(track.x, track.y))
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
							break
					self.snake.move(self.speedX, self.speedY)

				touchID = self.walls.isWallTouch(self.snake.snake,self.snake.size)

				if touchID != None:
					self.fallBlocks.speed = touchID[1]+5
					for i in range(len(self.snake.snake)-1, touchID[0]-1, -1):
						self.fallBlocks.snake.append(self.snake.snake[i])
						self.snake.snake.remove(self.snake.snake[i])

				print(self.fallBlocks.snake, len(self.fallBlocks.snake))

				self.walls.move()

			self.timeSinceTap += 1
			self.clock.tick(30)

			pygame.display.flip()

def main():
	game = Game()
	choice = game.myMenu.menu(False)
	if not choice:
		print("END")
		return

	game.mainGame()

main()

pygame.quit()