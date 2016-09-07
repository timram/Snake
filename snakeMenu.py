import pygame, time, os
from random import randint, choice
import inputbox

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

	def __init__(self):
		self.x = randint(0,750)
		self.y = randint(0,550)
		self.minRad = randint(5,15)
		self.maxRad = randint(35,45)
		self.rad = randint(self.minRad, self.maxRad)
		self.add = 1
		self.speedX = choice([-1,1])
		self.speedY = choice([-1,1])
		self.color = choice([[204,132,245], [153,247,213], [240,201,86]])
		self.availColor = [col for col in [[204,132,245], [153,247,213], [240,201,86]] if col != self.color]
		self.nextColor = choice(self.availColor) 
		
	def changeColor(self):
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
	def __init__(self,screen,clock, background):
		self.screen = screen
		self.clock  = clock
		self.num = 40
		self.font = pygame.font.Font(None, 25)
		self.bestfont = pygame.font.Font(None, 50)
		self.background = background

	def changeCircle(self, circle):
		for i in range(self.num):
			if circle[i].rad == circle[i].maxRad or circle[i].rad == circle[i].minRad - 1:
				circle[i].add *= -1
			circle[i].rad += circle[i].add
			if circle[i].x + circle[i].rad > 800 or circle[i].x - circle[i].rad < -20:
				circle[i].speedX *= -1
			if circle[i].y + circle[i].rad > 600 or circle[i].y - circle[i].rad < -20:
				circle[i].speedY *= -1
			circle[i].x += circle[i].speedX
			circle[i].y += circle[i].speedY

	def showResult(self, result, name):
		text = self.bestfont.render("%s : %d"%("BEST",result['best']), True, (63, 64, 59))
		text1 = self.font.render("For clear history press 'c'", True, (63,64,59))
		self.screen.blit(text, [350, 50])
		self.screen.blit(text1, [20, 20])
		y = 100
		for key in result:
			if key != "best":
				text = self.font.render("%s : %d"%(key,result[key]), True, (63, 64, 59))
				self.screen.blit(text, [350, y])
				y += 25

	def showWarMes(self):
		pygame.draw.rect(self.screen, (255,255,255), [280, 200, 350,100])
		text = self.font.render("Are you sure whant to clear hystory?", True, (0,0,0))
		self.screen.blit(text, [300, 220])
		text = self.font.render("(y/n)", True, (0,0,0))
		self.screen.blit(text, [435, 250])

	def clearHistory(self, result):
		file = open("Result.txt", 'w')
		file.close()
		for key in result:
			result[key]=0

	def menu(self, isPlay, result, name):
		buttons = [button("PLAY"), button("STAT"), button("EXIT")]
		y = [75,250,425]
		buttons[0].isSelect = True
		done = True
		n = 0
		circle = [Circle() for i in range(self.num)]
		exit = False
		showResult = False
		showWarMes = False
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
					elif event.key == pygame.K_RETURN and buttons[1].isSelect and not showWarMes:
						if showResult:
							showResult = False
						else:
							showResult = True
					elif event.key == 99 and showResult:
						showWarMes = True
					elif event.key == 121 and showWarMes:
						self.clearHistory(result)
						showWarMes = False
					elif event.key == 110 and showWarMes:
						showWarMes = False
					elif event.key == pygame.K_ESCAPE:
						if showResult:
							showResult = False
						else:
							if isPlay:
								return True
							return False

			self.screen.fill(self.background)
			self.changeCircle(circle)
			for i in range(self.num):
				pygame.draw.circle(self.screen, circle[i].color, (circle[i].x,circle[i].y),circle[i].rad)
				if circle[i].changeColor():
					circle[i].availColor = [col for col in [[204,132,245], [153,247,213], [240,201,86]] if col != circle[i].color]
					circle[i].nextColor = choice(circle[i].availColor)

			if showResult:
				if showWarMes:
					self.showWarMes()
				self.showResult(result, name) 
			else:
				for i in range(3):
					buttons[i].draw(self.screen, 300, y[i])
			pygame.display.flip()
			self.clock.tick(60)