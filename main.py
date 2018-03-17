#main.pygame
from main_vars import *
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
back = transform.scale(image.load("SPRITES/Background/DemonCastle1.png").convert_alpha(),size)	
fname = load_pygame("Maps/grasslands.tmx", pixelalpha = True)
while running:
	for evt in event.get(): 
		if evt.type == QUIT:
			running = False
		if evt.type == MOUSEBUTTONDOWN:
			if evt.button == 1:
				print(mx,my)
				test2.append((mx,my))
				# print(invisSurface.get_at((mx,my)))
				# pass
		if evt.type == KEYDOWN:
			if evt.key == K_ESCAPE:
				running = False
			if evt.key == K_1:
				cf, cd, cr, cl = crowWalkForward, crowWalkDown, crowWalkRight, crowWalkLeft
			if evt.key == K_2:
				cf, cd, cr, cl = ravenWalkForward, ravenWalkDown, ravenWalkRight, ravenWalkLeft	
			# if evt.key == K_RIGHT:
			# 	x += 1	
			# if evt.key == K_LEFT:
			# 	x -= 1
			# if evt.key == K_UP:
			# 	y -= 1
			# if evt.key == K_DOWN:
			# 	y += 1	
		# if evt.type == KEYUP:
		# 	if evt.key == K_RIGHT:
		# 		x = 0		
		# 	if evt.key == K_LEFT:
		# 		x = 0	
		# 	if evt.key == K_UP:
		# 		y = 0
		# 	if evt.key == K_DOWN:
		# 		y = 0			
	####
	mx,my = mouse.get_pos()
	mb = mouse.get_pressed()
	kp = key.get_pressed()
	U = R = D = L = moving = False
	if kp[K_UP]:
		y_diff += 10
		# y += 10
		sy -= speed
		U = True
		pressed = "UP"
		moving = True
	elif kp[K_RIGHT]:
		x_diff -= 10
		# x -= 10
		sx += speed
		R = True
		pressed = "RIGHT"
		moving = True	
	elif kp[K_DOWN]:
		y_diff -= 10
		# y -= 10
		sy += speed
		D = True	
		pressed = "DOWN"
		moving = True	
	elif kp[K_LEFT]:
		x_diff += 10
		# x += 10
		sx -= speed
		L = True
		pressed = "LEFT"
		moving = True	
	# else:
		# x = y = 0
	# for f in lists:
	# 	invisSurface.fill(0)
	# 	for i in range(len(f)):
	# 		invisSurface.fill(0)
	# 		f[i][0] += x_diff / 2
	# 		for n in range(2):
	# 			invisSurface.fill(0)
	# 			f[i][1] += y_diff / 2		

	if moving:
		counter += 1
		if counter > 2:
			counter = 0
			frame += 1
			if frame >= len(crowWalkForward):
				frame = 0	
	###############

	# for layer in fname.visible_object_groups:
	# 	for x, y, gid, in layer:
	# 		tile = fname.get_tile_image_by_gid(gid)
	# 		screen.blit(tile, (x * fname.tilewidth, y * fname.tileheight))

	for layer in fname.visible_layers:
		if isinstance(layer, TiledTileLayer):
			for x, y, gid, in layer:
				tile = fname.get_tile_image_by_gid(gid)
				if tile:
					screen.blit(tile, ((x * fname.tilewidth) + x_diff, (y * fname.tileheight) + y_diff))
	###############			
	

	# alpha.filled_polygon(invisSurface,test,(0,0,0,255))
	# alpha.filled_polygon(invisSurface,test2,(0,0,0,255))
	try:
		# invisSurface.fill((255,255,255,0))
		# alpha.filled_polygon(invisSurface,test,(0,0,0,255))
		pass
	except:
		pass	
	# screen.blit(back,(0,0)) # COMPULSORY
	screen.blit(invisSurface,(0,0))
	try:
		col = invisSurface.get_at((sx,sy))
		ccol = invisSurface.get_at((sx + 35,sy + 45))
		cccol = invisSurface.get_at((sx,sy + 45))
		ccccol = invisSurface.get_at((sx + 35,sy))
	except:
		pass	
	if ccol == (0,0,0,0) and U or cccol == (0,0,0,0) and U or col == (0,0,0,0) and U or ccccol == (0,0,0,0) and U:
		speed = 0
		sy += 5
	elif ccol == (0,0,0,0) and R or cccol == (0,0,0,0) and R or col == (0,0,0,0) and R or ccccol == (0,0,0,0) and R:
		speed = 0
		sx -= 5
	elif ccol == (0,0,0,0) and L or cccol == (0,0,0,0) and L or col == (0,0,0,0) and L or ccccol == (0,0,0,0) and L:
		speed = 0	
		sx += 5
	elif ccol == (0,0,0,0) and D or cccol == (0,0,0,0) and D or col == (0,0,0,0) and D or ccccol == (0,0,0,0) and D:
		speed = 0	
		sy -= 5
	else:
		speed = 5	
	if U:
		screen.blit(cf[frame], (sx,sy))
	elif R:
		screen.blit(cr[frame], (sx,sy))
	elif D:
		screen.blit(cd[frame], (sx,sy))
	elif L:
		screen.blit(cl[frame], (sx,sy))
	else:
		if pressed == "UP" or pressed == "NULL":
			screen.blit(cf[0], (sx,sy))
		elif pressed == "DOWN":
			screen.blit(cd[0], (sx,sy))
		elif pressed == "LEFT":
			screen.blit(cl[0], (sx,sy))
		elif pressed == "RIGHT":
			screen.blit(cr[0], (sx,sy))
	display.flip() 
	myClock.tick(600)
print("test =",test2)	
quit()