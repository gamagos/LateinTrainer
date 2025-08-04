from datetime import datetime
from typing import Callable, Union

class DebugUtils:
    def __init__( self, callback_write_log: Callable[[ str ], None ] ) -> None:
        print( f"[INIT] { self.__class__.__name__ }" )
        self.callback_write_log = callback_write_log
        self.debug = True #!False
        
    def debug_print( self, *toPrint: Union[ tuple, list, str ], write_log: bool = True ) -> None:
        if not self.debug:
            return
        time = str( datetime.now() ) + ": "
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
        
        if write_log:
            self.callback_write_log( output )
#class DebugUtils