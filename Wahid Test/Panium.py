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
########################################## USE IN FINAL PRODUCT ##########################################
# screen = display.set_mode(size, FULLSCREEN)
# width, height = size = (min(1920,display.Info().current_w), min(1080,display.Info().current_h))
########################################## USE IN FINAL PRODUCT ##########################################
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
s = 5
c = 'NULL'
menu_base = transform.scale(image.load("img/menu/selction.png").convert_alpha(),(WIDTH, HEIGHT))
dialogue_box = transform.scale(image.load("img/dialogue boxes/Dialog_Box.png").convert_alpha(), (WIDTH, int(HEIGHT / 3.25)))
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
		elif tile_object.name == 'chest':
			chest = Chest(tile_object.x, tile_object.y, tile_object.width, tile_object.height, tile_object.type, tile_object.ChestName)	
			chests.add(chest)
		elif tile_object.name == "Portal":
			port = Portal(tile_object.x, tile_object.y, tile_object.width, tile_object.height, tile_object.type)	
			portals.add(port)
		elif tile_object.name == "Clerk":
			clerk = Store_Clerk(tile_object.x, tile_object.y, tile_object.type)
			clerks.add(clerk)
		elif tile_object.name == 'NPC':
			npc = NPC(tile_object.x, tile_object.y, tile_object.type, tile_object.Dialogue, tile_object.item, tile_object.Name)	
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
	counter = 0
	tmp_inv = inv
	# tmp_inv = []
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
					counter += 1
					if arrow_pos > 16:
						tmp_inv = []
						for i in inv[(counter - 16):]:
							tmp_inv.append(i)
						arrow_pos = 16	
					print(arrow_pos)
				if evt.key == K_UP:
					arrow_pos -= 1
					counter -= 1
					# if arrow_pos < 0:
					# 	tmp_inv = []
					# 	for i in inv[(counter - 16):(counter + 16)]:
					# 		tmp_inv.append(i)
					# 	arrow_pos = 0
					print(arrow_pos)
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
		screen.blit(menu_base, (0,0))
		# if arrow_pos > 16:
		# 	tmp_inv = []
		# 	for i in inv[(arrow_pos - 16):]:
		# 		tmp_inv.append(i)
		for i in range(len(tmp_inv)):
			ItemName = medievalFont.render(tmp_inv[i], True, (0,0,0))
			if arrow_pos == len(inv):
				arrow_pos -= 1
			if arrow_pos < 0:
				arrow_pos += 1	
			draw.circle(screen, (0,0,0), (455,65 + 30 * arrow_pos), 6)
			screen.blit(ItemName, (470, 20 + 30 * (i + 1)))
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
				 "npc_items": npc_item,
				 "Current Charachter": currChar}
	item_value = {'Potion': 75,
				  'Elixer': 50,
				  'Sword': 25,
				  'Shield': 25}  	 			  

	crow_data = {"HP": Crow_HP,
				 "Attack": 0,
				 "Defense": 0,
				 "Magic Attack": 0,
				 "Magic Defense": 0,
				 "Dexterity": 0}	  	 
	raven_data = {"HP": Raven_HP,
				 "Attack": 0,
				 "Defense": 0,
				 "Magic Attack": 0,
				 "Magic Defense": 0,
				 "Dexterity": 0}
	p.dump(prog_data, open("prog.dat", "wb"))
	p.dump(crow_data, open("crow_stats.dat", "wb"))	
	p.dump(raven_data, open("raven_stats.dat", 'wb'))
	p.dump(item_value, open("item_value.dat", 'wb'))

lvl = str(load_dict()[0]["lvl"])
x_diff, y_diff = load_dict()[0]['Coords'][0], load_dict()[0]['Coords'][1]
openedChests = load_dict()[0]["Chests"]
# inventory = load_dict()[0]["inv"]
inventory = ['1','2','3','4','5','6','7','8','9','10',
			 '11','12','13','14','15','16','17','18','19','20',
			 '21','22','23','24','25','26','27','28','29','30']
gold = load_dict()[0]["Gold"]
npc_item = load_dict()[0]['npc_items']
print(npc_item)
currChar = load_dict()[0]["Current Charachter"]

Crow_HP = load_dict()[1]["HP"]

Raven_HP = load_dict()[2]["HP"]

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

class NPC(sprite.Sprite):
	def __init__(self, x, y, importance, speech, item, name):
		sprite.Sprite.__init__(self)
		self.type = importance
		self.speech = speech
		self.item = item
		self.name = name
		self.image = image.load("img/NPCs/" + self.type + ".png")#.convert_alpha()
		self.rect = self.image.get_rect()
		self.interact = False
		self.display_text = False
		self.x, self.y = x, y
	def update(self):
		self.rect.topleft = self.x + x_diff, self.y + y_diff
	def display_speech(self, interact, display_text):
		self.interact = interact
		self.display_text = display_text
		self.prog = 0
		self.sent = ''
		self.n = 0
		self.s = 100
		self.text_y = 30
		if self.interact:
			while self.display_text:
				for evt in event.get():  
					if evt.type == QUIT: 
						self.display_text = False
						self.disp = False
					if evt.type == KEYDOWN:
						if evt.key == K_z and self.prog == len(self.split) - 1:
							if self.item != 'NULL' and self.name not in npc_item:
								self.item_split = self.item.split(' // ')
								for i in self.item_split:
									inventory.append(i)
								npc_item[self.name] = self.name
							self.display_text = False
							self.interact = False
						if evt.key == K_SPACE:
							if self.prog < len(self.split) - 1:
								self.prog += 1	
								self.n = 0
								self.sent = ''
								self.text_y = 30
				mx,my=mouse.get_pos()
				mb=mouse.get_pressed()
				# print(mx,my)
				screen.blit(dialogue_box, (0,0))
				self.split = self.speech.split(' // ')
				if self.n == 0:
					for i in self.split[self.prog]:
						self.sent += i
						if i == '#':
							self.sent = ''
							self.s = 0	
							self.text_y += 30
							time.wait(600)
						if self.s <= 1:
							self.s += 1
							self.sent = ''	
						else:	
							self.s = 100
						screen.blit(timesNewRomanFont.render(self.sent, True, (150,150,150)), (45,self.text_y))
						display.flip()
						# time.wait(70)
						time.wait(35)
					self.n = 1	

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
				npc_item = {}
			if evt.key == K_b:
				mode = 1 - mode	
			if evt.key == K_o:
				mixer.music.stop()
			if evt.key == K_p:
				mixer.music.play()		
			if evt.key == K_j:
				print(gold)	
	mx,my=mouse.get_pos()
	mb=mouse.get_pressed()
	kp = key.get_pressed()
	U = R = D = L = moving = False
	# print(myClock.get_fps())
	# print(load_dict()[4])
	# KEYBOARD MOVEMENT	
	if mode == 0:
		if currChar == "Crow":
			Player_HP = Crow_HP
			cf, cd, cr, cl = crowWalkForward, crowWalkDown, crowWalkRight, crowWalkLeft
		elif currChar == "Raven":
			Player_HP = Raven_HP
			cf, cd, cr, cl = ravenWalkForward, ravenWalkDown, ravenWalkRight, ravenWalkLeft
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
		if npc_interact and kp[K_SPACE]:
			print(npc_interact[0].item)
			npc_interact[0].display_speech(True, True)
				

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
	display.flip()
	myClock.tick(FPS)
quit()