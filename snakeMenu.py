import pygame, time
from random import randint, choice

class button(object):
    def __init__(self, name):
        self.name = name
        self.isSelect = False
        self.font = pygame.font.Font(None, 50)

    def draw(self,screen,x,y):
        text = self.font.render(self.name, True, (255,255,255))
        if self.isSelect:
            pygame.draw.rect(screen, (226,247,141), [x,y,230,130])
        else:
            pygame.draw.rect(screen, (226,247,141), [x,y,200,100])

        screen.blit(text, [x+50, y+25])

class Circle(object):
	def __init__(self, colors):
		self.x = randint(0,750)
		self.y = randint(0,550)
		self.rad = randint(10,30)
		self.add = 1
		self.speedX = choice([-1,1])
		self.speedY = choice([-1,1])
		self.color = choice(colors)
		self.addR = 1
		self.addG = 1
		self.addB = 1

	def changeColor(self):
		if self.color[0] >= 240 or self.color[0] <= 153:
			self.addR *= -1
		if self.color[1] >= 247 or self.color[1] <= 132:
			self.addG *= -1
		if self.color[2] >= 245 or self.color[2] <= 86:
			self.addB *= -1
		self.color[0] += self.addR; self.color[1] += self.addG; self.color[2] += self.addB

class Menu(object):
	def __init__(self,screen,clock):
		self.screen = screen
		self.clock  = clock
		self.num = 25
		self.colors = [[204,132,245], [153,247,213], [240,201,86]]

	def changeCircle(self, circle):
		for i in range(self.num):
			if circle[i].rad == 40 or circle[i].rad == 9:
				circle[i].add *= -1
			circle[i].rad += circle[i].add
			if circle[i].x + circle[i].rad > 800 or circle[i].x - circle[i].rad < -20:
				circle[i].speedX *= -1
			if circle[i].y + circle[i].rad > 600 or circle[i].y - circle[i].rad < -20:
				circle[i].speedY *= -1
			circle[i].x += circle[i].speedX
			circle[i].y += circle[i].speedY

	def menu(self, isPlay):
		buttons = [button("PLAY"), button("STAT"), button("EXIT")]
		y = [75,250,425]
		buttons[0].isSelect = True
		done = True
		n = 0
		circle = [Circle(self.colors) for i in range(self.num)]
		exit = False
		while done:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					return False
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_UP:
						for i in range(3):
							if buttons[i].isSelect:
								prev = i
								break
						buttons[prev].isSelect = False
						if prev == 0:
							buttons[2].isSelect = True
						else:
							buttons[prev-1].isSelect = True
					elif event.key == pygame.K_DOWN:
						for i in range(3):
							if buttons[i].isSelect:
								prev = i
								break
						buttons[prev].isSelect = False
						if prev == 2:
							buttons[0].isSelect = True
						else:
							buttons[prev+1].isSelect = True
					elif event.key == pygame.K_RETURN and buttons[2].isSelect:
						return False
					elif event.key == pygame.K_RETURN and buttons[0].isSelect:
						return True
					elif event.key == pygame.K_ESCAPE:
						if isPlay:
							return True
						return False

			self.screen.fill((247,141,235))
			self.changeCircle(circle)
			for i in range(self.num):
				pygame.draw.circle(self.screen, circle[i].color, (circle[i].x,circle[i].y),circle[i].rad)
				circle[i].changeColor()
			for i in range(3):
				buttons[i].draw(self.screen, 300, y[i])
			pygame.display.flip()
			self.clock.tick(60)