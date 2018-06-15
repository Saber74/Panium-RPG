from pygame import * # used for literally everything
from pytmx import * # used for loading TMX files in python
from random import randint as r
import os
import pickle as p # used for saving all game data in encrypted incorporations
WIDTH, HEIGHT = 800, 600 
size=(WIDTH, HEIGHT)
os.environ['SDL_VIDEO_WINDOW_POS'] = '0,10'
screen = display.set_mode(size)
########################################## USE IN FINAL PRODUCT ##########################################
# screen = display.set_mode(size, FULLSCREEN)
# width, height = size = (min(1920,display.Info().current_w), min(1080,display.Info().current_h))
########################################## USE IN FINAL PRODUCT ##########################################
battle = False # used to check if you are attacking
#####################################fonts##################################
font.init()
fireFont = font.Font("FONTS/Breathe Fire.otf",30)
#######################################fonts##############################
#############battle variables
Enemy_HP = 100 # sets base enemy hp
xp = 0 # sets base xp
charNum = 0 # sets base character
stage = 0 # used for the stages of battle
currNum = 0
Z = X = C = False # this is for using buttons for battle
######################################### Fighting Screen ################################################
attackRect=Rect(0,round(HEIGHT*7/8,0),round(WIDTH*1/3,0),HEIGHT-round(HEIGHT*7/8,0)) # creates rects for battle
attack1Rect=Rect(0,round(HEIGHT*7/8,0),round(WIDTH*1/3,0),HEIGHT-round(HEIGHT*7/8,0)) # creates rects for battle
attack3Rect=Rect(round(WIDTH*2/3,0),round(HEIGHT*7/8,0),round(WIDTH*1/3),HEIGHT-round(HEIGHT*7/8,0)) # creates rects for battle
attack2Rect=Rect(round(WIDTH*1/3,0),round(HEIGHT*7/8,0),round(WIDTH*1/3),HEIGHT-round(HEIGHT*7/8,0)) # creates rects for battle
defenseRect=Rect(round(WIDTH*1/3,0),round(HEIGHT*7/8,0),round(WIDTH*1/3),HEIGHT-round(HEIGHT*7/8,0)) # creates rects for battle
itemRect=Rect(round(WIDTH*2/3,0),round(HEIGHT*7/8,0),round(WIDTH*1/3),HEIGHT-round(HEIGHT*7/8,0)) # creates rects for battle
###############################################
myClock = time.Clock() # creates a clock
FPS = 60 # sets the frames per seconc
Player_HP = 100 # sets base player health
battleAnimation = [] # creates an empty list that stores the animations for battle
pressed = "NULL" # Stores the last direction the character was in
frame = 0 # frame is the animation frame for the character animation
counter = 0 # counter that will time out the rate at which the frame is added to
x_diff = y_diff = 0 # these are the offsets for the actual map as the characters don't move
pan = 1 # pan is the rate at which the offset is increased or decreased
mode = 0 # your mode determines whether you are in battle or in normal mode
s = 5 # s is your speed at which you move and the speed at which the animation is completed
step_counter = 0 # step_counter is the variable that counts how many steps you take until you are forced into battle
npc_item = {} # npc_item stores whether you have received an item from an NPC or not
c = 'NULL' # will check whether the player is in buy or sell mode in the various stores
quit_stat = '' # will checck whether the player is quitting or not
menu_base = transform.scale(image.load("img/menu/selection.png").convert_alpha(),(WIDTH, HEIGHT))
dialogue_box = transform.scale(image.load("img/dialogue boxes/Dialog_Box.png").convert_alpha(), (WIDTH, int(HEIGHT / 3.25)))
currChar = "Crow" # stores which character is in play and which character will be used in battle
# the following lists store what specific items do to a specific stats
HP_items = ["Potion // 50", "Meat // 100", "Poison // -50", "Chilli // 100"]
Attack_items = ["Wood Sword // 2", "Stone Sword // 3", "Iron Sword // 5", "Diamond Sword // 8", 'Adamantium Sword // 10']
Defence_items = ["Leather Armour // 4", "Iron Armour // 7", "Diamond Armour // 9", "Adamantium Armour 12"]

font.init()
timesNewRomanFont = font.SysFont("Times New Roman", 24)
medievalFont = font.SysFont("Times New Roman", 24)
fancyFont=font.Font("FONTS/Friedolin.ttf", 95)
# Load the enemys and then adds them to a list
enemy1=image.load("img/enemies/Irongiant.png")
enemy2=image.load("img/enemies/Spider.png")
enemy3=image.load("img/enemies/Death.png")
enemy4=image.load("img/enemies/Demon.png")
enemy5=image.load("img/enemies/Dragon.png")
enemy6=image.load("img/enemies/Earthspirit.png")
enemy7=image.load("img/enemies/Ghost.png")
enemy8=image.load("img/enemies/Gargoyle.png")
enemy9=image.load("img/enemies/Gazer.png")
enemy10=image.load("img/enemies/Lamia.png")
enemy11=image.load("img/enemies/Ogre.png")
enemy12=image.load("img/enemies/Skeleton.png")
enemy13=image.load("img/enemies/Minotaur.png")
enemy14=image.load("img/enemies/Sahuagin.png")
enemy15=image.load("img/enemies/Plant.png")
enemylist=[enemy1,enemy2,enemy3,enemy4,enemy5,enemy6,enemy7,enemy8,enemy9,enemy10,enemy11,enemy12,enemy13,enemy14,enemy15]
##################################################### MUSIC #####################################################
def music(channel, music, length):
	# this function allows us to have any channel play any track for any amount of time / loops
	channels[channel].play(music, length)
mixer.pre_init(44100, -16, 1, 512)# initializes the music mixer before it is actually initialized
mixer.init() 
mixer.set_num_channels(4) ###setting number of channels up
channels = [mixer.Channel(0), mixer.Channel(1), mixer.Channel(2)] # adds the channels to a list

# music and sound selection will add the sound tracks to a list for easier access
music_selection = [mixer.Sound("Music/bgm/Village.wav"), mixer.Sound("Music/bgm/Castle.wav"), mixer.Sound("Music/bgm/Starting.wav"),
				   mixer.Sound("Music/bgm/Boss fight.wav")]
sound_selection = [mixer.Sound("Music/se/The Greatest Pokemon Sound Effects (1).wav"),
				   mixer.Sound("Music/se/GUI sel decision.ogg"), mixer.Sound("music/se/Door exit.ogg")]
# sets channel volume to specific values
channels[0].set_volume(.1)
channels[1].set_volume(.2)
channels[2].set_volume(2)
##################################################### MUSIC #####################################################
def load_dict():
	# this will load data from the .dat files
	prog_data = p.load(open("prog.dat", 'rb'))
	crow_data = p.load(open("crow_stats.dat", 'rb'))
	item_value = p.load(open("item_value.dat", 'rb'))
	raven_data = p.load(open("raven_stats.dat", 'rb'))
	return prog_data, crow_data, raven_data, item_value
