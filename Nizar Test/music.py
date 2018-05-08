from pygame import *
init()
mixer.init() 
mixer.set_num_channels(4) ###setting number of channels up
channel1=mixer.Channel(0) ##declaring each channel, makes it easier to control them
channel2=mixer.Channel(1)
channel3=mixer.Channel(2)
soundGrandma=mixer.Sound("Music/GRANDMA DESTRUCTION.wav") ###creating a sound object that can be played in the channel ##this only works with wav and of something
channel1.play(soundGrandma,-1) ###playing the actual "Sound" the number is the loop which is infinity
channel1.set_volume(0.1) ##to set volume for things so you don't get deaf
BossFight=mixer.Sound("Music/Starting.wav") 
channel2.play(BossFight,-1) ##playing on the second channel
size=(800,600)
screen = display.set_mode(size) 
                                 
running = True
while running:
    for evt in event.get():  
        if evt.type == QUIT: 
            running = False

    mx,my=mouse.get_pos()
    mb=mouse.get_pressed()
                
    
    display.flip() 
quit()