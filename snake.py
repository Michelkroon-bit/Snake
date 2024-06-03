import random
COMPUTER = True
# ----------------------------------------------
# from machine import Pin
# Change for NepPixel
# The next line must be commented when work with the NepPixel
# and Neopixel should be imported and initiazed
if COMPUTER:
    from libraries.computer.pyMatrix import pyMatrix
else:
    from machine import Pin
    from neopixel import NeoPixel
# ----------------------------------------------

COLOUR_BACKGROUND = (100, 100, 100)  # (R, G, B)
COLOUR_RED        = (255,   0,   0)
COLOUR_GREEN      = (  0, 255,   0)
COLOUR_BLUE       = (  0,   0, 255)
COLOUR_WHITE      = (255, 255, 255)
COLOURS = (COLOUR_RED, COLOUR_GREEN,COLOUR_BLUE, COLOUR_WHITE )

def getRandomPos(maxX, maxY, notX = -1, notY=-1):
    x = random.randint(0,maxX-1)
    y = random.randint(0,maxY-1)
    if x == notX or y == notY:
        return getRandomPos(maxX, maxY, notX, notY)
    return x,y


def change(keys: list, x,y, colour):
#   if any(keys):
#     print(keys)
    if 27 in keys:	 # esc
        game.quit()
    if ord("c") in keys:
        colour = random.choice(COLOURS)
    elif 1073741905 in keys:
        x, y = ( 0,  1)
    elif 1073741906 in keys:
        x, y = ( 0, -1)
    elif 1073741904 in keys:
        x, y = (-1,  0)
    elif 1073741903 in keys:
        x, y = ( 1,  0)
    return x, y, colour

_oldMilliseconds = None
def moveObject(milliseconds:int):
    global objectX, objectY, _oldMilliseconds
    if _oldMilliseconds is None:
        _oldMilliseconds = milliseconds

    if milliseconds - _oldMilliseconds > 8000:
        objectX, objectY = getRandomPos(maxX, maxY, posX, posY)
        _oldMilliseconds = milliseconds


maxX, maxY = (32,16)

# ----------------------------------------------
# Change for NepPixel
if COMPUTER:
    game = pyMatrix(maxX, maxY, colourBackground=COLOUR_BACKGROUND, speed=5, timed_callback=moveObject)
    game.clear((255,0,0))
else:
    pixel_pin = Pin(28, Pin.OUT)
    pixels = NeoPixel(pixel_pin, maxX * maxY)

    # Initialize buttons
    button_up   = Pin(0, Pin.IN)
    button_down = Pin(1, Pin.IN)
    button_left = Pin(2, Pin.IN)
    button_right = Pin(3, Pin.IN)
# ----------------------------------------------
    
posX = maxX // 2
posY = maxY // 2
objectX, objectY = getRandomPos(maxX, maxY, posX, posY)
moveX, moveY = (1, 0)
colour = COLOUR_RED
while True:
    # ----------------------------------------------
    # Change for for real buttons
    # Read the machine.Pin when working with buttons on the Pico
    if COMPUTER:
        keys = game.getPressedKey()
    else:
        keys = []  
    # ----------------------------------------------
        
    moveX, moveY, colour = change(keys, moveX, moveY, colour)

    # ----------------------------------------------
    # Change for NepPixel
    # Create a function that checks if the position is allowed
    if COMPUTER:
        if game.isPosAllowed(posX + moveX, posY + moveY):
            # ------------------------------------------
            posX += moveX
            posY += moveY
    else:
        if 0 <= posX + moveX < maxX and 0 <= posY + moveY < maxY:
            posX += moveX
            posY += moveY
            
    if objectX == posX and objectY == posY:
        objectX, objectY = getRandomPos(maxX, maxY, posX, posY)

    positions =[(objectX, objectY, COLOUR_GREEN)
               , (posX, posY, colour)
               ]
    # ----------------------------------------------
    # Change for the Neopixel
    # something like :
   
    if COMPUTER:
        game.showList(positions )
    else:
        def xy_to_index(x, y, num_columns):
            if y % 2 == 0:  # Even rows
                index = y * num_columns + x
            else:  # Odd rows
                index = (y + 1) * num_columns - 1 - x
            return index

        for x, y, color in positions:
            index = xy_to_index(x, y, maxX)
            pixels[index] = color
        pixels.write()
        
    # ----------------------------------------------
