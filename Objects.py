import pygame, random

class Block(object):
	def __init__(self, x, y):
		self.x = x
		self.y = y

	def draw(self, screen, size):
		pygame.draw.rect(screen, (255,0,0), [self.x, self.y, size, size])


class Snake(object):
	def __init__(self):
		self.snake = []
		self.snake.append(Block(100,100))
		self.speed = 3
		self.size = 20

	def move(self, speedX, speedY):
		if speedX != 0:	
			addX = speedX + int((1/abs(speedX) * speedX))
			addY = 0
		else:
			addX = 0
			addY = speedY + int((1/abs(speedY) * speedY))

		
		x = self.snake[0].x + addX
		y = self.snake[0].y + addY

		self.snake.insert(0, Block(x, y))
		self.snake.remove(self.snake[-1])

	def gameover(self, width, high):
		head = self.snake[0]
		if head.x <= 0 or head.x + self.size >= width or head.y <= 0 or head.y + self.size >= high:
			return True
		for coor in self.snake[3:]:
			if head.x in range(coor.x, coor.x+self.size) and head.y in range(coor.y, coor.y + self.size):
				return True
		return False

	def resize(self, inc):
		self.size -= inc*5

	def draw(self, screen):
		for i in range(len(self.snake)):
			self.snake[i].draw(screen, self.size)


class Food(object):
	def __init__(self):
		self.x = 0
		self.y = 0
		self.ys = -20
		self.speed = 1
		self.toDown = True
		self.stop = False
		self.typ = 0
		self.color = (0,0,0)

	def checkCoor(self, list1, list2, availX, availY, size1, size2):
		self.x = random.choice(availX)
		self.y = random.choice(availY)
		inSnake = False
		inFood = False
		for block in list1:
			if self.x in range(block.x - size1, block.x + size1) and self.y in range(block.y - size1, block.y + size1):
				inSnake = True

		for block in list2:
			if self.x != block.x and self.y != block.y and self.x in range(block.x - size2, block.x + size2) and \
			self.y in range(block.y - size2, block.y + size2):
				inFood = True

		if inSnake or inFood:
			self.checkCoor(list1, list2, availX, availY, size1, size2)

	def create(self, snake, food, availX, availY):
		self.ys = -20
		self.speed = 1
		self.toDown = True
		self.stop = False

		self.typ = random.choice((-1,0,1))

		if self.typ == -1:
			self.color = (255,0,0)
		elif self.typ == 0:
			self.color = (0,255,0)
		else:
			self.color = (0,0,255)

		self.checkCoor(snake.snake, food, availX, availY, snake.size, 20)

	def fall(self):
		if not self.stop:
			if self.toDown:
				self.ys += self.speed
				self.speed += 0.5
				if self.ys >= self.y:
					self.toDown = False
					self.speed /= 2
					if self.speed <= 1:
						self.stop = True
			else:
				self.ys -= self.speed
				self.speed -= 0.5
				if self.speed <= 0:
					self.toDown = True

	def draw(self,screen):
		pygame.draw.rect(screen, self.color, [self.x, self.ys, 20,20])
		self.fall()
