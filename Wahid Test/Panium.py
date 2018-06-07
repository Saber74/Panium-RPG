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
battle = False
#####################################fonts##################################
font.init()
fireFont = font.Font("Breathe Fire.otf",30)
#######################################fonts##############################
#############battle variables
Enemy_HP = 100
xp = 0
charNum = 0
stage = 0
currNum = 0
rec = False
################ entry and openning pic and gif"""""""""""""""""""""''
# for i in range(0,71):
# 	screen.fill((37,34,39))
# 	screen.blit(image.load("Entry\output-%i.png"%i),(100,75))
# 	display.update() # time.wait(100)
# #####rects
# newGamerect=Rect(WIDTH//2-120,HEIGHT//2-30,200,75)
# screen.blit(transform.scale(image.load("option1.jpg"),(WIDTH,HEIGHT)),(0,0))
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
attack1Rect=Rect(0,round(HEIGHT*7/8,0),round(WIDTH*1/3,0),HEIGHT-round(HEIGHT*7/8,0))
attack3Rect=Rect(round(WIDTH*2/3,0),round(HEIGHT*7/8,0),round(WIDTH*1/3),HEIGHT-round(HEIGHT*7/8,0))
attack2Rect=Rect(round(WIDTH*1/3,0),round(HEIGHT*7/8,0),round(WIDTH*1/3),HEIGHT-round(HEIGHT*7/8,0))
defenseRect=Rect(round(WIDTH*1/3,0),round(HEIGHT*7/8,0),round(WIDTH*1/3),HEIGHT-round(HEIGHT*7/8,0))
itemRect=Rect(round(WIDTH*2/3,0),round(HEIGHT*7/8,0),round(WIDTH*1/3),HEIGHT-round(HEIGHT*7/8,0))
###############################################
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
step_counter = 0
npc_item = {}
c = 'NULL'
quit_stat = ''
menu_base = transform.scale(image.load("img/menu/selection.png").convert_alpha(),(WIDTH, HEIGHT))
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
def start_screen():
	running = True
	while running:

		for evt in event.get():  
			if evt.type == QUIT: 
				running = False

		mx,my=mouse.get_pos()
		mb=mouse.get_pressed()
							  
		display.flip() 
	quit()
def display_main_menu():
	# screen_back = screen.copy()
	menu = transform.scale(image.load("img/menu/main_menu.png").convert_alpha(), (200, 500))
	screen.blit(screen_back, (0,0))
	screen.blit(menu, (100,50))
	arrow_pos = 0
	options = ['Inventory', 'Statistics', 'Quests', 'Save', 'Exit', 'Quit']
	main = True
	while main:
		for evt in event.get():  
			if evt.type == KEYUP:
				if evt.key == K_ESCAPE:
					return
				if evt.key == K_DOWN:	
					arrow_pos += 1
				if evt.key == K_UP:
					arrow_pos -= 1
				if evt.key == K_SPACE and len(options) > 0:
					if options[arrow_pos] == 'Inventory':
						InventoryDisplay(currChar, 0, inventory)
					elif options[arrow_pos] == 'Exit':
						return
					elif options[arrow_pos] == 'Quit':
						save_menu('Quit')
						global quit_stat
						quit_stat = 'quit'
						return
					elif options[arrow_pos] == 'Save':
						save_menu('')
					elif options[arrow_pos] == 'Quests':
						display_quest()	

		count = 0			
		screen.blit(screen_back, (0,0))
		screen.blit(menu, (100,50))
		for i in range(len(options)):
			count += 1
			optionName = medievalFont.render(options[i], True, (0,0,0))
			if arrow_pos == len(options):
				arrow_pos -= 1
			if arrow_pos < 0:
				arrow_pos += 1	
			draw.circle(screen, (0,0,0), (110,75 + 30 * arrow_pos), 6)
			screen.blit(optionName, (120, 30 + 30 * count))
		mx, my = mouse.get_pos()
		display.flip()
