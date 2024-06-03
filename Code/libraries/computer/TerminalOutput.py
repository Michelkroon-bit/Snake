
"""
    about : terminalOutput is a default text output via the terminal
    Version : 1.0.2
    Date    : 11 April 2024
"""

import sys
sys.path.insert(0, '..//')
sys.path.insert(1, './/')
sys.path.insert(2, './/libraries/')
sys.path.insert(3, './/libraries/computer')

from IDisplay import IDisplay

class TerminalOutput(IDisplay):
    
    def __init__(self, width, height, dictColor2Character: dict, unknown:str = "?"):
        self._width = width
        self._height = height
        self._unknown = unknown
        self._dictColor2Character = dictColor2Character
        
        self.clear()
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
        return self._width, self._height
    
    
    def clear(self, color:tuple[int,int,int] = None) -> None:
        """
            IDisplay
            clear the complete matrix
        """
        self._matrix = []
        for _ in range(self._height):
            self._matrix.append(self._width * [" "])

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
        for y, line in enumerate(matrix):
            for x, color in enumerate(line):
                x1 = offsetX + x
                y1 = offsetY + y
                if 0 <= x1 < self._width :
                    if 0 <= y1 < self._height:
                        self._matrix[y1][x1] = self._color2Character(color)
        self._printMatrix()


    def showPixels(self, positions: tuple[int, int, tuple[int,int,int]], colour:tuple[int,int,int]=None) -> None:
        """
            IDisplay
            Only show new pixels, don't disturb the old ones.
        """
        for x, y, color in positions:
            if 0 <= x < self._width :
                if 0 <= y < self._height:
                    self._matrix[y][x] = self._color2Character(color)                
        
        self._printMatrix()

    def showList(self, positions: tuple[int, int, tuple[int,int,int]], colour:tuple[int,int,int]=None, animate:bool=False) -> None:
        """
            IDisplay
            position is a list of (x, y, color)
            if color is None, the background color is reset.
            R = (255,  0,  0)
            B = (  0,  0,255)
            e.g. position = [ (1,1,R), (10,3,B) ]
        """
        self.clear()
        self.showPixels(positions, colour)
        

    def refresh(self) -> None:
        """            
            IDisplay : refresh display
        """
        pass
    
    

    """
             ____       _            _          __                  _   _                 
            |  _ \ _ __(_)_   ____ _| |_ ___   / _|_   _ _ __   ___| |_(_) ___  _ __  ___ 
            | |_) | '__| \ \ / / _` | __/ _ \ | |_| | | | '_ \ / __| __| |/ _ \| '_ \/ __|
            |  __/| |  | |\ V / (_| | ||  __/ |  _| |_| | | | | (__| |_| | (_) | | | \__ \
            |_|   |_|  |_| \_/ \__,_|\__\___| |_|  \__,_|_| |_|\___|\__|_|\___/|_| |_|___/
    """
    def _color2Character(self, color):
        if color not in self._dictColor2Character:
            return self._unknown
        return self._dictColor2Character[color]
        
    def _printMatrix(self):
        for line in self._matrix:
            printLine = ""
            for c in line:
                printLine += c
            print(printLine)

"""
             _____ _____ ____ _____      __  ____  _____ __  __  ___  
            |_   _| ____/ ___|_   _|    / / |  _ \| ____|  \/  |/ _ \ 
              | | |  _| \___ \ | |     / /  | | | |  _| | |\/| | | | |
              | | | |___ ___) || |    / /   | |_| | |___| |  | | |_| |
              |_| |_____|____/ |_|   /_/    |____/|_____|_|  |_|\___/ 
"""
if "__main__" == __name__:
    COLOUR_BACKGROUND = (100, 100, 100)  # (R, G, B)
    COLOUR_RED        = (255,   0,   0)
    COLOUR_GREEN      = (  0, 255,   0)
    COLOUR_BLUE       = (  0,   0, 255)
    COLOUR_WHITE      = (255, 255, 255)
    COLOURS = (COLOUR_RED, COLOUR_GREEN,COLOUR_BLUE, COLOUR_WHITE )
    
    dictColor2Character = {COLOUR_BACKGROUND: " ",
                           COLOUR_RED       : "R",
                           COLOUR_GREEN     : "G",
                           COLOUR_BLUE      : "B",
                           COLOUR_WHITE     : "W"
        }
    
    display = TerminalOutput(32,16, dictColor2Character, " ")    
        
    import matrixHelper 
    from matrix_06x08 import MATRIX

    listMatrixGame = matrixHelper.elementsToMatrix("Game", MATRIX)
    textMatrixGame = matrixHelper.appendMatrixHorizontal(listMatrixGame, 1)
    
    listMatrixOver = matrixHelper.elementsToMatrix("Over", MATRIX)
    textMatrixOver = matrixHelper.appendMatrixHorizontal(listMatrixOver, 1)
            
    textMatrixG = matrixHelper.changeColor(textMatrixGame, 1, COLOUR_RED)
    textMatrixO = matrixHelper.changeColor(textMatrixOver, 1, COLOUR_RED)
    
    #display.showMatrix(textMatrixG, 2,2)
    #display.showMatrix(textMatrixO, 2,9)
    
    matrix = matrixHelper.createMatrix(" ", width=32, height=16)
    matrixHelper.plot(matrix, textMatrixG, (2,2))
    matrixHelper.plot(matrix, textMatrixO, (2,9))
    
    display.showMatrix(matrix)      
    

    