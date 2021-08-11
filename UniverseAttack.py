#[[3] * 200] * 200
#Initialize stuff
import pygame, sys, random, json, time
from pygame.locals import *
pygame.init()
canvas = pygame.display.set_mode((1360, 660))
pygame.display.set_caption("Universe Attack")
#Load images
Home = pygame.image.load("Images/Home.png")
Continue = pygame.image.load("Images/Continue.png")
Restart = pygame.image.load("Images/Restart.png")
RestartGameDialog = pygame.image.load("Images/RestartGameDialog.png")
NeverMind = pygame.image.load("Images/NeverMind.png")
Sand = pygame.image.load("Images/Sand.png")
Blank = pygame.image.load("Images/Blank.png")
HomeBase = pygame.image.load("Images/HomeBase.png")
Build = pygame.image.load("Images/Build.png")
BuildPageImg = pygame.image.load("Images/BuildPage.png")
BuildingSelection = pygame.image.load("Images/BuildingSelection.png")
class CoinManager:
	def __init__(self):
		self.num_coin_collectors = 0
		timer = time.time()
		commit_timer = None
	def get_no_coins(self):
		if time.time() - timer >= 5:
			timer = time.time()
			return self.num_coin_collectors * 10
		return 0
	def pause_mode(self):
		commit_timer = time.time() - timer
	def continue_mode(self):
		if commit_timer == None:
			return
		timer = time.time() - commit_timer
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
		info = {"board":[], "ids":[], "loc" : [0, 0], "HomeColor" : "", "EnemyColor" : "", "Sidebar" : None, "Coins" : 500, "Buildings_Queue":[]} #200x200
		home = [random.randint(0, 198), random.randint(0, 198)]
		#print (home)
		enemy = [random.randint(0, 198), random.randint(0, 198)]
		for x in range(0, 200):
			info["board"].append([])
			for y in range(0, 200):
				info["board"][-1].append(3)
#		print (home)
#		print (enemy)
		info["board"][home[0]][home[1]] = 0
		info["board"][home[0] + 1][home[1]] = 0
		info["board"][home[0] + 1][home[1] + 1] = 0
		info["board"][home[0]][home[1] + 1] = 0
		info["board"][enemy[0]][enemy[1]] = 1
		info["board"][enemy[0] + 1][enemy[1]] = 1
		info["board"][enemy[0] + 1][enemy[1] + 1] = 1
		info["board"][enemy[0]][enemy[1] + 1] = 1
		info["loc"] = [home[0] - 8, home[1] - 5]
		#-----------------------------------------------------------
		#1360, 660
		#68, 66
		displayed = False
		for x in range(info["loc"][0], info["loc"][0] + 16):
			if x >= 200 or x < 0:
				continue
			for y in range(info["loc"][1], info["loc"][1] + 10):
				if not displayed:
					print ("{0}, {1}".format(x, y))
				if y >= 200 or y < 0 or info["board"][x][y] in [0, 1]:
					continue
				info["board"][x][y] = 2
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
	timer = time.time()
	move_timer = time.time()
	while True:
		if time.time() - timer >= 5:
			timer = time.time()
			info["Coins"] += len([x for x in info["ids"] if x == ["Home", "Coin Collector"]]) * 10
		canvas.fill((0, 0, 0))
		HomeCount = 0
		for x in range(info["loc"][0], info["loc"][0] + 16):
			for y in range(info["loc"][1], info["loc"][1] + 10):
#				print (y, x)
				if x >= 200 or y >= 200 or x < 0 or y < 0:
					break
				value = info["ids"][info["board"][x][y]]
				if value[1] == None:
					continue
				loc_x = ((x - info["loc"][0]) * 68)
				loc_y = ((y - info["loc"][1]) * 66)
				canvas.blit(Sand, (loc_x, loc_y))
				if value[1] == "Base":
#					print ("Base")
					if value[0] == "Home":
#						print (HomeCount + 1)
						HomeCount += 1
						img = pygame.image.load("Images/{}Base.png".format(info["HomeColor"]))
						canvas.blit(img, (loc_x, loc_y))
					if value[0] == "Enemy":
#						print ("Enemy")
						img = pygame.image.load("Images/{}Base.png".format(info["EnemyColor"]))
						canvas.blit(img, (loc_x, loc_y))
				if value[1] == "Coin Collector":
					print ("CoinColector")
#					print ("Base")
					if value[0] == "Home":
#						print (HomeCount + 1)
						HomeCount += 1
						img = pygame.image.load("Images/{}CoinCollector.png".format(info["HomeColor"]))
						canvas.blit(img, (loc_x, loc_y))
					if value[0] == "Enemy":
#						print ("Enemy")
						img = pygame.image.load("Images/{}CoinCollector.png".format(info["EnemyColor"]))
						canvas.blit(img, (loc_x, loc_y))
				if value[1] == "Black Widow Factory":
#					print ("Base")
					if value[0] == "Home":