def save_menu(purp):
	menu = transform.scale(image.load("img/menu/main_menu_rotated.png").convert_alpha(), (500, 200))
	y = 45
	arrow_pos = 0
	mode = 'save_select'
	saving = True
	while saving:
		for evt in event.get():  
			if evt.type == KEYUP:
				if evt.key == K_ESCAPE:
					saving = False
					return
				if evt.key == K_DOWN:	
					y = 75
				if evt.key == K_UP:
					y = 45
				if evt.key == K_SPACE:
					if y == 45:
						mode = 'saving'
					if y == 75:
						saving = False
						return	
		if mode == 'save_select':				
			screen.blit(screen_back, (0,0))
			screen.blit(menu, (0,0))
			if purp == 'Quit':
				screen.blit(medievalFont.render('Do you want to save before you quit?', True, (0,0,0)), (0, 0))
			else:	
				screen.blit(medievalFont.render('Do you want to save?', True, (0,0,0)), (0, 0))
			screen.blit(medievalFont.render('Yes?', True, (0,0,0)), (20, 30))
			screen.blit(medievalFont.render('No?', True, (0,0,0)), (20, 60))
			draw.circle(screen, (0,0,0), (10,y), 6)
		elif mode == 'saving':
			screen.blit(menu, (0,0))
			saving_txt = 'Saving.....'
			saved_txt = 'Saved'
			prog_txt = ''
			for i in saving_txt:
				prog_txt += i
				screen.blit(menu, (0,0))
				screen.blit(medievalFont.render(prog_txt, True, (0,0,0)), (0, 0))
				time.wait(100)
				display.flip()	
			time.wait(1000)
			screen.blit(menu, (0,0))
			screen.blit(medievalFont.render(saved_txt, True, (0,0,0)), (0, 0))
			display.flip()
			time.wait(1000)
			save_dict()
			saving = False
			return		
		display.flip()		
def display_quest():
	back = transform.scale(image.load("img/menu/parchment.png").convert_alpha(), (WIDTH, HEIGHT))
	selectedRect = Rect(0,0,800,200)
	display_range = 0
	quest_dict = {}
	display_txt = []

	prog_dict = {}
	prog_txt = []
	
	rec_dict = {}
	rec_txt = []
	for i in quest_completion:
		if quest_completion[i][0] == 'true' and quest_completion[i][-1] == 'false':
			quest_dict[i] = quest_completion[i][1] + ' with ' + quest_completion[i][2]
			if quest_completion[i][1] == 'Talk':
				if quest_completion[i][3] == 'true':
					prog_dict[i] = 'Progress: You have talked with ' + quest_completion[i][2]
				if quest_completion[i][3] == 'false':
					prog_dict[i] = 'Progress: You have not talked with ' + quest_completion[i][2]
			if quest_completion[i][3] == 'true':	
				rec_dict[i] = 'Quest Completion: Talk to ' + i + ' to complete your quest!'
			else:
				rec_dict[i] = "Quest Completion: You haven't completed the quest yet!"
	for i in quest_dict:
		t = timesNewRomanFont.render('Quest: ' + quest_dict[i], True, (0,0,0))
		display_txt.append(t)	
	for i in prog_dict:
		t = timesNewRomanFont.render(prog_dict[i], True, (0,0,0))
		prog_txt.append(t)	
	for i in rec_dict:
		t = timesNewRomanFont.render(rec_dict[i], True, (0,0,0))
		rec_txt.append(t)	
	counter = 0
	quest_thang = True
	while quest_thang:
		for evt in event.get():  
			if evt.type == QUIT: 
				quest_thang = False	
			if evt.type == KEYUP:
				if evt.key == K_ESCAPE:
					quest_thang = False
					return	
				if evt.key == K_UP:
					if selectedRect.y == 0 and display_range > 0:
						display_range -= 1
					else:
						if selectedRect.y > 0: 
							selectedRect.y -= 200
				if evt.key == K_DOWN:
					if selectedRect.y == 400:
						if len(display_txt) % 3 != 0:
							if display_range < len(display_txt) % 3:
								display_range += 1
						else:
							if display_range < len(display_txt) - 3:	
								display_range += 1
					else:	
						if selectedRect.y < 400:
							selectedRect.y += 200
				if evt.key == K_j:
					print(len(quest_completion))	
		mx,my=mouse.get_pos()
		mb=mouse.get_pressed()
		screen.blit(back, (0,0))
		draw.rect(screen, (0,0,0), selectedRect, 5)
		if len(display_txt) <= 3 and display_range > 0:
			display_range = 0
		for i in range(display_range, len(display_txt)):
			screen.blit(display_txt[i], (10, 0 + 200 * counter))
			screen.blit(prog_txt[i], (10, 25 + 200 * counter))
			screen.blit(rec_txt[i], (10, 50 + 200 * counter))
			counter += 1
		counter = 0	
		display.flip()
