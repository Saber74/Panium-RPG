from pygame import *
init()
mixer.init() 
mixer.set_num_channels(4) ###setting number of channels up
channel1=mixer.Channel(0) ##declaring each channel, makes it easier to control them
channel2=mixer.Channel(1)
channel3=mixer.Channel(2)

soundGrandma=mixer.Sound("Music/Village.wav") ###creating a sound object that can be played in the channel ##this only works with wav and of something
channel1.play(soundGrandma,-1) ###playing the actual "Sound" the number is the loop which is infinity
channel1.set_volume(0.1) ##to set volume for things so you don't get deaf
BossFight=mixer.Sound("Music/Castle.wav") 
channel2.play(BossFight,-1) ##playing on the second channel
WIDTH,HEIGHT=800,600
screen = display.set_mode((WIDTH,HEIGHT)) 
mode=1
xp=110
statupgrade=0
currlevel=0
selecnum=0
selectionList=["attack","defense","magic","magicdefense","health","mana"]
arrowselected=""
levelattackRect=Rect(WIDTH//2,round(HEIGHT*1/7),WIDTH//5,HEIGHT//10)
leveldefenseRect=Rect(WIDTH//2,round(HEIGHT*2/7),WIDTH//5,HEIGHT//10)
levelmagicRect=Rect(WIDTH//2,round(HEIGHT*3/7),WIDTH//5,HEIGHT//10)
levelmagicdefenseRect=Rect(WIDTH//2,round(HEIGHT*4/7),WIDTH//5,HEIGHT//10)
levelhealthRect=Rect(WIDTH//2,round(HEIGHT*5/7),WIDTH//5,HEIGHT//10)
levelmanaRect=Rect(WIDTH//2,round(HEIGHT*6/7),WIDTH//5,HEIGHT//10)
running = True
x=0
uparrow=image.load("sortup.png")
downarrow=image.load("sortdown.png")
uparrowclicked=image.load("sortupclicked.png")
downarrowclicked=image.load("sortdownclicked.png")
downarrowRect=Rect(75,HEIGHT//2,132,65)
uparrowRect=Rect(75,HEIGHT//2-HEIGHT//7,132,65)
levelup=False
while running:
	for evt in event.get():  
		if evt.type == QUIT: 
			running = False
		if evt.type==KEYDOWN:
			if evt.key==K_z:
				if mode==1:
					mode=2
	mx,my=mouse.get_pos()
	mb=mouse.get_pressed()
	screen.fill((255,255,255))
	if mode==2:
		# charlevel,xp=levelup(7,xp)
		draw.rect(screen,(211,211,211),Rect(WIDTH//4,HEIGHT//2,WIDTH//2,HEIGHT//20))
		for i in range(xp//10):
			draw.rect(screen,(18,107,60),Rect(WIDTH//4+x,HEIGHT//2,WIDTH//2//10,HEIGHT//20))
			x=WIDTH//2//10*i
			time.wait(100)
			display.flip()
			if i>=10:
				xp-=100
				currlevel+=1
				levelup=True
				time.wait(1000)		
		if levelup:
			if evt.type==KEYDOWN:
				if evt.key==K_UP:
					arrowselected="up"
				elif evt.key==K_DOWN:
					arrowselected="down"
				elif evt.key==K_LEFT:
					if selecnum!=0:
						selecnum-=1
				elif evt.key==K_RIGHT:
					if selecnum!=len(selectionList)-1:
						selecnum+=1
			selected=selectionList[selecnum]
			screen.fill((255,255,255))
			screen.blit(uparrow,(75,HEIGHT//2-HEIGHT//7))
			screen.blit(downarrow,(75,HEIGHT//2))
			draw.rect(screen,(130, 82, 1),levelattackRect,0)
			draw.rect(screen,(130, 82, 1),leveldefenseRect,0)
			draw.rect(screen,(130, 82, 1),levelmagicRect,0)
			draw.rect(screen,(130, 82, 1),levelmagicdefenseRect,0)
			draw.rect(screen,(130, 82, 1),levelhealthRect,0)
			draw.rect(screen,(130, 82, 1),levelmanaRect,0)
			if selected=="attack":
				draw.rect(screen,(130, 82, 130),levelattackRect,0)			
			elif selected=="defense":
				draw.rect(screen,(130, 82, 130),leveldefenseRect,0)
			elif selected=="magic":
				draw.rect(screen,(130, 82, 130),levelmagicRect,0)
			elif selected=="magicdefense":
				draw.rect(screen,(130, 82, 130),levelmagicdefenseRect,0)
			elif selected=="health":
				draw.rect(screen,(130, 82, 130),levelhealthRect,0)
			elif selected=="mana":
				draw.rect(screen,(130, 82, 130),levelmanaRect,0)
			if arrowselected=="up":
				screen.blit(uparrowclicked,(75,HEIGHT//2-HEIGHT//7))
			elif arrowselected=="down":
				screen.blit(downarrowclicked,(75,HEIGHT//2))
	print(statupgrade)	
	display.flip() 
quit()