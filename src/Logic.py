import os

from src.Utils import DebugUtils, DictUtils, FileUtils, GeneralUtils


class Logic( GeneralUtils, FileUtils, DictUtils, DebugUtils ):
    VERSION = "2.0.0.0"
    
    def __init__( self ) -> None:
        print( f"[INIT] { self.__class__.__name__ }" )
        DebugUtils.__init__( self, self.write_log )
        DictUtils.__init__( self )
        debug_utils_for_file_utils = DebugUtils( self.write_log )
        FileUtils.__init__( self, debug_utils_for_file_utils )
        GeneralUtils.__init__( self )

        self.data_path = os.path.join( self.BASE_PATH, "data" )
        self.forms_json_path = os.path.join( self.data_path, "forms.json" )
        self.FORMS_DICT_NAME = "forms"
        
        self.current_forms: set = {}
    #TODO write more comments  
    def select_form_manually( self, top_key: str, key: str, checked: bool ) -> dict:
        
#class Logic

# JetBrains Mono is such an amazing font, espacially with ligatures on