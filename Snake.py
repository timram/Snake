import pygame, random
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

	myMap = Map()

	myMenu = Menu(screen, clock)


	def __init__(self):
		self.speed  = 20

		self.speedX = self.speed
		self.speedY = 0

		self.score = 0
		self.addScore = 5

		self.food = [Food() for i in range(3)]
		for i in range(3):
			self.food[i].create(self.snake, self.food, self.myMap.curMap.availX, self.myMap.curMap.availY)

		self.gameover = False

		self.moveSpeed = 0

		self.timeSinceTap = self.snake.speed

		self.myMap.__init__()
		self.snake.__init__()

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

			self.myMap.draw(self.screen)

			self.snake.draw(self.screen)

			text = self.font.render("%d"%(self.score), True, (255,0,0))
			self.screen.blit(text, [25,25])

			for i in range(3):
				self.food[i].draw(self.screen)

			if self.snake.gameover(self.width, self.high) or self.myMap.isTouchWall(self.snake.snake[0], self.snake.size):
				self.gameover = True

			if not self.gameover:
				track = self.snake.snake[-1]
				
				self.moveSpeed += 1

				self.score += self.addScore

				if self.moveSpeed >= self.snake.speed:
					
					self.moveSpeed = 0

					for i in range(3):
						if self.snake.snake[0].x in range(self.food[i].x-self.snake.size, self.food[i].x + 20) and \
						self.snake.snake[0].y in range(int(self.food[i].ys)-self.snake.size, int(self.food[i].ys) + 20):
							self.snake.snake.append(Block(track.x, track.y))
							self.snake.speed -= self.food[i].typ
							if self.addScore >= 1:
								self.addScore -= self.food[i].typ
							self.snake.resize(self.food[i].typ)
							self.speed -= self.food[i].typ*5
							if self.speed != 0:
								if self.speedX != 0:
									self.speedX -= int(((self.food[i].typ*5)/abs(self.speedX) * self.speedX))
								else:
									self.speedY -= int(((self.food[i].typ*5)/abs(self.speedY) * self.speedY))
								self.food[i].create(self.snake, self.food, self.myMap.curMap.availX, self.myMap.curMap.availY)
							else:
								self.gameover = True
							break
					self.snake.move(self.speedX, self.speedY)

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