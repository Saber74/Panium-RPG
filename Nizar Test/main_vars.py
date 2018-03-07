# main_vars.py
from pygame import * ; from pygame import gfxdraw as alpha ; from main_vars import *
size = (800,700)
invisSurface = Surface(size,SRCALPHA)
screen = display.set_mode(size)
myClock = time.Clock()
# screen.set_alpha(0)
# screen.fill((255,255,255))
running = True
every = [(0,0),(800,0),(800,600),(750,600),(750,50),(0,50)]
crowWalkForward, crowWalkDown, crowWalkRight, crowWalkLeft = [], [], [], []
ravenWalkForward, ravenWalkDown, ravenWalkRight, ravenWalkLeft = [], [], [], []
voldeWalkBack=[]
voldeAnimation=[]
voldeAnimation2=[]
transitionIntoBattle=[]
activateAnimation=False
ani=0
selectedChar=0
sx, sy = 0, 500
ccol = 0
counter = 0
moving = False
check = False
frame = 0
pressed = "NULL"
speed = 2
invisSurface.fill((255,255,255,0))