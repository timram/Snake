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
		self.availColor = [col for col in colors if col != self.color]
		self.nextColor = choice(self.availColor) 
		
	def changedColor(self):
		for i in range(len(self.color)):
			if self.color[i] > self.nextColor[i]:
				self.color[i] -= 1
			elif self.color[i] < self.nextColor[i]:
				self.color[i] += 1

		if self.color == self.nextColor:
			return True
		else:
			return False

class Menu(object):
	def __init__(self,screen,clock, result):
		self.screen = screen
		self.clock  = clock
		self.num = 30
		self.result = result
		self.font = pygame.font.Font(None, 25)
		self.bestfont = pygame.font.Font(None, 50)

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

	def showResult(self):
		text = self.bestfont.render("%s : %d"%("BEST",self.result['best']), True, (255,255,255))
		self.screen.blit(text, [350, 50])
		y = 100
		for key in self.result:
			if key != "best":
				text = self.font.render("%s : %d"%(key,self.result[key]), True, (255,255,255))
				self.screen.blit(text, [350, y])
				y += 25

	def menu(self, isPlay):
		buttons = [button("PLAY"), button("STAT"), button("EXIT")]
		y = [75,250,425]
		buttons[0].isSelect = True
		done = True
		n = 0
		circle = [Circle([[204,132,245], [153,247,213], [240,201,86]]) for i in range(self.num)]
		exit = False
		showResult = False
		while done:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					return False
				if event.type == pygame.KEYDOWN:
					if not showResult:
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
					if event.key == pygame.K_RETURN and buttons[2].isSelect:
						return False
					elif event.key == pygame.K_RETURN and buttons[0].isSelect:
						return True
					elif event.key == pygame.K_RETURN and buttons[1].isSelect:
						if showResult:
							showResult = False
						else:
							showResult = True
					elif event.key == pygame.K_ESCAPE:
						if isPlay:
							return True
						return False

			self.screen.fill((247,141,235))
			self.changeCircle(circle)
			for i in range(self.num):
				pygame.draw.circle(self.screen, circle[i].color, (circle[i].x,circle[i].y),circle[i].rad)
				if circle[i].changedColor():
					circle[i].availColor = [col for col in [[204,132,245], [153,247,213], [240,201,86]] if col != circle[i].color]
					circle[i].nextColor = choice(circle[i].availColor)

			if showResult:
				self.showResult() 
			else:
				for i in range(3):
					buttons[i].draw(self.screen, 300, y[i])
			pygame.display.flip()
			self.clock.tick(60)