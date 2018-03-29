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
crowWalkForward, crowWalkDown, crowWalkRight, crowWalkLeft = [], [], [], []
ravenWalkForward, ravenWalkDown, ravenWalkRight, ravenWalkLeft = [], [], [], []
chest_open = []
tier1 = ["Potion", "Sword", "Shield", "Elixir", "Poison"]
inventory = []
cf, cd, cr, cl = crowWalkForward, crowWalkDown, crowWalkRight, crowWalkLeft
pressed = "NULL"
frame = 0
counter = 0
x_diff = y_diff = 0
speed = 0
pan = 10
cm = image.load("SPRITES/Crow/Walk/Forward/Forward-0.png").convert_alpha()
fname = load_pygame("Maps/grasslands.tmx", pixelalpha = True)
tops = load_pygame("Maps/over0.tmx", pixelalpha = True)
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
class Player(sprite.Sprite):
	# sprite for the player
	def __init__(self, x, y, s):
		sprite.Sprite.__init__(self)
		self.image = cm
		self.rect = self.image.get_rect()
		self.x = x ; self.y = y
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
		# self.rect.x = x ; self.rect.y = y

	def update(self):
		self.rect.topleft = self.x + x_diff, self.y + y_diff
class Chest(sprite.Sprite):
	def __init__(self, x, y, w, h, tier):
		sprite.Sprite.__init__(self)
		self.tier = tier
		self.opened = False
		self.images = [image.load("SPRITES/Chest/Tier" + str(self.tier) + "/0.png"), image.load("SPRITES/Chest/Tier" + str(self.tier) + "/1.png")]
		self.prev_image = self.image = self.images[0] ; self.rect = Rect(x, y, w, h) ; self.prev_image = self.image
		self.x, self.y = x, y
	def update(self):
		global chest_open
		self.rect.topleft = self.x + x_diff, self.y + y_diff
		if self.image == self.prev_image and self.opened and kp[K_SPACE]:
			self.image = self.images[1]
			item = r(0,len(tier1) - 1)
			inventory.append(tier1[item])
			del tier1[item]
			print(inventory)

all_sprites = sprite.Group()                                 
walls = sprite.Group()
chests = sprite.Group()
player = Player(WIDTH / 2, HEIGHT / 2 + 50, speed)
all_sprites.add(player)
for tile_object in fname.objects:
	if tile_object.name == 'wall':
		obs = Obstacle(tile_object.x, tile_object.y, tile_object.width, tile_object.height)
		walls.add(obs)
	if tile_object.name == 'chest':
		chest = Chest(tile_object.x, tile_object.y, tile_object.width, tile_object.height, tile_object.type)	
		chests.add(chest)
			
running = True
while running:
	for evt in event.get():  
		if evt.type == QUIT: 
			running = False
		if evt.type == KEYDOWN:
			if evt.key == K_ESCAPE:
				running = False    	
			if evt.key == K_1:
				cf, cd, cr, cl = crowWalkForward, crowWalkDown, crowWalkRight, crowWalkLeft
			if evt.key == K_2:
				cf, cd, cr, cl = ravenWalkForward, ravenWalkDown, ravenWalkRight, ravenWalkLeft
			if evt.key == K_i:
				print(inventory)
			if evt.key == K_q:
				print(tier1)		
	mx,my=mouse.get_pos()
	mb=mouse.get_pressed()
	kp = key.get_pressed()
	U = R = D = L = moving = False
	# KEYBOARD MOVEMENT
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
		U = R = D = L = moving = False

	# UPDATE
	all_sprites.update()
	walls.update()
	chests.update()
	# camera.update(player)
	# check to see if the mob hit the player
	hit = sprite.spritecollide(player, walls, False)
	if hit:
		n += 1
		print(n)	
		# print("HIT THE WALL ON ME")

	chest_open = sprite.spritecollide(player, chests, False)	
	if chest_open and kp[K_SPACE]:
		chest_open[0].opened = True

	# ANIMATION CONTROL
	if moving:
		counter += 1
		if counter > 2:
			counter = 0
			frame += 1
			if frame >= len(crowWalkDown):
				frame = 0

	# Map Loading
	screen.fill(0)
	for layer in fname.visible_layers:
		if isinstance(layer, TiledTileLayer):
			for x, y, gid in layer:
				tile = fname.get_tile_image_by_gid(gid)
				if tile:
					screen.blit(tile, ((x * fname.tilewidth) + x_diff, (y * fname.tileheight) + y_diff))
	chests.draw(screen)
	all_sprites.draw(screen)
	for layer in tops.visible_layers:
		if isinstance(layer, TiledTileLayer):
			for x, y, gid in layer:
				tile = tops.get_tile_image_by_gid(gid)
				if tile:
					screen.blit(tile,((x * tops.tilewidth) + x_diff, (y * tops.tileheight) + y_diff))				
	# MOVEMENT ANIMATION
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
	# DRAW / RENDER         
	# screen.fill(0)
	# chests.draw(screen)
	# all_sprites.draw(screen)
	walls.draw(screen)
	display.flip() 
	myClock.tick(FPS)
quit()