from pygame import * 
size=(800,600)
screen = display.set_mode(size) 
myClock = time.Clock()
FPS = 30
x = y = 0
crowWalkForward, crowWalkDown, crowWalkRight, crowWalkLeft = [], [], [], []
ravenWalkForward, ravenWalkDown, ravenWalkRight, ravenWalkLeft = [], [], [], []
cf, cd, cr, cl = crowWalkForward, crowWalkDown, crowWalkRight, crowWalkLeft
pressed = "NULL"
frame = 0
counter = 0
cm = image.load("SPRITES/Crow/Walk/Forward/Forward-0.png").convert_alpha()

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
	def __init__(self):
		sprite.Sprite.__init__(self)
		self.image = cm
		# self.image.fill((0,255,0))
		self.rect = self.image.get_rect()
		self.rect.center = (400,300)
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
all_sprites = sprite.Group()                                 
player = Player()
all_sprites.add(player)
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
	mx,my=mouse.get_pos()
	mb=mouse.get_pressed()
	kp = key.get_pressed()
	U = R = D = L = moving = False

	# KEYBOARD MOVEMENT
	if kp[K_RIGHT]:
		x = 5
		R = True
		moving = True
		pressed = "RIGHT"
	elif kp[K_LEFT]:
		x = -5
		L = True
		moving = True
		pressed = "LEFT"
	elif kp[K_UP]:
		y = -5
		U = True
		moving = True
		pressed = "UP"
	elif kp[K_DOWN]:
		y = 5
		D = True
		moving = True
		pressed = "DOWN"
	else:
		x = y = 0			
		U = R = D = L = moving = False
	# ANIMATION CONTROL
	if moving:
		counter += 1
		if counter > 2:
			counter = 0
			frame += 1
			print(frame)
			if frame >= len(crowWalkDown):
				frame = 0

	# UPDATE
	all_sprites.update()

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
	print(pressed)		
	# DRAW / RENDER         
	screen.fill(0)
	all_sprites.draw(screen)
	display.flip() 
	myClock.tick(FPS)
quit()