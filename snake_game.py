#from pyMatrix import pyMatrix
from neopixel import NeoPixel
import random

maxX, maxY = (32, 16)

COLOUR_BACKGROUND = (100, 100, 100)  # (R, G, B)
COLOUR_RED = (255, 0, 0)
COLOUR_GREEN = (0, 255, 0)
COLOUR_BLUE = (0, 0, 255)
COLOUR_WHITE = (255, 255, 255)
COLOUR_BLACK = (0, 0, 0)
COLOUR_PURPLE = (160, 32, 240)
COLOURS = (COLOUR_GREEN, COLOUR_WHITE, COLOUR_BLACK , COLOUR_PURPLE )


def getRandomPos(maxX, maxY, notX=-1, notY=-1):
    x = random.randint(0, maxX - 1)
    y = random.randint(0, maxY - 1)
    if x == notX or y == notY:
        return getRandomPos(maxX, maxY, notX, notY)
    return x, y

def xy_to_index(x, y, num_columns):
    """
    Converteert x- en y-coördinaten naar een index die overeenkomt met de positie van de LED in de strip.

    Parameters:
    - x: De x-coördinaat (kolomnummer, nul-gebaseerd).
    - y: De y-coördinaat (rijnummer, nul-gebaseerd).
    - num_columns: Het aantal kolommen in de LED-matrix.

    Return:
    - index: De index die overeenkomt met de positie van de LED in de strip.
    """
    # Bereken de index op basis van de rij- en kolomnummers
    if y % 2 == 0:  # Even rijen
        index = y * num_columns + x
    else:  # Oneven rijen
        index = (y + 1) * num_columns - 1 - x
    return index

def drawGame(positions):
    for x,y,color in positions:
        index =xy_to_index(x,y,8)
        neopixel[index] = color
        neopixel.write()
    
    
    
def change(keys: list, x, y, colour):
    if 27 in keys:  # esc
        game.quit()
    if ord("q") in keys:
        colour = random.choice(COLOURS)
    elif ord("s") in keys:
        x, y = (0, 1)
    elif ord("w") in keys:
        x, y = (0, -1)
    elif ord("a") in keys:
        x, y = (-1, 0)
    elif ord("d") in keys:
        x, y = (1, 0)
    return x, y, colour


_oldMilliseconds = None


def moveObject(milliseconds: int):
    global objectX, objectY, _oldMilliseconds
    if _oldMilliseconds is None:
        _oldMilliseconds = milliseconds

    if milliseconds - _oldMilliseconds > 8000:
        objectX, objectY = getRandomPos(maxX, maxY, posX, posY)
        _oldMilliseconds = milliseconds
        
TOTAL_SCREEN = (maxX,maxY)
playing_field = (22 , maxY)

#game = pyMatrix(maxX, maxY, colourBackground=COLOUR_BACKGROUND, timed_callback=moveObject)
posX = maxX // 2
posY = maxY // 2
objectX, objectY = getRandomPos(maxX, maxY, posX, posY)

moveX, moveY = (1, 0)
colour = COLOUR_RED
snake = [(posX, posY)]  # Initialize snake with one segment
speed = 10
counter = 0
snake_length = 1  # Initial length of the snake

def checkCollision(snake):
    head = snake[0]
    body = snake[1:]
    if head in body:
        return True  # Collision occurred
    return False

while True:
    if posX == objectX and posY == objectY:
        colour = random.choice(COLOURS)         
        snake_length += 1  # Increase snake length when it eats an object
        objectX, objectY = getRandomPos(maxX, maxY, posX, posY)  # Move the object

    if posX == objectX and posY == objectY and colour == COLOUR_PURPLE:
        quit()
    
    if colour == COLOUR_GREEN:
        speed = 10
    if colour == COLOUR_BLACK:
        speed = 5
    if colour == COLOUR_WHITE:
        speed = 20


    keys = []#game.getPressedKey()
    moveX, moveY, colour = change(keys, moveX, moveY, colour)

    if counter % speed == 0:
        new_posX = posX + moveX
        new_posY = posY + moveY
        if game.isPosAllowed(new_posX, new_posY):
            snake_head = snake.insert(0, (new_posX, new_posY))  
            if len(snake) > snake_length:
                snake.pop()
            posX = new_posX
            posY = new_posY
        
    if checkCollision(snake):
        snake = [(posX, posY)]
        quit()
        #snake_length = 1  # Reset de lengte van de slang
        
    positions = [(objectX, objectY, COLOUR_GREEN), (posX, posY, colour)]
    positions.extend([(x, y, colour) for x, y in snake])
    #game.
    drawGame(positions)

    counter += 1

#objectX = apple
#posX = snake 
