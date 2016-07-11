import pygame, random

class mapBlock(object):
	def __init__(self, getBlocks):
		self.blocks = [block for block in getBlocks]
		self.busyX = []
		self.busyY = []
		for block in self.blocks:
			for x in range(block[0]-20, block[0]+block[2]+10):
				self.busyX.append(x)
			for y in range(block[1]-20, block[1]+block[3]+10):
				self.busyY.append(y)
		self.availX = [x for x in range(780) if x not in self.busyX]
		self.availY = [y for y in range(580) if y not in self.busyY]


class Map(object):
	def __init__(self):
		self.allMaps = [mapBlock([[300,200,100,200],[500,200,100,200]]), mapBlock([[300,200,200,100], [300,400,200,100]])]
		self.curMap = random.choice(self.allMaps) 

	def draw(self,screen):
		for block in self.curMap.blocks:
			pygame.draw.rect(screen, (0,0,0), block)

	def isTouchWall(self, head, size):
		for block in self.curMap.blocks:
			if head.x in range(block[0]-size, block[0]+block[2]) and head.y in range(block[1]-size, block[1]+block[3]):
				return True
		return False