"""
                         ___ ____  _           _             
                        |_ _|  _ \(_)___ _ __ | | __ _ _   _ 
                         | || | | | / __| '_ \| |/ _` | | | |
                         | || |_| | \__ \ |_) | | (_| | |_| |
                        |___|____/|_|___/ .__/|_|\__,_|\__, |
                                        |_|            |___/ 
"""

class IDisplay:
    """
        Interface class for general display perposes.
        Version : 1.0.0
        Date    : 10 April 2024
    """
    
    
    def refresh(self) -> None:
        """
            Refreshed the screen
        """
        raise NotImplementedError()
    
    
    def getWidthHeight(self) -> tuple[int, int]:
        """
            return the width and height of the output
        """
        raise NotImplementedError()
    
    
    def clear(self, color:tuple[int,int,int] = None, animate:bool=False) -> None:
        """
        """
        raise NotImplementedError()
    
    
    def showMatrix(self, matrix:tuple[tuple[tuple[int,int,int]]], offsetX:int = 0, offsetY:int = 0) -> None:
        """
        update the matrix with a input matrix of rows, columns and color of the pixel
        R = (255,0,0)
        B = (  0,0,0)
        e.g. [ [R, B, B], [B, R, B], [B, B, R] ]
        offsetX : x-offset of the matrix on the pyMatrix screen
        offsetY : y-offset of the matrix on the pyMatrix screen
        """
        raise NotImplementedError()
    
    
    def showPixels(self, positions: tuple[int, int, tuple[int,int,int]], colour:tuple[int,int,int]=None) -> None:
        """
            Show the new pixels on the screen, dont change the current ones
        """
        raise NotImplementedError()
    
    
    def showList(self, positions: tuple[int, int, tuple[int,int,int]], colour:tuple[int,int,int]=None, animate:bool=False) -> None:
        """
            position is a list of (x, y, color)
            if color is None, the background color is reset.
            R = (255,  0,  0)
            B = (  0,  0,255)
            e.g. position = [ (1,1,R), (10,3,B) ]
        """
        raise NotImplementedError()
    
    
    
