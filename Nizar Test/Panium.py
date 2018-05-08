from pygame import * 	
from pytmx import *
from random import randint as r
import os
import pickle as p
WIDTH, HEIGHT = 800, 600 
font.init()
# WIDTH, HEIGHT = 1366, 768 
size=(WIDTH, HEIGHT)
os.environ['SDL_VIDEO_WINDOW_POS'] = '0,10'
########entrance screen stuff
screen = display.set_mode(size)
#####################################fonts##################################
fireFont=font.Font("Breathe Fire.otf",30)
#######################################fonts##############################
#############battle variables
dmg=0
Enemy_HP=100
hp=0
defense=0
magicdmg=0
magicdefense=0
luck=0
mana=0
charNum=0
stage=0
################# entry and openning pic and gif"""""""""""""""""""""''
# for i in range(0,71):
# 	screen.fill((37,34,39))
# 	screen.blit(image.load("Entry\output-%i.png"%i),(100,75))
# 	display.update()
# 	time.wait(100)
#####rects
# newGamerect=Rect(WIDTH//2-120,HEIGHT//2-30,200,75)
# screen.blit(transform.scale(image.load("option2.jpg"),(WIDTH,HEIGHT)),(0,0))
# draw.rect(screen,(0,0,0),newGamerect,0)
# display.update()
# time.wait(5000)
###################################entry and oppening pic and gif"
########################################## USE IN FINAL PRODUCT ##########################################
# screen = display.set_mode(size, FULLSCREEN)
# width, height = size = (min(1920,display.Info().current_w), min(1080,display.Info().current_h))
########################################## USE IN FINAL PRODUCT ##########################################
######################################### Fighting Screen ################################################
attackRect=Rect(0,round(HEIGHT*7/8,0),round(WIDTH*1/3,0),HEIGHT-round(HEIGHT*7/8,0))
defenseRect=Rect(round(WIDTH*1/3,0),round(HEIGHT*7/8,0),round(WIDTH*1/3),HEIGHT-round(HEIGHT*7/8,0))
itemRect=Rect(round(WIDTH*2/3,0),round(HEIGHT*7/8,0),round(WIDTH*1/3),HEIGHT-round(HEIGHT*7/8,0))
###########################################################################################
myClock = time.Clock()
FPS = 60
x = y = n = 0
save = False
Player_HP = 40
battleAnimation=[]
pressed = "NULL"
frame = 0
counter = 0
x_diff = y_diff = 0
pan = 1
mode = 0
speed = 0
gold = 100
s = 5
c = 'NULL'

menu_base = transform.scale(image.load("img/menu/selction.png").convert_alpha(),(WIDTH, HEIGHT))

currChar = "Crow"
HP_items = ["Potion 50", "Meat 100", "Poison -50"]
mixer.pre_init(44100, -16, 1, 512)# initializes the music mixer before it is actually initialized
mixer.init()# initializes the music mixer
mixer.music.load("Audio/BGM/aaronwalz_veldarah.ama")
mixer.music.stop()
font.init()
timesNewRomanFont = font.SysFont("Times New Roman", 24)
medievalFont=font.Font("FONTS/DUKEPLUS.TTF", 24)
fancyFont=font.Font("FONTS/Friedolin.ttf", 95)
def start_Screen():
	running = True
	while running:

		for evt in event.get():  
			if evt.type == QUIT: 
				running = False

		mx,my=mouse.get_pos()
		mb=mouse.get_pressed()
							  
		
		display.flip() 
	quit()
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
		if tile_object.name == 'NPC':
			npc = NPC(tile_object.x, tile_object.y, tile_object.type)	
			npcs.add(npc)
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
	kill = [chests, walls, portals, clerks, npcs]
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
		display_inventory(s, current_Character, 'inventory')	
	elif num == 1:
		return s
	elif num == 2:
		display_inventory(s, current_Character, 'sell')	

