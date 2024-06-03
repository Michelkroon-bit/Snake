"""
                                 ___ ____            _             _ 
                                |_ _/ ___|___  _ __ | |_ _ __ ___ | |
                                 | | |   / _ \| '_ \| __| '__/ _ \| |
                                 | | |__| (_) | | | | |_| | | (_) | |
                                |___\____\___/|_| |_|\__|_|  \___/|_|
"""


    
class IControl:
    """
        Handle the control for the program
        Version : 1.0.0
        Date    : 10 April 2024
    """
    
    
    def quit(self) -> None:
        """
            Quit the application
        """
        raise NotImplementedError()
    
    
    def setSpeed(self, speed: int) -> None:
        """
            sets the speed of the game
        """
        raise NotImplementedError()
    
    
    def getSpeed(self) -> int:
        """
            gets the speed of the game
        """
        raise NotImplementedError()
    
    
