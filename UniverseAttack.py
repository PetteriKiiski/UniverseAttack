#[[3] * 200] * 200
#Initialize stuff
import pygame, sys, random, json
from pygame.locals import *
pygame.init()
canvas = pygame.display.set_mode((1360, 660))
pygame.display.set_caption("Universe Attack")
#Load images
Home = pygame.image.load("Home.png")
Continue = pygame.image.load("Continue.png")
Restart = pygame.image.load("Restart.png")
RestartGameDialog = pygame.image.load("RestartGameDialog.png")
NeverMind = pygame.image.load("NeverMind.png")
Sand = pygame.image.load("Sand.png")
#Make Home page
def HomePage():
	#MainLoop
	while True:
		#Set up screen for this loop
		canvas.fill((255, 255, 255))
		canvas.blit(Home, (0, 0))
		canvas.blit(Continue, (228, 560))
		canvas.blit(Restart, (681, 560))
		#Catch events
		for event in pygame.event.get():
			#Quit if needed
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			#Restart or play game if needed
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
		#Update display
		pygame.display.update()
#Create Game Page
def GamePage():
	#Read game file
	try:
		with open("game.json", "r") as fh:
			info = json.load(fh)
	except EnvironmentError:
		print ("Unable to load")
	except Exception as err:
		print (err)
#	print (info)
	#if there is no information in the json file, we need to write the information ourselves
	if info == None:
		info = {"board":[], "ids":[], "loc" : [0, 0], "HomeColor" : "", "EnemyColor" : ""} #200x200
		home = [random.randint(0, 198), random.randint(0, 198)]
		enemy = [random.randint(0, 198), random.randint(0, 198)]
		for x in range(0, 200):
			info["board"].append([])
			for y in range(0, 200):
				info["board"][-1].append(3)
		print (home)
		print (enemy)
		info["board"][home[0]][home[1]] = 0
		info["board"][home[0] + 1][home[1]] = 0
		info["board"][home[0] + 1][home[1] + 1] = 0
		info["board"][home[0]][home[1] + 1] = 0
		info["board"][enemy[0]][enemy[1]] = 1
		info["board"][enemy[0] + 1][enemy[1]] = 1
		info["board"][enemy[0] + 1][enemy[1] + 1] = 1
		info["board"][enemy[0]][enemy[1] + 1] = 1
		info["loc"] = [home[0] - 10, home[1] - 5]
		#-----------------------------------------------------------
		#1360, 660
		#68, 66
		for x in range(info["loc"][0], info["loc"][0] + 20):
			if x >= 30 or x < 0:
				continue
			for y in range(info["loc"][1], info["loc"][1] + 10):
				if y >= 30 or y < 0 or info["board"][y][x] in [0, 1]:
					continue
				info["board"][y][x] = 2
		print (info["board"])
#for x in range(scannable[0], scannable[0] + 20):
#	if x >= 30 or x < 0:
#		continue
#	for y in range(scannable[1], scannable[1] + 10):
#		if y >= 30 or y < 0 or l[y][x] == 1:
#			continue
#		l[y][x] = 2

#		for x in range(info["loc"][0], info["loc"][0] + 20):
#			for y in range(info["loc"][1], info["loc"][1] + 10):
#				if x >= 200 or y >= 200 or x < 0 or y < 0 or info["board"][y][x] != 3:
#					break
#				info["board"][y][x] = 2
		info["ids"] += [["Home", "Base"]]
		info["ids"] += [["Enemy", "HiddenBase"]]
		info["ids"] += [["Neutral", "Sand"]]
		info["ids"] += [["Neutral", None]]
		colors = ["Red", "Blue", "Green"]
		info["HomeColor"] = random.choice(colors)
		del colors[colors.index(info["HomeColor"])]
		info["EnemyColor"] = random.choice(colors)
		try:
			with open("game.json", "w") as fh:
				json.dump(info, fh)
		except EnvironmentError:
			print ("Unable to save scenario")
		except Exception as err:
			print (err)
	while True:
		canvas.fill((0, 0, 0))
		HomeCount = 0
		for x in range(info["loc"][0], info["loc"][0] + 20):
			for y in range(info["loc"][1], info["loc"][1] + 10):
#				print (y, x)
				if x >= 200 or y >= 200 or x < 0 or y < 0:
					break
				value = info["ids"][info["board"][y][x]]
				if value[1] == None:
					continue
				loc_x = ((x - info["loc"][0]) * 68)
				loc_y = ((y - info["loc"][1]) * 66)
				canvas.blit(Sand, (loc_x, loc_y))
				if value[1] == "Base":
					print ("Base")
					if value[0] == "Home":
						print (HomeCount + 1)
						HomeCount += 1
						img = pygame.image.load("{}Base.png".format(info["HomeColor"]))
						canvas.blit(img, (loc_x, loc_y))
					if value[0] == "Enemy":
#						print ("Enemy")
						img = pygame.image.load("{}Base.png".format(info["EnemyColor"]))
						canvas.blit(img, (loc_x, loc_y))
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