def load_object(fname, chests, walls, portals):
	global quest_completion
	for tile_object in fname.objects:
		if tile_object.name == 'wall':
			obs = Obstacle(tile_object.x, tile_object.y, tile_object.width, tile_object.height)
			walls.add(obs)
		elif tile_object.name == 'chest':
			chest = Chest(tile_object.x, tile_object.y, tile_object.width, tile_object.height, tile_object.type, tile_object.ChestName, tile_object.Item)	
			chests.add(chest)
		elif tile_object.name == "Portal":
			port = Portal(tile_object.x, tile_object.y, tile_object.width, tile_object.height, tile_object.type, tile_object.xd, tile_object.yd)	
			portals.add(port)
		elif tile_object.name == "Clerk":
			clerk = Store_Clerk(tile_object.x, tile_object.y, tile_object.type)
			clerks.add(clerk)
		elif tile_object.name == 'NPC':
			npc = NPC(tile_object.x, tile_object.y, tile_object.type, [tile_object.Dialogue], tile_object.item, tile_object.Name, tile_object.width, tile_object.height)	
			npcs.add(npc)
		elif tile_object.name == 'Quest_NPC':
			quest_npc = Quest_NPC(tile_object.x, tile_object.y, tile_object.type, [tile_object.Dialogue, tile_object.DialogueQuest, tile_object.DialogueFinish], tile_object.item, tile_object.Name, tile_object.Quest)	
			if tile_object.Name not in quest_completion:
				quest_completion[tile_object.Name] = [tile_object.Quest, tile_object.Key, tile_object.Goal, tile_object.Complete, tile_object.Received]
			npcs.add(quest_npc)
def levelSelect(lvl, chests, walls, portals):
	if lvl == '0':
		fname = load_pygame("Maps/STORE.tmx")
		tops = load_pygame("Maps/blank.tmx")
	elif lvl == '1':
		fname = load_pygame("Maps/grasslands.tmx")
		tops = load_pygame("Maps/over0.tmx")
	elif lvl == '2':
		fname = load_pygame("Maps/desert.tmx")
		tops = load_pygame("Maps/blank.tmx")
	elif lvl == '3':
		fname = load_pygame("Maps/Town.tmx")
		tops = load_pygame("Maps/Town_Tops.tmx")
	elif lvl == '4':
		fname = load_pygame("Maps/snow_place.tmx")
		tops = load_pygame("Maps/snow_place_tops.tmx")
	elif lvl == '5':
		fname = load_pygame("Maps/house1.tmx")
		tops = load_pygame("Maps/blank.tmx")
		# player.re = True
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
def InventoryDisplay(current_Character, num, inventory):
	global inv_dict
	inv = ''
	inventory = inventory
	if num != 5:
		for i in inventory:
			number = 0
			for n in inventory:
				if i == n:
					number += 1
			inv += i + ' ' + 'x' + str(number) + ', '
		split = inv.split(', ')
		del split[split.index('')]
		for i in split:
			s1 = i.split(' x')
			if s1[0] not in inventory:
				inv_dict[s1[0]] = ''
			else:
				inv_dict[s1[0]] = i
	else:
		split = inventory.split(' // ')
		for i in split:
			number = 0
			for n in split:
				if i == n:
					number += 1
			if i + ' ' + 'x' + str(number) not in inv:		
				inv += i + ' ' + 'x' + str(number) + ' // '

	if num == 0:
		display_inventory(inv_dict, current_Character, 'inventory')	
	elif num == 1:
		return inv_dict
	elif num == 2:
		display_inventory(inv_dict, current_Character, 'sell')	
	elif num == 3:
		display_inventory(inv_dict, current_Character, 'battle')	
	elif num == 5:
		alert_display(inv, 1)	
			
