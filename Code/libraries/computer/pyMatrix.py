
"""
    about : pyMatrix is a pyGame matrix of n x m pixels
    Version : 1.0.2
    Date    : 11 April 2024
    
    0.3.0 : Breaking change with version 0.2.0 : drawGame is renamed to showList
    1.0.1 : IControl added
    1.0.2 : ShowMatrix 2 matrixes would only remember position of second one.
"""

import sys
sys.path.insert(0, '..//')
sys.path.insert(1, './/')
sys.path.insert(2, './/libraries/')
sys.path.insert(3, './/libraries/computer')

from IDisplay import IDisplay
from IInput import IInput
from IControl import IControl
import pygame


class pyMatrix(IDisplay, IInput, IControl):
    """
        Matrix with dimensions width, height to simulate a Neopixel display
        This version uses X, Y position, a neopixel matrix works with an index number.
    """
    LINE_WIDTH = 3
    RESIZE_SCREEN_PERCENTAGE = 0.8
    TIMER_EVENT = pygame.USEREVENT+1
    

    def __init__(self, width=32, height=16, colourBackground=(100, 100, 100)
                 , caption='Pixel matrix', speed=60, onlyShowNewPixels=True, timed_callback=None, timerInterval=1000):
        """
        init function of the class
        
        onlyShowNewPixels : All old pixels are automatically cleared when not in new set
        callbackTimer : callback function with : def functionName(milliseconds:int)
        """
        self._timed_callback = timed_callback
        self._timerInterval = timerInterval
        self._onlyShowNewPixels = onlyShowNewPixels
        self._screen = pygame.display.set_mode()
        self.pixelsX, self.PixelsY = self._screen.get_size()
        self.pixelsX *= self.RESIZE_SCREEN_PERCENTAGE
        self.PixelsY *= self.RESIZE_SCREEN_PERCENTAGE
        self._oldPositions = set()
        self._maxX = width
        self._maxY = height
        self._fpSpeed = speed
        self._colourBackground = colourBackground
        self._squareSize       = min((self.pixelsX / self._maxX) - self.LINE_WIDTH * ((self.pixelsX + 1) / self.pixelsX)
                                    ,(self.PixelsY / self._maxY) - self.LINE_WIDTH * ((self.PixelsY + 1) / self.pixelsX)
                                    )
        self._resolution 	  = ((self._squareSize + self.LINE_WIDTH) * self._maxX
                                ,(self._squareSize + self.LINE_WIDTH) * self._maxY
                                )

        pygame.init()
        pygame.time.set_timer(pyMatrix.TIMER_EVENT, self._timerInterval)
        self._screen = pygame.display.set_mode(self._resolution)

        self._clock = pygame.time.Clock()  # to set max FPS
        pygame.display.set_caption(caption)
        self._drawScreen()

    def isPosAllowed(self, posX:int, posY:int) -> bool:
        """
            True if the PosX, posY is within the boundaries of the matrix
        """
        if posX < 0 or posY < 0:
            return False
        if posX >= self._maxX:
            return False
        if posY >= self._maxY:
            return False
        return True

    def getEvents(self):
        """
            Get the raise events
        """
        self._clock.tick(self._fpSpeed)  # max FPS = 60
        return pygame.event.get()
    

    """
                         ___ ____            _             _ 
                        |_ _/ ___|___  _ __ | |_ _ __ ___ | |
                         | | |   / _ \| '_ \| __| '__/ _ \| |
                         | | |__| (_) | | | | |_| | | (_) | |
                        |___\____\___/|_| |_|\__|_|  \___/|_|
    """
    def setSpeed(self, speed: int):
        """
            Change the speed
        """
        self._fpSpeed = speed


    def getSpeed(self) -> int:
        """
        """
        return self._fpSpeed

    
    def quit(self) -> None:
        """
            quit the matrix and the program
        """
        pygame.quit()
        quit()



    """
                         ___ ____  _           _             
                        |_ _|  _ \(_)___ _ __ | | __ _ _   _ 
                         | || | | | / __| '_ \| |/ _` | | | |
                         | || |_| | \__ \ |_) | | (_| | |_| |
                        |___|____/|_|___/ .__/|_|\__,_|\__, |
                                        |_|            |___/ 
    """
    def getWidthHeight(self) -> tuple[int, int]:
        """
            IDisplay
            return the width and height (in positions)  of the matrix
        """
        return self._maxX, self._maxY
    
    
    def clear(self, color:tuple[int,int,int] = None) -> None:
        """
            IDisplay
            clear the complete matrix
        """
        if color is None:
            self.showList([], animate=True)
        else:
            pixels = []
            for y in range(self._maxY):
                for x in range(self._maxX):
                    pixels.append((x,y,color))
                    
            self.showList(set(pixels), animate=True)


    def showMatrix(self, matrix:tuple[tuple[tuple[int,int,int]]], offsetX:int = 0, offsetY:int = 0) -> None:
        """
        IDisplay
        update the matrix with a input matrix of rows, columns and color of the pixel
        R = (255,0,0)
        B = (  0,0,0)
        e.g. [ [R, B, B], [B, R, B], [B, B, R] ]
        offsetX : x-offset of the matrix on the pyMatrix screen
        offsetY : y-offset of the matrix on the pyMatrix screen
        """        
        region = None
        for y, line in enumerate(matrix):
            for x, color in enumerate(line):
                x1 = offsetX + x
                y1 = offsetY + y
                self._oldPositions.add((x1, y1))
                
                if 0 == color:
                    color = self._colourBackground                
                geometry = self._draw_square(x1, y1, color)
                region = self._updateRegion(geometry, region)

        geometry = self._convertRegion2Geometry(region)
        pygame.display.update(geometry)


    def showPixels(self, positions: tuple[int, int, tuple[int,int,int]], colour:tuple[int,int,int]=None) -> None:
        """
            IDisplay
            Only show new pixels, don't disturb the old ones.
        """
        region = None
        newCoordinates = set((p[0],p[1]) for p in positions )
        for x,y,c in positions:
            if colour is not None:
                if colour in ( (-1, -1, -1), (0, 0, 0) ):
                    c = self._colourBackground
                else:
                    c = colour
            geometry = self._draw_square(x, y, c)
            region = self._updateRegion(geometry, region)

        if region is not None:
            geometry = self._convertRegion2Geometry(region)
            pygame.display.update(geometry)
        self._oldPositions = newCoordinates

    def showList(self, positions: tuple[int, int, tuple[int,int,int]], colour:tuple[int,int,int]=None, animate:bool=False) -> None:
        """
            IDisplay
            position is a list of (x, y, color)
            if color is None, the background color is reset.
            R = (255,  0,  0)
            B = (  0,  0,255)
            e.g. position = [ (1,1,R), (10,3,B) ]
        """
        
        # ---------------------
        # pixels not in the new list are turned off
        # ---------------------
        newCoordinates = set((p[0],p[1]) for p in positions )
        region = None
        # reset pixels that are no longer used
        if self._onlyShowNewPixels:
            for xy in self._oldPositions:
                if xy not in newCoordinates:
                    geometry = self._draw_square(xy[0], xy[1], self._colourBackground)
                    if animate:
                        pygame.display.update(geometry)
                    else:
                        region = self._updateRegion(geometry, region)
        self._oldPositions = newCoordinates
        
        # ---------------------
        # show the new pixels
        # ---------------------
        for x,y,c in positions:
            if colour is not None:
                if colour in ( (-1, -1, -1), (0, 0, 0) ):
                    c = self._colourBackground
                else:
                    c = colour
            geometry = self._draw_square(x, y, c)
            if animate:
                pygame.display.update(geometry)
            else:
                region = self._updateRegion(geometry, region)

        if not animate and region is not None:
            geometry = self._convertRegion2Geometry(region)
            pygame.display.update(geometry)
        

    def refresh(self) -> None:
        """            
            IDisplay : refresh display
        """
        self._clock.tick(self._fpSpeed)  # max FPS = 60

        for event in self.getEvents():
            if event.type == pygame.QUIT:
                self.quit()
            elif event.type == pyMatrix.TIMER_EVENT:
                if self._timed_callback is not None:
                    self._timed_callback(pygame.time.get_ticks())



    """
                         ___ ___                   _   
                        |_ _|_ _|_ __  _ __  _   _| |_ 
                         | | | || '_ \| '_ \| | | | __|
                         | | | || | | | |_) | |_| | |_ 
                        |___|___|_| |_| .__/ \__,_|\__|
                                  |_|              
    """
    def getPressedKey(self) -> tuple[int]:
        """
            IInput : input a key
            return the keys pressed (ascii value)
        """
        keys = []
        for event in self.getEvents():
            if event.type == pygame.KEYDOWN:
                keys.append(event.key)
            elif event.type == pygame.QUIT:
                self.quit()
            elif event.type == pyMatrix.TIMER_EVENT:
                if self._timed_callback is not None:
                    self._timed_callback(pygame.time.get_ticks())
        return keys



    """
             ____       _            _          __                  _   _                 
            |  _ \ _ __(_)_   ____ _| |_ ___   / _|_   _ _ __   ___| |_(_) ___  _ __  ___ 
            | |_) | '__| \ \ / / _` | __/ _ \ | |_| | | | '_ \ / __| __| |/ _ \| '_ \/ __|
            |  __/| |  | |\ V / (_| | ||  __/ |  _| |_| | | | | (__| |_| | (_) | | | \__ \
            |_|   |_|  |_| \_/ \__,_|\__\___| |_|  \__,_|_| |_|\___|\__|_|\___/|_| |_|___/
    """
    def _updateRegion(self, geometry, updateRegion):
        """

        """
        if updateRegion is None:
            updateRegion = [geometry[0], geometry[1], geometry[0] + geometry[2], geometry[1] + geometry[3]]
        else:
            updateRegion[0] = min(geometry[0], updateRegion[0])
            updateRegion[1] = min(geometry[1], updateRegion[1])
            updateRegion[2] = max(geometry[0] + geometry[2], updateRegion[2])
            updateRegion[3] = max(geometry[1] + geometry[3], updateRegion[3])
        return updateRegion

    def _convertRegion2Geometry(self, region):
        """
        """
        return (region[0], region[1],
                region[2] - region[0], region[3] - region[1])


    def _getPixelPos(self, posX, posY):
        """
            from the position posX, posY calculate and return the position in pixels.
        """
        return (self.LINE_WIDTH * (posX + 1) + self._squareSize * posX,
                self.LINE_WIDTH * (posY + 1) + self._squareSize * posY)


    def _draw_square(self, posX, posY, colour=None):
        """
            Draw a square on the PosX, PosY location with a given colod
        """
        if colour is None:
            colour = self._colourBackground
        x, y = self._getPixelPos(posX, posY)
        geometry = (x, y, self._squareSize, self._squareSize)
        pygame.draw.rect(self._screen, colour, geometry)
        return geometry


    def _draw_squares(self):
        """
            Draw all the squares on the screen
        """
        for y in range(self._maxY):
            for x in range(self._maxX):
                self._draw_square(x, y)


    def _drawScreen(self):
        """
            Redraw the complete screen
        """
        self._screen.fill((0, 0, 0))  # Fill screen with black color.
        self._draw_squares()
        pygame.display.flip()  # Update the screen.




