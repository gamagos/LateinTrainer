import os

from enum import Enum

class ANSICodes:
    """
    SYNOPSIS:
        Many useful ANSI codes
    REMARKS:
        Only use strings in here!
    """
    ESC_SEQUENCE = "\x1b"
    RESET = "\x1b[0m"
    
    """
    SYNOPSIS:
        Generates an ANSI escape sequence to change the text's 
        foreground color to a certain color in terminals that support ANSI escape Codes
    PARAMETERS:
        R,G,B: Integer values from 0-255 for red green and blue channels
    REMARKS:
        YOU NEED TO USE THE "ANSICodes.RESET" ESCAPE SEQUENCE AFTER THE TEXT YOU WANTED TO COLOR
        TO CHANGE THE COLOR BACK TO NORMAL OR ELSE THE ENTIRE REST OF THE TEXT WILL REMAIN COLORED!!
    """
    @staticmethod
    def generate_ANSI_24bit_color(R: int, G: int, B: int) -> str: # type: ignore
        result: str = f"{ANSICodes.ESC_SEQUENCE}[38;2;{R};{G};{B}m"
        return result;


class Paths(Enum):#TODO really need to write more comments
    """many paths used throughout the program"""    
    BASE_PATH = os.path.dirname( os.path.dirname( os.path.abspath( __file__ ))) #same as ../../
    DATA_PATH = os.path.join( BASE_PATH, "data" )
    FORMS_JSON_PATH = os.path.join( DATA_PATH, "forms.json" )


class AssetFolders(Enum):
    """All folders in which the programs assets are stored
    """
    ASSETS_PATH = os.path.join( Paths.BASE_PATH.value, "assets" )
    SETTINGS_BUTTON_PNG_FOLDER = str( os.path.join( ASSETS_PATH, "settings_button" ) )
            
            
class DarkModeAssets(Enum):
    """All paths to the dark mode assets"""
    SETTINGS_BUTTON = os.path.join( AssetFolders.SETTINGS_BUTTON_PNG_FOLDER.value, "settings_darkmode.png" )
    SETTINGS_BUTTON_DISABLED = os.path.join( AssetFolders.SETTINGS_BUTTON_PNG_FOLDER.value, "settings_disabled_darkmode.png" )

    ICON = os.path.join( AssetFolders.ASSETS_PATH.value, "icon_darkmode.ico" )
    
    
class LightModeAssets(Enum):
    """All paths to the light mode assets"""
    SETTINGS_BUTTON = os.path.join( AssetFolders.SETTINGS_BUTTON_PNG_FOLDER.value, "settings.png" )
    SETTINGS_BUTTON_DISABLED = os.path.join( AssetFolders.SETTINGS_BUTTON_PNG_FOLDER.value, "settings_disabled.png" )
    
    ICON = os.path.join( AssetFolders.ASSETS_PATH.value, "icon.ico" )
#TODO if name = main in main.py and make main method there