def display_inventory(Inventory, current_Character, mode):
	global inv_dict
	screen.blit(menu_base, (0,0))
	arrow_pos = 0
	inventory_open = True
	inv = []
	display_range = 0
	tmp_inv = []
	counter = 0
	Inventory = Inventory
	for i in Inventory:
		if inv_dict[i] != '':
			inv.append(i)
	while inventory_open:
		for evt in event.get():  
			if evt.type == KEYUP:
				if evt.key == K_ESCAPE or evt.key == K_i and mode != 'sell':
					if mode == "sell":
						global c
						c = 'NULL'
						return c
					inventory_open = False
					return
			if evt.type == KEYDOWN:
				if evt.key == K_DOWN:
					if arrow_pos == 16 and display_range < 16:	
						if display_range < len(inv) - 17:
							display_range += 1
						# display_range += 1
					if arrow_pos < 16:
						arrow_pos += 1
					if counter < len(inv):	
						counter += 1
				if evt.key == K_UP:
					if arrow_pos == 0 and display_range > 0:
						display_range -= 1	
					if arrow_pos > 0:
						arrow_pos -= 1
					if counter > 0:	
						counter -= 1
				if evt.key == K_SPACE and len(inv) > 0:
					if mode == 'inventory':
						x = inv_dict[inv[counter]]
						y = x.split(" x")
						if y[1] == '1':
							inv_dict[y[0]] = ''
						for i in HP_items:
							i = i.split(' ')
							if y[0] in i:
								print("HP +", i[1])
								HP_Change(i[1])
						del inv[counter]	
						del inventory[inventory.index(y[0])]
						tmp = InventoryDisplay(current_Character, 1, inventory)
						inv = []
						for i in tmp:
							if inv_dict[i] != '':
								inv.append(i)
					if mode == 'sell':
						global gold
						x = inv_dict[inv[counter]]
						y = x.split(" x")
						if y[1] == '1':
							inv_dict[y[0]] = ''
						try:
							gold += load_dict()[3][y[0]]
							print("You have gained", str(load_dict()[3][y[0]]), "gold!! Now you have", str(gold), "gold in total!!")
						except:
							gold += 100
							print("You have gained", str(100), "gold!! Now you have", str(gold), "gold in total!!")
						del inv[counter]	
						del inventory[inventory.index(y[0])]
						tmp = InventoryDisplay(current_Character, 1, inventory)
						inv = []
						for i in tmp:
							if inv_dict[i] != '':
								inv.append(i)
					if mode == 'battle':
						global used
						x = inv[counter]
						y = x.split(" x")
						for i in HP_items:
							i = i.split(' ')
							if y[0] in i:
								print("HP +", i[1])
								HP_Change(i[1])
						del inv[counter]	
						del inventory[inventory.index(y[0])]
						used = True
						return used
		count = 0			
		screen.blit(menu_base, (0,0))
		tmp_inv = []	
		for i in range(display_range, len(inv)):
			tmp_inv.append(inv[i])	
		if arrow_pos > len(inv):
			arrow_pos = len(inv)
		if counter >= len(inv) - 1:	
			counter = len(inv) - 1
		if len(inv) > 16:	
			if len(inv) - 17 < display_range:
				display_range = len(inv) - 17
		for i in range(len(tmp_inv)):
			if i <= 16:
				count += 1
				ItemName = medievalFont.render(inv_dict[tmp_inv[i]], True, (0,0,0))
				screen.blit(ItemName, (470, 20 + 30 * count))
				if arrow_pos == len(inv):
					arrow_pos -= 1
				if arrow_pos < 0:
					arrow_pos += 1	
				draw.circle(screen, (0,0,0), (455,65 + 30 * arrow_pos), 6)
		if current_Character == "Crow":
			screen.blit(transform.scale(image.load("img/faces/crow.png").convert_alpha(), (130,185)),(30,35))			
		elif current_Character == "Raven":
			screen.blit(transform.scale(image.load("img/faces/raven.png").convert_alpha(), (130,185)),(30,35))			
		mx, my = mouse.get_pos()
		display.flip()

	arrow_pos = 0

def alert_display(item, mode):
	item = item
	n = 0
	text_y = 60
	alert = True
	while alert:
		for evt in event.get():  
			if evt.type == QUIT: 
				alert = False
			if evt.type == KEYDOWN:
				if evt.key == K_z:
					alert = False
					return	
				if evt.key == K_ESCAPE:
					alert = False
					return	
		mx,my=mouse.get_pos()
		mb=mouse.get_pressed()
		kp = key.get_pressed()
		if n == 0:
			screen.blit(dialogue_box, (0,0))
			screen.blit(timesNewRomanFont.render('You have received the following items:', True, (150,150,150)), (45, 30))
			split = item.split(' // ')
			if '' in split:
				del split[split.index('')]
			for i in range(len(split)):
				screen.blit(timesNewRomanFont.render(split[i], True, (150,150,150)), (45, text_y + 30 * i))
				# time.wait(100)
				display.flip()
			n = 1	
		display.flip() 
	quit()

def HP_Change(HP):
	global stats
	if currChar == 'Crow':
		stats[0][2] += int(HP)
	if currChar == 'Raven':
		stats[1][2] += int(HP)
def FIGHTANIMATION(surf, enemy, battleBack):
	surf.blit(battleBack,(0,0))
	surf.blit(enemy,(187.5,0))	
def load_dict():
	prog_data = p.load(open("prog.dat", 'rb'))
	crow_data = p.load(open("crow_stats.dat", 'rb'))
	item_value = p.load(open("item_value.dat", 'rb'))
	raven_data = p.load(open("raven_stats.dat", 'rb'))
	return prog_data, crow_data, raven_data, item_value
