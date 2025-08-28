import os

from enum import Enum


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
    
    
class LightModeAssets(Enum):
    """All paths to the light mode assets"""
    SETTINGS_BUTTON = os.path.join( AssetFolders.SETTINGS_BUTTON_PNG_FOLDER.value, "settings.png" )
    SETTINGS_BUTTON_DISABLED = os.path.join( AssetFolders.SETTINGS_BUTTON_PNG_FOLDER.value, "settings_disabled.png" )
    
    ICON = os.path.join( AssetFolders.ASSETS_PATH.value, "icon.ico" )
            
            
class DarkModeAssets(Enum):
    """All paths to the dark mode assets"""
    SETTINGS_BUTTON = os.path.join( AssetFolders.SETTINGS_BUTTON_PNG_FOLDER.value, "settings_darkmode.png" )
    SETTINGS_BUTTON_DISABLED = os.path.join( AssetFolders.SETTINGS_BUTTON_PNG_FOLDER.value, "settings_disabled_darkmode.png" )

    ICON = os.path.join( AssetFolders.ASSETS_PATH.value, "icon_darkmode.ico" )
#class Assets
#TODO if name = main in main.py and make main method there