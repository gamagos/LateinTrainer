from src.Utils.DebugUtils import DebugUtils


class GeneralUtils:    
    def __init__( self ) -> None:
        DebugUtils.debug_print( DebugUtils.Tag.INIT, f"{ self.__class__.__name__ }" )
        self.darkmode_on = True
        
        
    def dummy( *args ) -> None:
        # * This is a dummy method it is meant to be an empty placeholder for event bound methods
        return
    
    
    class Dummy:
        pass
#class Utils