def save_dict():
	prog_data = {"lvl": lvl,
				 "Coords": [x_diff, y_diff],
				 "Chests": openedChests,
				 "inv": inventory,
				 "Gold": gold,
				 "npc_items": npc_item,
				 "Current Charachter": currChar,
				 "Quests": quest_completion,
				 "inv_dict": inv_dict}
	item_value = {'Potion': 75,
				  'Elixer': 50,
				  'Sword': 25,
				  'Shield': 25}  	 			  
	crow_data = {"Stats": stats[0]}	  	 
	raven_data = {"Stats": stats[1]}	  	 
	p.dump(prog_data, open("prog.dat", "wb"))
	p.dump(crow_data, open("crow_stats.dat", "wb"))	
	p.dump(raven_data, open("raven_stats.dat", 'wb'))
	p.dump(item_value, open("item_value.dat", 'wb'))

lvl = str(load_dict()[0]["lvl"])
x_diff, y_diff = load_dict()[0]['Coords'][0], load_dict()[0]['Coords'][1]
openedChests = load_dict()[0]["Chests"]
inventory = load_dict()[0]["inv"]
gold = load_dict()[0]["Gold"]
npc_item = load_dict()[0]['npc_items']
currChar = load_dict()[0]["Current Charachter"]
quest_completion = load_dict()[0]['Quests']
print(quest_completion)
inv_dict = load_dict()[0]['inv_dict']
stats = [load_dict()[1]["Stats"], load_dict()[2]["Stats"]]
stats[0][2] = 10000
crowWalkForward, crowWalkDown, crowWalkRight, crowWalkLeft = [], [], [], []
ravenWalkForward, ravenWalkDown, ravenWalkRight, ravenWalkLeft = [], [], [], []
cf, cd, cr, cl = crowWalkForward, crowWalkDown, crowWalkRight, crowWalkLeft
cm = image.load("SPRITES/Crow/Walk/Up/0.png").convert_alpha()
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

############################################### ATTACK ANIMATIONS ###############################################
Darkness1 = []
for i in range(22):
	Darkness1.append(image.load("SPRITES/Crow Attacks/%i.png" % i).convert_alpha())
############################################### ATTACK ANIMATIONS ###############################################

############################################ LOADING MAP AND SPRITES ############################################
for i in range(3):
	crowWalkForward.append(image.load("SPRITES/Crow/Walk/Up/%i.png" % i).convert_alpha())
	crowWalkRight.append(image.load("SPRITES/Crow/Walk/Right/%i.png" % i).convert_alpha())	
	crowWalkDown.append(image.load("SPRITES/Crow/Walk/Down/%i.png" % i).convert_alpha())	
	crowWalkLeft.append(image.load("SPRITES/Crow/Walk/Left/%i.png" % i).convert_alpha())	
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
		self.re = False
	def update(self):
		if lvl != '5':
		 self.re = False	
		if self.re:
			self.image = transform.scale(cm, (15,20))
		else:	
			self.image = cm
		self.rect = self.image.get_rect()
		self.rect.x, self.rect.y = self.x, self.y - self.rect.height

class Obstacle(sprite.Sprite):
	def __init__(self, x, y, w, h):
		sprite.Sprite.__init__(self)
		self.rect = Rect(x, y, w, h)
		self.x, self.y = x, y
	def update(self):
		self.rect.topleft = self.x + x_diff, self.y + y_diff

class Portal(sprite.Sprite):
	def __init__(self, x, y, w, h, location, xd, yd):
		sprite.Sprite.__init__(self)
		self.rect = Rect(x, y, w, h)
		self.x, self.y = x, y
		self.xd, self.yd = xd, yd
		self.type = location
	def update(self):
		self.rect.topleft = self.x + x_diff, self.y + y_diff		

class NPC(sprite.Sprite):
	def __init__(self, x, y, importance, speech, item, name, width, height):
		sprite.Sprite.__init__(self)
		global inv_dict
		self.type = importance
		self.speech = speech
		self.item = item
		self.name = name
		self.width, self.height = width, height
		if self.type != '00':
			self.image = image.load("img/NPCs/" + self.type + ".png")#.convert_alpha()
			self.rect = self.image.get_rect()
		else:
			self.image = image.load("img/NPCs/" + self.type + ".png")#.convert_alpha()
			self.image = transform.scale(self.image, (int(self.width), int(self.height)))
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
		self.text_y = 60
		for i in quest_completion:
			if quest_completion[i][2] == self.name and quest_completion[i][3] == 'false' and quest_completion[i][0] == 'true':
				quest_completion[i][3] = 'true'
		if self.interact:
			while self.display_text:
				for evt in event.get():  
					if evt.type == QUIT: 
						self.display_text = False
						self.disp = False
				mx,my=mouse.get_pos()
				mb=mouse.get_pressed()
				kp = key.get_pressed()
				screen.blit(dialogue_box, (0,0))
				screen.blit(timesNewRomanFont.render(self.name + ':', True, (150,150,150)), (45,30))
				self.split = self.speech[0].split(' // ')
				if kp[K_SPACE]:
					if self.prog < len(self.split) - 1 and self.n == 1:
						self.prog += 1	
						self.n = 0
						self.sent = ''
						self.text_y = 60
				if kp[K_z] and self.prog == len(self.split) - 1:
						if self.item != 'NULL' and self.name not in npc_item:
							self.item_split = self.item.split(' // ')
							for i in self.item_split:
								inventory.append(i)
								if i not in inv_dict:
									inv_dict[i] = ''
							npc_item[self.name] = self.name
							InventoryDisplay(currChar, 5, self.item)
						self.display_text = False
						self.interact = False		
				if self.n == 0:
					for i in self.split[self.prog]:
						self.sent += i
						if i == '#':
							self.sent = ''
							self.s = 0	
							self.text_y += 30
							time.wait(650)
						if self.s <= 1:
							self.s += 1
							self.sent = ''	
						else:	
							self.s = 100
						screen.blit(timesNewRomanFont.render(self.sent, True, (150,150,150)), (45,self.text_y))
						display.flip()
						time.wait(35)
					self.n = 1	

