"""
                         ___ ___                   _   
                        |_ _|_ _|_ __  _ __  _   _| |_ 
                         | | | || '_ \| '_ \| | | | __|
                         | | | || | | | |_) | |_| | |_ 
                        |___|___|_| |_| .__/ \__,_|\__|
                                      |_|              
"""
    
class IInput:
    """
        Handle the input for the program
        Version : 1.0.0
        Date    : 10 April 2024
    """
    
    def getPressedKey(self) -> tuple[int]:
        """
            return the keys pressed (ascii value)
        """
        raise NotImplementedError()
    
    