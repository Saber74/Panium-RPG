# main.py
from main_vars import *
characterList=["Crow"]
character=characterList[selectedChar]
for i in range(9):
	crowWalkForward.append(image.load("SPRITES/Crow/Walk/Forward/Forward-%i.png" % (i + 1)).convert_alpha())
	crowWalkRight.append(image.load("SPRITES/Crow/Walk/Right/Right-%i.png" % (i + 1)).convert_alpha())  
	crowWalkDown.append(image.load("SPRITES/Crow/Walk/Back/Back-%i.png" % (i + 1)).convert_alpha()) 
	crowWalkLeft.append(image.load("SPRITES/Crow/Walk/Left/Left-%i.png" % (i + 1)).convert_alpha())
for i in range(2):
	voldeWalkBack.append(image.load("SPRITES/Volde/Move/Down/%i.png" % (i + 1)).convert_alpha())
for i in range(27):
	voldeAnimation.append(image.load("SPRITES/Animation/%i.png" % (i + 1)).convert_alpha())
# for i in range(23):
# 	transitionIntoBattle.append(image.load("SPRITES/gif/%i.gif" % (i + 1)).convert_alpha())

back = transform.scale(image.load("SPRITES/Background/DemonCastle1.png").convert_alpha(),size)  
voldeRect=Rect(350,250,100,100)
while running:
	# screen.fill((255,255,255))
	character=characterList[selectedChar]
	print(selectedChar)
	for evt in event.get(): 
		if evt.type == QUIT:
			running = False
		if evt.type == MOUSEBUTTONDOWN:
			if evt.button == 1:
				print(invisSurface.get_at((mx,my)))
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
	elif kp[K_n]:
		selectedChar+=1
		if selectedChar==len(characterList):
			selectedChar=0  
	if moving:
		counter += 1
		if counter > 5:
			counter = 0
			frame += 1
			if frame >= len(crowWalkForward):
				frame = 0   
	screen.fill((255,255,255))              
	alpha.filled_polygon(invisSurface,every,(0,0,0,1))
	screen.blit(back,(0,0))
	draw.polygon(screen,(0,255,0),every)
	screen.blit(invisSurface,(0,0))
	try:
		ccol = invisSurface.get_at((sx,sy))
	except:
		pass    
	if ccol == (0,0,0,0) and U:
		speed = 0
		sy += 5
	elif ccol == (0,0,0,0) and R:
		speed = 0
		sx -= 5
	elif ccol == (0,0,0,0) and L:
		speed = 0   
		sx += 5
	elif ccol == (0,0,0,0) and D:
		speed = 0   
		sy -= 5
	else:
		speed = 2
	if character=="Crow":
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
	screen.blit(voldeWalkBack[0],(400,300))
	if voldeRect.collidepoint(sx,sy):
		activateAnimation=True
	if activateAnimation and check == False:
		for i in range(27):
			screen.blit(pic,(0,0))
			screen.blit(voldeAnimation[i],(335,125))
			screen.blit(voldeAnimation[i],(135,200))
			screen.blit(voldeAnimation[i],(535,200))
			screen.blit(voldeAnimation[i],(335,400))
			time.wait(10)
			display.flip()
		check = True	
		
	for i in range(22):
		screen.blit(transitionIntoBattle[i],(400,400))
		time.wait(100)
		display.flip()
	activateAnimation=False


	display.flip() 
	pic=screen.copy()
	myClock.tick(600)
quit()
