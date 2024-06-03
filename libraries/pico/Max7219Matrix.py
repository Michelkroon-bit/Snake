
"""
    about   : Max7219Matrix is IDisplay inherrited class for displaying
              on a max 7219 matrix connected to a pico
    Version : 1.0.0
    Date    : 10 April 2024
    
    MAX7219 driver: https://github.com/mcauser/micropython-max7219
    Note: this driver is designed for 4-in-1 MAX7219 modules.
"""

import sys
sys.path.insert(0, '..//')
sys.path.insert(1, './/')
sys.path.insert(2, './/libraries/')
sys.path.insert(3, './/libraries/pico')

from machine import Pin, SPI
from utime import sleep
from IDisplay import IDisplay
from Max7219 import Matrix8x8

class Max7219Matrix(IDisplay):
    PIXELS_MODULE_WIDTH: int = 8
    PIXELS_MODULE_HEIGHT:int = 8
    PIXELS_HEIGHT = PIXELS_MODULE_WIDTH
    PSI_CHANNEL = 0
    SCROLL_DELAY = 50  # MAX7219 display scrolling speed (ms)
    SLEEP_ANIMATION = .5
    PIXEL_ON = 1
    PIXEL_OFF = 0

    def __init__(self, pin_sck:int = 2, pin_mosi:int = 3, pin_cs:int = 5, number_of_modules_x:int = 4, number_of_modules_y:int = 1, brightness:int = 4):
        """
            VCC 		= 3.3V or 5V
            GND 		= GND
            PIN_SCK 	= 2  # CLK: SCK 2
            PIN_MOSI 	= 3  # DIN: MOSI 3
            PIN_CS 		= 5  # CS:  5
        """
        self._pin_sck = pin_sck
        self._pin_mosi = pin_mosi
        self._pin_cs = pin_cs
        self._brightness = brightness
        self.number_of_modules_x = number_of_modules_x
        self.number_of_modules_y = number_of_modules_y
        self._width  = self.number_of_modules_x * Max7219Matrix.PIXELS_MODULE_WIDTH
        self._height = self.number_of_modules_y * Max7219Matrix.PIXELS_MODULE_HEIGHT
        _spi = SPI(Max7219Matrix.PSI_CHANNEL, sck=Pin(pin_sck), mosi=Pin(pin_mosi))
        _cs = Pin(pin_cs, Pin.OUT)
        self._display = Matrix8x8(_spi, _cs, number_of_modules_x * number_of_modules_y)
        self._display.brightness(self._brightness)
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
        """
            Refreshed the screen
        """
        pass
    
    
    def getWidthHeight(self) -> tuple[int, int]:
        """
            return the width and height of the output
        """
        return self._width, self._height
    
    
    def clear(self, color:tuple[int,int,int] = None, animate:bool=False) -> None:
        """
        """
        ledOn =  color is not None and color != (0,0,0) and color != (-1,-1,-1)
        if not ledOn:
            self._oldPositions = set()
        else:
            for y in range(self._height):
                for x in range(self._width):
                    self._oldPositions.add((x,y))
        
        self._display.fill(ledOn)
        self._display.show()
    
    
    def showMatrix(self, matrix:tuple[tuple[tuple[int,int,int]]], offsetX:int = 0, offsetY:int = 0) -> None:
        """
        update the matrix with a input matrix of rows, columns and color of the pixel
        R = (255,0,0)
        B = (  0,0,0)
        e.g. [ [R, B, B], [B, R, B], [B, B, R] ]
        offsetX : x-offset of the matrix on the pyMatrix screen
        offsetY : y-offset of the matrix on the pyMatrix screen
        """
        for y, line in enumerate(matrix):
            for x, color in enumerate(line):
                self._oldPositions.add( (x + offsetX, y + offsetY) )
                color = self._pixelOn(color)     
                self._display.pixel(x+ offsetX, y+ offsetY, color)                
        self._display.show()

    
    def showPixels(self, positions: tuple[int, int, tuple[int,int,int]], colour:tuple[int,int,int]=None) -> None:
        """
            Show the new pixels on the screen, dont change the current ones
        """
        for x, y, color in positions:
            self._oldPositions.add( (x,y) )
            color = self._pixelOn(color, colour)     
            self._display.pixel(x, y, color)
        self._display.show()
    
    
    def showList(self, positions: tuple[int, int, tuple[int,int,int]], colour:tuple[int,int,int]=None, animate:bool=False) -> None:
        """
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
        for xy in self._oldPositions:
            if xy not in newCoordinates:
                self._display.pixel(xy[0], xy[1], Max7219Matrix.PIXEL_OFF)                
        self._oldPositions = newCoordinates
        
        # ---------------------
        # show the new pixels
        # ---------------------
        if not any(positions):
            return
        if animate:
            positions = set(positions)
        for x, y, color in positions:
            color = self._pixelOn(color, colour)            
            self._display.pixel(x, y, color)
        self._display.show()

    """
             ____       _            _          __                  _   _                 
            |  _ \ _ __(_)_   ____ _| |_ ___   / _|_   _ _ __   ___| |_(_) ___  _ __  ___ 
            | |_) | '__| \ \ / / _` | __/ _ \ | |_| | | | '_ \ / __| __| |/ _ \| '_ \/ __|
            |  __/| |  | |\ V / (_| | ||  __/ |  _| |_| | | | | (__| |_| | (_) | | | \__ \
            |_|   |_|  |_| \_/ \__,_|\__\___| |_|  \__,_|_| |_|\___|\__|_|\___/|_| |_|___/
    """   
    def _pixelOn(self, color, overrideColor = None):
        if overrideColor is not None and (overrideColor == (-1,-1,-1) or overrideColor == (0,0,0)):
            return Max7219Matrix.PIXEL_OFF
        elif color is None or color == (-1,-1,-1) or color == (0,0,0):
            return Max7219Matrix.PIXEL_OFF
        return Max7219Matrix.PIXEL_ON
    
#     def _getFrameBuffer(self):
#         return self._display.framebuf
#     
#     # framebuffer is an instance of frameBuf
#     def setByteArray(self, framebuffer, allCharacters):
#         yMax = len(allCharacters)
#         if yMax == 0:
#             return
#         for y in range(yMax):
#             for x in range(len(allCharacters[y])):
#                 framebuffer.pixel(x, y, allCharacters[y][x])


"""
                         _____ _____ ____ _____      __  ____  _____ __  __  ___  
                        |_   _| ____/ ___|_   _|    / / |  _ \| ____|  \/  |/ _ \ 
                          | | |  _| \___ \ | |     / /  | | | |  _| | |\/| | | | |
                          | | | |___ ___) || |    / /   | |_| | |___| |  | | |_| |
                          |_| |_____|____/ |_|   /_/    |____/|_____|_|  |_|\___/ 
"""

if "__main__" == __name__:
    SLEEP = 2
    
    display = Max7219Matrix(2,3,5)
    
    display.clear((1,1,1))
    print("all on")
    
    sleep( SLEEP )
    display.clear()
    # both pixels should be displayed
    print("Show one pixel on (1,1)")
    display.showPixels([(1,1,(255,  0,   0))])
    
    sleep( SLEEP )
    print("Show two pixels on (0,0) and (1,1)")
    display.showPixels([(0,0,(  0, 255,  0))])
    
    sleep( SLEEP )
    display.clear()
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