import time
import board
import microcontroller
import displayio
import busio
from analogio import AnalogIn
from digitalio import DigitalInOut
import neopixel
import adafruit_adt7410
from adafruit_bitmap_font import bitmap_font
from adafruit_display_text.label import Label
from adafruit_button import Button
import adafruit_touchscreen
from adafruit_pyportal import PyPortal


pyportal = PyPortal()
pyportal.set_background('/images/BEV_Logo.bmp')
pyportal.play_file('/sounds/SoundStart.wav')

WHITE = 0xffffff
RED = 0xff0000
YELLOW = 0xffff00
GREEN = 0x00ff00
BLUE = 0x0000ff
PURPLE = 0xff00ff
BLACK = 0x000000

#Define groups
main = displayio.Group(max_size=3)
mainScreen = displayio.Group(max_size=3)
screen1 = displayio.Group(max_size=3)
screen2 = displayio.Group(max_size=3)

#Import images
image_file1 = open("/images/speed.bmp", "rb")
image1 = displayio.OnDiskBitmap(image_file1)
image_sprite1 = displayio.TileGrid(image1, pixel_shader=displayio.ColorConverter())
image_sprite1.x = 0
image_sprite1.y = 0

image_file2 = open("/images/needle.bmp", "rb")
image2 = displayio.OnDiskBitmap(image_file2)
image_sprite2 = displayio.TileGrid(image2, pixel_shader=displayio.ColorConverter())
image_sprite2.x = 60
image_sprite2.y = 275

mainScreen.append(image_sprite1)
mainScreen.append(image_sprite2)


#Setup pinouts
pin1 = AnalogIn(board.D4)
pin2 = AnalogIn(board.D3)

#Text box stuff
font = bitmap_font.load_font("/fonts/Bookman_Old_Style.bdf")
font.load_glyphs(b'abcdefghjiklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890- ()')

TABS_X = 5
TABS_Y = 50

minOnesValue = 0
minTensValue = 0
secOnesValue = 0
secTensValue = 0

timeGroup = displayio.Group(max_size=1)

timeSinceOn1 = Label(font, text="Active: " + str(minTensValue) + str(minOnesValue) + ":" + str(secTensValue) + str(secOnesValue), color = BLACK, max_glyphs=200, scale=1)
timeSinceOn2 = Label(font, text="Active: " + str(minTensValue) + str(minOnesValue) + ":" + str(secTensValue) + str(secOnesValue), color = WHITE, max_glyphs=200, scale=1)
timeSinceOn3 = Label(font, text="Active: " + str(minTensValue) + str(minOnesValue) + ":" + str(secTensValue) + str(secOnesValue), color = WHITE, max_glyphs=200, scale=1)
timeSinceOn1.x = TABS_X + 365
timeSinceOn1.y = TABS_Y - 35
timeSinceOn2.x = TABS_X + 365
timeSinceOn2.y = TABS_Y - 35
timeSinceOn3.x = TABS_X + 365
timeSinceOn3.y = TABS_Y - 35
#timeGroup.append(timeSinceOn)


number = 0;
'''
feed1_label = Label(font, text=str(number), color = RED, max_glyphs=200, scale=4)
feed1_label.x = TABS_X + 50
feed1_label.y = TABS_Y + 100
myGroup.append(feed1_label)
'''

#board.DISPLAY.show(myGroup)
#board.DISPLAY.show(timeGroup)

#Add all screens to main display group
main.append(mainScreen)
main.append(screen1)
main.append(screen2)

#Add timer to all screens
mainScreen.append(timeSinceOn1)
screen1.append(timeSinceOn2)
screen2.append(timeSinceOn3)

counter = 0

#Time stuff
measure1 = time.time()
measure2 = time.time()
measure3 = time.time()
measure4 = time.time()

#cwd=("/" + __file__).rsplit('/',1)[0]
#PyPortal.set_background(cwd+'/images/white_background.bmp')



#switch between screens
ms = False
s1 = True
s2 = False

# ------------- Layer Functions ------------- #
# Hide a given Group by removing it from the main display Group.
def hideLayer(i):
    try:
        main.remove(i)
    except ValueError:
        pass
# Show a given Group by adding it to the main display Group.
def showLayer(i):
    try:
        main.append(i)
    except ValueError:
        pass


