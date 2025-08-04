import random
from typing import Any, Union
#TODO I was working on splitting up my Utils, making sure everything works again then and making sure all __init__files tell where what is being imported


class DictUtils:
    def __init__( self ) -> None:
        print( f"[INIT] { self.__class__.__name__ }" )
        
        
    def get_dict_minimum_depth( self, dictionary: dict[ Union[ dict, Any ]] ) -> int:
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
#class DictUtils