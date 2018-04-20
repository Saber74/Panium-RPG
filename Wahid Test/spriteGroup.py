from pygame import * 	
from pytmx import *
from random import randint as r
import os
WIDTH, HEIGHT = 800, 600 
# WIDTH, HEIGHT = 1366, 768 
size=(WIDTH, HEIGHT)
os.environ['SDL_VIDEO_WINDOW_POS'] = 'FULLSCREEN'
screen = display.set_mode(size) 
myClock = time.Clock()
FPS = 60
x = y = n = 0
save = False
Player_HP = 100
battleAnimation = []
pressed = "NULL"
frame = 0
counter = 0
x_diff = y_diff = 0
speed = 0
pan = 5
mode = 0
# mode = 1
s = 5
lvl = 1
mixer.pre_init(44100, -16, 1, 512)# initializes the music mixer before it is actually initialized
mixer.init()# initializes the music mixer
mixer.music.load("Audio/BGM/aaronwalz_ylisfar.ama")
mixer.music.play()
def load_object(fname, chests, walls):
	for tile_object in fname.objects:
		if tile_object.name == 'wall':
			obs = Obstacle(tile_object.x, tile_object.y, tile_object.width, tile_object.height)
			walls.add(obs)
		if tile_object.name == 'chest':
			chest = Chest(tile_object.x, tile_object.y, tile_object.width, tile_object.height, tile_object.type,tile_object.ChestName)	
			chests.add(chest)
def levelSelect(lvl, chests, walls):
	if lvl == 1:
		fname = load_pygame("Maps/grasslands.tmx")
		tops = load_pygame("Maps/over0.tmx")
	if lvl == 2:
		fname = load_pygame("Maps/desert.tmx")
		tops = load_pygame("Maps/blank.tmx")
	for i in chests:
		i.kill()
	for i in walls:
		i.kill()		
	return fname, tops		
def MapLoad(Map_Name):
	for layer in Map_Name.visible_layers:
		if isinstance(layer, TiledTileLayer):
			for x, y, gid in layer:
				tile = Map_Name.get_tile_image_by_gid(gid)
				if tile:
					screen.blit(tile, ((x * Map_Name.tilewidth) + x_diff, (y * Map_Name.tileheight) + y_diff))
def Save():
	for i in inventory:
		inventorySave.write(i + '\n')
	for i in openedChests:
		openChests.write(i + '\n')	
	lvlSave.write(str(lvl))	
	CoordSave.write(str(x_diff) + ',' + str(y_diff))		
	lvlSave.close()
	inventorySave.close()
	openChests.close()
	CoordSave.close()
def InventoryDisplay():
	inv = ''
	for i in inventory:
		number = 0
		for n in inventory:
			if i == n:
				number += 1
		inv += i + ' ' + 'x' + str(number) + ', '
	split = inv.split(', ')
	del split[split.index('')]	
	s = set(split)
	if len(s) == 0:
		print("YOU HAVE NO ITEMS!!!!")
	else:	
		print(s,"\n", "and you have",len(inventory),"item(s)!")	
	return s
def FIGHTANIMATION(surf, enemy, battleBack):
	surf.blit(battleBack,(0,0))
	surf.blit(enemy,(187.5,0))	
############################################# LOADING CHEST STATES #############################################
openedChests = []
openChests = open("Chest.txt", "r").read().strip().split('\n')
for i in openChests:
	if i != '':
		openedChests.append(i)
openChests = open("Chest.txt", "w")
############################################# LOADING CHEST STATES #############################################

############################################### LOADING INVENTORY ###############################################
inventory = []
inventorySave = open("Inventory.txt", "r").read().strip().split('\n')
for i in inventorySave:
	if i != '':
		inventory.append(i)
inventorySave = open("Inventory.txt", "w")
############################################### LOADING INVENTORY ###############################################

################################################ CHARACTER STATS ################################################
crowStats = []
crowStatsSave = open("CrowStats.txt", 'r').read().strip().split('\n')
for i in crowStatsSave:
	if i != '':
		crowStats.append(i)
