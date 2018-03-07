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
while running:
	for evt in event.get(): 
		if evt.type == QUIT:
			running = False
		if evt.type == MOUSEBUTTONDOWN:
			if evt.button == 1:
				print(mx,my)
				test.append((mx,my))
				# pass
		if evt.type == KEYDOWN:
			if evt.key == K_ESCAPE:
				running = False
			if evt.key == K_1:
				cf, cd, cr, cl = crowWalkForward, crowWalkDown, crowWalkRight, crowWalkLeft
			if evt.key == K_2:
				cf, cd, cr, cl = ravenWalkForward, ravenWalkDown, ravenWalkRight, ravenWalkLeft
	####
	mx,my = mouse.get_pos()
	mb = mouse.get_pressed()
	kp = key.get_pressed()
	moving = False	
	U = R = D = L = moving = False
	if kp[K_UP]:
		sy -= speed
		U = True
		pressed = "UP"
		moving = True
	elif kp[K_RIGHT]:
		sx += speed
		R = True
		pressed = "RIGHT"
		moving = True	
	elif kp[K_DOWN]:
		sy += speed
		D = True	
		pressed = "DOWN"
		moving = True	
	elif kp[K_LEFT]:
		sx -= speed
		L = True
		pressed = "LEFT"
		moving = True	
	if moving:
		counter += 1
		if counter > 5:
			counter = 0
			frame += 1
			if frame >= len(crowWalkForward):
				frame = 0	
	try:
		# alpha.polygon(invisSurface,test,(0,0,0,255))
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
		speed = 2	
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
# print("test =",test)	
quit()