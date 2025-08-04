import json
import os

from datetime import datetime
from typing import Union

from src.Utils.DebugUtils import DebugUtils


class FileUtils:
    def __init__( self, debug_utils: DebugUtils ) -> None:
        print( f"[INIT] { self.__class__.__name__ }" )
        
        self.BASE_PATH = os.path.dirname( os.path.dirname( os.path.dirname( os.path.abspath( __file__ )))) #same as ../../../
        self.debug_utils: DebugUtils = debug_utils
        
        
    def get_dict_from_json( self, path: str, *keys: Union[ str, list ] ) -> dict:# * For each key in *keys the method will go one subkey deeper.     
        with open( path, "r" ) as file:                                          # * If we have a list of different keys in any of *key, all of them
            data = json.load( file )                                             # * will be returned in one dict so more than a single subkey
                                                                                 # * may be retrived. 
        def recursive_get( data, keys ):
            if not keys:
                return data
            key = keys[0]
            rest = keys[1:]

            if isinstance( key, list ):
                return { sub_key: recursive_get( data[ sub_key ], rest ) for sub_key in key }
            elif isinstance( key, str ):
                return recursive_get( data[ key ], rest )
        return recursive_get( data, keys )
    #def get_dict_from_json
        
        
    def write_log( self, *to_write: Union[ tuple , list ] ) -> bool:
        logs_path = os.path.join( self.BASE_PATH, "logs", "log.txt" )
        time = str( datetime.now() )
        
        def write_one() -> bool:
            try:
                with open( logs_path, "a" ) as File:
                    File.write( f"[{ time }]: { to_write }\n" )
                return True
            except Exception as e:
                self.debug_utils.debug_print( f"Error in FileManager.write_log(). {e}", write_log = False )
                return False
            
        def write_many() -> bool:
            try:
                with open( logs_path, "a" ) as File:
                    lines = []
                    for line in to_write:
                        lines.append( f"[{ time }]: { line }\n" )
                    File.writelines( lines )
                return True
            except Exception as e:
                self.debug_utils.debug_print( f"Error in FileManager.write_log(). {e}", write_log = False )
                return False  
        
        if isinstance( to_write, str ):
            write_one()
        elif isinstance( to_write, list ) or isinstance( to_write, tuple ):
            write_many()
        else:
            return False
    #def write_log
#class FileManager