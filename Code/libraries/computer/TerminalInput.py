
"""
    about : terminalInput is a default text input via the terminal
    Version : 1.0.2
    Date    : 11 April 2024
"""

import sys
sys.path.insert(0, '..//')
sys.path.insert(1, './/')
sys.path.insert(2, './/libraries/')
sys.path.insert(3, './/libraries/computer')

from IInput import IInput

class TerminalInput(IInput):
    
    def __init__(self, message: str):
        self._message = message
    
    
    
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
        keys = [ord(i) for i in input(self._message)] 
        return keys

"""
             _____ _____ ____ _____      __  ____  _____ __  __  ___  
            |_   _| ____/ ___|_   _|    / / |  _ \| ____|  \/  |/ _ \ 
              | | |  _| \___ \ | |     / /  | | | |  _| | |\/| | | | |
              | | | |___ ___) || |    / /   | |_| | |___| |  | | |_| |
              |_| |_____|____/ |_|   /_/    |____/|_____|_|  |_|\___/ 
"""
if "__main__" == __name__:
    inp = TerminalInput("Geef de coordinaten : ")
    print(inp.getPressedKey())

    
    