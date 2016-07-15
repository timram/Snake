import pygame, random

class Wall(object):
	def __init__(self, x):
		self.x = x
		self.width = random.randint(50,150)
		self.high = random.randint(50,150)
		self.y = 0 - self.high
		self.speed = int(0.001 * (self.width* self.high))

class BlockWall(object):
	def __init__(self):
		self.wall = [[Wall(250), 250], [Wall(600),600]]

	def draw(self, screen):
		for i in range(len(self.wall)):
			pygame.draw.rect(screen, (0,0,0), [self.wall[i][0].x, self.wall[i][0].y, self.wall[i][0].width, self.wall[i][0].high])

	def move(self):
		for i in range(len(self.wall)):
			self.wall[i][0].y += self.wall[i][0].speed
			if self.wall[i][0].y >= 600:
				self.wall[i][0].__init__(self.wall[i][1])

	def isTouchWall(self,head, size):
		for i in range(len(self.wall)):
			if head.x+size in range(self.wall[i][0].x, self.wall[i][0].x + self.wall[i][0].width) and\
			head.y+size in range(self.wall[i][0].y, self.wall[i][0].y + self.wall[i][0].high):
				return True
		return False

	def isWallTouch(self, snake):	
		for i in range(1, len(snake)):
			if (snake[i].x in range(self.wall[0][0].x, self.wall[0][0].x + self.wall[0][0].width) and\
			snake[i].y in range(self.wall[0][0].y, self.wall[0][0].y + self.wall[0][0].high)) or\
			(snake[i].x in range(self.wall[1][0].x, self.wall[1][0].x + self.wall[1][0].width) and\
			snake[i].y in range(self.wall[1][0].y, self.wall[1][0].y + self.wall[1][0].high)):
				if snake[i].x < 500 :
					return [i, self.wall[0][0].speed]
				return [i, self.wall[1][0].speed]
		return None