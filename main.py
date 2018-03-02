#main.pygame
from pygame import * ; from pygame import gfxdraw as alpha
size = (800,600)
screen = display.set_mode(size)
myClock = time.Clock()
screen.set_alpha(255)
screen.fill((255,255,255))
running = True
every = [(0,0),(800,0),(800,600),(750,600),(750,50),(0,50)]
crowWalkForward = []
sx, sy = 0, 500
ccol = 0
counter = 0
moving = False
frame = 0
for i in range(9):
	crow = image.load("SPRITES/Crow/Walk/Forward/Forward-%i.png" % (i + 1)).convert_alpha()
	crowWalkForward.append(crow)
while running:
	screen.fill((255,255,255))
	# moving = False
	for evt in event.get(): 
		if evt.type == QUIT:
			running = False
		if evt.type == MOUSEBUTTONDOWN:
			if evt.button == 1:
				ccol = screen.get_at((mx - 5,my - 5))
				print(ccol)
				if ccol == (0,0,0,255):
					print("poop")
		if evt.type == KEYDOWN:
			if evt.key == K_ESCAPE:
				running = False
	####
	mx,my = mouse.get_pos()
	mb = mouse.get_pressed()
	kp = key.get_pressed()
	moving = False	
	if kp[K_UP]:
		sy -= 2
		moving = True
	if moving:
		counter += 1
		if counter > 5:
			counter = 0
			frame += 1
			if frame >= len(crowWalkForward):
				frame = 0
	screen.fill((255,255,255))				
	alpha.filled_polygon(screen,every,(0,0,0,255))
	screen.blit(crowWalkForward[frame], (sx,sy))

	display.flip() 
	myClock.tick(60)
quit()