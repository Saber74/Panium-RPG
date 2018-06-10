from pygame import *
init()
mixer.init() 
mixer.set_num_channels(4) ###setting number of channels up
channel1=mixer.Channel(0) ##declaring each channel, makes it easier to control them
channel2=mixer.Channel(1)
channel3=mixer.Channel(2)
 ##to set volume for things so you don't get deaf
WIDTH,HEIGHT=800,600
def introscreen():
	firsttime=True
	intromix=mixer.Sound("Music/Starting.wav") ###creating a sound object that can be played in the channel ##this only works with wav and of something
	channel1.play(intromix,-1) ###playing the actual "Sound" the number is the loop which is infinity
	channel1.set_volume(0.7) ##to set volume for things so you don't get deaf
	# yes=image.load("yes_notclicked.png")
	# yes_clicked=image.load("yes_clicked.png")
	# no=image.load("no_notclicked.png")
	# no_clicked=image.load("no_clicked.png")
	######################################rects###################
	yesRect=Rect(180,255,200,120)
	noRect=Rect(470,255,170,120)
	newGameRect=Rect(380,400,240,65)
	continueGameRect=Rect(470,470,320,75)
	quitRect=Rect(0,425,140,55)
	###################################################
	go=False #bolean for checking click on quit
	init()
	running = True
	while running:
		for evt in event.get():  
			if evt.type == QUIT: 
				running = False
			if evt.type == KEYUP:
				if evt.key == K_ESCAPE:
					quit()
		mx,my=mouse.get_pos()
		mb=mouse.get_pressed()
		WIDTH, HEIGHT = 800, 600 
		# WIDTH, HEIGHT = 1366, 768
		size=(WIDTH, HEIGHT)
		screen = display.set_mode(size)
		# screen = display.set_mode(size, FULLSCREEN)
		# width, height = size = (min(1920,display.Info().current_w), min(1080,display.Info().current_h))
		#################################intro gif######################################3
		if firsttime==True:
			for i in range(3):
				for i in range(0,16):
					# screen.fill((37,34,39))
					screen.blit(image.load("ezgif-4-9108664653-gif-im/%i.gif"%i),(100,75))
					display.update()
					time.wait(50)
			firsttime=False
		###########################################################

		###############################################graphics for the intro screen including text and pictures########################
		screen.blit(transform.scale(image.load("olga-antonenko-monolith-final.jpg"),(WIDTH,HEIGHT)),(0,0))
		# draw.rect(screen,(216, 163, 149),newGameRect,0)
		# draw.rect(screen,(216,163,149),continueGameRect,0)
		# draw.rect(screen,(100,100,100),quitRect,10)
		# titleFont=font.Font("Carta_Magna-line-demo-FFP.ttf",45)
		titleFontcont=font.Font("Carta_Magna-line-demo-FFP.ttf",85)
		smalltextFont=font.Font("Carta_Magna-line-demo-FFP.ttf",50)
		quitFont=font.Font("Carta_Magna-line-demo-FFP.ttf",40)
		newGametext=str("New Game")
		continueGameText=str("Continue Game")
		# title=str("The battle of")
		titlecont=str("PANIUM")
		quitText=str("QUIT")
		quitEdit=quitFont.render(quitText,True,(255,0,0))
		# titleEdit=titleFont.render(title,True,(125,44,23))
		titleEditcont=titleFontcont.render(titlecont,True,(255,99,71))
		newGameEdit=smalltextFont.render(newGametext,True,(255,163,149))
		continueGameEdit=smalltextFont.render(continueGameText,True,(255,163,149))
		# screen.blit(titleEdit,(430,0))
		screen.blit(titleEditcont,(60,-10))
		screen.blit(newGameEdit,(380,400))
		screen.blit(continueGameEdit,(470,470))
		screen.blit(quitEdit,(10,420))
		######################################################################################
		copy=screen.copy()
		############################collision to call each function on the intro screen when required
		if newGameRect.collidepoint(mx,my):
			newGameEdit=smalltextFont.render(newGametext,True,(255,31,80))
			screen.blit(newGameEdit,(380,400))
			if mb[0]:
				pass
		elif continueGameRect.collidepoint(mx,my):
			continueGameEdit=smalltextFont.render(continueGameText,True,(255,31,80))	
			screen.blit(continueGameEdit,(470,470))
			if mb[0]:
				pass
		elif quitRect.collidepoint(mx,my):
			quitEdit=quitFont.render(quitText,True,(255,31,80))
			screen.blit(quitEdit,(10,420))
			if mb[0]:
				go=True

		if go:	####are you sure you want to quit###############################################################3
			screen.blit(transform.scale(image.load("olga-antonenko-monolith-final.jpg"),(WIDTH,HEIGHT)),(0,0))
			# draw.rect(screen,(255,9,99),noRect,10)
			# draw.rect(screen,(255,9,99),yesRect,10)
			# screen.blit(yes,(100,300))
			# screen.blit(no,(600,300))
			confirmquit=font.Font("Something Strange.ttf",110)
			yesnoFont=font.Font("Something Strange.ttf",130)
			text=str("Are you a coward?")
			yesText=str("YES")
			noText=str("NO")
			yesInfo=yesnoFont.render(yesText,True,(0,0,0))
			noInfo=yesnoFont.render(noText,True,(0,0,0))
			info=confirmquit.render(text,True,(255,255,255))
			screen.blit(yesInfo,(200,250))
			screen.blit(noInfo,(500,250))
			screen.blit(info,(30,50))
			display.update()
			if yesRect.collidepoint((mx,my)):
				yesInfo=yesnoFont.render(yesText,True,(255,0,0))
				screen.blit(yesInfo,(200,250))
				# screen.blit(yes_clicked,(100,300))
				if mb[0]:
					quit()
			elif noRect.collidepoint((mx,my)):
				noInfo=yesnoFont.render(noText,True,(255,0,0))
				screen.blit(noInfo,(500,250))
				# screen.blit(no_clicked,(600,300))
				if mb[0]:
					# screen.blit(copy,(0,0))
					go=False
		display.update()
				########################################################################################
	quit()					  

	

# introscreen()