class Quest_NPC(sprite.Sprite):
	def __init__(self, x, y, importance, speech, item, name, quest):
		sprite.Sprite.__init__(self)
		global inv_dict
		self.type = importance
		self.speech = speech
		self.item = item
		self.name = name
		self.quest = quest
		self.quest_speech = 0
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
		self.text_y = 60
		if self.name in quest_completion and quest_completion[self.name][0] == 'true':
			self.quest_speech = 1
		if 	quest_completion[self.name][3] == 'true':
			quest_completion[self.name][4] = 'true'
			self.quest_speech = 2
		if self.interact:
			while self.display_text:
				for evt in event.get():  
					if evt.type == QUIT: 
						self.display_text = False
						self.disp = False
				mx,my=mouse.get_pos()
				mb=mouse.get_pressed()
				kp = key.get_pressed()
				screen.blit(dialogue_box, (0,0))
				screen.blit(timesNewRomanFont.render(self.name + ':', True, (150,150,150)), (45,30))
				self.split = self.speech[self.quest_speech].split(' // ')
				if kp[K_SPACE]:
					if self.prog < len(self.split) - 1 and self.n == 1:
						if self.prog < len(self.split) - 1:
							self.prog += 1	
							self.n = 0
							self.sent = ''
							self.text_y = 60
				if kp[K_z] and self.prog == len(self.split) - 1:
					if self.name in quest_completion and quest_completion[self.name][0] == 'false':
						quest_completion[self.name][0] = 'true'
						self.quest_speech = 1
					if self.item != 'NULL' and self.name not in npc_item and quest_completion[self.name][3] == 'true':
						self.item_split = self.item.split(' // ')
						for i in self.item_split:
							inventory.append(i)
							if i not in inv_dict:
								inv_dict[i] = ''
						InventoryDisplay(currChar, 5, self.item)		
						npc_item[self.name] = self.name
					self.display_text = False
					self.interact = False
				if self.n == 0:
					for i in self.split[self.prog]:
						self.sent += i
						if i == '#':
							self.sent = ''
							self.s = 0	
							self.text_y += 30
							time.wait(650)
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
				InventoryDisplay(currChar, 2, inventory)
				self.event = c
			mx, my = mouse.get_pos()
			display.flip()	