lvl = str(load_dict()[0]["lvl"]) # this will store which map is the current map
x_diff, y_diff = load_dict()[0]['Coords'][0], load_dict()[0]['Coords'][1] # this will store the coordinates/offset of the map
openedChests = load_dict()[0]["Chests"] # stores which chests have been opened
inventory = load_dict()[0]["inv"] # will store the inventory of the player
gold = load_dict()[0]["Gold"] # the amount of gold the player has
# gold = 100000
npc_item = load_dict()[0]['npc_items'] # the npcs that have given there held items to the player
currChar = load_dict()[0]["Current Charachter"] # the current character being used
quest_completion = load_dict()[0]['Quests'] # this keeps track of the progress of the quests
inv_dict = load_dict()[0]['inv_dict'] # this will store the order of which items were received. This is used in the inventory for scrolling
stats = [load_dict()[1]["Stats"], load_dict()[2]["Stats"]] # this stores the stats of the two characters
# stats=[[0,0,30,7,5,5,5,5,100], [0,0,30,7,5,5,5,5,100]]
selections = load_dict()[0]['settings'] # this will load saved settings such as screen mode, BGM, and SE
# selections = ['Windowed', "On", 'On']
def introscreen():
	# this loads the introscreen before the player starts to play the game
	firsttime=True # this boolean will run the starting animation
	music(0, music_selection[2], -1) # loads in the music
	channels[0].set_volume(0.7) ##to set volume for things so you don't get deaf
	######################################rects###################
	yesRect=Rect(180,255,200,120)
	noRect=Rect(470,255,170,120)
	newGameRect=Rect(380,400,240,65)
	continueGameRect=Rect(470,470,320,75)
	quitRect=Rect(0,425,140,55)
	###################################################
	go=False #bolean for checking click on quit
	init()
	global quit_stat
	running = True
	while running:
		for evt in event.get():  
			if evt.type == QUIT: 
				running = False
			if evt.type == KEYUP:
				if evt.key == K_ESCAPE:
					quit_stat = 'quit'
					return
		mx,my=mouse.get_pos()
		mb=mouse.get_pressed()
		#################################intro gif######################################3
		if firsttime==True:
			for i in range(3):
				for i in range(0,16):
					screen.blit(image.load("img/ezgif-4-9108664653-gif-im/%i.gif"%i),(100,75))
					display.update()
					time.wait(50)
			firsttime=False
		###########################################################

		###############################################graphics for the intro screen including text and pictures########################
		screen.blit(transform.scale(image.load("img/backs/olga-antonenko-monolith-final.jpg"),(WIDTH,HEIGHT)),(0,0))
		titleFontcont=font.Font("FONTS/Carta_Magna-line-demo-FFP.ttf",85)
		smalltextFont=font.Font("FONTS/Carta_Magna-line-demo-FFP.ttf",50)
		quitFont=font.Font("FONTS/Carta_Magna-line-demo-FFP.ttf",40)
		newGametext=str("New Game")
		continueGameText=str("Continue Game")
		titlecont=str("PANIUM")
		quitText=str("QUIT")
		quitEdit=quitFont.render(quitText,True,(255,0,0))
		titleEditcont=titleFontcont.render(titlecont,True,(255,99,71))
		newGameEdit=smalltextFont.render(newGametext,True,(255,163,149))
		continueGameEdit=smalltextFont.render(continueGameText,True,(255,163,149))
		screen.blit(titleEditcont,(60,-10))
		screen.blit(newGameEdit,(380,400))
		screen.blit(continueGameEdit,(470,470))
		screen.blit(quitEdit,(10,420))
		######################################################################################
		copy=screen.copy()
		############################collision to call each function on the intro screen when required
		surf = Surface((WIDTH,HEIGHT), SRCALPHA)
		if newGameRect.collidepoint(mx,my):
			newGameEdit=smalltextFont.render(newGametext,True,(255,31,80))
			screen.blit(newGameEdit,(380,400))
			if mb[0]:
				# if the player selects the new game options then the game will load in the default data
				global x_diff, y_diff, openedChests, inventory, gold, npc_item, currChar, quest_completion, inv_dict, stats, lvl
				lvl = '5'
				x_diff, y_diff = 90, -15
				openedChests = []
				inventory = []
				gold = 0
				npc_item = {}
				currChar = "Raven"
				quest_completion = {}
				inv_dict = {}
				stats = [[3, 3, 3, 3, 3, 3, 3, 3], [3, 3, 3, 3, 3, 3, 3, 3]]
				stats[1][2] = 10000
				for i in range(255):
					time.wait(10)
					surf.fill((0,0,0,i))
					screen.blit(surf, (0,0))
					display.flip()
				return
		elif continueGameRect.collidepoint(mx,my):
			continueGameEdit=smalltextFont.render(continueGameText,True,(255,31,80))	
			screen.blit(continueGameEdit,(470,470))
			if mb[0]:
				# if they decide to continue then the game will continue as usual
				for i in range(255):
					time.wait(10)
					surf.fill((0,0,0,i))
					screen.blit(surf, (0,0))
					display.flip()
				return
		elif quitRect.collidepoint(mx,my):
			quitEdit=quitFont.render(quitText,True,(255,31,80))
			screen.blit(quitEdit,(10,420))
			if mb[0]:
				go=True

		if go:	####are you sure you want to quit###############################################################3
			screen.blit(transform.scale(image.load("olga-antonenko-monolith-final.jpg"),(WIDTH,HEIGHT)),(0,0))
			confirmquit=font.Font("Something Strange.ttf",110)
			yesnoFont=font.Font("Something Strange.ttf",130)
			text=str("Are you a coward?")
			yesText=str("YES")
			noText=str("NO")
			yesInfo=yesnoFont.render(yesText,True,(0,0,0))
			noInfo=yesnoFont.render(noText,True,(0,0,0))
			info=confirmquit.render(text,True,(255,255,255))
			screen.blit(yesInfo,(200,250))
			screen.blit(noInfo,(500,250))
			screen.blit(info,(30,50))
			display.update()
			if yesRect.collidepoint((mx,my)):
				yesInfo=yesnoFont.render(yesText,True,(255,0,0))
				screen.blit(yesInfo,(200,250))
				if mb[0]:
					quit_stat = 'quit'
					return
			elif noRect.collidepoint((mx,my)):
				noInfo=yesnoFont.render(noText,True,(255,0,0))
				screen.blit(noInfo,(500,250))
				if mb[0]:
					go=False
		display.flip()
				########################################################################################
# introscreen()
if quit_stat == 'quit':
	# it will quit the game
	running = False
