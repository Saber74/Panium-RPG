from main_vars import *
init()
for i in range(1,100):
	loadingAnimation.append(image.load("SPRITES/gif/0 (%i).gif" % (i + 1)).convert_alpha())
for i in range(1,99):
	screen.blit(loadingAnimation[i],(150,150))
	display.flip()
	time.wait(50)
                                 
 
quit()