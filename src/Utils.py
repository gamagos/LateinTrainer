import random

from datetime import datetime
from typing import Union


class Utils:
    VERSION = "2.0.0.0"
    
    def __init__( self ) -> None:
        print(f"[INIT] {self.__class__.__name__}")
        self.darkmode_on = True
        self.debug = True #!False
        
        self.callback_write_log = None
        
           
    def debug_print( self, *toPrint: Union[ tuple, list, str ] ) -> None:
        time = str( datetime.now() ) + ": "
        if not self.debug:
            return
        formatted_toPrints = []
        for arg in toPrint:
            if isinstance( arg, str ):
                formatted_toPrints.append( arg )
            else:
                try:
                    formatted_toPrints.append( str( arg ))
                except Exception:
                    pass
        output = " ".join( formatted_toPrints )
        print( time, output )
        self.callback_write_log( output )
        
        
    def get_dict_minimum_depth( self, dictionary: dict ) -> int:
        keys = dictionary.keys()
        try:
            for key in keys:
                dictionary[ key ].keys()
            return 1 + self.get_dict_minimum_depth( dictionary[ key ] )
        except Exception:
            return 0
        
        
    def shuffle_dict( self, dictionary: dict ) -> dict:
        keys = list( dictionary.keys() )
        random.shuffle( keys )
        return { key: dictionary[ key ] for key in keys }
        
        
    def dummy( *args ) -> None:
        # * This is a dummy method it is meant to be an empty placeholder for event bound methods
        return
#class Utils