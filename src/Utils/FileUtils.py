import json

from typing import Any, Union

from src.Utils.DebugUtils import DebugUtils


class FileUtils:
    """
    A class with various methods to handle certain file operations in the program.
    """    
    def __init__( self ) -> None:
        DebugUtils.debug_print( f"{ DebugUtils.Tag.INIT } { self.__class__.__name__ }" )        
        
        
    def get_dict_from_json( self, path: str, *keys: Union[str, list] ) -> dict:# * For each key in *keys the method will go one subkey deeper.     
        """A method that get's a dict or a value out of a nested dict.
        Example input path = test.json, keys = i, ii
        content of test.json:
        "i": {
            "ii": {
                "iii": {
                    "one": 1,
                    "two": 2,
                    "three": 3
                }
            }
        }
        Example output:
        iii": {
           "one": 1,
           "two": 2,
           "three": 3
        }
        Args:
            path (str): path leading to a .json file

        Returns:
            dict: returns the dict associated with the last key
        """
        with open( path, "r" ) as file:
            data: dict = json.load( file )

        def recursive_get( data: dict, keys ) -> Union[Any, dict]:
            """recursively get's the content for all the keys given

            Args:
                data (dict): The dict in which to search
                keys: The keys to search for in the dict in data

            Returns:
                Any/dict: returns whichever values were asociated with the keys 
            """            
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
    #! I really need to write more comments and docstrings!
#class FileManager

#JetBrains Mono is so awesome!