#						print (HomeCount + 1)
						HomeCount += 1
						img = pygame.image.load("Images/{}BlackWidowFactory.png".format(info["HomeColor"]))
						canvas.blit(img, (loc_x, loc_y))
					if value[0] == "Enemy":
#						print ("Enemy")
						img = pygame.image.load("Images/{}BlackWidowFactory.png".format(info["EnemyColor"]))
						canvas.blit(img, (loc_x, loc_y))
		for x in range(info["loc"][0] + 16, info["loc"][0] + 20):
			for y in range(info["loc"][1], info["loc"][1] + 10):
				loc_x = ((x - info["loc"][0]) * 68)
				loc_y = ((y - info["loc"][1]) * 66)
				canvas.blit(Blank, (loc_x, loc_y))
		if info["Sidebar"] == ["Home", "Base"]:
			img = pygame.image.load("Images/{}Base.png".format(info["HomeColor"]))
			canvas.blit(img, (1190, 132))
			canvas.blit(HomeBase, (1088, 0))
			canvas.blit(Build, (1088, 264))
		if info["Sidebar"] == ["Enemy", "Base"]:
			img = pygame.image.load("Images/{}Base.png".format(info["HomeColor"]))
			canvas.blit(img, (1190, 132))
			canvas.blit(HomeBase, (1088, 0))
		if len(info["Buildings_Queue"]) != 0 and pygame.mouse.get_pos()[0] < 1020:
#			print ("Executing")
			x = pygame.mouse.get_pos()[0]
			y = pygame.mouse.get_pos()[1]
			loc_x = x // 68
			loc_y = y // 66
			#print (loc_x, loc_y)
			canvas.blit(BuildingSelection, (loc_x, loc_y))
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			if event.type == MOUSEBUTTONDOWN:
				pos = pygame.mouse.get_pos()
				x = abs((pos[0] // 68 + 1) - info["loc"][0]) + 1 # * 68
				y = abs((pos[1] // 66 + 1) - info["loc"][1]) + 1 # * 66
				print (x, y)
				info["Sidebar"] = info["ids"][info["board"][x][y]]
				if info["Sidebar"] == ["Home", "Base"]:
					if pygame.Rect(1088, 264, 272, 68).collidepoint(pos):
						save_time = time.time() - timer
						build_dict = {"Images/{}BlackWidowFactory.png".format(info["HomeColor"]): 500, "Images/{}CoinCollector.png".format(info["HomeColor"]) : 100, "Images/{}Base.png".format(info["HomeColor"]):2000}
						obj = BuildPage(build_dict, info["Coins"])
						if obj == "Images/{}BlackWidowFactory.png".format(info["HomeColor"]):
							info["Coins"] -= 500
							info["Buildings_Queue"] += [len(info["ids"])]
							info["ids"] += ["Home", "Black Widow Factory"]
						if obj == "Images/{}CoinCollector.png".format(info["HomeColor"]):
							#print ("Collector")
							info["Coins"] -= 100
							#print (info["Coins"])
							info["Buildings_Queue"] += [len(info["ids"])]
							#print (info["Buildings_Queue"])
							info["ids"] += ["Home", "Coin Collector"]
						if obj == "Images/{}Base.png".format(info["HomeColor"]):
							info["Coins"] -= 2000
							info["Buildings_Queue"] += [len(info["ids"])]
							info["ids"] += ["Home", "Base"]
						timer = time.time() - save_time
				elif len(info["Buildings_Queue"]) > 0:
					#print ("Doing")
					loc_x = ((x - info["loc"][0]) * 68)
					loc_y = ((y - info["loc"][1]) * 66)
					info["board"][x][y] = info["Buildings_Queue"][0]
					info["board"][x + 1][y] = info["Buildings_Queue"][0]
					info["board"][x][y + 1] = info["Buildings_Queue"][0]
					info["board"][x + 1][y + 1] = info["Buildings_Queue"][0]
		pygame.display.update()
def BuildPage(Options, coins):
	id = 0
	leavepage = False
	while not leavepage:
		canvas.fill((255, 255, 255))
		canvas.blit(BuildPageImg, (0, 0))
		img = pygame.image.load(list(Options.keys())[id])
		tr_img = pygame.transform.scale(img, (500, 500))
		canvas.blit(tr_img, (580, 80))
		font = pygame.font.SysFont(None, 48)
		txt = font.render(str(list(Options.values())[id]), True, ((0, 0, 255) if coins >= list(Options.values())[id] else (255, 0, 0)))
		canvas.blit(txt, (0, 0))
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			if event.type == KEYDOWN:
				if event.key == K_DOWN and id + 1 != len(list(Options.keys())):
					id += 1
				if event.key == K_UP and id - 1 >= 0:
					id -= 1
				if event.key == K_LEFT:
					leavepage = True
				if event.key == K_SPACE:
					return None
				if event.key == K_RETURN:
					if coins >= list(Options.values())[id]:
						return list(Options.keys())[id]
					else:
						return None
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