class Chest(sprite.Sprite):
	def __init__(self, x, y, w, h, tier, name, item):
		sprite.Sprite.__init__(self)
		self.tier = tier
		self.name = name
		self.opened = False
		self.item = item
		self.images = [image.load("SPRITES/Chest/Tier" + str(self.tier) + "/0.png"),
					   image.load("SPRITES/Chest/Tier" + str(self.tier) + "/1.png")]
		self.prev_image = self.image = self.images[0] ; self.rect = Rect(x, y, w, h)
		if self.name in openedChests:
			self.image = self.images[1] 
		self.x, self.y = x, y
	def update(self):
		global chest_open
		self.rect.topleft = self.x + x_diff, self.y + y_diff
		if self.image == self.prev_image and self.opened and kp[K_SPACE]:
			self.image = self.images[1]
			self.split = self.item.split(' // ')
			openedChests.append(self.name)
			for i in self.split:
				inventory.append(i)
				print(i, "has been obtained!!")
			InventoryDisplay(currChar, 5, self.item)
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
	print(x_diff, y_diff)
	for evt in event.get():  
		if evt.type == QUIT: 
			save_dict()
			running = False
		if evt.type == KEYDOWN:
			if evt.key == K_ESCAPE:
				running = False    	
		if evt.type == KEYUP:
			if evt.key == K_1:
				cf, cd, cr, cl = crowWalkForward, crowWalkDown, crowWalkRight, crowWalkLeft
				currChar = "Crow"
			if evt.key == K_2:
				cf, cd, cr, cl = ravenWalkForward, ravenWalkDown, ravenWalkRight, ravenWalkLeft
				currChar = "Raven"
			if evt.key == K_o:
				mixer.music.stop()
			if evt.key == K_p:
				mixer.music.play()		
			if mode == 0:	
				if evt.key == K_i:
					InventoryDisplay(currChar, 0, inventory)	
				if evt.key == K_q:
					inventory = []
					openedChests = []
					npc_item = {}
					quest_completion = {}
					inv_dict = {}
				if evt.key == K_l:
					fname, tops = levelSelect(lvl, chests, walls, portals)
					load_object(fname, chests, walls, portals)
					print("reload")
					time.wait(100)
				if evt.key == K_j:
					# if currChar == 'Crow':
					# 	stats[0][2] += 100 	
					# 	print(stats[0][2])
					# if currChar == 'Raven':
					# 	stats[1][2] += 100 	
					# 	print(stats[1][2])
					# print(stats)
					# print(inv_dict)
					print(quest_completion)
				if evt.key==K_a:
					if stage>0:
						stage-=1
				if evt.key==K_h:
					stats[currNum][2]=30
				if evt.key==K_x:
					rec = not rec
				if evt.key==K_n:
					stage=10	
				if evt.key == K_r:
					mode = 0		
				if evt.key == K_m:
					if pressed == "UP":
						cm = cf[0]
					elif pressed == "DOWN":
						cm = cd[0]
					elif pressed == "LEFT":
						cm = cl[0]
					elif pressed == "RIGHT":
						cm = cr[0]
					screen_back = screen.copy()	
					display_main_menu()
			if evt.key==K_a:
				if stage>0:
					stage-=1
			if evt.key==K_h:
				stats[currNum][2]=30
			if evt.key==K_n:
				stage=10	
			if evt.key == K_r:
				mode = 0	
		if evt.type==MOUSEBUTTONUP:
			if stage==1:
				battle=True		
	mx,my=mouse.get_pos()
	mb=mouse.get_pressed()
	kp = key.get_pressed()
	U = R = D = L = moving = False
	# xp+=10
	print(openedChests)
	# screen.fill((255,255,255))
	# screen.blit(image.load("pvw1854.png"),(WIDTH//4,HEIGHT//3))
	# KEYBOARD MOVEMENT	
	if quit_stat == 'quit':
		running = False
	# encounter_steps = r(10,80)	
	# if int(step_counter) == encounter_steps:
	# 	step_counter = 0
	# 	mode = 1
	# print(step_counter)	
	if rec:
		draw.rect(screen, (0,0,0), player.rect)
	if mode == 0:
		if currChar == "Crow":
			Player_HP = stats[0][2]
			cf, cd, cr, cl = crowWalkForward, crowWalkDown, crowWalkRight, crowWalkLeft
		elif currChar == "Raven":
			Player_HP = stats[1][2]
			cf, cd, cr, cl = ravenWalkForward, ravenWalkDown, ravenWalkRight, ravenWalkLeft
		if kp[K_RIGHT]:
			x_diff -= pan
			R = True
			moving = True
			pressed = "RIGHT"
			step_counter += .2
		elif kp[K_LEFT]:
			x_diff += pan
			L = True
			moving = True
			pressed = "LEFT"
			step_counter += .2
		elif kp[K_UP]:
			y_diff += pan
			U = True
			moving = True
			pressed = "UP"
			step_counter += .2
		elif kp[K_DOWN]:
			y_diff -= pan
			D = True
			moving = True
			pressed = "DOWN"
			step_counter += .2
		else:
			x = y = 0	
		if kp[K_LSHIFT]:
			pan = 10
			s = 2
		else:
			pan = 5
			s = 5
		# print(myClock.get_fps())	
		# if myClock.get_fps() < 50:
		# 	print("DROPPED FRAME")
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
			npc_interact[0].display_speech(True, True)
		hit = sprite.spritecollide(player, walls, False)
		if hit:
			if player.rect.colliderect(hit[0].rect):
				if L:
					x_diff -= pan
				elif D:
					y_diff += pan
				elif U:
					y_diff -= pan
				elif R:
					x_diff += pan
				npcs.update()
				chests.update()	
				clerks.update()
		tel = sprite.spritecollide(player, portals, False)
		if tel: #and kp[K_SPACE]:
			lvl = tel[0].type
			x_diff, y_diff = int(tel[0].xd), int(tel[0].yd)
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
				cm = cf[1]
			elif pressed == "DOWN":
				cm = cd[1]
			elif pressed == "LEFT":
				cm = cl[1]
			elif pressed == "RIGHT":
				cm = cr[1]
		########################################### MOVEMENT ANIMATION ###########################################
	else:
		pass
		if mode == 1:
			turn = "Player"		
			used = False
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
		for i in range(stats[currNum][2]//2):
			# INSERT
			draw.rect(screen,(255,0,0),Rect(x,round(HEIGHT*6/8),10,15))
			x+=13
		x=0
		hpText=str("Player HP:"+str(stats[currNum][2]))
		hpEdit=fireFont.render(hpText,True,(0,200,0))
		screen.blit(hpEdit,(0,round(HEIGHT*6/8-40,0)))
		for i in range(stats[currNum][5]//2):
			draw.rect(screen,(0,0,255),Rect(x,round(HEIGHT*6/8+50),10,15))
			x+=13
		x=0
		manaText=str("Player Mana: "+str(stats[currNum][5]))
		manaEdit=fireFont.render(manaText,True,(0,200,0))
		screen.blit(manaEdit,(0,round(HEIGHT*6/8+20)))
		enemyhp=str("name of enemy HP: "+str(Enemy_HP))
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
				Attack_DMG = stats[currNum][1]*4
				print("Your attack will do",Attack_DMG,"damage to the enemy!!")	###[1 is dmg][3 is magic dmg]
			elif defenseRect.collidepoint(mx,my):
				Attack_DMG = stats[currNum][3]*5
				print("Your attack will do",Attack_DMG,"damage to the enemy!!") ###[1 is dmg][3 is magic dmg]	
			elif itemRect.collidepoint(mx,my):
				Attack_DMG = stats[currNum][3]*3+stats[currNum][1]*3	###[1 is dmg][3 is magic dmg]	
				print("Your attack will do",Attack_DMG,"damage to the enemy!!")	
		########################################## ATTACK SELECTION ##########################################

		############################################### BATTLE ###############################################
		# used = False
		if turn == "Player" and stats[currNum][2] > 0 :
			if stage==1:
				if battle and mb[0]and attackRect.collidepoint(mx,my) or kp[K_z]:
					print(turn + "'s turn to attack!!")
					for i in CrowZ:
						FIGHTANIMATION(screen, enemy, battleBack)	
						screen.blit(i,(300,100))
						time.wait(50)
						display.flip()
					Enemy_HP -= Attack_DMG
					turn = "Enemy"
					stage=0
					battle=False
				elif battle and mb[0] and defenseRect.collidepoint(mx,my) or kp[K_x] and stats[currNum][-1]>=10:
					for i in CrowX:
						FIGHTANIMATION(screen, enemy, battleBack)	
						screen.blit(i,(300,100))
						time.wait(50)
						display.flip()
					stats[currNum][-1]-=10
					Enemy_HP -= Attack_DMG
					turn = "Enemy"
					stage=0
				elif battle and mb[0] and itemRect.collidepoint(mx,my) or kp[K_c] and stats[currNum][-1]>=5:
					for i in CrowC:
						FIGHTANIMATION(screen, enemy, battleBack)	
						screen.blit(i,(300,100))
						time.wait(50)
						display.flip()
					stats[currNum][-1]
					Enemy_HP -= Attack_DMG
					turn = "Enemy"
					stage=0
				# elif stage==2: ####for defencive items or other stuff??? idk we can decide on it later
			elif stage==3 and len(inventory) > 0:
				if used == False:
					InventoryDisplay(currChar, 3, inventory)
					stage = 1	
				else:
					print("You Have Already Used An Item!")	

		if turn == "Enemy" and Enemy_HP > 0:
			used = False
			time.wait(100)
			print(turn + "'s turn to attack!!")
			# stats[currNum][2] -= stats[currNum][1]*3//stats[currNum][2] ###20 is enemy damage and must be changed soon
			stats[currNum][2] -= 100 ###20 is enemy damage and must be changed soon
			print("Player HP:",stats[currNum][2])	
			turn = "Player"
		if stats[currNum][2] <= 0 or Enemy_HP <= 0:	
			if stats[currNum][2] <= 0:
				print("YOU LOST!!")		
			elif Enemy_HP <= 0:	
				print("YOU WON!!")	
			elif stats[currNum][2] <= 0 and Enemy_HP <= 0:
				print("YOU LOST!!")		
			mode = 0	
		print(used)
		############################################### BATTLE ###############################################
	# DRAW / RENDER
	display.flip()
	myClock.tick(FPS)
quit()