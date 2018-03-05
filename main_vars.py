# main_vars.py
from pygame import * ; from pygame import gfxdraw as alpha ; from main_vars import *
size = (800,600)
screen = display.set_mode(size)
myClock = time.Clock()
screen.set_alpha(255)
screen.fill((255,255,255))
running = True
every = [(0,0),(800,0),(800,600),(750,600),(750,50),(0,50)]
crowWalkForward, crowWalkDown, crowWalkRight, crowWalkLeft = [], [], [], []
sx, sy = 0, 500
ccol = 0
counter = 0
moving = False
frame = 0
pressed = "NULL"
speed = 2
invisSurface = Surface(size,SRCALPHA)
invisSurface.fill((0,0,0,255))