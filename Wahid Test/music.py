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