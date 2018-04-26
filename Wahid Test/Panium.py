from pygame import * 	
from pytmx import *
from random import randint as r
import os
import pickle as p
WIDTH, HEIGHT = 800, 600 
# WIDTH, HEIGHT = 1366, 768 
size=(WIDTH, HEIGHT)
os.environ['SDL_VIDEO_WINDOW_POS'] = '0,10'
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
pan = 1
mode = 0
speed = 0
gold = 100
# mode = 1
s = 5
# lvl = '1'
currChar = "Crow"
HP_items = ["Potion 50", "Meat 100", "Poison -50"]
mixer.pre_init(44100, -16, 1, 512)# initializes the music mixer before it is actually initialized
mixer.init()# initializes the music mixer
mixer.music.load("Audio/BGM/aaronwalz_veldarah.ama")
mixer.music.stop()
font.init()
timesNewRomanFont = font.SysFont("Times New Roman", 24)
medievalFont=font.Font("FONTS/DUKEPLUS.TTF", 24)
def load_object(fname, chests, walls, portals):
	for tile_object in fname.objects:
		if tile_object.name == 'wall':
			obs = Obstacle(tile_object.x, tile_object.y, tile_object.width, tile_object.height)
			walls.add(obs)
		if tile_object.name == 'chest':
			chest = Chest(tile_object.x, tile_object.y, tile_object.width, tile_object.height, tile_object.type,tile_object.ChestName)	
			chests.add(chest)
		if tile_object.name == "Portal":
			port = Portal(tile_object.x, tile_object.y, tile_object.width, tile_object.height, tile_object.type)	
			portals.add(port)
		if tile_object.name == "Clerk":
			clerk = Store_Clerk(tile_object.x, tile_object.y, tile_object.type)	
			clerks.add(clerk)
def levelSelect(lvl, chests, walls, portals):
	if lvl == '0':
		fname = load_pygame("Maps/STORE.tmx")
		tops = load_pygame("Maps/blank.tmx")
	if lvl == '1':
		fname = load_pygame("Maps/grasslands.tmx")
		tops = load_pygame("Maps/over0.tmx")
	if lvl == '2':
		fname = load_pygame("Maps/desert.tmx")
		tops = load_pygame("Maps/blank.tmx")
	kill = [chests, walls, portals, clerks]
	for i in kill:
		for n in i:
			n.kill()	
	return fname, tops		
def MapLoad(Map_Name):
	for layer in Map_Name.visible_layers:
		if isinstance(layer, TiledTileLayer):
			for x, y, gid in layer:
				tile = Map_Name.get_tile_image_by_gid(gid)
				if tile:
					screen.blit(tile, ((x * Map_Name.tilewidth) + x_diff, (y * Map_Name.tileheight) + y_diff))
def InventoryDisplay(current_Character, num):
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
	if num == 0:
		display_inventory(s, current_Character)	
	elif num == 1:
		return s	
def display_inventory(Inventory, current_Character):
	menu_base = transform.scale(image.load("img/menu/selction.png").convert_alpha(),(WIDTH, HEIGHT))
	screen.blit(menu_base, (0,0))
	arrow_pos = 0
	inventory_open = True
	inv = list(Inventory)
	while inventory_open:
		for evt in event.get():  
			if evt.type == KEYDOWN:
				if evt.key == K_i:
					inventory_open = False
				if evt.key == K_DOWN:
					arrow_pos += 1
				if evt.key == K_UP:
					arrow_pos -= 1
				if evt.key == K_SPACE and len(inv) > 0:
					x = inv[arrow_pos]
					y = x.split(" x")
					for i in HP_items:
						i = i.split(' ')
						if y[0] in i:
							print("HP +", i[1])
							HP_Change(i[1])
					del inv[arrow_pos]	
					del inventory[inventory.index(y[0])]
					inv = list(InventoryDisplay(current_Character, 1))
		count = 0			
		screen.blit(menu_base, (0,0))
		for i in range(len(inv)):
			count += 1
			ItemName = medievalFont.render(inv[i], True, (0,0,0))
			if arrow_pos == len(inv):
				arrow_pos -= 1
			if arrow_pos < 0:
				arrow_pos += 1	
			draw.circle(screen, (0,0,0), (455,65 + 30 * arrow_pos), 6)
			screen.blit(ItemName, (470, 20 + 30 * count))
		if current_Character == "Crow":
			screen.blit(transform.scale(image.load("img/faces/crow.png").convert_alpha(), (130,185)),(30,35))			
		elif current_Character == "Raven":
			screen.blit(transform.scale(image.load("img/faces/raven.png").convert_alpha(), (130,185)),(30,35))			
		mx, my = mouse.get_pos()
		# print(str(mx) + ', ' + str(my))
		display.flip()
