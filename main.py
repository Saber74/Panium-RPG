#main.pygame
from main_vars import *
for i in range(9):
	crowWalkForward.append(image.load("SPRITES/Crow/Walk/Forward/Forward-%i.png" % (i + 1)).convert_alpha())
	crowWalkRight.append(image.load("SPRITES/Crow/Walk/Right/Right-%i.png" % (i + 1)).convert_alpha())	
	crowWalkDown.append(image.load("SPRITES/Crow/Walk/Back/Back-%i.png" % (i + 1)).convert_alpha())	
	crowWalkLeft.append(image.load("SPRITES/Crow/Walk/Left/Left-%i.png" % (i + 1)).convert_alpha())	
while running:
	# screen.fill((255,255,255))
	for evt in event.get(): 
		if evt.type == QUIT:
			running = False
		if evt.type == MOUSEBUTTONDOWN:
			if evt.button == 1:
				ccol = screen.get_at((sx,sy))
				print(ccol)
				alpha.filled_polygon(screen,every,(0,0,0,1))
				if ccol == (254,254,254,255):
					print("poop")
		if evt.type == KEYDOWN:
			if evt.key == K_ESCAPE:
				running = False
	####
	mx,my = mouse.get_pos()
	mb = mouse.get_pressed()
	kp = key.get_pressed()
	moving = False	
	U = R = D = L = moving = False
	if kp[K_UP]:
		sy -= 2
		U = True
		pressed = "UP"
		moving = True
	elif kp[K_RIGHT]:
		sx += 2
		R = True
		pressed = "RIGHT"
		moving = True	
	elif kp[K_DOWN]:
		sy += 2
		D = True	
		pressed = "DOWN"
		moving = True	
	elif kp[K_LEFT]:
		sx -= 2
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
	screen.fill((255,255,255))				
	alpha.filled_polygon(screen,every,(0,0,0,1))
	try:
		ccol = screen.get_at((sx,sy))
	except:
		pass	
	if ccol == (254,254,254,255):
		sx += 0 ; sy += 0
		print("HIT")
	try:
		print(screen.get_at((sx,sy)))
	except:
		pass	
	if U:
		screen.blit(crowWalkForward[frame], (sx,sy))
	elif R:
		screen.blit(crowWalkRight[frame], (sx,sy))
	
	elif D:
		screen.blit(crowWalkDown[frame], (sx,sy))
	elif L:
		screen.blit(crowWalkLeft[frame], (sx,sy))
	else:
		if pressed == "UP" or pressed == "NULL":
			screen.blit(crowWalkForward[0], (sx,sy))
		elif pressed == "DOWN":
			screen.blit(crowWalkDown[0], (sx,sy))
		elif pressed == "LEFT":
			screen.blit(crowWalkLeft[0], (sx,sy))
		elif pressed == "RIGHT":
			screen.blit(crowWalkRight[0], (sx,sy))
	display.flip() 
	myClock.tick(60)
quit()