"""
                         _____ _____ ____ _____      __  ____  _____ __  __  ___  
                        |_   _| ____/ ___|_   _|    / / |  _ \| ____|  \/  |/ _ \ 
                          | | |  _| \___ \ | |     / /  | | | |  _| | |\/| | | | |
                          | | | |___ ___) || |    / /   | |_| | |___| |  | | |_| |
                          |_| |_____|____/ |_|   /_/    |____/|_____|_|  |_|\___/ 
"""
if "__main__" == __name__:

    import random
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
#         if any(keys):
#             print(keys)
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
    game = pyMatrix(maxX, maxY, colourBackground=COLOUR_BACKGROUND, speed=5, timed_callback=moveObject)
    game.clear((255,0,0))
    posX = maxX // 2
    posY = maxY // 2
    objectX, objectY = getRandomPos(maxX, maxY, posX, posY)
    moveX, moveY = (1, 0)
    colour = COLOUR_RED
    while True:
        keys = game.getPressedKey()
        moveX, moveY, colour = change(keys, moveX, moveY, colour)

        if game.isPosAllowed(posX + moveX, posY + moveY):
            posX += moveX
            posY += moveY
        if objectX == posX and objectY == posY:
            objectX, objectY = getRandomPos(maxX, maxY, posX, posY)

        positions =[(objectX, objectY, COLOUR_GREEN)
                   , (posX, posY, colour)
                   ]

        game.showList(positions )
    