def HP_Change(Add):
	global Crow_HP
	hp_change = int(Add)
	Crow_HP += hp_change
def FIGHTANIMATION(surf, enemy, battleBack):
	surf.blit(battleBack,(0,0))
	surf.blit(enemy,(187.5,0))	
def load_dict():
	prog_data = p.load(open("prog.dat", 'rb'))
	crow_data = p.load(open("crow_stats.dat", 'rb'))
	return prog_data, crow_data
def save_dict(lvl, x, y, Chests, inv, Gold, Crow_HP):
	prog_data = {"lvl": lvl,
			  	 "Coords": [x, y],
			  	 "Chests": Chests,
			  	 "inv": inv,
			  	 "Gold": Gold}
	crow_data = {"HP": Crow_HP}		  	 
	p.dump(prog_data, open("prog.dat", "wb"))	
	p.dump(crow_data, open("crow_stats.dat", "wb"))	
lvl = str(load_dict()[0]["lvl"])	
x_diff, y_diff = load_dict()[0]['Coords'][0], load_dict()[0]['Coords'][1]
openedChests = load_dict()[0]["Chests"]
inventory = load_dict()[0]["inv"]
gold = load_dict()

Crow_HP = load_dict()[1]["HP"]

################################################ CHARACTER STATS ################################################
# crowStats = []
# crowStatsSave = open("CrowStats.txt", 'r').read().strip().split('\n')
# for i in crowStatsSave:
# 	if i != '':
# 		crowStats.append(i)
# crowStatsSave = open("CrowStats.txt", 'w')
################################################ CHARACTER STATS ################################################

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
tier2 = ['Lightening Essence','Lightening Essence']
tier3 = ['Sword of Water', 'Sword of Lightening', "Sword of Fire"]
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
		self.x, self.y = x, y
		self.rect = self.image.get_rect()
		self.rect.midbottom = (self.x,self.y)
	def update(self):
		self.image = cm
		self.x, self.y = x, y
class Obstacle(sprite.Sprite):
	def __init__(self, x, y, w, h):
		sprite.Sprite.__init__(self)
		self.rect = Rect(x, y, w, h)
		self.x, self.y = x, y
	def update(self):
		self.rect.topleft = self.x + x_diff, self.y + y_diff

class Portal(sprite.Sprite):
	def __init__(self, x, y, w, h, location):
		sprite.Sprite.__init__(self)
		self.rect = Rect(x, y, w, h)
		self.x, self.y = x, y
		self.type = location
	def update(self):
		self.rect.topleft = self.x + x_diff, self.y + y_diff		