#Show screen
board.DISPLAY.show(main)

# ------------- Code Loop ------------- #
while True:
    if (ms):
        hideLayer(screen1)
        hideLayer(screen2)
        showLayer(mainScreen)
        ms = False
    elif (s1):
        hideLayer(mainScreen)
        hideLayer(screen2)
        showLayer(screen1)
        s1 = False
    elif (s2):
        hideLayer(mainScreen)
        hideLayer(screen1)
        showLayer(screen2)
        s2 = False
        

    #board.DISPLAY.show(myGroup)
    #Test on-screen counter
    '''
    counter = counter + 1
    board.DISPLAY.show(myGroup)
    board.DISPLAY.show(timeGroup)
    if (number < 9 and measure2 - measure1 >= 1):
        number = number + 1
        myGroup.pop()

        measure1 = measure2
        measure2 = time.time()


        feed1_label = Label(font, text=str(number), color = RED, max_glyphs=200, scale=4)
        feed1_label.x = TABS_X + 50
        feed1_label.y = TABS_Y + 100
        myGroup.append(feed1_label)

        counter = 0
    elif (number == 9 and measure2 - measure1 >= 1):
        number = 0
        myGroup.pop()

        measure1 = measure2
        measure2 = time.time()

        feed1_label = Label(font, text=str(number), color = RED, max_glyphs=200, scale=4)
        feed1_label.x = TABS_X + 50
        feed1_label.y = TABS_Y + 100
        myGroup.append(feed1_label)

        counter = 0
    
    measure2 = time.time()
'''
    #Active timer
    '''
    if (measure4 - measure3 >= 1):
        measure3 = measure4
        measure4 = time.time()
        secOnesValue = secOnesValue + 1
        timeGroup.pop()
        timeSinceOn = Label(font, text="Active: " + str(minTensValue) + str(minOnesValue) + ":" + str(secTensValue) + str(secOnesValue), color = WHITE, max_glyphs=200, scale=1)
        timeGroup.append(timeSinceOn)
        if (secOnesValue == 10):
            secTensValue = secTensValue + 1
            secOnesValue = 0
            timeGroup.pop()
            timeSinceOn = Label(font, text="Active: " + str(minTensValue) + str(minOnesValue) + ":" + str(secTensValue) + str(secOnesValue), color = WHITE, max_glyphs=200, scale=1)
            timeGroup.append(timeSinceOn)
        if (secTensValue == 6):
            minOnesValue = minOnesValue + 1
            secTensValue = 0
            timeGroup.pop()
            timeSinceOn = Label(font, text="Active: " + str(minTensValue) + str(minOnesValue) + ":" + str(secTensValue) + str(secOnesValue), color = WHITE, max_glyphs=200, scale=1)
            timeGroup.append(timeSinceOn)
        if (minOnesValue == 10):
            minTensValue = minTensValue + 1
            minOnesValue = 0
            timeGroup.pop()
            timeSinceOn = Label(font, text="Active: " + str(minTensValue) + str(minOnesValue) + ":" + str(secTensValue) + str(secOnesValue), color = WHITE, max_glyphs=200, scale=1)
            timeGroup.append(timeSinceOn)
    timeSinceOn.text="hi"
    
    timeSinceOn.x = TABS_X + 365
    timeSinceOn.y = TABS_Y - 35
    measure4 = time.time()
    '''

    #Active timer
    if (measure4 - measure3 >= 1):
        measure3 = measure4
        secOnesValue = secOnesValue + 1
        if (secOnesValue == 10):
            secTensValue = secTensValue + 1
            secOnesValue = 0
            #test = image_file1.rotate(45)
        if (secTensValue == 6):
            minOnesValue = minOnesValue + 1
            secTensValue = 0
        if (minOnesValue == 10):
            minTensValue = minTensValue + 1
            minOnesValue = 0
    timeSinceOn1.text = "Active: " + str(minTensValue) + str(minOnesValue) + ":" + str(secTensValue) + str(secOnesValue)
    timeSinceOn2.text = "Active: " + str(minTensValue) + str(minOnesValue) + ":" + str(secTensValue) + str(secOnesValue)
    timeSinceOn3.text = "Active: " + str(minTensValue) + str(minOnesValue) + ":" + str(secTensValue) + str(secOnesValue)
    measure4 = time.time()
