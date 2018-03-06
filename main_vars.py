# main_vars.py
from pygame import * ; from pygame import gfxdraw as alpha ; from main_vars import *
size = (800,600)
invisSurface = Surface(size,SRCALPHA)
screen = display.set_mode(size)
myClock = time.Clock()
# screen.set_alpha(0)
# screen.fill((255,255,255))
running = True
every = [(0,0),(800,0),(800,600),(750,600),(750,50),(0,50)]
every1 = [(0,0),(0,800),(600,800),(600,750),(50,750),(50,0)]
crowWalkForward, crowWalkDown, crowWalkRight, crowWalkLeft = [], [], [], []
ravenWalkForward, ravenWalkDown, ravenWalkRight, ravenWalkLeft = [], [], [], []
cf, cd, cr, cl = crowWalkForward, crowWalkDown, crowWalkRight, crowWalkLeft
sx, sy = 100, 500
ccol = 0
counter = 0
moving = False
frame = 0
pressed = "NULL"
speed = 2
invisSurface.fill((255,255,255,0))