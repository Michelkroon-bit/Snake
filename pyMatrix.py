"""
    about : pyMatrix is a pyGame matrix of n x m pixels
    Version : 0.2.0
    Date    : 6 April 2024
"""
import sys
sys.path.insert(0, './/')
sys.path.insert(1, './/libraries/')
sys.path.insert(1, './/libraries/computer')
from IDisplay import IDisplay

import pygame
import pygame.sysfont as sysfont


class pyMatrix(IDisplay):
    """
        Matrix with dimensions width, height to simulate a Neopixel display
        This version uses X, Y position, a neopixel matrix works with an index number.
    """
    LINE_WIDTH = 3
    RESIZE_SCREEN_PERCENTAGE = 0.8
    TIMER_EVENT = pygame.USEREVENT+1
    
    def __init__(self, width=32, height=16, colourBackground=(100, 100, 100)
                 , caption='Pixel matrix', speed=60, onlyShowNewPixels = True, timed_callback = None, timerInterval = 1000):
        """
        init function of the class
        
        onlyShowNewPixels : All old pixels are automaticly cleared when not in new set
        callbackTimer : callback function with : def functionName(milliseconds:int)
        """
        self._timed_callback = timed_callback
        self._timerInterval = timerInterval
        self._onlyShowNewPixels = onlyShowNewPixels
        self._screen = pygame.display.set_mode()
        self.pixelsX, self.PixelsY = self._screen.get_size()
        self.pixelsX *= self.RESIZE_SCREEN_PERCENTAGE
        self.PixelsY *= self.RESIZE_SCREEN_PERCENTAGE
        # print( sysfont.get_fonts()[0])
        # self.font = pygame.font.SysFont(sysfont.get_fonts()[0], 25)
        self._oldPositions = set()
        self._maxX = width
        self._maxY = height
        self._fpspeed = speed
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
    
    def setSpeed(self, speed):
        """
            Change the speed
        """
        self._fpspeed = speed
    
    def getSpeed(self) -> int:
        """
        """
        return self._fpspeed
    
    
    def getWidthHeight(self):
        """
            return the width and height (in positions)  of the matrix
        """
        return self._maxX, self._maxY
    

    def isPosAllowed(self, posX, posY):
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
    
    
    def clear(self, color = None):
        """
            clear the complete matrix
        """
        self.drawGame([], animate=True)
        
        
    def showMatrix(self, matrix, offsetX=0, offsetY=0):
        """
        update the matrix with a input matrix of rows, columns and color of the pixel
        R = (255,0,0)
        B = (  0,0,0)
        e.g. [ [R, B, B], [B, R, B], [B, B, R] ]
        offsetX : x-offset of the matrix on the pyMatrix screen
        offsetY : y-offset of the matrix on the pyMatrix screen
        """
        self._oldPositions = set()
        region = None
        for y in range(len(matrix)):
            for x in range(len(matrix[0])):
                color = matrix[y][x]
                if color == 0:
                    color = self._colourBackground
                self._oldPositions.add((offsetX + x, offsetY + y))
                geometry = self._draw_square(offsetX + x, offsetY + y, color)
                region = self._updateRegion(geometry, region)
                    
        geometry = self._convertRegion2Geometry(region)
        pygame.display.update(geometry)            


    def showPixels(self, positions: list):
        """
            Only show new pixels, dont disturbate the old ones.
        """
        region = None
        newCoordinates = set((p[0],p[1]) for p in positions )
        for x,y,c in positions:            
            geometry = self._draw_square(x, y, c)            
            region = self._updateRegion(geometry, region)
                
        if region is not None:
            geometry = self._convertRegion2Geometry(region)
            pygame.display.update(geometry)
        self._oldPositions = newCoordinates
    
    def drawGame(self, positions: list, colour=None, animate=False):
        """
            position is a list of (x, y, color)
            if color is None, the background color is reset.
            R = (255,  0,  0)
            B = (  0,  0,255)
            e.g. position = [ (1,1,R), (10,3,B) ]
        """
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
                        
        #show the new pixels    
        for x,y,c in positions:
            if colour is not None:
                c = colour
            geometry = self._draw_square(x, y, c)
            if animate:
                pygame.display.update(geometry)
            else:
                region = self._updateRegion(geometry, region)
                
        if not animate and region is not None:
            geometry = self._convertRegion2Geometry(region)
            pygame.display.update(geometry)
        self._oldPositions = newCoordinates


    def quit(self):
        """
            quit the matrix and the program
        """
        pygame.quit()
        quit()        


    def refresh(self) -> None:
        """
            IDisplay : refresh display
        """
        self._clock.tick(self._fpspeed)  # max FPS = 60
        
        for event in self.getEvents():
            if event.type == pygame.QUIT:
                self.quit()
            elif event.type == pyMatrix.TIMER_EVENT:
                if self._timed_callback is not None:
                    self._timed_callback(pygame.time.get_ticks())
                    
        
    def getEvents(self):
        """
            Get the raise events
        """
        self._clock.tick(self._fpspeed)  # max FPS = 60
        return pygame.event.get()
    

    def getPressedKey(self):
        """
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
          
    """ ----------------------- Private functions ------------------------- """
    
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



if __name__ == "__main__":

    import random
    punten = 0
    MAX_BORDERS = (24, 16)
    COLOUR_BACKGROUND = (100, 100, 100)  # (R, G, B)
    COLOUR_RED = (255, 0, 0)
    COLOUR_GREEN = (0, 255, 0)
    COLOUR_BLUE = (0, 0, 255)
    COLOUR_WHITE = (255, 255, 255)
    COLOUR_BLACK = (0, 0, 0)
    COLOUR_PURPLE = (160, 32, 240)
    COLOURS = (COLOUR_GREEN, COLOUR_WHITE, COLOUR_BLACK, COLOUR_PURPLE)

    def getRandomPos(maxX, maxY, notX = -1, notY=-1):
        x = random.randint(0,maxX-1)
        y = random.randint(0,maxY-1)
        if x == notX or y == notY:
            return getRandomPos(maxX, maxY, notX, notY)
        return x,y
    
    
    def change(keys: list, x,y, colour):
        if 27 in keys:	#esc
            game.quit()
        if ord("q") in keys:
            colour = random.choice(COLOURS)
        elif ord("s") in keys:
            x, y = ( 0,  1)
        elif ord("w") in keys:
            x, y = ( 0, -1)
        elif ord("a") in keys:
            x, y = (-1,  0)
        elif ord("d") in keys:
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
        
        
    if True:
        maxX, maxY = (32, 16)
        scherm = maxX , maxY
        game = pyMatrix(maxX, maxY, colourBackground=COLOUR_BACKGROUND, timed_callback = moveObject)
        posX = maxX // 2
        posY = maxY // 2
        objectX, objectY = getRandomPos(maxX, maxY, posX, posY)
        moveX, moveY = (1, 0)
        colour = random.choice(COLOURS)
        speed = 10
        counter = 0
        snake = [(posX, posY)]  # Initialize snake with one segment
        #main loop
        while True:
            if colour == COLOUR_GREEN:
                speed = 10
            if colour == COLOUR_BLACK:
                speed = 5
            if colour == COLOUR_WHITE:
                speed = 20
            if colour == COLOUR_PURPLE:
                speed = 15
            keys = game.getPressedKey()
            moveX, moveY, colour = change(keys, moveX, moveY, colour)

            if counter % speed == 0:
                new_head = (posX + moveX, posY + moveY)
                
                if new_head in snake:
                    game.quit()  
                else:
                    posX, posY = new_head
                    snake.insert(0, (posX, posY)) 

                # slang eet appel
                if objectX == posX and objectY == posY:
                    objectX, objectY = getRandomPos(maxX, maxY, posX, posY)
                    colour = random.choice(COLOURS)
                    snake_colour = colour
                    if snake_colour == colour:
                        colour = random.choice(COLOURS)
                    punten += 1
                    

                else:
                    snake.pop()
                    
            #appel en slang positie
            positions = [(objectX, objectY, COLOUR_RED)]
            positions.extend([(x, y, colour) for x, y in snake]) 
            game.drawGame(positions)

            counter += 1
