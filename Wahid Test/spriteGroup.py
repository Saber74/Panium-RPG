from pygame import * 
from random import *
from pytmx import *
import os
size=(1366,768)
invisSurface = Surface(size,SRCALPHA)
invisSurface.fill((255,255,255,0))
os.environ['SDL_VIDEO_WINDOW_POS'] = 'FULLSCREEN'
screen = display.set_mode(size) 
myClock = time.Clock()
FPS = 60
x = y = 0
crowWalkForward, crowWalkDown, crowWalkRight, crowWalkLeft = [], [], [], []
ravenWalkForward, ravenWalkDown, ravenWalkRight, ravenWalkLeft = [], [], [], []
cf, cd, cr, cl = crowWalkForward, crowWalkDown, crowWalkRight, crowWalkLeft
pressed = "NULL"
frame = 0
counter = 0
x_diff = y_diff = 0
speed = 5
# pan = 10
cm = image.load("SPRITES/Crow/Walk/Forward/Forward-0.png").convert_alpha()
fname = load_pygame("Maps/grasslands.tmx", pixelalpha = True)
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
	def __init__(self, x, y):
		sprite.Sprite.__init__(self)
		self.image = cm
		self.rect = self.image.get_rect()
		self.rect.center = (x,y)
	def update(self):
		self.image = cm
		if pressed == "LEFT" or pressed == "RIGHT":
			self.rect.x += x
		elif pressed == "UP" or pressed == "DOWN":	
			self.rect.y += y
		if self.rect.left  > 800:
			self.rect.right = 0
		elif self.rect.right < 0:
			self.rect.left = 800
		elif self.rect.bottom < 0:
			self.rect.top = 600	
		elif self.rect.top > 600:
			self.rect.bottom = 0	
class Mob(sprite.Sprite):
	def __init__(self):
		sprite.Sprite.__init__(self)
		self.image = Surface((30,40))		
		self.image.fill((255,0,0))
		self.rect = self.image.get_rect()
		self.rect.x = randint(0, 800 - self.rect.width)
		self.rect.y = randint(-100,-40)
		self.speedy = randint(1,8)
		self.speedx = randint(-3,3)
	def update(self):
		self.rect.y += self.speedy
		self.rect.x += self.speedx
		if self.rect.top > 600 + 10 or self.rect.left < -25 or self.rect.right > 800 + 20:
			self.rect.x = randint(0 ,800 - self.rect.width)
			self.rect.y = randint(-100,-40)	
			self.speedy = randint(5,8)
class Obstacle(sprite.Sprite):
	def __init__(self, x, y, w, h):
		sprite.Sprite.__init__(self)
		self.image = Surface((x, y), SRCALPHA)
		self.image.fill((255,255,255,0))
		self.rect = Rect(x, y, w, h)
		self.x = x
		self.y = y
		self.rect.x = x
		self.rect.y = y
		print("HIT")

# for i in range(8):
# 	m = Mob()
# 	all_sprites.add(m)
# 	mobs.add(m)
all_sprites = sprite.Group()                                 
mobs = sprite.Group()
walls = sprite.Group()
player = Player(1366 / 2, 768 / 2)
all_sprites.add(player)
for tile_object in fname.objects:
	if tile_object.name == 'wall':
		obs = Obstacle(tile_object.x, tile_object.y, tile_object.width, tile_object.height)
		walls.add(obs)
		print("hit")
running = True
while running:
	for evt in event.get():  
		if evt.type == QUIT: 
			running = False
		if evt.type == MOUSEBUTTONDOWN:
			if evt.button == 1:
				print((mx,my))	
		if evt.type == KEYDOWN:
			if evt.key == K_ESCAPE:
				running = False    	
			if evt.key == K_1:
				cf, cd, cr, cl = crowWalkForward, crowWalkDown, crowWalkRight, crowWalkLeft
			if evt.key == K_2:
				cf, cd, cr, cl = ravenWalkForward, ravenWalkDown, ravenWalkRight, ravenWalkLeft	
	mx,my=mouse.get_pos()
	mb=mouse.get_pressed()
	kp = key.get_pressed()
	U = R = D = L = moving = False
	# KEYBOARD MOVEMENT
	if kp[K_RIGHT]:
		# x_diff -= pan
		x = speed
		R = True
		moving = True
		pressed = "RIGHT"
	elif kp[K_LEFT]:
		# x_diff += pan
		x = -speed
		L = True
		moving = True
		pressed = "LEFT"
	elif kp[K_UP]:
		# y_diff += pan
		y = -speed
		U = True
		moving = True
		pressed = "UP"
	elif kp[K_DOWN]:
		# y_diff -= pan
		y = speed
		D = True
		moving = True
		pressed = "DOWN"
	else:
		x = y = 0			
		U = R = D = L = moving = False

	# UPDATE
	all_sprites.update()
	# check to see if the mob hit the player
	hit = sprite.spritecollide(player, walls, False)
	if hit:
		running = False
	# hits = sprite.spritecollide(player, mobs, True)
	# if hits:
	# 	running = False

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
			for x, y, gid, in layer:
				tile = fname.get_tile_image_by_gid(gid)
				if tile:
					screen.blit(tile, ((x * fname.tilewidth) + x_diff, (y * fname.tileheight) + y_diff))
	screen.blit(invisSurface, (0 + x_diff,0 + y_diff))				
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
	# print(fname.get_rect())		
	# DRAW / RENDER         
	# screen.fill(0)
	all_sprites.draw(screen)
	walls.draw(screen)
	display.flip() 
	myClock.tick(FPS)
quit()