def poop(list1,num,currlevel):
	screen.fill((150,220,255))
	timesNewRomanFont = font.SysFont("Times New Roman", 32)
	mode=1 # the process of the xp increase
	xp=110 # the xp
	statuspgrade=0 # how much was added to the stat
	upgrade=0# the number of available points to allocate the points to stats
	selecnum=0 # which stat is currently selected
	point=5 # will see at which point you are at on the stat selection
	stablepoint=5 # the max for the max amount of movement
	selectionList=["attack","defense","magic","magicdefense","health","mana"] # stores stat names
	arrowselected="" # to see what picture will be displayed for the arrows
	# creates the rects for stats
	levelattackRect=Rect(275,200,200,50)
	leveldefenseRect=Rect(550,200,200,50)
	levelmagicRect=Rect(275,350,200,50)
	levelmagicdefenseRect=Rect(550,350,200,50)
	levelhealthRect=Rect(275,500,200,50)
	levelmanaRect=Rect(550,500,200,50)
	# creates the rects for stats
	running = True
	x=0
	# loads images
	uparrow=image.load("img/XP/sortup.png")
	downarrow=image.load("img/XP/sortdown.png")
	uparrowclicked=image.load("img/XP/sortupclicked.png")
	downarrowclicked=image.load("img/XP/sortdownclicked.png")
	downarrowRect=Rect(75,HEIGHT//2,132,65)
	uparrowRect=Rect(75,HEIGHT//2-HEIGHT//7,132,65)
	backlevel=transform.scale(image.load("img/battlebacks1/Translucent.png"), (WIDTH, HEIGHT))	
	levelup=False # bool that stores whether or not that a level up had occurred
	while running:
		for evt in event.get():  
			if evt.type == QUIT: 
				running = False
			if evt.type==KEYDOWN:
				if evt.key == K_ESCAPE:
					# will quit
					global quit_stat
					quit_stat = 'quit'
					return
				if levelup:
					# will determine the limits of the selection
					if evt.key==K_UP:
						arrowselected="up"
						if point>0:
							upgrade+=1
							point-=1
					elif evt.key==K_DOWN:
						arrowselected="down"
						if point<=stablepoint:
							upgrade-=1
							point+=1
					elif evt.key==K_LEFT:
						if selecnum!=0:
							selecnum-=1
					elif evt.key==K_RIGHT:
						if selecnum!=len(selectionList)-1:
							selecnum+=1
		mode=2
		# mx,my=mouse.get_pos()
		if mode==2:
			draw.rect(screen,(211,211,211),Rect(WIDTH//4,HEIGHT//2,WIDTH//2,HEIGHT//20))
			if not levelup:
				# this will draw the xp bar
				for i in range(xp//10):
					draw.rect(screen,(18,107,60),Rect(WIDTH//4+x,HEIGHT//2,WIDTH//2//10,HEIGHT//20))
					x=WIDTH//2//10*i
					time.wait(100)
					display.flip()
			if i>=10 and not levelup:
				# this will reset the xp and will add to the level of the character and levelup becomes true
				xp-=100
				currlevel+=1
				levelup = True
				time.wait(1000)		
				selected=selectionList[selecnum]
			if levelup:
				selected=selectionList[selecnum]
				screen.blit(backlevel,(0,0))
				# renders font and draws them and other items
				# Font=font.Font("FONTS/Carta_Magna-line-demo-FFP.ttf",40)
				attackstat=timesNewRomanFont.render(str(list1[num][3]),True,(0,0,0))
				attacktext=timesNewRomanFont.render(str("Attack"),True,(0,0,0))
				hpstat=timesNewRomanFont.render(str(list1[num][2]),True,(0,0,0))
				hptext=timesNewRomanFont.render(str("HP"),True,(0,0,0))
				defencestat=timesNewRomanFont.render(str(list1[num][4]),True,(0,0,0))
				defencetext=timesNewRomanFont.render(str("Defence"),True,(0,0,0))
				magicstat=timesNewRomanFont.render(str(list1[num][5]),True,(0,0,0))
				magictext=timesNewRomanFont.render(str("Magic"),True,(0,0,0))
				magicdefstat=timesNewRomanFont.render(str(list1[num][6]),True,(0,0,0))
				magiddeftext=timesNewRomanFont.render(str("Magic Resitance"),True,(0,0,0))
				manastat=timesNewRomanFont.render(str(list1[num][7]),True,(0,0,0))
				manaText=timesNewRomanFont.render(str("Mana"),True,(0,0,0))
				screen.blit(uparrow,(75,HEIGHT//2-HEIGHT//7))
				screen.blit(downarrow,(75,HEIGHT//2))
				draw.rect(screen,(150,220,255),levelattackRect,0)
				draw.rect(screen,(150,220,255),leveldefenseRect,0)
				draw.rect(screen,(150,220,255),levelmagicRect,0)
				draw.rect(screen,(150,220,255),levelmagicdefenseRect,0)
				draw.rect(screen,(150,220,255),levelhealthRect,0)
				draw.rect(screen,(150,220,255),levelmanaRect,0)
				screen.blit(attacktext,(335,160))
				screen.blit(defencetext,(595,160))
				screen.blit(magictext,(330,310))
				screen.blit(magiddeftext,(560,310))
				screen.blit(hptext,(355,460))
				screen.blit(manaText,(610,460))
				# will change the colour of each rectangle when it is selected
				if selected=="attack":
					draw.rect(screen,(140, 82, 150),levelattackRect,0)	
					upgrade=list1[num][3]		
				elif selected=="defense":
					draw.rect(screen,(140, 82, 150),leveldefenseRect,0)
					upgrade=list1[num][4]
				elif selected=="magic":
					draw.rect(screen,(140, 82, 150),levelmagicRect,0)
					upgrade=list1[num][5]
				elif selected=="magicdefense":
					draw.rect(screen,(140, 82, 150),levelmagicdefenseRect,0)
					upgrade=list1[num][6]
				elif selected=="health":
					draw.rect(screen,(140, 82, 150),levelhealthRect,0)
					upgrade=list1[num][2]
				elif selected=="mana":
					draw.rect(screen,(140, 82, 150),levelmanaRect,0)
					upgrade=list1[num][7]
				# will change arrow colours	
				if arrowselected=="up":
					screen.blit(uparrowclicked,(75,HEIGHT//2-HEIGHT//7))
				elif arrowselected=="down":
					screen.blit(downarrowclicked,(75,HEIGHT//2))
				screen.blit(attackstat,(365,210))
				screen.blit(defencestat,(640,210))
				screen.blit(magicstat,(365,360))
				screen.blit(magicdefstat,(640,360))
				screen.blit(hpstat,(365,510))
				screen.blit(manastat,(640,510))
				display.flip()
				print(selecnum, selected)	
	display.flip() 
	quit()		
def display_main_menu():
	# displays the main menu
	global screen, size, WIDTH, HEIGHT 
	menu = transform.scale(image.load("img/menu/main_menu.png").convert_alpha(), (200, 500))
	screen.blit(screen_back, (0,0))
	screen.blit(menu, (100,50))
	# arrow_pos will be referring to the index of options, it will be able to tell which option is being selected
	arrow_pos = 0
	options = ['Inventory', 'Statistics', 'Quests', 'Save', "Options", 'Exit', 'Quit']
	main = True
	while main:
		for evt in event.get():  
			if evt.type == KEYUP:
				# these key presses are for sound effects
				if evt.key == K_ESCAPE or evt.key == K_z:
					music(2, sound_selection[1], 0)
					return
				if evt.key == K_DOWN:	
					music(2, sound_selection[1], 0)
					arrow_pos += 1
				if evt.key == K_UP:
					music(2, sound_selection[1], 0)
					arrow_pos -= 1
				if evt.key == K_SPACE and len(options) > 0:
					music(2, sound_selection[1], 0)
					if options[arrow_pos] == 'Inventory':
						# calls the inventory function
						InventoryDisplay(currChar, 0, inventory)
					elif options[arrow_pos] == 'Exit':
						# exits the function
						return
					elif options[arrow_pos] == 'Quit':
						# will run the save function first and then will close the program
						save_menu('Quit')
						global quit_stat
						quit_stat = 'quit'
						return
					elif options[arrow_pos] == 'Save':
						# This will be called when the player just wants to save their progress and continue playing
						save_menu('')
					elif options[arrow_pos] == 'Quests':
						display_quest()	
					elif options[arrow_pos] == 'Options':
						# This will call the options menu and will also update whatever settings are changed
						global selections
						opts = options_menu(selections)
						selections = opts
						for i in range(len(opts)):
							if i == 0:
								if opts[i] == 'Windowed':
									screen = display.set_mode(size)
								else:	
									screen = display.set_mode(size, FULLSCREEN)
									WIDTH, HEIGHT = size = (min(1920,display.Info().current_w), min(1080,display.Info().current_h))
							elif i == 1:
								if opts[i] == 'Off':
									channels[0].set_volume(0)
								else:
									channels[0].set_volume(.1)
							elif i == 2:
								if opts[i] == 'Off':
									channels[1].set_volume(0)	
									channels[2].set_volume(0)	
								else:
									channels[1].set_volume(.5)	
									channels[2].set_volume(.5)
		# count is for how the coordinates of what I blit will be.							
		count = 0					
		screen.blit(screen_back, (0,0))
		screen.blit(menu, (100,50))
		for i in range(len(options)):
			count += 1
			optionName = medievalFont.render(options[i], True, (0,0,0))
			# limits the scrolling
			if arrow_pos == len(options):
				arrow_pos -= 1
			if arrow_pos < 0:
				arrow_pos += 1	
			draw.circle(screen, (0,0,0), (110,75 + 30 * arrow_pos), 6) # draws the selection circle
			screen.blit(optionName, (120, 30 + 30 * count)) # draws the animation
		mx, my = mouse.get_pos()
		display.flip()
def options_menu(selections):
	back = transform.scale(image.load("img/menu/parchment.png").convert_alpha(), (WIDTH, HEIGHT))		
	# sets default positions for the arrow pos and selection
	arrow_pos = 1
	select_pos = 1
	# defines the options and their toggles
	options = ['Screen', 'BGM', "SE"]
	toggles = [['Windowed', 'Fullscreen'], ["On", 'Off'], ["On", 'Off']]
	selected = selections # this will load in the saved options
	selecting = False # this will check if you are selecting one of the toggle options
	running = True
	while running:
		for evt in event.get():
			if evt.type == QUIT:
				return
			if evt.type == KEYUP:
				if evt.key == K_ESCAPE or evt.key == K_z:
					music(2, sound_selection[1], 0) # loads in the sound effects
					return selected # returns all the changed options or not changed options
				if evt.key == K_DOWN:
					music(2, sound_selection[1], 0)
					# this will change the selections and the arrow_pos
					if not selecting:
						arrow_pos += 1
					else:
						select_pos += 1
				if evt.key == K_UP:
					# this will change the selections and the arrow_pos
					music(2, sound_selection[1], 0)
					if not selecting:
						arrow_pos -= 1
					else:
						select_pos -= 1	
				if evt.key == K_SPACE:
					music(2, sound_selection[1], 0)
					# this will fetch the selected option
					if selecting:
						selected[arrow_pos - 1] = toggles[arrow_pos - 1][select_pos - 1]
					else:
						select_pos = 1	
					selecting = not selecting # this will switch then status of selecting bool
		mx, my = mouse.get_pos()		
		screen.blit(back, (0,0))
		# the following parameters sets the maximum boundaries for the positions
		if arrow_pos > 3:
			arrow_pos = 3
		if arrow_pos < 1:
			arrow_pos = 1
		if select_pos < 1:
			select_pos = 1	
		if select_pos > 2:
			select_pos = 2	
		# the reset is just playing with positions and blitting items on to the screen	
		# basically the circle position is set on to the option you are toggling and
		# when you press space, another circle will appear leaving the first circle at the option name
		# then you will be able to change the toggles
		current_settings = medievalFont.render('Current Settings:', True, (0,0,0))	
		screen.blit(current_settings, (460, 30))	
		for i in range(len(selected)):
			setting = medievalFont.render(options[i] + ': ' + selected[i], True, (0,0,0))
			screen.blit(setting, (460, 60 + 30 * i))
		draw.circle(screen, (0,0,0), (45, 45 + 135 * (arrow_pos - 1)), 5)
		if selecting:
			draw.circle(screen, (0,0,0), (110, 40 + (135 * (arrow_pos - 1)) + 50 * select_pos), 5)
		for i in range(len(options)):
			optionName = medievalFont.render(options[i] + ':', True, (0,0,0))
			screen.blit(optionName, (50, 30 + i * 135))
			for n in range(len(toggles[i])):
				toggleName = medievalFont.render(toggles[i][n], True, (0,0,0))
				screen.blit(toggleName, (125, (80 + i * 135) + 50 * n))
		display.flip()			
def save_menu(purp):
	menu = transform.scale(image.load("img/menu/main_menu_rotated.png").convert_alpha(), (500, 200))
	y = 45 # sets default position for the circle / select icon thing
	arrow_pos = 0 # for selection
	mode = 'save_select' # what mode you are using whether
	saving = True
	while saving:
		for evt in event.get():  
			if evt.type == KEYUP:
				if evt.key == K_ESCAPE:
					music(2, sound_selection[1], 0)
					saving = False
					return
				if evt.key == K_DOWN:	
					music(2, sound_selection[1], 0)
					y = 75
				if evt.key == K_UP:
					music(2, sound_selection[1], 0)
					y = 45
				if evt.key == K_SPACE:
					music(2, sound_selection[1], 0)
					# according to the y, the game will either save or will just quit and close
					if y == 45:
						mode = 'saving'
					if y == 75:
						saving = False
						return	
		if mode == 'save_select':	
			# this will allow the player to select whether or not the player wants to save			
			# and depending on the purp variable it will ask you if you want to save before quitting
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
			# if the player decides to save, it will show a little "animation"
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
	selectedRect = Rect(0,0,800,200) # this will highlight the quest that the player is looking at
	display_range = 0 # this will control the scrolling of the quests of there are more than 3
	quest_dict = {} # This will store all the quests
	display_txt = [] # this will hold the text to be displayed on screen corresponding with quest_dict

	prog_dict = {} # this will record your progress that you have made to complete the quest
	prog_txt = [] # this will store the progress text corresponding with the prog_dict
	
	rec_dict = {} # this will determine whether or not the player received the item for
				  # completing the quest
	rec_txt = [] # this is the text that corresponds with the rec_dict
	# this right here will check the quest_completion to display on screen the progress of your quest
	# it will display on screen your progress and will tell the steps to do so and who to go to
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
	# renders all the text that will be displayed on screen			
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
				if evt.key == K_ESCAPE or evt.key == K_z:
					music(2, sound_selection[1], 0)
					quest_thang = False
					return	
				if evt.key == K_UP:
					music(2, sound_selection[1], 0)
					# will set restrictions and will allow the user to move their selections box
					if selectedRect.y == 0 and display_range > 0:
						display_range -= 1
					else:
						if selectedRect.y > 0: 
							selectedRect.y -= 200
				if evt.key == K_DOWN:
					music(2, sound_selection[1], 0)
					# controls scrolling and will also allow you to change the display_range for scrolling
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
		# sets restrictions for the display_range and the blitting of the information on the screen
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
	global quest_completion # I global quest_completion just to add the quests from the quest npcs
	for tile_object in fname.objects:
		# basically this just goes through the tmx file and it reads all the object names. According to the object name,
		# these if statements will do different things. For example the wall objects will call the wall class and so on and so forth
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
			# for every new quest npc i add the quest will be added to quest completion with all the requirements
			if tile_object.Name not in quest_completion:
				quest_completion[tile_object.Name] = [tile_object.Quest, tile_object.Key, tile_object.Goal, tile_object.Complete, tile_object.Received]
			npcs.add(quest_npc)
def levelSelect(lvl, chests, walls, portals):
	# the first part here basically goes through all my sprite group =s and deletes / ills all sprites from them
	kill = [chests, walls, portals, clerks, npcs]
	for i in kill:
		for n in i:
			n.kill()	
	# according to the level attached to the portal I hit, the lvl will assign a certain map to fname and tops
	# which will be loaded later using the MapLoad function.		
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
	elif lvl == '6':
		fname = load_pygame('Maps/house2.tmx')	
		tops = load_pygame("Maps/blank.tmx")
	elif lvl == '7':
		fname = load_pygame('Maps/STORE2.tmx')	
		tops = load_pygame("Maps/blank.tmx")
	elif lvl == '8':
		fname = load_pygame('Maps/goodhouse1.tmx')	
		tops = load_pygame("Maps/blank.tmx")
	return fname, tops		
def MapLoad(Map_Name):
	for layer in Map_Name.visible_layers: # this loop goes through all the visivle layers in the map
		if isinstance(layer, TiledTileLayer): # if the layer and the tiled layer exist then it will go throught with this statement
			for x, y, gid in layer: # this for loop gets the x, y and the global identification
				tile = Map_Name.get_tile_image_by_gid(gid) # then theis command will fetch the corresponding image according to the gif
				if tile: # if the tile is not empty then the tile will be blit on to the screen
					# the reason that the x_diff and y_diff is added to x and y respectively is because the offset of the map is what changes
					# the character stays on one spot on the screen and the map moves
					screen.blit(tile, ((x * Map_Name.tilewidth) + x_diff, (y * Map_Name.tileheight) + y_diff))
def InventoryDisplay(current_Character, num, inventory):
	# this function is used for creating the strings that are displayed on screen for the incventory menu and the item received pop up
	global inv_dict # this makes the 
	inv = '' # inv stores the series of strings of the item names and there numbers next to them
	inventory = inventory # inventory lisst is assigned to another variable or the items received 
	if num != 5:
		for i in inventory: # this will go through the list
			number = 0 # This will count the number of recurring items to count the total number of them in the list
			for n in inventory:# once you have your item then I run through the list again and add to count the matching ones
				if i == n:
					number += 1
			inv += i + ' ' + 'x' + str(number) + ', ' # this creates a string seperated by a comma inbetween
		split = inv.split(', ') # this will split the list by the commas now
		del split[split.index('')] # this will delete the empty space within the list
		for i in split: # now I loop through the list
			s1 = i.split(' x') # i split it by ' x' to get the name of the item
			if s1[0] not in inventory: # if the item is not in the inventory then the item will be added to inv_dict which will
									   # allow me to blit the items in the inventory menu in the same order to keep scrolling working
				inv_dict[s1[0]] = ''
			else:
				inv_dict[s1[0]] = i
	else:
		# this else statement basically says that this is for the items received in the alert_display function
		split = inventory.split(' // ') # this will take the string and split all the items  
		for i in split: # this will now go through the list
			number = 0 # this is a counter for reocurrences
			for n in split: # this will now count the reocurrences and add them to count
				if i == n:
					number += 1
			if i + ' ' + 'x' + str(number) not in inv: # this will add it to inv as long as it is not in there already		
				inv += i + ' ' + 'x' + str(number) + ' // ' # i dont delete ' // ' because it is just a blank being blit on the screen
	# this num variable is used to call a certain function or to return a variable
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
	inv = [] # this is what the string items will be added to
	display_range = 0 # this will be used for scrolling
	tmp_inv = [] # this is the list that will only store from items from the inventory according to the display_range 
	counter = 0 # counter is for the indexing of the full list
	display_bool = False # This will be used to show the effect of whatever item you use
	Inventory = Inventory # and inventory list is assigned to inventory variable
	# this will go through the list and add to inv the items as long as they aren't empty
	for i in Inventory:
		if inv_dict[i] != '':
			inv.append(i)
	while inventory_open:
		for evt in event.get():  
			if evt.type == KEYUP:
				# this is used for sound effects
				if evt.key == K_ESCAPE or evt.key == K_i or evt.key == K_z and mode != 'sell':
					music(2, sound_selection[1], 0)
					# if the mode is sell it will return c to open the buying menu and will close this menu
					if mode == "sell":
						global c
						c = 'NULL'
						return c
					inventory_open = False
					# if not sell then it will just exit out
					return
				if evt.key == K_SPACE and len(inv) > 0:
					# for sound effect
					music(2, sound_selection[1], 0)
			if evt.type == KEYDOWN:
				if evt.key == K_DOWN:
					music(2, sound_selection[1], 0)
					# this is for controlling the display range and the arrow pos
					if arrow_pos == 16 and display_range < 16:	
						if display_range < len(inv) - 17:
							display_range += 1
					if arrow_pos < 16:
						arrow_pos += 1
						# counter also increases
					if counter < len(inv):	
						counter += 1
				if evt.key == K_UP:
					music(2, sound_selection[1], 0)
					if arrow_pos == 0 and display_range > 0:
						display_range -= 1	
					if arrow_pos > 0:
						arrow_pos -= 1
					if counter > 0:	
						counter -= 1
				if evt.key == K_SPACE and len(inv) > 0:
					if mode == 'inventory':
						# if you press space and the mode is inventory then string will be split
						x = inv_dict[inv[counter]] # x will be the item in the full list according to the counter
						y = x.split(" x")
						if y[1] == '1': # if a certain item is at 1 total items then the item will be erased or made blank
							inv_dict[y[0]] = '' 
						for i in HP_items: # this will go through the HP_items list and it will get the hp a certain item adds
										   # to your characters health. It will also create a text render with the effects
							i = i.split(' // ')
							if y[0] in i:
								print("HP +", i[1])
								mes = timesNewRomanFont.render(i[1] + ' added to HP!', True, (0,0,0))
								mes2 = medievalFont.render('', True, (0,0,0))
								display_bool = True
								HP_Change(i[1])
						del inv[counter] # this will delete the item so that it can be updated
						del inventory[inventory.index(y[0])] # this will delete the item from the inventory list
						tmp = InventoryDisplay(current_Character, 1, inventory) # this will create the list again just like it was 
																				# done above but instead to update it.
						inv = []
						for i in tmp:
							if inv_dict[i] != '':
								inv.append(i)
					if mode == 'sell':
						# if you press space on an item and you are selling
						global gold
						# it will get the name of the item the same way it does above
						x = inv_dict[inv[counter]] 
						y = x.split(" x")
						if y[1] == '1':
							inv_dict[y[0]] = ''
						# I did a try except statement be cause I was too lazy to create an if statement checking if the item was in the item_value dictionary	
						try:
							# this would add to gold the amount that the item was worth
							gold += load_dict()[3][y[0]]
							mes = medievalFont.render("You have gained " + str(load_dict()[3][y[0]]) + " gold!!", True, (0,0,0))
							mes2 = medievalFont.render("Now you have " + str(gold) + " gold in total!!", True, (0,0,0))
						except:
							# if the item did not have a predetermined selling value then it will automatically give you 100 gold for it
							gold += 100
							mes = medievalFont.render("You have gained " + str(100) + " gold!!", True, (0,0,0))
							mes2 = medievalFont.render("Now you have " + str(100) + " gold in total!!", True, (0,0,0))
						del inv[counter]	
						del inventory[inventory.index(y[0])]
						tmp = InventoryDisplay(current_Character, 1, inventory)
						inv = []
						for i in tmp:
							if inv_dict[i] != '':
								inv.append(i)
						display_bool = True		
					if mode == 'battle':
						global used
						# if the mode is battle it will only be able to use items for hp
						x = inv_dict[inv[counter]] # x will be the item in the full list according to the counter
						y = x.split(" x")
						if y[1] == '1': # if a certain item is at 1 total items then the item will be erased or made blank
							inv_dict[y[0]] = '' 
						for i in HP_items: # this will go through the HP_items list and it will get the hp a certain item adds
										   # to your characters health. It will also create a text render with the effects
							i = i.split(' // ')
							if y[0] in i:
								HP_Change(i[1])
						del inv[counter]	
						del inventory[inventory.index(y[0])]
						used = True
						return
		count = 0 # count is to manipulate the item positions on screen			
		screen.blit(menu_base, (0,0))
		tmp_inv = [] # this variable will store the items that are displayed on screen
		if display_bool:
			# this will display the effects of an item if they even have any
			screen.blit(mes, (30,255))
			screen.blit(mes2, (30,285))
		for i in range(display_range, len(inv)):
			# this will blit from the display range to the length of inv
			tmp_inv.append(inv[i])
		# this would set restrictions on arrow_pos and the display_range 	
		if arrow_pos > len(inv):
			arrow_pos = len(inv)
		if counter >= len(inv) - 1:	
			counter = len(inv) - 1
		# whenever you see -17 it is because there are only 17 objects allowed on screen at a time
		# when the 17 objects are added they are treated as null. Meaning that they are treated as 
		# if they don't exist. 	
		if len(inv) > 16:	
			if len(inv) - 17 < display_range:
				display_range = len(inv) - 17
		for i in range(len(tmp_inv)):
			# basically blitting the items on screen while going through the tmp_inv 
			if i <= 16:
				count += 1
				ItemName = medievalFont.render(inv_dict[tmp_inv[i]], True, (0,0,0))
				screen.blit(ItemName, (470, 20 + 30 * count))
				# more restrictiions
				if arrow_pos == len(inv):
					arrow_pos -= 1
				if arrow_pos < 0:
					arrow_pos += 1	
				# it draws the circle that is highlighting the item to be selected	
				draw.circle(screen, (0,0,0), (455,65 + 30 * arrow_pos), 6)
		# this is responsible for selecting the image of the current character that is being blit on screen		
		if current_Character == "Crow":
			screen.blit(transform.scale(image.load("img/faces/crow.png").convert_alpha(), (130,185)),(30,35))			
		elif current_Character == "Raven":
			screen.blit(transform.scale(image.load("img/faces/raven.png").convert_alpha(), (130,185)),(30,35))			
		display.flip()
	arrow_pos = 0
def alert_display(item, mode):
	# alert_display's main purpose is to tell the player which items they have required
	# either from npcs or chests
	item = item # item is the string of items received
	n = 0 # n is to limit the loop to running only one time
	text_y = 60 # this is the initial position of the text
	alert = True
	while alert:
		for evt in event.get():  
			if evt.type == QUIT: 
				alert = False
			if evt.type == KEYDOWN:
				# again, for sound effects
				if evt.key == K_z:
					alert = False
					return music(2, sound_selection[1], 0)
				if evt.key == K_ESCAPE:
					alert = False
					return music(2, sound_selection[1], 0)
		kp = key.get_pressed()
		if n == 0:
			screen.blit(dialogue_box, (0,0))
			screen.blit(timesNewRomanFont.render('You have received the following items:', True, (150,150,150)), (45, 30))
			split = item.split(' // ') # this splits the item string
			if '' in split: # this will delete the empty space and will delete it
				del split[split.index('')]
			for i in range(len(split)): # this will blit the items received on to the screen
				screen.blit(timesNewRomanFont.render(split[i], True, (150,150,150)), (45, text_y + 30 * i))
				display.flip()
			n = 1 # stops the loop from running again
		display.flip() 
	quit()
def HP_Change(HP):
	global stats
	# adds the number given to the current character's HP
	print(HP)
	if currChar == 'Crow':
		stats[0][2] += int(HP)
		if stats[0][2] > 100:
			stats[0][2] = 100
	if currChar == 'Raven':
		stats[1][2] += int(HP)
		if stats[1][2] > 100:
			stats[1][2] = 100
def FIGHTANIMATION(surf, enemy, battleBack):
	# fight animation blits the background and the enemy for battle
	surf.blit(battleBack,(0,0))
	rect = enemy.get_rect()
	# the enemy is blit so that is centered on the screen
	surf.blit(enemy,(WIDTH / 2 - rect.width / 2, HEIGHT / 2 - rect.height / 2))	
def save_dict():
	# these are dictionaries which save the progress of the players
	# it will also save other native information of the game
	prog_data = {"lvl": lvl,
				 "Coords": [x_diff, y_diff],
				 "Chests": openedChests,
				 "inv": inventory,
				 "Gold": gold,
				 "npc_items": npc_item,
				 "Current Charachter": currChar,
				 "Quests": quest_completion,
				 "inv_dict": inv_dict,
				 "settings": selections}
	item_value = {'Potion': 75,
				  'Elixer': 50,
				  'Sword': 25,
				  'Shield': 25}  	 			  
	crow_data = {"Stats": stats[0]}	  	 
	raven_data = {"Stats": stats[1]}	  	 
	# I use pickle to dump the encrypted dictionaries into a .dat file
	p.dump(prog_data, open("prog.dat", "wb"))
	p.dump(crow_data, open("crow_stats.dat", "wb"))	
	p.dump(raven_data, open("raven_stats.dat", 'wb'))
	p.dump(item_value, open("item_value.dat", 'wb'))
crowWalkForward, crowWalkDown, crowWalkRight, crowWalkLeft = [], [], [], [] # these are for player animations
ravenWalkForward, ravenWalkDown, ravenWalkRight, ravenWalkLeft = [], [], [], []
cf, cd, cr, cl = crowWalkForward, crowWalkDown, crowWalkRight, crowWalkLeft
cm = image.load("SPRITES/Crow/Walk/Up/0.png").convert_alpha()
chest_open = []
############################################### ATTACK ANIMATIONS ###############################################
# the following are the attack animations for each of the characters
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
for i in range(45):
	RavenC.append(image.load("SPRITES/Raven Attacks/RavenC/%i.png" % i).convert_alpha())
for i in range(16):
	RavenX.append(image.load("SPRITES/Raven Attacks/RavenX/%i.png" % i).convert_alpha())
for i in range(21):
	RavenZ.append(image.load("SPRITES/Raven Attacks/RavenZ/%i.png" % i).convert_alpha())	
############################################### ATTACK ANIMATIONS ###############################################
############################################ LOADING MAP AND SPRITES ############################################
# this loads the sprite animation for both the characters ; their walking animations
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
# for i in range(24):
	# battleAnimation.append(transform.scale(image.load("gif/%i.png" % i),(800,600)).convert_alpha())
############################################ LOADING MAP AND SPRITES ############################################
class Player(sprite.Sprite):
	def __init__(self, x, y):
		sprite.Sprite.__init__(self)
		self.image = cm # cm is the animation of the character
		self.x, self.y = x, y # x and y variable assigned
		self.rect = self.image.get_rect() # creates the rect
		# self.rect.midbottom = (self.x,self.y) # sets the midbottom
	def update(self):
		self.image = cm # this will update the image of the character to create animation
		self.rect = self.image.get_rect() # it is always creating the rect because the size
										  # of the image is always changing
		self.rect.x, self.rect.y = self.x, self.y - self.rect.height # sets the rect.x and rect.y
class Obstacle(sprite.Sprite):
	def __init__(self, x, y, w, h):
		sprite.Sprite.__init__(self)
		self.rect = Rect(x, y, w, h) # the x,y,w,h are passed in to make the rect objects for the walls
		self.x, self.y = x, y 
	def update(self):
		self.rect.topleft = self.x + x_diff, self.y + y_diff # this updates the position according to the offsets for the map
class Portal(sprite.Sprite):
	def __init__(self, x, y, w, h, location, xd, yd):
		sprite.Sprite.__init__(self)
		self.rect = Rect(x, y, w, h) # creates rect objects for portalllllls
		self.x, self.y = x, y
		self.xd, self.yd = xd, yd # this is for the destination of the player on the new map
		self.type = location # this is for the map that the player will be teleported to
	def update(self):
		self.rect.topleft = self.x + x_diff, self.y + y_diff		
class NPC(sprite.Sprite):
	def __init__(self, x, y, importance, speech, item, name, width, height):
		sprite.Sprite.__init__(self)
		global inv_dict
		self.type = importance # nothing to do with importance, just to select sprite
		self.speech = speech # this is the list that stores what the npc will say to you
		self.item = item # this is the item that the npc could give to you
		self.name = name # this is the name of the NPC
		self.width, self.height = width, height
		if self.type != '00': # for inanimate objects I have a blank picture that will be strecthed to the size of the npc box in the tmx file
			self.image = image.load("img/NPCs/" + self.type + ".png").convert_alpha()
			self.rect = self.image.get_rect() # this will create the rect object
		else:
			# essentially the same thing as above except there is an actual image on the screen
			self.image = image.load("img/NPCs/" + self.type + ".png").convert_alpha()
			self.image = transform.scale(self.image, (int(self.width), int(self.height)))
			self.rect = self.image.get_rect()
		self.interact = False # this will become true if the player talks with the NPC
		self.display_text = False # this will be for thw while loop for displaying text
		self.x, self.y = x, y
	def update(self):
		self.rect.topleft = self.x + x_diff, self.y + y_diff # updating according to offset of map
	def display_speech(self, interact, display_text):
		self.interact = interact # this willbe true if the player actually trys to talk to npc
		self.display_text = display_text # this will be true 
		self.prog = 0 # this is the progress for each different "slide" of text
		self.sent = '' # this will be the text being displayed on screen
		self.n = 0 # To stop it from running infinitely
		self.s = 100 # It causes a buffering effect for the text when a new line is started as
					 # the position of the text would start more to the left and not be centered
		self.text_y = 60 # sets default position of the text to start
		for i in quest_completion:
			# This will check if the character is in a certain character is involved in a quest or not
			# if it is it will set it tp true and will continue the players quest progression
			if quest_completion[i][2] == self.name and quest_completion[i][3] == 'false' and quest_completion[i][0] == 'true':
				quest_completion[i][3] = 'true'
		if self.interact:
			while self.display_text:
				for evt in event.get():  
					if evt.type == QUIT: 
						self.display_text = False
						self.disp = False
					if evt.type == KEYUP:
						# sound effects
						if evt.key == K_SPACE:	
							music(2, sound_selection[1], 0)
						if evt.key == K_z and self.prog == len(self.split) - 1:	
							music(2, sound_selection[1], 0)
				kp = key.get_pressed()
				screen.blit(dialogue_box, (0,0))
				# this will put the npcs name on screen
				screen.blit(timesNewRomanFont.render(self.name + ':', True, (150,150,150)), (45,30))
				self.split = self.speech[0].split(' // ') # this will get the seperate "slides" of text and will save them in a list
				if kp[K_SPACE]:
					if self.prog < len(self.split) - 1 and self.n == 1:
						# this will continue to blit to the next slide and will allow the loop to show text on the screen
						self.prog += 1	
						self.n = 0
						self.sent = ''
						self.text_y = 60
				if kp[K_z] and self.prog == len(self.split) - 1:
					if self.item != 'NULL' and self.name not in npc_item:
						# if the npc is holding an item and the npc isn't in npc_item
						# then the item will be given to us and will call the alert_display function through the InventoryDisplay function
						self.item_split = self.item.split(' // ')
						for i in self.item_split:
							inventory.append(i)
							if i not in inv_dict:
								inv_dict[i] = ''
						npc_item[self.name] = self.name
						InventoryDisplay(currChar, 5, self.item)
					# ends the loop	
					self.display_text = False
					self.interact = False		
				if self.n == 0:
					for i in self.split[self.prog]:
						# this will loop through the string for the npc
						self.sent += i # this will add it to self.sent and that will be blit on screen
						if i == '#': # this is for the text to start another line
							self.sent = ''
							self.s = 0	
							self.text_y += 30 # increases position
							time.wait(650) # adds a delay
						if self.s <= 1:
							self.s += 1 # this will be like a buffer
							self.sent = ''	
						else:	
							self.s = 100
						# the below blits the letters in a one by one animation	
						screen.blit(timesNewRomanFont.render(self.sent, True, (150,150,150)), (45,self.text_y))
						display.flip()
						time.wait(35)
					self.n = 1	

class Quest_NPC(sprite.Sprite):
	def __init__(self, x, y, importance, speech, item, name, quest):
		sprite.Sprite.__init__(self)
		global inv_dict
		self.type = importance # this is for character sprite
		self.speech = speech # this is for speech of the character
		self.item = item # this is for the item(s) that you are going to be given
		self.name = name # this is the name of the character
		self.quest = quest # this is the quest the npc wants you to do
		self.quest_speech = 0 # this is the index for the list of speech for each step of the quest process
		self.image = image.load("img/NPCs/" + self.type + ".png").convert_alpha() # this is the image
		self.rect = self.image.get_rect() # this creates the rect based on the image
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
			# this will check if you have already acquired this quest and it will go to the next part of the text
			self.quest_speech = 1
		if 	quest_completion[self.name][3] == 'true':
			# this will check if you have completed the objective of the quest or not
			# (Not to be confused with completing the quest)
			quest_completion[self.name][4] = 'true' # this sets the quest itself to be complete
			self.quest_speech = 2 # goes to the next stage of text
		if self.interact:
			while self.display_text:
				for evt in event.get():  
					if evt.type == QUIT: 
						self.display_text = False
						self.disp = False
					if evt.type == KEYUP:
						if evt.key == K_SPACE:
							music(2, sound_selection[1], 0)
						if evt.key == K_z and self.prog == len(self.split) - 1:	
							music(2, sound_selection[1], 0)
				mx,my=mouse.get_pos()
				mb=mouse.get_pressed()
				kp = key.get_pressed()
				screen.blit(dialogue_box, (0,0))
				screen.blit(timesNewRomanFont.render(self.name + ':', True, (150,150,150)), (45,30))
				self.split = self.speech[self.quest_speech].split(' // ')
				# this is the same as in the NPC class
				if kp[K_SPACE]:
					if self.prog < len(self.split) - 1 and self.n == 1:
						if self.prog < len(self.split) - 1:
							self.prog += 1	
							self.n = 0
							self.sent = ''
							self.text_y = 60
				if kp[K_z] and self.prog == len(self.split) - 1:
					# the main difference is that this will also check if the quest is completed
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
						time.wait(35)
					self.n = 1

class Store_Clerk(sprite.Sprite):
	def __init__(self, x, y, tier):
		sprite.Sprite.__init__(self)
		self.tier = tier # this will determine which items will be sold
		# the following are the items that can be sold
		self.s1 = ['Potion' + " " * 88 + '100', 'Elixer' + " " * 88 + '75', 'Sword' + " " * 88 + '50', 'Shield' + " " * 88 + '50']
		self.s2 = ['Potion' + " " * 88 + '100', 'Elixer' + " " * 88 + '75', 'Sword' + " " * 88 + '50', 'Shield' + " " * 88 + '50']
		self.s3 = ['Potion' + " " * 88 + '100', 'Elixer' + " " * 88 + '75', 'Sword' + " " * 88 + '50', 'Shield' + " " * 88 + '50']
		self.s4 = ['Potion' + " " * 88 + '100', 'Elixer' + " " * 88 + '75', 'Sword' + " " * 88 + '50', 'Shield' + " " * 88 + '50']
		# the image of the store clerk according to type
		self.image = image.load("img/Store Clerks/Clerk" + self.tier + ".png").convert_alpha()
		self.rect = self.image.get_rect() # creates the rect
		self.x, self.y = x, y
		self.interact = False
		self.back = transform.scale(image.load("img/menu/parchment.png").convert_alpha(), (WIDTH, HEIGHT))
		self.event = "buy" # to see if you are buying or selling
	def update(self):
		self.rect.topleft = self.x + x_diff, self.y + y_diff	
	def open_store(self):
		self.selection = self.s1
		self.display = False
		# the tier will determine what items you sell
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
				if evt.type == KEYUP:
					# sound effects
					if evt.key == K_ESCAPE or evt.key == K_z:
						music(2, sound_selection[1], 0)
					if evt.key == K_UP:
						music(2, sound_selection[1], 0)
					if evt.key == K_DOWN:
						music(2, sound_selection[1], 0)
					if evt.key == K_SPACE:
						music(2, sound_selection[1], 0)
				if evt.type == KEYDOWN:
					if evt.key == K_ESCAPE or evt.key == K_z:
						self.interact = False
						return
					if evt.key == K_UP:
						arrow_pos -= 1
					if evt.key == K_DOWN:
						arrow_pos += 1		
					if evt.key == K_SPACE:
						if self.event == 'buy' or self.event == 'NULL':
							# basically if the player hits space on an item it will split it to get the value of the item and the item name
							# then it will check wheter or not you have enough gold. It will create a message to be displayed on screen. 
							x = self.selection[arrow_pos]
							y = x.split(" " * 88)
							if int(y[1]) <= gold:
								mes = medievalFont.render("You have bought a " + y[0] + ' for ' + y[1] + '!! You have ' + str(gold) + ' gold left!!', True, (0,0,0))
								inventory.append(y[0])
								gold -= int(y[1])
							if int(y[1]) > gold:
								mes = medievalFont.render("You don't have enough money!!", True, (0,0,0))
							self.display = True	
					if evt.key == K_b:
						self.event = 'buy'		
					if evt.key == K_s:
						self.event = 'sell'	
			if self.event == 'buy' or self.event == 'NULL':			
				screen.blit(self.back, (0,0))
				ShopName = fancyFont.render("The Item Shop", True, (0,0,0))
				Gold = medievalFont.render('Gold: ' + str(gold), True, (0,0,0))
				screen.blit(ShopName, (100,0))
				screen.blit(Gold, (575,0))
				if self.display:
					# this will display the message on screen
					screen.blit(mes, (55,275))
				for i in range(len(self.selection)):
					# arrow pos restrictions
					if arrow_pos == len(self.selection):
						arrow_pos -= 1
					if arrow_pos < 0:
						arrow_pos += 1	
					# draws selection circle and items	
					draw.circle(screen, (0,0,0), (100, 105 + 30 * arrow_pos), 3)
					ItemName = medievalFont.render(self.selection[i], True, (0,0,0))			
					screen.blit(ItemName, (105, 90 + 30 * i))
			if self.event == 'sell':
				# this will go to your inventory and will allow you to sell your items
				InventoryDisplay(currChar, 2, inventory)
				self.event = c
			display.flip()	

class Chest(sprite.Sprite):
	def __init__(self, x, y, w, h, tier, name, item):
		sprite.Sprite.__init__(self)
		self.tier = tier # the tier is used for what sprite is going to be used for the chest
		self.name = name # the name of the chest is to check if a certain chest has been opened or not
		self.opened = False # this checks if the chest is being interacted with or not
		self.item = item # the item is the item or items that the chest gives you
		# this stores the images within a list ( for open and closed )
		self.images = [image.load("SPRITES/Chest/Tier" + str(self.tier) + "/0.png"),
					   image.load("SPRITES/Chest/Tier" + str(self.tier) + "/1.png")]
		# this assigns a variable called prev_image that save the image and self.image has the closed chest assigned to it			   
		self.prev_image = self.image = self.images[0]
		self.rect = Rect(x, y, w, h) # the rect is created
		if self.name in openedChests:
			# this will check if the chest has been opened up before, if it has the opened chest sprite will be applied here 
			self.image = self.images[1] 
		self.x, self.y = x, y # sets the x and y position of the chest
	def update(self):
		global chest_open
		self.rect.topleft = self.x + x_diff, self.y + y_diff # this update the position of the chest according to the x and y diff
		if self.image == self.prev_image and self.opened and kp[K_SPACE]: # this will check if the images are both the same and the player has pressed space
			music(2, sound_selection[1], 0) # sound effect
			self.image = self.images[1] # changes the image to opened chest image
			self.split = self.item.split(' // ') # this will split all the items into a list
			openedChests.append(self.name) # this will append the name of this chest to a list which stores all opened chests
			for i in self.split:
				# this will go through the split list and will append all the items to the inventory list
				inventory.append(i)
			InventoryDisplay(currChar, 5, self.item) # then this calls the alert_display function to tell the player what they got
# these create sprite groups that will store certain sprites in them			
all_sprites = sprite.Group() # this was originally meant to store all sprites but ended up just becoming the player sprite group
walls = sprite.Group() # this stores all the walls
chests = sprite.Group() # this stores all the chests
portals = sprite.Group() # stores all the portal objects
clerks = sprite.Group() # stores all the clerk objects
npcs = sprite.Group() # stores all the npc objects
player = Player(WIDTH / 2, HEIGHT / 2 + 50) # this centers the player
all_sprites.add(player) # as you can see, we only added one thing
fname = levelSelect(lvl, chests, walls, portals)[0] # this is the first layer of the map
tops = levelSelect(lvl, chests, walls, portals)[1] # this is the top layer of the map so that the character can go underneath objects to creat a layering effect
load_object(fname, chests, walls, portals) # this will load all the objects that the certain map holds
running = True
# key.set_repeat(100,100)
channels[0].fadeout(1000) # this fill fade out the intro screen music
playing = True
while playing:
	if not channels[0].get_busy(): # if there is no more music playing
		channels[0].set_volume(.1) # this sets the volume to .1
		for i in range(len(selections)): # this will go through your settings and load them
			if i == 0:
				if selections[i] == 'Windowed':
					screen = display.set_mode(size) # normal windowed mode
				else:	
					# this will be fullscreen that fits to the size of the screen
					screen = display.set_mode(size, FULLSCREEN)
					WIDTH, HEIGHT = size = (min(1920,display.Info().current_w), min(1080,display.Info().current_h))
			elif i == 1:
				# this will control music
				if selections[i] == 'Off':
					channels[0].set_volume(0)
				else:
					channels[0].set_volume(.1)
			elif i == 2:
				# this will control sound effects
				if selections[i] == 'Off':
					channels[1].set_volume(0)	
					channels[2].set_volume(0)	
				else:
					channels[1].set_volume(.5)	
					channels[2].set_volume(.5)		
		music(0, music_selection[0], -1) # this will play music
		playing = False # this will end the loop
while running:
	print(x_diff, y_diff)
	for evt in event.get():  
		if evt.type == QUIT: 
			running = False
		if evt.type == KEYDOWN:
			if evt.key == K_ESCAPE:
				running = False    	
		if evt.type == KEYUP:
			if evt.key == K_1:
				# this will change the characters
				currNum = 0
				Player_HP = stats[0][2]
				cf, cd, cr, cl = crowWalkForward, crowWalkDown, crowWalkRight, crowWalkLeft
				currChar = "Crow"
			if evt.key == K_2:
				# this will change the characters
				currNum = 1
				Player_HP = stats[1][2]
				cf, cd, cr, cl = ravenWalkForward, ravenWalkDown, ravenWalkRight, ravenWalkLeft
				currChar = "Raven"
			if evt.key == K_r:
				poop(stats,stats[currNum][0],stats[currNum][1])
				mode = 0	
			if evt.key == K_l:
				music(2, sound_selection[1], 0)
				fname, tops = levelSelect(lvl, chests, walls, portals)
				load_object(fname, chests, walls, portals)
				print("reload")
				time.wait(100)
			if evt.key == K_m:
				music(2, sound_selection[1], 0)
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
			if evt.key == K_l:
				stats[currNum][2] = 100	
			if mode != 0:
				if evt.key == K_z:
					Z = True	
				if evt.key == K_x:
					X = True
				if evt.key == K_c:
					C = True			
				if evt.key == K_k:
					stats[currNum][2] = 0	
		if evt.type==MOUSEBUTTONUP:
			if stage==1:
				battle=True		
	kp = key.get_pressed()
	mx, my = mouse.get_pos()
	mb = mouse.get_pressed()
	U = R = D = L = moving = False # this is to check if the player is moving and in which direction using booleans
	if quit_stat == 'quit':
		running = False
	encounter_steps = r(10,80) # this will select a random number between 10 and 80 repetitively	
	if int(step_counter) >= encounter_steps and stats[1][2] > 0:
		step_counter = 0 # will reset steps counter
		mode = 1 # this will make it mode 1 which is the mode for battle
	print(step_counter)	
	if mode == 0: # this is to check if the game is in normal mode
		if currChar == "Crow":
			# this will set the currNum and the animations
			currNum = 0
			cf, cd, cr, cl = crowWalkForward, crowWalkDown, crowWalkRight, crowWalkLeft
		elif currChar == "Raven":
			# this will set the currNum and the animations
			currNum = 1
			cf, cd, cr, cl = ravenWalkForward, ravenWalkDown, ravenWalkRight, ravenWalkLeft
		# the following is just for movement	
		if kp[K_RIGHT]:
			x_diff -= pan # this will change the x_diff by the pan (speed)
			R = True # this will show that the right button is being pressed
			moving = True # this will be for the animation loop to signify that the buttons for movement are being pressed
			pressed = "RIGHT" # this will save the right button as the last button pressed
							  # this is used for the direction in which the character faces after the buttons stop being pressed
			step_counter += .2 # this will add .2 to the steps counter
		# the following is the same as above with minor changes with the pan and x_diff / y_diff	
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
		if kp[K_LSHIFT]:
			# if you press shiftm then the pan becomes faster and so does the animation
			pan = 10
			s = 2
		else:
			# this sets it back to normal
			pan = 5
			s = 5
		# The following will just update all the positions and sprites on screen for all the sprite group classes
		all_sprites.update()
		npcs.update()
		clerks.update()
		walls.update()
		chests.update()
		portals.update()
		# check to see if the mob hit the player
		clerk_Interact = sprite.spritecollide(player, clerks, False) # this will check for collision  between the player and the clerk objects
		if clerk_Interact and kp[K_SPACE]: # if you are colliding with the clerk and press space
			music(2, sound_selection[1], 0) # sound effect will play
			clerk_Interact[0].interact = True # this will make interact for this item in the class true
			clerk_Interact[0].open_store() # this will run the open_store function within the Store_Clerk class
		npc_interact = sprite.spritecollide(player, npcs, False) # checks for collision between the npc and the player	
		if npc_interact and kp[K_SPACE]: # if there is a collision
			music(2, sound_selection[1], 0) # sound effect plays
			npc_interact[0].display_speech(True, True) # then will call display speech from the NPC class
		hit = sprite.spritecollide(player, walls, False) # this will check for collision between the player and the walls
		if hit: # if the player is colliding
			if player.rect.colliderect(hit[0].rect): # this will check if the rect of the player is colliding with the walls
				if moving: # this will check if there is actual buttons being pressed / movement happening
					if not channels[2].get_busy(): # this will play the collision sound as long as the channel isn't already playing something
						music(2, sound_selection[0], 0) # plays the sound effect
					# the following depending on the direction will negate what pan is doing to the x_diff or y_diff	
					if L:
						x_diff -= pan
					elif D:
						y_diff += pan
					elif U:
						y_diff -= pan
					elif R:
						x_diff += pan
				# this updates the classes so as to update them with the negated x_diff and y_diff		
				npcs.update()
				chests.update()	
				clerks.update()
		tel = sprite.spritecollide(player, portals, False) # will check if the player is colliding with portals
		if tel:
			music(2, sound_selection[2], 0) # plays sound effect
			lvl = tel[0].type # this will fetch the level that the portal wants to take you to
			x_diff, y_diff = int(tel[0].xd), int(tel[0].yd) # this assigns the x_dif and y_diff new values for the new map
			fname, tops = levelSelect(lvl, chests, walls, portals) # this will load the new map
			load_object(fname, chests, walls, portals) # this will load the objects for the map
		chest_open = sprite.spritecollide(player, chests, False) # checks for collision between chests and player
		if chest_open and kp[K_SPACE]: 
			chest_open[0].opened = True # this will make opened true
			# in the update that happend above this will take affect and will run
		# this is the animation counter
		if moving:
			counter += 1
			if counter > s:
				counter = 0
				frame += 1
				if frame >= len(crowWalkDown):
					frame = 0
		############################################## Map Loading ##############################################
		screen.fill(0) # this will erase what is on the screen
		MapLoad(fname) # this will load the map
		chests.draw(screen) # this will draw the chests on to the screen on top of the map
		clerks.draw(screen) # this will draw the clerks on top of the chests
		npcs.draw(screen) # this will draw the npcs on top of the clerks
		all_sprites.draw(screen) # this will draw the player on top of everything else
		MapLoad(tops) # this will load in the top of the maps ultimately causing a layering effect
		############################################## Map Loading ##############################################

		########################################### MOVEMENT ANIMATION ###########################################
		# this will update the animations according to the pressed keys
		if U:
			cm = cf[frame]
		elif R:
			cm = cr[frame]
		elif D:
			cm = cd[frame]
		elif L:
			cm = cl[frame]
		else:
			# this here will point your character in the last direction it was walking in
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
		if mode == 1:
			x = 0
			music(0, music_selection[3], -1)
			enemystatnum1=r(1,4)
			enemystatnum2=r(0,3)
			enemystatnum3=r(2,4)
			enemystats=[50+enemystatnum1*stats[currNum][2]//2,3+enemystatnum2*stats[currNum][3]//3,enemystatnum3*stats[currNum][4]//2]
			num=r(0,14)
			enemy = enemylist[num]
			turn = "Player"		
			used = False
			print(turn,"GOES FIRST!!!")	
			enemystats[0] = 100
			print("PRESS SPACE TO ATTACK")
			for i in battleAnimation:
				screen.blit(i,(0,0))
				time.wait(25)
				display.flip() 
			mode = 2	
		battleBack = transform.scale(image.load("img/battlebacks1/DarkSpace.png"), (WIDTH, HEIGHT))	
		FIGHTANIMATION(screen, enemy, battleBack)
		draw.rect(screen,(46,50,128),attackRect,0)
		draw.rect(screen,(210,75,146),itemRect,0)
		for i in range(stats[currNum][2]//2):
			# INSERT
			draw.rect(screen,(255,0,0),Rect(x,round(HEIGHT*6/8),10,15))
			x+=13
		x=0
		hpText=str("Player HP:"+str(stats[currNum][2]))
		hpEdit=fireFont.render(hpText,True,(0,200,0))
		screen.blit(hpEdit,(0,round(HEIGHT*6/8-40,0)))
		for i in range(stats[currNum][-1]//2):
			draw.rect(screen,(0,0,255),Rect(x,round(HEIGHT*6/8+50),10,15))
			x+=13
		x=0
		manaText=str("Player Mana: "+str(stats[currNum][-1]))
		manaEdit=fireFont.render(manaText,True,(0,200,0))
		screen.blit(manaEdit,(0,round(HEIGHT*6/8+20)))
		enemyhp=str("name of enemy HP: "+str(enemystats[0]))
		enemyhpEdit=fireFont.render(enemyhp,True,(0,200,0))
		screen.blit(enemyhpEdit,(0,0))
		count=0
		y=round(HEIGHT*1/8)
		for i in range(enemystats[0]//2):
			draw.rect(screen,(255,0,0),Rect(x,y,10,15))
			x+=12
			count+=1
			if count%17==0:
				y+=18
				x=0
		x=0
		if stage==0:
			text=str("Attack Skills")
			text3=str("Items")
			edit1=fireFont.render(text,True,(0,0,200))
			edit3=fireFont.render(text3,True,(0,0,200))
			screen.blit(edit1,(50,round(HEIGHT*7/8+15,0)))
			screen.blit(edit3,(round(50+WIDTH*2/3,0),round(HEIGHT*7/8+15,0)))
			if attackRect.collidepoint(mx,my) and mb[0] or Z:
				Z = not Z
				stage = 1
			if len(inventory) > 0:	
				if itemRect.collidepoint(mx,my) and mb[0] or C:
					C = not C
					stage=3
		########################################## ATTACK SELECTION ##########################################
		if stage==1:
			draw.rect(screen,(255,255,255),defenseRect,0)
			text=str("Attack1")
			text2=str("Attack2")
			text3=str("Attack3")
			edit1=fireFont.render(text,True,(0,0,200))
			edit2=fireFont.render(text2,True,(0,0,200))
			edit3=fireFont.render(text3,True,(0,0,200))
			screen.blit(edit1,(50,round(HEIGHT*7/8+15,0)))
			screen.blit(edit2,(round(50+WIDTH*1/3,0),round(HEIGHT*7/8+15,0)))
			screen.blit(edit3,(round(WIDTH*2/3+50,0),round(HEIGHT*7/8+15,0)))
			if attackRect.collidepoint(mx,my) or Z:
				Attack_DMG = stats[currNum][3]*4
				print("Your attack will do",Attack_DMG,"damage to the enemy!!")	###[1 is dmg][3 is magic dmg]
			elif defenseRect.collidepoint(mx,my) or X:
				Attack_DMG = stats[currNum][4]*5
				print("Your attack will do",Attack_DMG,"damage to the enemy!!") ###[1 is dmg][3 is magic dmg]	
			elif itemRect.collidepoint(mx,my) or C:
				Attack_DMG = stats[currNum][3]*3+stats[currNum][4]*3	###[1 is dmg][3 is magic dmg]	
				print("Your attack will do",Attack_DMG,"damage to the enemy!!")	
		########################################## ATTACK SELECTION ##########################################

		############################################### BATTLE ###############################################
		# used = False
		if turn == "Player" and stats[currNum][2] > 0 :
			if stage==1:
				if battle and mb[0]and attackRect.collidepoint(mx,my) or Z:
					Z = not Z
					if currNum==0:
						for i in CrowZ:
							FIGHTANIMATION(screen, enemy, battleBack)	
							enemyrect = i.get_rect()
							screen.blit(i,(WIDTH / 2 - enemyrect.width / 2, HEIGHT / 2 - enemyrect.height / 2))
							time.wait(50)
							display.flip()
					elif currNum==1:
						for i in CrowZ:
							FIGHTANIMATION(screen, enemy, battleBack)	
							enemyrect = i.get_rect()
							screen.blit(i,(WIDTH / 2 - enemyrect.width / 2, HEIGHT / 2 - enemyrect.height / 2))
							time.wait(50)
							display.flip()
					print(Attack_DMG)		
					enemystats[0] -= Attack_DMG
					turn = "Enemy"
					stage=0
					battle=False
				elif battle and mb[0] and defenseRect.collidepoint(mx,my) or X and stats[currNum][-1]>=10:
					X = not X
					if currNum==0:
						for i in CrowX:
							FIGHTANIMATION(screen, enemy, battleBack)	
							enemyrect = i.get_rect()
							screen.blit(i,(WIDTH / 2 - enemyrect.width / 2, HEIGHT / 2 - enemyrect.height / 2))
							time.wait(50)
							display.flip()
					elif currNum==1:
						for i in RavenX:
							FIGHTANIMATION(screen, enemy, battleBack)	
							enemyrect = i.get_rect()
							screen.blit(i,(WIDTH / 2 - enemyrect.width / 2, HEIGHT / 2 - enemyrect.height / 2))
							time.wait(50)
							display.flip()
					stats[currNum][-1]-=10
					enemystats[0] -= Attack_DMG
					turn = "Enemy"
					stage=0
				elif battle and mb[0] and itemRect.collidepoint(mx,my) or C and stats[currNum][-1]>=5:
					C = not C
					if currNum==0:
						for i in CrowC:
							FIGHTANIMATION(screen, enemy, battleBack)	
							enemyrect = i.get_rect()
							screen.blit(i,(WIDTH / 2 - enemyrect.width / 2, HEIGHT / 2 - enemyrect.height / 2))
							time.wait(50)
							display.flip()
					elif currNum==1:
						for i in RavenC:
							FIGHTANIMATION(screen, enemy, battleBack)	
							enemyrect = i.get_rect()
							screen.blit(i,(WIDTH / 2 - enemyrect.width / 2, HEIGHT / 2 - enemyrect.height / 2))
							time.wait(50)
							display.flip()
					stats[currNum][-1]-=5
					enemystats[0] -= Attack_DMG
					turn = "Enemy"
					stage=0
				# elif stage==2: ####for defencive items or other stuff??? idk we can decide on it later
			elif stage==3 and len(inventory) > 0:
				if used == False:
					InventoryDisplay(currChar, 3, inventory)
					stage = 0
				stage = 0
			else:
				X = Z = C = False		

		if turn == "Enemy" and enemystats[0] > 0:
			used = False
			time.wait(100)
			print(turn + "'s turn to attack!!")
			# stats[currNum][2] -= stats[currNum][1]*3//stats[currNum][2] ###20 is enemy damage and must be changed soon
			stats[currNum][2] -= enemystats[1] ###20 is enemy damage and must be changed soon
			print("Player HP:",stats[currNum][2])	
			turn = "Player"
		if stats[currNum][2] <= 0 or enemystats[0] <= 0:	
			if stats[currNum][2] <= 0:
				print("YOU LOST!!")		
				surf = Surface((800,600), SRCALPHA)
				for i in range(255):
					surf.fill((0,0,0,i))
					screen.blit(surf, (0,0))
					display.flip()	
					time.wait(10)
				for i in range(255):
					screen.blit(transform.scale(image.load('img/Screens/GameOver.png'), (WIDTH, HEIGHT)), (0,0))
					surf.fill((0,0,0, 255 - i))
					screen.blit(surf, (0,0))
					display.flip()	
					time.wait(10)	
				lvl = str(load_dict()[0]["lvl"]) # this will store which map is the current map
				x_diff, y_diff = load_dict()[0]['Coords'][0], load_dict()[0]['Coords'][1] # this will store the coordinates/offset of the map
				openedChests = load_dict()[0]["Chests"] # stores which chests have been opened
				inventory = load_dict()[0]["inv"] # will store the inventory of the player
				gold = load_dict()[0]["Gold"] # the amount of gold the player has
				npc_item = load_dict()[0]['npc_items'] # the npcs that have given there held items to the player
				currChar = load_dict()[0]["Current Charachter"] # the current character being used
				quest_completion = load_dict()[0]['Quests'] # this keeps track of the progress of the quests
				inv_dict = load_dict()[0]['inv_dict'] # this will store the order of which items were received. This is used in the inventory for scrolling
				stats = [load_dict()[1]["Stats"], load_dict()[2]["Stats"]] # this stores the stats of the two characters
				selections = load_dict()[0]['settings'] # this will load saved settings such as screen mode, BGM, and SE	
			elif enemystats[0] <= 0:	
				stats[currNum][0] += r(5,40)
				poop(stats,stats[currNum][0],stats[currNum][1])
			elif stats[currNum][2] <= 0 and enemystats[0] <= 0:
				print("YOU LOST!!")	
			mode = 0
		############################################### BATTLE ###############################################
	display.flip()
	myClock.tick(FPS)
quit()