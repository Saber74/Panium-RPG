# main_vars.py
from pygame import * ; from pygame import gfxdraw as alpha ; from main_vars import * ; import os ; from pytmx import *
from pyscroll import * #; from pyscroll import 
size = (1366,768)
invisSurface = Surface(size,SRCALPHA)
os.environ['SDL_VIDEO_WINDOW_POS'] = 'FULLSCREEN'
screen = display.set_mode(size)
myClock = time.Clock()
# screen.set_alpha(0)
# screen.fill((255,255,255))
running = True
test = [[438, 245], [436, 330], [490, 331], [493, 245]]
test2 = [[628, 371], [628, 396], [685, 396], [683, 372]]
lists = [test,test2]
crowWalkForward, crowWalkDown, crowWalkRight, crowWalkLeft = [], [], [], []
ravenWalkForward, ravenWalkDown, ravenWalkRight, ravenWalkLeft = [], [], [], []
cf, cd, cr, cl = crowWalkForward, crowWalkDown, crowWalkRight, crowWalkLeft
sx, sy = 683, 384
ccol = 0
counter = 0
moving = False
frame = 0
pressed = "NULL"
speed = 0
invisSurface.fill((255,255,255,0))
x_diff = y_diff = 0
x = y = 0