class IDisplay:
    """
        Interface class for general display perposes.
    """
    
    
    def refresh(self) -> None:
        """
            Refreshed the screen
        """
        pass
    
    
    def getWidthHeight(self) -> list:
        """
            return the width and height of the output
        """
        pass
    
    
    def clear(self, color = None):
        """
        """
        pass
    
    
    def showMatrix(self, matrix, offsetX=0, offsetY=0):
        """
        update the matrix with a input matrix of rows, columns and color of the pixel
        R = (255,0,0)
        B = (  0,0,0)
        e.g. [ [R, B, B], [B, R, B], [B, B, R] ]
        offsetX : x-offset of the matrix on the pyMatrix screen
        offsetY : y-offset of the matrix on the pyMatrix screen
        """
        pass
    
    
    def showPixels(self, positions: list):
        """
            Show a single pixel on the screen
        """
        pass
    
    
    def drawGame(self, positions: list, colour=None, animate=False):
        """
            position is a list of (x, y, color)
            if color is None, the background color is reset.
            R = (255,  0,  0)
            B = (  0,  0,255)
            e.g. position = [ (1,1,R), (10,3,B) ]
        """
        pass
    
    
    