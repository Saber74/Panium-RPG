from pygame import * 
size=(800,600)
screen = display.set_mode(size)
screen.fill((255,255,255)) 
thickness=5                               
running = True
while running:
    for evt in event.get(): 
        if evt.type == QUIT:
            running = False
        if evt.type == MOUSEBUTTONDOWN:
            if evt.button == 3:
                for i in range(3):
                    LindusStatsNum[i] += 1
                print("Lindus: ",LindusStats)
                print("Stats: ",LindusStatsNum)

            if evt.button == 1:
                print("Lindus: ",LindusStats)
                print("Stats: ",LindusStatsNum) 
        
        if evt.type == KEYDOWN:
            if evt.key == K_ESCAPE:
                running=False       

    mx,my=mouse.get_pos()
    mb=mouse.get_pressed()

    draw.circle(screen,(255,0,0),(100,100),100)

    display.flip() 
quit() 