def display_inventory(Inventory, current_Character, mode):
	screen.blit(menu_base, (0,0))
	arrow_pos = 0
	inventory_open = True
	inv = list(Inventory)
	while inventory_open:
		for evt in event.get():  
			if evt.type == KEYDOWN:
				if evt.key == K_ESCAPE or evt.key == K_i:
					if mode == "sell":
						global c
						c = 'NULL'
						return c
					inventory_open = False
				if evt.key == K_DOWN:
					arrow_pos += 1
				if evt.key == K_UP:
					arrow_pos -= 1
				if evt.key == K_SPACE and len(inv) > 0:
					if mode == 'inventory':
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
					if mode == 'sell':
						global gold
						x = inv[arrow_pos]
						y = x.split(" x")
						try:
							gold += load_dict()[3][y[0]]
							print("You have gained", str(load_dict()[3][y[0]]), "gold!! Now you have", str(gold), "gold in total!!")
						except:
							gold += 100
							print("You have gained", str(100), "gold!! Now you have", str(gold), "gold in total!!")
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

	arrow_pos = 0
def HP_Change(HP):
	global Crow_HP
	Crow_HP += int(HP)
# def Gold_Change(Gold):
# 	global gold
# 	gold += Gold	
def FIGHTANIMATION(surf, enemy, battleBack):
	surf.blit(battleBack,(0,0))
	surf.blit(enemy,(187.5,0))	
def load_dict():
	prog_data = p.load(open("prog.dat", 'rb'))
	crow_data = p.load(open("crow_stats.dat", 'rb'))
	raven_data = p.load(open("raven_stats.dat", 'rb'))
	item_value = p.load(open("item_value.dat", 'rb'))
	return prog_data, crow_data, raven_data, item_value
def save_dict():
	prog_data = {"lvl": lvl,
				 "Coords": [x_diff, y_diff],
				 "Chests": openedChests,
				 "inv": inventory,
				 "Gold": gold,
				 "Current Charachter": currChar}

	crow_data = {"HP": Crow_HP,
				 "Attack": 7,
				 "Defense": 5,
				 "Magic Attack": 5,
				 "Magic Defense": 5,
				 "Dexterity": 1,
				 "Mana": 100}	  	 
	raven_data = {"HP": Raven_HP,
				 "Attack": 0,
				 "Defense": 0,
				 "Magic Attack": 0,
				 "Magic Defense": 0,
				 "Dexterity":0,
				 "Mana": 0}
	item_value = {'Potion': 75,
				  'Elixer': 50,
				  'Sword': 25,
				  'Shield': 25}		  	 
	p.dump(prog_data, open("prog.dat", "wb"))
	p.dump(crow_data, open("crow_stats.dat", "wb"))	
	p.dump(raven_data, open("raven_stats.dat", 'wb'))
	p.dump(item_value, open("item_value.dat", 'wb'))

lvl = str(load_dict()[0]["lvl"])
x_diff, y_diff = load_dict()[0]['Coords'][0], load_dict()[0]['Coords'][1]
openedChests = load_dict()[0]["Chests"]
inventory = load_dict()[0]["inv"]
gold = load_dict()[0]["Gold"]
currChar = load_dict()[0]["Current Charachter"]

Crow_HP = load_dict()[1]["HP"]

Raven_HP = load_dict()[2]["HP"]

crowWalkForward, crowWalkDown, crowWalkRight, crowWalkLeft = [], [], [], []
ravenWalkForward, ravenWalkDown, ravenWalkRight, ravenWalkLeft = [], [], [], []
cf, cd, cr, cl = crowWalkForward, crowWalkDown, crowWalkRight, crowWalkLeft
cm = image.load("SPRITES/Crow/Walk/Forward/Forward-0.png").convert_alpha()
chest_open = []

############################################### ATTACK ANIMATIONS ###############################################
CrowZ = []
CrowX=[]
CrowC=[]
RavenZ=[]
RavenX=[]
RavenC=[]
for i in range(17):
	CrowC.append(image.load("SPRITES/Crow Attacks/CrowC/%i.png" % i).convert_alpha())
for i in range(19):
	CrowX.append(image.load("SPRITES/Crow Attacks/CrowX/%i.png" % i).convert_alpha())
for i in range(22):
	CrowZ.append(image.load("SPRITES/Crow Attacks/CrowZ/%i.png" % i).convert_alpha())
