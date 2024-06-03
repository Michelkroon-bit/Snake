from machine import Pin
from neopixel import NeoPixel
import random
import time

maxX, maxY = (32, 16)

# Initialize NeoPixel
pixel_pin = Pin(28, Pin.OUT)
pixels = NeoPixel(pixel_pin, maxX * maxY)

# Initialize buttons
button_up = Pin(0, Pin.IN, Pin.PULL_UP)
button_down = Pin(1, Pin.IN, Pin.PULL_UP)
button_left = Pin(2, Pin.IN, Pin.PULL_UP)
button_right = Pin(3, Pin.IN, Pin.PULL_UP)

# Colors
COLOUR_BACKGROUND = (100, 100, 100)
COLOUR_RED = (255, 0, 0)
COLOUR_GREEN = (0, 255, 0)
COLOUR_BLUE = (0, 0, 255)
COLOUR_WHITE = (255, 255, 255)
COLOUR_BLACK = (0, 0, 0)
COLOUR_PURPLE = (160, 32, 240)
COLOURS = (COLOUR_GREEN, COLOUR_WHITE, COLOUR_BLACK, COLOUR_PURPLE)

# Helper functions
def getRandomPos(maxX, maxY, notX=-1, notY=-1):
    x = random.randint(0, maxX - 1)
    y = random.randint(0, maxY - 1)
    if x == notX or y == notY:
        return getRandomPos(maxX, maxY, notX, notY)
    return x, y

def xy_to_index(x, y, num_columns):
    if y % 2 == 0:  # Even rows
        index = y * num_columns + x
    else:  # Odd rows
        index = (y + 1) * num_columns - 1 - x
    return index

def drawGame(positions):
    for x, y, color in positions:
        index = xy_to_index(x, y, maxX)
        pixels[index] = color
    pixels.write()

def change_direction():
    global moveX, moveY
    if not button_up.value():
        moveX, moveY = (0, -1)
    elif not button_down.value():
        moveX, moveY = (0, 1)
    elif not button_left.value():
        moveX, moveY = (-1, 0)
    elif not button_right.value():
        moveX, moveY = (1, 0)

def checkCollision(snake):
    head = snake[0]
    body = snake[1:]
    return head in body

# Initialize game variables
posX = maxX // 2
posY = maxY // 2
objectX, objectY = getRandomPos(maxX, maxY, posX, posY)
moveX, moveY = (1, 0)
colour = COLOUR_RED
snake = [(posX, posY)]
speed = 10
counter = 0
snake_length = 1

while True:
    change_direction()

    if counter % speed == 0:
        posX += moveX
        posY += moveY
        posX %= maxX
        posY %= maxY

        snake.insert(0, (posX, posY))

        if len(snake) > snake_length:
            snake.pop()

        if checkCollision(snake):
            snake = [(posX, posY)]
            snake_length = 1
            colour = COLOUR_RED
            posX, posY = maxX // 2, maxY // 2
            objectX, objectY = getRandomPos(maxX, maxY, posX, posY)

        if posX == objectX and posY == objectY:
            colour = random.choice(COLOURS)
            snake_length += 1
            objectX, objectY = getRandomPos(maxX, maxY, posX, posY)

        positions = [(objectX, objectY, COLOUR_GREEN)] + [(x, y, colour) for x, y in snake]
        drawGame(positions)

    counter += 1
    time.sleep(0.05)
