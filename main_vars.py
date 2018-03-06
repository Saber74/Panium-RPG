# main_vars.py
from pygame import * ; from pygame import gfxdraw as alpha ; from main_vars import *
size = (800,600)
invisSurface = Surface(size,SRCALPHA)
screen = display.set_mode(size)
myClock = time.Clock()
# screen.set_alpha(0)
# screen.fill((255,255,255))
running = True
riverBank = [(577,234), (694,233), (696,331), (740,331), (743,358), (697,361), (692,448), (652,452), (649,488), (630,498), (603,497), (591,546), (556,544), (555,596), (290,596), (298,524), (339,514), (349,476), (382,473), (397,433), (480,428), (491,388), (518,388), (535,353), (529,328), (529,311), (537,302), (551,297), (566,294), (577,283), (579,258), (576,238)]
riverBank2 = [(580, -80), (579, 131), (695, 137), (696, -80)]
test = []
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