crowStatsSave = open("CrowStats.txt", 'w')
################################################ CHARACTER STATS ################################################

############################################ COORDINATES / PLAYER POSITION ############################################
CoordSave = open("Coordinates.txt", 'r').read().strip().split(',')
for i in CoordSave:
	if i != '':
		if CoordSave.index(i) == 0:
			x_diff = int(i)
		elif CoordSave.index(i) == 1:
			y_diff = int(i)
CoordSave = open("Coordinates.txt", 'w')
############################################ COORDINATES / PLAYER POSITION ############################################

################################################### LEVEL LOAD ###################################################
lvlSave = open("lvl.txt", "r").read().strip()
lvl = int(lvlSave)
lvlSave = open("lvl.txt", "w")
################################################### LEVEL LOAD ###################################################

crowWalkForward, crowWalkDown, crowWalkRight, crowWalkLeft = [], [], [], []
ravenWalkForward, ravenWalkDown, ravenWalkRight, ravenWalkLeft = [], [], [], []
cf, cd, cr, cl = crowWalkForward, crowWalkDown, crowWalkRight, crowWalkLeft
cm = image.load("SPRITES/Crow/Walk/Forward/Forward-0.png").convert_alpha()
chest_open = []

############################################### ATTACK ANIMATIONS ###############################################
Darkness1 = []
for i in range(22):
	Darkness1.append(image.load("SPRITES/Crow Attacks/%i.png" % i).convert_alpha())
############################################### ATTACK ANIMATIONS ###############################################

############################################# POSSIBLE CHEST ITEMS #############################################
tier1 = ["Potion", "Sword", "Shield", "Elixir", "Poison"]
tier2 = ['Lightening Essence']
tier3 = ['Sword of Water (II)', 'Sword of Lightening (V)']
tier4 = ['Wind Staff', 'Wind Staff']
############################################# POSSIBLE CHEST ITEMS #############################################

############################################ LOADING MAP AND SPRITES ############################################
for i in range(9):
	crowWalkForward.append(image.load("SPRITES/Crow/Walk/Forward/Forward-%i.png" % (i + 1)).convert_alpha())
	crowWalkRight.append(image.load("SPRITES/Crow/Walk/Right/Right-%i.png" % (i + 1)).convert_alpha())	
	crowWalkDown.append(image.load("SPRITES/Crow/Walk/Back/Back-%i.png" % (i + 1)).convert_alpha())	
	crowWalkLeft.append(image.load("SPRITES/Crow/Walk/Left/Left-%i.png" % (i + 1)).convert_alpha())	
	########
	ravenWalkForward.append(image.load("SPRITES/Raven/Walk/Up/%i.png" % i).convert_alpha())
	ravenWalkRight.append(image.load("SPRITES/Raven/Walk/Right/%i.png" % i).convert_alpha())
	ravenWalkDown.append(image.load("SPRITES/Raven/Walk/Down/%i.png" % i).convert_alpha())
	ravenWalkLeft.append(image.load("SPRITES/Raven/Walk/Left/%i.png" % i).convert_alpha())
for i in range(24):
	battleAnimation.append(transform.scale(image.load("gif/%i.png" % i),(800,600)).convert_alpha())
############################################ LOADING MAP AND SPRITES ############################################

class Player(sprite.Sprite):
	# sprite for the player
	def __init__(self, x, y, s):
		sprite.Sprite.__init__(self)
		self.image = cm
		self.x = x ; self.y = y
		self.rect = self.image.get_rect()
		self.rect.center = (self.x,self.y)
	def update(self):
		self.image = cm
		self.x = x ; self.y = y
		if pressed == "LEFT" or pressed == "RIGHT":
			self.rect.x += self.x
		elif pressed == "UP" or pressed == "DOWN":	
			self.rect.y += self.y
class Obstacle(sprite.Sprite):
	def __init__(self, x, y, w, h):
		sprite.Sprite.__init__(self)
		self.image = Surface((x, y), SRCALPHA) ; self.image.fill((0,0,0,0))
		self.rect = Rect(x, y, w, h)
		self.x = x ; self.y = y
	def update(self):
		self.rect.topleft = self.x + x_diff, self.y + y_diff
