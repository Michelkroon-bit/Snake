
"""
    about   : NeoPixelMatrix is IDisplay inherrited class for displaying
              on a NeoPixel matrix connected to a pico
    Version : 1.0.0
    Date    : 10 April 2024
"""

import sys
sys.path.insert(0, '..//')
sys.path.insert(1, './/')
sys.path.insert(2, './/libraries/')
sys.path.insert(3, './/libraries/pico')

from IDisplay import IDisplay
from machine import Pin
import neopixel
from utime import sleep


class NeoPixelMatrix(IDisplay):
    PIXEL_OFF = (0,0,0)
    def __init__(self, pinData: int, callbackPosition, width: int = 32, height: int = 16):
        if callbackPosition is None:
            raise AttributeError
        self._pinData = pinData
        self._maxX = width
        self._maxY = height
        self._callbackPosition = callbackPosition
        self._neopixel = neopixel.NeoPixel(Pin(pinData), width * height)   
        self._oldPositions = set()
    
    """
                             ___ ____  _           _             
                            |_ _|  _ \(_)___ _ __ | | __ _ _   _ 
                             | || | | | / __| '_ \| |/ _` | | | |
                             | || |_| | \__ \ |_) | | (_| | |_| |
                            |___|____/|_|___/ .__/|_|\__,_|\__, |
                                            |_|            |___/ 
    """    
    def refresh(self) -> None:
        pass


    def getWidthHeight(self) -> tuple[int, int]:
        return self._maxX, self._maxY


    def clear(self, color:tuple[int,int,int] = None, animate:bool=False) -> None:
        if color is None:
            color = NeoPixelMatrix.PIXEL_OFF
        pixels = []
        for x,y in self._oldPositions:
            pixels.append((x,y, color))                
        self.showList(pixels, animate=animate)


    def showMatrix(self, matrix:tuple[tuple[tuple[int,int,int]]], offsetX:int = 0, offsetY:int = 0) -> None:
        height = len(matrix)
        if height == 0:
            return
        width = len(matrix[0])
        for y, line in enumerate(matrix):
            for x, color in enumerate(line):
                
                self._oldPositions.add( (x + offsetX, y + offsetY) )
                
                index = self._callbackPosition(x + offsetX, y + offsetY, self._maxX, self._maxY)                
                self._showPixel(index, color, False)
        self._neopixel.write()


    def showPixels(self, positions: tuple[int, int, tuple[int,int,int]], colour:tuple[int,int,int]=None) -> None:
        if not any(positions):
            return        
        for x, y, color in positions:
            self._oldPositions.add( (x, y) )
            if colour is not None:
                if colour == (-1,-1,-1):
                    color = NeoPixelMatrix.PIXEL_OFF
                else:
                    color = colour
            index = self._callbackPosition(x, y, self._maxX, self._maxY)
            self._showPixel(index, color, False)
        self._neopixel.write()
            
            
    def showList(self, positions: tuple[int, int, tuple[int,int,int]], colour:tuple[int,int,int]=None, animate:bool=False) -> None:
        # ---------------------
        # pixels not in the new list are turned off
        # ---------------------
        newCoordinates = set((p[0],p[1]) for p in positions )
        for xy in self._oldPositions:
            if xy not in newCoordinates:
                index = self._callbackPosition(xy[0], xy[1], self._maxX, self._maxY)
                self._showPixel(index, NeoPixelMatrix.PIXEL_OFF, animate)
        self._oldPositions = newCoordinates
        
        # ---------------------
        # show the new pixels
        # ---------------------
        if not any(positions):
            return
        if animate:
            positions = set(positions)
        for x, y, color in positions:
            index = self._callbackPosition(x,y, self._maxX, self._maxY)
            if colour is not None:
                if colour == (-1,-1,-1):
                    color = NeoPixelMatrix.PIXEL_OFF
                else:
                    color = colour
            self._showPixel(index, color, animate)
        if not animate:
            self._neopixel.write()
        
        
    """
             ____       _            _          __                  _   _                 
            |  _ \ _ __(_)_   ____ _| |_ ___   / _|_   _ _ __   ___| |_(_) ___  _ __  ___ 
            | |_) | '__| \ \ / / _` | __/ _ \ | |_| | | | '_ \ / __| __| |/ _ \| '_ \/ __|
            |  __/| |  | |\ V / (_| | ||  __/ |  _| |_| | | | | (__| |_| | (_) | | | \__ \
            |_|   |_|  |_| \_/ \__,_|\__\___| |_|  \__,_|_| |_|\___|\__|_|\___/|_| |_|___/
    """    
    
    # check if the index in invalid
    def _isInvalidIndex(self, index:int) -> bool:
        if index is None or index < 0 or index >= len(self._neopixel):
           return True
        return False
    
    def _showPixel(self, index:int, color:tuple[int,int,int], now:bool=True) -> None:
        if self._isInvalidIndex(index):
            return
        self._neopixel[index] = color
        if now:
            self._neopixel.write()
            

"""
                         _____ _____ ____ _____      __  ____  _____ __  __  ___  
                        |_   _| ____/ ___|_   _|    / / |  _ \| ____|  \/  |/ _ \ 
                          | | |  _| \___ \ | |     / /  | | | |  _| | |\/| | | | |
                          | | | |___ ___) || |    / /   | |_| | |___| |  | | |_| |
                          |_| |_____|____/ |_|   /_/    |____/|_____|_|  |_|\___/ 
"""

if __name__ == "__main__":
    SLEEP = 2
    def convertXYtoPosition(x: int, y: int, maxX:int, maxY:int) -> int:        
        if x % 2 == 1: # oneven            
            return (x+1) * maxY - y - 1
        return maxY * x + y 

    display = NeoPixelMatrix(28, convertXYtoPosition)
    
    # both pixels should be displayed
    print("Show one pixel on (1,1)")
    display.showPixels([(1,1,(255,  0,   0))])
    
    sleep( SLEEP )
    print("Show two pixels on (0,0) and (1,1)")
    display.showPixels([(0,0,(  0, 255,  0))])
    
    sleep( SLEEP )
    print("Clear the screen")
    display.clear()
    
    sleep( SLEEP )
    print("Show one pixel on (1,1)")
    # one pixel at the time
    display.showList([(1,1,(255,0,0))])
    
    sleep( SLEEP )
    print("Show one pixel on (2,2)")
    display.showList([(2,2,(255,0,0))])
    
    sleep( SLEEP )
    print("Show matrix - 1")
    B = (0,0,0)
    R = (255,0,0)
    G = (0,255,0)
    matrix = ((R, B, B, G),
              (B, R, G, B),
              (B, G, R, B),
              (G, B, B, R)
              )
    display.showMatrix(matrix, 1, 1 )
    
    sleep( SLEEP )
    print("Show matrix - 2")
    display.showMatrix(matrix, 5, 5 )
    
    sleep( SLEEP )
    display.clear()
    