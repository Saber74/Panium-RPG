from pygame import *
cm = image.load("SPRITES/Crow/Walk/Forward/Forward-0.png")
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
		# self.rect.x = x ; self.rect.y = y
	def update(self):
		self.rect.topleft = self.x + x_diff, self.y + y_diff
class Chest(sprite.Sprite):
	def __init__(self, x, y, w, h, tier, name):
		sprite.Sprite.__init__(self)
		self.tier = tier
		self.opened = False
		self.images = [image.load("SPRITES/Chest/Tier" + str(self.tier) + "/0.png"), image.load("SPRITES/Chest/Tier" + str(self.tier) + "/1.png")]
		self.prev_image = self.image = self.images[0] ; self.rect = Rect(x, y, w, h)
		self.x, self.y = x, y
		self.c = tier1
		self.name = name
		self.nameBool = False
	def update(self):
		global chest_open
		self.rect.topleft = self.x + x_diff, self.y + y_diff
		if self.image == self.prev_image and self.opened and kp[K_SPACE]:
			self.image = self.images[1]
			if self.tier == '1':
				self.c = tier1
				print(self.name)
				if self.opened:
					openedChests.append([self.name,self.nameBool])
			elif self.tier == '2':	
				self.c = tier2
				print(self.name)
				if self.opened:
					openedChests.append([self.name,self.nameBool])
			elif self.tier == '3':
				self.c = tier3
				print(self.name)
				if self.opened:
					openedChests.append([self.name,self.nameBool])
			elif self.tier == '4':
				self.c = tier4
				print(self.name)
				if self.opened:
					openedChests.append([self.name,self.nameBool])
			item = r(0, len(self.c) - 1)
			inventory.append(self.c[item])
			del self.c[item]
			# print(inventory)			
			print(openedChests)
			# print(loadedChests)
			# print("Image =",self.image, "||" , " Prev_Image =",self.prev_image)
			# print("Opened =", self.opened)