# for i in range():
# 	RavenC.append(image.load("SPRITES/Raven Attacks/RavenC/%i.png" % i).convert_alpha())
# for i in range():
# 	RavenX.append(image.load("SPRITES/Raven Attacks/RavenX/%i.png" % i).convert_alpha())
# for i in range():
# 	RavenZ.append(image.load("SPRITES/Raven Attacks/RavenZ/%i.png" % i).convert_alpha())
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

class NPC(sprite.Sprite):
	def __init__(self, x, y, importance):
		sprite.Sprite.__init__(self)
		self.type = importance
		self.image = image.load("img/NPCs/" + self.type + ".png")#.convert_alpha()
		self.rect = self.image.get_rect()
		self.x, self.y = x, y
	def update(self):
		self.rect.topleft = self.x + x_diff, self.y + y_diff

class Store_Clerk(sprite.Sprite):
	def __init__(self, x, y, tier):
		sprite.Sprite.__init__(self)
		self.tier = tier
		self.s1 = ['Potion' + " " * 88 + '100', 'Elixer' + " " * 88 + '75', 'Sword' + " " * 88 + '50', 'Shield' + " " * 88 + '50']
		self.s2 = ['Potion' + " " * 88 + '100', 'Elixer' + " " * 88 + '75', 'Sword' + " " * 88 + '50', 'Shield' + " " * 88 + '50']
		self.s3 = ['Potion' + " " * 88 + '100', 'Elixer' + " " * 88 + '75', 'Sword' + " " * 88 + '50', 'Shield' + " " * 88 + '50']
		self.s4 = ['Potion' + " " * 88 + '100', 'Elixer' + " " * 88 + '75', 'Sword' + " " * 88 + '50', 'Shield' + " " * 88 + '50']
		self.image = image.load("img/Store Clerks/Clerk" + self.tier + ".png").convert_alpha()
		self.rect = self.image.get_rect()
		self.x, self.y = x, y
		self.interact = False
		self.back = transform.scale(image.load("img/menu/parchment.png").convert_alpha(), (WIDTH, HEIGHT))
		self.event = "NULL"
	def update(self):
		self.rect.topleft = self.x + x_diff, self.y + y_diff	
	def open_store(self):
		self.selection = self.s1
		if self.tier == '1':
			self.selection = self.s1
		elif self.tier == '2':
			self.selection = self.s2
		elif self.tier == '3':
			self.selection = self.s3
		elif self.tier == '4':
			self.selection = self.s4		
		arrow_pos = 0	
		global gold
		while self.interact:
			for evt in event.get():  
				if evt.type == KEYDOWN:
					if evt.key == K_ESCAPE:
						self.interact = False
						return
					if evt.key == K_UP:
						arrow_pos -= 1
					if evt.key == K_DOWN:
						arrow_pos += 1		
					if evt.key == K_SPACE:
						if self.event == 'buy' or self.event == 'NULL':
							x = self.selection[arrow_pos]
							y = x.split(" " * 88)
							if int(y[1]) <= gold:
								print("You have bought a " + y[0] + '!!')
								inventory.append(y[0])
								gold -= int(y[1])
							if int(y[1]) > gold:
								print("You don't have enough money!!")
					if evt.key == K_b:
						self.event = 'buy'		
					if evt.key == K_s:
						self.event = 'sell'	
			if self.event == 'buy' or self.event == 'NULL':			
				screen.blit(self.back, (0,0))
				ShopName = fancyFont.render("Shop Number 1", True, (0,0,0))
				screen.blit(ShopName, (185,0))
				for i in range(len(self.selection)):
					if arrow_pos == len(self.selection):
						arrow_pos -= 1
					if arrow_pos < 0:
						arrow_pos += 1	
					draw.circle(screen, (0,0,0), (100, 105 + 30 * arrow_pos), 3)
					ItemName = medievalFont.render(self.selection[i], True, (0,0,0))			
					screen.blit(ItemName, (105, 90 + 30 * i))
			if self.event == 'sell': 
				InventoryDisplay(currChar, 2)
				self.event = c
			mx, my = mouse.get_pos()
			# print(str(mx) + ', ' + str(my))
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
npcs = sprite.Group()
player = Player(WIDTH / 2, HEIGHT / 2 + 50, speed)
all_sprites.add(player)
fname = levelSelect(lvl, chests, walls, portals)[0]
tops = levelSelect(lvl, chests, walls, portals)[1]
load_object(fname, chests, walls, portals)
print("PRESS B TO INITIATE BATTLE ; Q TO RESET (PRESS Q THEN RERUN THE PROGRAM) ; PRESS I TO PRINT YOUR INVENTORY ; PRESS SPACE TO INTERACT WITH CHESTS ; M&N TO TOGGLE MAP ; O&P TOGGLE MUSIC ; J TO PRINT GOLD")			
running = True
key.set_repeat(100,100)
while running:
	for evt in event.get():  
		if evt.type == QUIT: 
			save_dict()
			running = False
		if evt.type == KEYDOWN:
			if evt.key == K_ESCAPE:
				save_dict()
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
			if evt.key==K_a:
				if stage>0:
					stage-=1
	mx,my=mouse.get_pos()
	mb=mouse.get_pressed()
	kp = key.get_pressed()
	U = R = D = L = moving = False
	# KEYBOARD MOVEMENT	
	if mode == 0:
		if currChar == "Crow":
			cf, cd, cr, cl = crowWalkForward, crowWalkDown, crowWalkRight, crowWalkLeft
			currNum=1
		elif currChar == "Raven":
			cf, cd, cr, cl = ravenWalkForward, ravenWalkDown, ravenWalkRight, ravenWalkLeft
			currNum=2
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
		# print(myClock.get_fps())	
		# UPDATE
		all_sprites.update()
		npcs.update()
		clerks.update()
		walls.update()
		chests.update()
		portals.update()
		# check to see if the mob hit the player
		clerk_Interact = sprite.spritecollide(player, clerks, False)
		if clerk_Interact and kp[K_SPACE]:
			clerk_Interact[0].interact = True
			clerk_Interact[0].open_store()

		npc_interact = sprite.spritecollide(player, npcs, False)	
		if npc_interact:
			print('npc')

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
		npcs.draw(screen)
		all_sprites.draw(screen)
		MapLoad(tops)
		############################################## Map Loading ##############################################

		##############################################Player Stat applying

		dmg= load_dict()[currNum]["Attack"]
		defense=load_dict()[currNum]["Defense"]
		magicdmg=load_dict()[currNum]["Magic Attack"]
		magicdefense=load_dict()[currNum]["Magic Defense"]
		luck=load_dict()[currNum]["Dexterity"]
		mana=load_dict()[currNum]["Mana"]


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
		draw.rect(screen,(46,50,128),attackRect,0)
		draw.rect(screen,(255,255,255),defenseRect,0)
		draw.rect(screen,(210,75,146),itemRect,0)
		for i in range(Player_HP//2):
			draw.rect(screen,(255,0,0),Rect(x,round(HEIGHT*6/8),10,15))
			x+=13
		x=0
		hpText=str("Player HP:%i"%Player_HP)
		hpEdit=fireFont.render(hpText,True,(0,200,0))
		screen.blit(hpEdit,(0,round(HEIGHT*6/8-40,0)))
		for i in range(mana//2):
			draw.rect(screen,(0,0,255),Rect(x,round(HEIGHT*6/8+50),10,15))
			x+=13
		x=0
		manaText=str("Player Mana:%i"%mana)
		manaEdit=fireFont.render(manaText,True,(0,200,0))
		screen.blit(manaEdit,(0,round(HEIGHT*6/8+20)))
		enemyhp=str("name of enemy HP:%i"%Enemy_HP)
		enemyhpEdit=fireFont.render(enemyhp,True,(0,200,0))
		screen.blit(enemyhpEdit,(0,0))
		count=0
		y=round(HEIGHT*1/8)
		for i in range(Enemy_HP//2):
			draw.rect(screen,(255,0,0),Rect(x,y,10,15))
			x+=12
			count+=1
			if count%17==0:
				y+=18
				x=0
		x=0
		if stage==0:
			text=str("Attack Skills")
			text2=str("Defencive Skills")
			text3=str("Items")
			edit1=fireFont.render(text,True,(0,0,200))
			edit2=fireFont.render(text2,True,(0,0,200))
			edit3=fireFont.render(text3,True,(0,0,200))
			screen.blit(edit1,(50,round(HEIGHT*7/8+15,0)))
			screen.blit(edit2,(round(50+WIDTH*1/3,0),round(HEIGHT*7/8+15,0)))
			screen.blit(edit3,(round(50+WIDTH*2/3,0),round(HEIGHT*7/8+15,0)))

			if mb[0]:
				if attackRect.collidepoint(mx,my):
					stage=1
				elif defenseRect.collidepoint(mx,my):
					stage=2
				elif itemRect.collidepoint(mx,my):
					stage=3
		########################################## ATTACK SELECTION ##########################################
		if stage==1:

			text=str("Attack1")
			text2=str("Attack2")
			text3=str("Attack3")
			edit1=fireFont.render(text,True,(0,0,200))
			edit2=fireFont.render(text2,True,(0,0,200))
			edit3=fireFont.render(text3,True,(0,0,200))
			screen.blit(edit1,(50,round(HEIGHT*7/8+15,0)))
			screen.blit(edit2,(round(50+WIDTH*1/3,0),round(HEIGHT*7/8+15,0)))
			screen.blit(edit3,(round(WIDTH*2/3+50,0),round(HEIGHT*7/8+15,0)))
			if attackRect.collidepoint(mx,my):
				Attack_DMG = dmg*4
				print("Your attack will do",Attack_DMG,"damage to the enemy!!")	
			elif defenseRect.collidepoint(mx,my):
				Attack_DMG = magicdmg*5
				print("Your attack will do",Attack_DMG,"damage to the enemy!!")	
			elif itemRect.collidepoint(mx,my):
				Attack_DMG = dmg*2+ magicdmg*2		
				print("Your attack will do",Attack_DMG,"damage to the enemy!!")	
		########################################## ATTACK SELECTION ##########################################

		############################################### BATTLE ###############################################
		if turn == "Player" and Player_HP > 0 :
			if stage==1:
				if mb[0] and attackRect.collidepoint(mx,my) or kp[K_z]:
					print(turn + "'s turn to attack!!")
					for i in CrowZ:
						FIGHTANIMATION(screen, enemy, battleBack)	
						screen.blit(i,(300,100))
						time.wait(50)
						display.flip()
					Enemy_HP -= Attack_DMG
					turn = "Enemy"
					stage=0
				elif mb[0] and defenseRect.collidepoint(mx,my) or kp[K_x] and mana>=10:
					for i in CrowX:
						FIGHTANIMATION(screen, enemy, battleBack)	
						screen.blit(i,(300,100))
						time.wait(50)
						display.flip()
					mana-=10
					Enemy_HP -= Attack_DMG
					turn = "Enemy"
					stage=0
				elif mb[0] and itemRect.collidepoint(mx,my) or kp[K_c] and mana>=5:
					for i in CrowC:
						FIGHTANIMATION(screen, enemy, battleBack)	
						screen.blit(i,(300,100))
						time.wait(50)
						display.flip()
					mana-=5
					Enemy_HP -= Attack_DMG
					turn = "Enemy"
					stage=0
				# elif stage==2: ####for defencive items or other stuff??? idk we can decide on it later
			# elif stage==3:


		# elif kp[K_x]:
		# 	print(turn + "'s turn to attack!!")
		# 	for i in CrowX:
		# 		FIGHTANIMATION(screen, enemy, battleBack)	
		# 		screen.blit(i,(300,100))
		# 		time.wait(50)
		# 		display.flip()
		# 	Enemy_HP -= Attack_DMG
		# 	print("Enemy HP:",Enemy_HP)
		# 	turn = "Enemy"
		# elif turn == "Player" and Player_HP > 0 and kp[K_c]:
		# 	print(turn + "'s turn to attack!!")
		# 	for i in CrowC:
		# 		FIGHTANIMATION(screen, enemy, battleBack)	
		# 		screen.blit(i,(300,100))
		# 		time.wait(50)
		# 		display.flip()
		# 	Enemy_HP -= Attack_DMG
		# 	print("Enemy HP:",Enemy_HP)
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
	display.flip()
	myClock.tick(FPS)
quit()