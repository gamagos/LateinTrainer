import os

from Trainer.Constants import Paths
from Trainer.Utils import DebugUtils, DictUtils, FileUtils, GeneralUtils


class Logic( GeneralUtils, FileUtils, DictUtils ):
    VERSION: str = "2.0.0.0"
    
    def __init__( self ) -> None:
        Tag = DebugUtils.Tag
        
        DebugUtils.debug_print( f"{ Tag.INIT } { self.__class__.__name__ }" )
        super().__init__()

        self.FORMS_DICT_NAME = "forms" #TODO make this more scaleable
        
        self.current_forms: set = {}
    #TODO write more comments  
    
    
    def select_form_manually( self, top_key: str, key: str, checked: bool ) -> dict:
        print( f"top_key: {top_key}, key: {key}, checked: {checked}" )
#class Logic