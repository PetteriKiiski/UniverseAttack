import pygame, sys, random, json
from pygame.locals import *
pygame.init()
canvas = pygame.display.set_mode((1360, 660))
pygame.display.set_caption("Universe Attack")
Home = pygame.image.load("Home.png")
Continue = pygame.image.load("Continue.png")
Restart = pygame.image.load("Restart.png")
RestartGameDialog = pygame.image.load("RestartGameDialog.png")
NeverMind = pygame.image.load("NeverMind.png")
def HomePage():
	while True:
		canvas.fill((255, 255, 255))
		canvas.blit(Home, (0, 0))
		canvas.blit(Continue, (228, 560))
		canvas.blit(Restart, (681, 560))
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			if event.type == MOUSEBUTTONDOWN:
				m_pos = pygame.mouse.get_pos()
				if pygame.Rect(681, 560, 250, 64).collidepoint(m_pos):
					if RestartGamePage() == True:
						try:
							with open("game.json", "w") as fh:
								json.dump(None, fh)
						except EnvironmentError:
							print ("Unable to Restart Game")
						except Exception as err:
							print (err)
				if pygame.Rect(228, 560, 250, 64).collidepoint(m_pos):
					GamePage()
		pygame.display.update()
def GamePage():
	try:
		with open("game.json", "r") as fh:
			info = json.load(fh)
	except EnvironmentError:
		print ("Unable to load")
	except Exception as err:
		print (err)
	if info == None:
		info = {"board":[[[None] * 500]] * 500}
	home = [random.randint(0, 500), random.randint(0, 500)]
	enemy = [random.randint(0, 500), random.randint(0, 500)]
	info[home[1]][home[0]] = "Home"
	info[home[1] + 1][home[0]] = "Home"
	info[home[1] + 1][home[0] + 1] = "Home"
	info[home[1]][home[0] + 1] = "Home"
	info[enemy[1]][enemy[0]] = "Enemy"
	info[enemy[1] + 1][enemy[0]] = "Enemy"
	info[enemy[1] + 1][enemy[0] + 1] = "Enemy"
	info[enemy[1]][enemy[0] + 1] = "Enemy"
	while True:
		canvas.fill((255, 255, 255))
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
		pygame.display.update()
def MenuPage():
	while True:
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
def RestartLevelPage():
	while True:
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
def RestartGamePage():
	while True:
		canvas.fill((255, 255, 255))
		canvas.blit(Home, (0, 0))
		canvas.blit(Continue, (228, 560))
		canvas.blit(Restart, (681, 560))
		canvas.blit(RestartGameDialog, (485, 220))
		canvas.blit(Restart, (485, 280))
		canvas.blit(NeverMind, (485, 350))
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			if event.type == MOUSEBUTTONDOWN:
				m_pos = pygame.mouse.get_pos()
				if pygame.Rect(485, 280, 350, 64).collidepoint(m_pos):
					return True
				if pygame.Rect(485, 350, 500, 64).collidepoint(m_pos):
					return False
		pygame.display.update()
def SaveGamePage():
	while True:
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
def ExitPage():
	while True:
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
HomePage()
