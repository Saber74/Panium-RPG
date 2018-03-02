# main.py
from pygame import * ; from pygame import gfxdraw as alpha
size = (800,600)
screen = display.set_mode(size)
screen.set_alpha(255)
screen.fill((255,255,255))
running = True
every = [(0,0),(800,0),(800,600),(750,600),(750,50),(0,50)]
# crowWalkForward = []
# sx, sy = 400, 300
# ccol = 0
# for i in range(10):
# 	crow = image.load("SPRITES/Crow/Walk/Forward/Forward-%1d.png" % i).convert_alpha()
# 	crowWalkForward.append(crow)
while running:
	screen.fill((255,255,255))
	alpha.filled_polygon(screen,every,(0,0,0,1))
	for evt in event.get(): 
		if evt.type == QUIT:
			running = False
		if evt.type == MOUSEBUTTONDOWN:
			if evt.button == 1:
				ccol = screen.get_at((mx - 0,my - 0))
				print(ccol)
				if ccol == (0,0,0,255):
					print("colour hit")
		if evt.type == KEYDOWN:
			if evt.key == K_ESCAPE:
				running = False
			# if evt.key == K_UP:
			# 	for i in range(len(crowWalkForward)):
			# 		screen.blit(crowWalkForward[i],(sx,sy))
			# 		time.wait(100)
			# 		display.flip()
			# 	sy -= 5		
			# 	print(sx,sy)
	####
	mx,my=mouse.get_pos()
	mb=mouse.get_pressed()

	display.flip() 
quit()