class Chest(sprite.Sprite):
	def __init__(self, x, y, w, h, tier, name):
		sprite.Sprite.__init__(self)
		self.tier = tier
		self.name = name
		self.opened = False
		self.images = [image.load("SPRITES/Chest/Tier" + str(self.tier) + "/0.png"),
					   image.load("SPRITES/Chest/Tier" + str(self.tier) + "/1.png")]
		self.prev_image = self.image = self.images[0] ; self.rect = Rect(x, y, w, h)
		if self.name in openedChests:
			self.image = self.images[1] 
		self.x, self.y = x, y
		self.c = tier1
	def update(self):
		global chest_open
		self.rect.topleft = self.x + x_diff, self.y + y_diff
		if self.image == self.prev_image and self.opened and kp[K_SPACE]:
			self.image = self.images[1]
			if self.tier == '1':
				self.c = tier1
			elif self.tier == '2':	
				self.c = tier2
			elif self.tier == '3':
				self.c = tier3
			elif self.tier == '4':
				self.c = tier4
			item = r(0, len(self.c) - 1)
			inventory.append(self.c[item])
			print(self.c[item], "has been obtained!!")
			del self.c[item]
			openedChests.append(self.name)
all_sprites = sprite.Group()                                 
walls = sprite.Group()
chests = sprite.Group()
player = Player(WIDTH / 2, HEIGHT / 2 + 50, speed)
all_sprites.add(player)
fname = levelSelect(lvl, chests, walls)[0]
tops = levelSelect(lvl, chests, walls)[1]
load_object(fname, chests, walls)
print("PRESS B TO INITIATE BATTLE ; Q TO RESET (PRESS Q THEN RERUN THE PROGRAM) ; PRESS I TO PRINT YOUR INVENTORY ; PRESS SPACE TO INTERACT WITH CHESTS ; M&N TO TOGGLE MAP ; O&P TOGGLE MUSIC")			
running = True
while running:
	for evt in event.get():  
		if evt.type == QUIT: 
			Save()
			running = False
		if evt.type == KEYDOWN:
			if evt.key == K_ESCAPE:
				Save()
				running = False    	
			if evt.key == K_1:
				cf, cd, cr, cl = crowWalkForward, crowWalkDown, crowWalkRight, crowWalkLeft
			if evt.key == K_2:
				cf, cd, cr, cl = ravenWalkForward, ravenWalkDown, ravenWalkRight, ravenWalkLeft
			if evt.key == K_i:
				InventoryDisplay()
			if evt.key == K_q:
				inventorySave = open("Inventory.txt", "w")
				inventory = []
				openChests = open("Inventory.txt", "w")
				openedChests = []
				CoordSave = open("Coordinates.txt", 'w')
			if evt.key == K_b:
				mode = 1 - mode	
			if evt.key == K_n:
				lvl = 2
				fname = levelSelect(lvl, chests, walls)[0]
				tops = levelSelect(lvl, chests, walls)[1]
				load_object(fname, chests, walls)		
				x_diff, y_diff = -1090, -420
			if evt.key == K_m:
				lvl = 1
				fname = levelSelect(lvl, chests, walls)[0]
				tops = levelSelect(lvl, chests, walls)[1]	
				load_object(fname, chests, walls)
				x_diff = y_diff = 0
			if evt.key == K_o:
				mixer.music.stop()
			if evt.key == K_p:
				mixer.music.play()		
	mx,my=mouse.get_pos()
	mb=mouse.get_pressed()
	kp = key.get_pressed()
	U = R = D = L = moving = False
	# KEYBOARD MOVEMENT
	if mode == 0:
		if kp[K_RIGHT]:
			x_diff -= pan
			x = speed
			R = True
			moving = True
			pressed = "RIGHT"
		elif kp[K_LEFT]:
			x_diff += pan
			x = -speed
			L = True
			moving = True
			pressed = "LEFT"
		elif kp[K_UP]:
			y_diff += pan
			y = -speed
			U = True
			moving = True
			pressed = "UP"
		elif kp[K_DOWN]:
			y_diff -= pan
			y = speed
			D = True
			moving = True
			pressed = "DOWN"
		else:
			x = y = 0	
		if kp[K_LSHIFT]:
			pan = 10
			s = 2
		else:
			pan = 5	
			s = 5
		# UPDATE
		all_sprites.update()
		walls.update()
		chests.update()
		# check to see if the mob hit the player
		hit = sprite.spritecollide(player, walls, False)
		if hit:
			pass

		chest_open = sprite.spritecollide(player, chests, False)	
		if chest_open and kp[K_SPACE]:
			chest_open[0].opened = True
		# ANIMATION CONTROL
		if moving:
			counter += 1
			if counter > s:
				counter = 0
				frame += 1
				if frame >= len(crowWalkDown):
					frame = 0

		############################################## Map Loading ##############################################
		screen.fill(0)
		MapLoad(fname)
		chests.draw(screen)
		all_sprites.draw(screen)
		MapLoad(tops)
		############################################## Map Loading ##############################################

		########################################### MOVEMENT ANIMATION ###########################################
		if U:
			cm = cf[frame]
		elif R:
			cm = cr[frame]
		elif D:
			cm = cd[frame]
		elif L:
			cm = cl[frame]
		else:
			if pressed == "UP" or pressed == "NULL":
				cm = cf[0]
			elif pressed == "DOWN":
				cm = cd[0]
			elif pressed == "LEFT":
				cm = cl[0]
			elif pressed == "RIGHT":
				cm = cr[0]
		########################################### MOVEMENT ANIMATION ###########################################
	else:
		if mode == 1:
			Attack_DMG = 20
			Selected_Attack = 'NONE'
			t = r(0,1)
			if t == 0:
				turn = "Player"	
			else:
				turn = "Enemy"	
			print(turn,"GOES FIRST!!!")	
			Enemy_HP = 100
			print("PRESS SPACE TO ATTACK")
			for i in battleAnimation:
				screen.blit(i,(0,0))
				time.wait(25)
				display.flip() 
			mode = 2	
		battleBack = transform.scale(image.load("img/battlebacks1/DarkSpace.png"), (WIDTH, HEIGHT))	
		enemy = image.load("img/enemies/Chimera.png")
		FIGHTANIMATION(screen, enemy, battleBack)	
		########################################## ATTACK SELECTION ##########################################
		if kp[K_z]:
			Attack_DMG = 20
			print("Your attack will do",Attack_DMG,"damage to the enemy!!")	
		elif kp[K_x]:
			Attack_DMG = 30
			print("Your attack will do",Attack_DMG,"damage to the enemy!!")	
		elif kp[K_c]:
			Attack_DMG = 40		
			print("Your attack will do",Attack_DMG,"damage to the enemy!!")	
		########################################## ATTACK SELECTION ##########################################

		############################################### BATTLE ###############################################
		if turn == "Player" and Player_HP > 0 and kp[K_SPACE]:
			print(turn + "'s turn to attack!!")
			for i in Darkness1:
				FIGHTANIMATION(screen, enemy, battleBack)	
				screen.blit(i,(300,100))
				time.wait(50)
				display.flip()
			Enemy_HP -= Attack_DMG
			print("Enemy HP:",Enemy_HP)
			turn = "Enemy"
		if turn == "Enemy" and Enemy_HP > 0:
			time.wait(100)
			print(turn + "'s turn to attack!!")
			Player_HP -= 10
			print("Player HP:",Player_HP)	
			turn = "Player"
		if Player_HP <= 0 or Enemy_HP <= 0:	
			if Player_HP <= 0:
				print("YOU LOST!!")		
			elif Enemy_HP <= 0:	
				print("YOU WON!!")		
			elif Player_HP <= 0 and Enemy_HP <= 0:
				print("YOU LOST!!")		
			mode = 0	
		############################################### BATTLE ###############################################
	# DRAW / RENDER         
	walls.draw(screen)
	display.flip() 
	myClock.tick(FPS)
quit()