class Store_Clerk(sprite.Sprite):
	def __init__(self, x, y, tier):
		sprite.Sprite.__init__(self)
		self.tier = tier
		self.image = image.load("img/Store Clerks/Clerk" + self.tier + ".png")
		self.rect = self.image.get_rect()
		self.x, self.y = x, y
		self.interact = False
		self.back = transform.scale(image.load("img/menu/parchment.png").convert_alpha(), (WIDTH, HEIGHT))
	def update(self):
		self.rect.topleft = self.x + x_diff, self.y + y_diff	
	def open_store(self):
		while self.interact:
			for evt in event.get():  
				if evt.type == KEYDOWN:
					if evt.key == K_ESCAPE:
						self.interact = False
						return
			screen.blit(self.back, (0,0))			
			display.flip()	

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
portals = sprite.Group()
clerks = sprite.Group()
player = Player(WIDTH / 2, HEIGHT / 2 + 50, speed)
all_sprites.add(player)
fname = levelSelect(lvl, chests, walls, portals)[0]
tops = levelSelect(lvl, chests, walls, portals)[1]
load_object(fname, chests, walls, portals)
print("PRESS B TO INITIATE BATTLE ; Q TO RESET (PRESS Q THEN RERUN THE PROGRAM) ; PRESS I TO PRINT YOUR INVENTORY ; PRESS SPACE TO INTERACT WITH CHESTS ; M&N TO TOGGLE MAP ; O&P TOGGLE MUSIC")			
running = True
while running:
	for evt in event.get():  
		if evt.type == QUIT: 
			save_dict(lvl, x_diff, y_diff, openedChests, inventory, gold,Crow_HP)
			running = False
		if evt.type == KEYDOWN:
			if evt.key == K_ESCAPE:
				save_dict(lvl, x_diff, y_diff, openedChests, inventory, gold,Crow_HP)
				running = False    	
			if evt.key == K_1:
				cf, cd, cr, cl = crowWalkForward, crowWalkDown, crowWalkRight, crowWalkLeft
				currChar = "Crow"
			if evt.key == K_2:
				cf, cd, cr, cl = ravenWalkForward, ravenWalkDown, ravenWalkRight, ravenWalkLeft
				currChar = "Raven"
			if evt.key == K_i:
				InventoryDisplay(currChar, 0)
			if evt.key == K_q:
				inventory = []
				openedChests = []
			if evt.key == K_b:
				mode = 1 - mode	
			if evt.key == K_o:
				mixer.music.stop()
			if evt.key == K_p:
				mixer.music.play()		
			if evt.key == K_j:
				print(gold)	
			if evt.key == K_k:
				gold += 100	
	mx,my=mouse.get_pos()
	mb=mouse.get_pressed()
	kp = key.get_pressed()
	U = R = D = L = moving = False
	# KEYBOARD MOVEMENT
	if mode == 0:
		if kp[K_RIGHT]:
			x_diff -= pan
			R = True
			moving = True
			pressed = "RIGHT"
		elif kp[K_LEFT]:
			x_diff += pan
			L = True
			moving = True
			pressed = "LEFT"
		elif kp[K_UP]:
			y_diff += pan
			U = True
			moving = True
			pressed = "UP"
		elif kp[K_DOWN]:
			y_diff -= pan
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
		clerks.update()
		walls.update()
		chests.update()
		portals.update()
		# check to see if the mob hit the player
		clerk_Interact = sprite.spritecollide(player, clerks, False)
		if clerk_Interact and kp[K_SPACE]:
			clerk_Interact[0].interact = True
			clerk_Interact[0].open_store()
		hit = sprite.spritecollide(player, walls, False)
		if hit:
			# print('s')
			# h = hit[0]
			# if h.rect.collidepoint((player.rect.centerx, player.rect.bottom -20)):
				# if player.rect.x > h.rect.x and L and not U and not D and not R:
					# pan = 0
				# elif player.rect.x < h.rect.x and R and not L and not U and not D:
					# pan = 0

				# if player.rect.y > h.rect.y and U and not D and not R and not L:
					# pan = 0
				# elif player.rect.y < h.rect.y and D and not U and not R and not L:
					# pan = 0	
			pass		
		tel = sprite.spritecollide(player, portals, False)
		if tel:
			# t = tel[0]
			# if t.rect.collidepoint((player.rect.centerx, player.rect.bottom -20)):
			# 	if player.rect.x > h.rect.x and L:
			# 		pan = 0
			# 	else:
			# 		pan = 5
				lvl = tel[-1].type
				if lvl == '0':
					x_diff, y_diff = 240, 100	
				elif lvl == '1':
					x_diff, y_diff = -545, -580
				elif lvl == '2':
					x_diff, y_diff = -1285, -495	
						
				fname, tops = levelSelect(lvl, chests, walls, portals)
				load_object(fname, chests, walls, portals)
				
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
		# print(x_diff,y_diff)			
		############################################## Map Loading ##############################################
		screen.fill(0)
		MapLoad(fname)
		chests.draw(screen)
		clerks.draw(screen)
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
		if turn == "Player" and Crow_HP > 0 and kp[K_SPACE]:
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
			Crow_HP -= 10
			print("Player HP:",Crow_HP)	
			turn = "Player"
		if Crow_HP <= 0 or Enemy_HP <= 0:	
			if Crow_HP <= 0:
				print("YOU LOST!!")		
			elif Enemy_HP <= 0:	
				print("YOU WON!!")		
			elif Crow_HP <= 0 and Enemy_HP <= 0:
				print("YOU LOST!!")		
			mode = 0	
		############################################### BATTLE ###############################################
	# DRAW / RENDER         
	display.flip()
	myClock.tick(FPS)
quit()