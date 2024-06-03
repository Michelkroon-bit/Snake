import sys
sys.path.insert(0, '..//')
sys.path.insert(1, './/')
sys.path.insert(2, './/libraries/')
sys.path.insert(3, './/libraries/pico')

from IInput import IInput
from machine import Pin

class Button(IInput):
    """
    One button
    """
    

    def __init__(self, pinNum:int, keyValue:int):
        self._pin = Pin(pinNum, Pin.IN)
        self._keyValue = keyValue
        self._oldState = False

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
            return the keys pressed (ascii value)
        """
        keys = []
        state = self._pin.value() == 1
        if state and not self._oldState:
            keys.append(self._keyValue)
        self._oldState = state
        return tuple(keys)
        
        
class Buttons(IInput):
    """
    """
    
    def __init__(self, pinNum:int, keyValue:int):
        self._buttons = []
        self.add(pinNum, keyValue)
        
        
    def add(self, pinNum:int, keyValue:int):
        """
        """
        self._buttons.append(Button(pinNum, keyValue))
        

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
            return the keys pressed (ascii value)
        """
        keys = []
        for b in self._buttons:
            keys += b.getPressedKey()
        return tuple(keys)
    
