#CHARtest.py
from pygame import *
size = (800,600)
screen = display.set_mode(size)
screen.fill((255,255,255))
CHARexp =    [ 2,        1,        1]
CHAR =       ['Lindus', 'Nimbus', 'Dingus']
CHARlevels = [ 1,        1,        1]
CharStats = ['Attack', 'Speed', 'Dexterity']
LindusStats = [5,       8,       9]
NimbusStats = [5,       10,      12]
DingusStats = [2,       7,       6]
curChar = "Lindus"
running = True
size=(800,600)
screen = display.set_mode(size)
screen.fill((255,255,255)) 
enemy = ""
running = True
def hardEnemy():
	if curChar == "Lindus":
		charInd = CHAR.index("Lindus")
		obtainedEXP = CHARexp[charInd]/(40/CHARlevels[charInd])
		EXPupdate = obtainedEXP + CHARexp[charInd]
		CHARexp[0] = EXPupdate
		print(CHARexp[0])
def amateurEnemy():
	if curChar == "Lindus":
		charInd = CHAR.index("Lindus")
		obtainedEXP = CHARexp[charInd]/(80/CHARlevels[charInd])
		EXPupdate = obtainedEXP + CHARexp[charInd]
		CHARexp[0] = EXPupdate
		print(CHARexp[0])
def easyEnemy():
	if curChar == "Lindus":
		charInd = CHAR.index("Lindus")
		obtainedEXP = CHARexp[charInd]/(90/CHARlevels[charInd])
		EXPupdate = obtainedEXP + CHARexp[charInd]
		CHARexp[0] = EXPupdate
		print(CHARexp[0])
hardRect=Rect(0,0,80,80)
mediumRect=Rect(100,0,80,80)
easyRect=Rect(200,0,80,80)		
while running:
	for evt in event.get(): 
		if evt.type == QUIT:
			running = False
		if evt.type == MOUSEBUTTONDOWN:
			if evt.button == 3:
				print("Lindus: ",CharStats)
				print("EXP: ",CHARexp)

			if evt.button == 1:
				if enemy == "Hard":
					print("Hard")
					hardEnemy()
				elif enemy == "Medium":
					print("Amateur")
					amateurEnemy()
				elif enemy == "Easy":		
					print("Easy")
					easyEnemy()
		if evt.type == KEYDOWN:
			if evt.key == K_ESCAPE:
				running=False      
	####
	mx,my=mouse.get_pos()
	mb=mouse.get_pressed()
	####
	if mb[0]:
		if hardRect.collidepoint(mx,my):
			enemy="Hard"
		if mediumRect.collidepoint(mx,my):
			enemy="Medium"
		if easyRect.collidepoint(mx,my):
			enemy="Easy"		
	####
	draw.rect(screen, (255,0,0), hardRect)
	draw.rect(screen, (255,255,0), mediumRect)
	draw.rect(screen, (0,255,0), easyRect)
	display.flip() 
quit() 