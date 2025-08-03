import os

class Assets():
    def __init__( self, base_path: str, darkmode_on: bool ) -> None:
        print( f"[INIT] { self.__class__.__name__ }" )
        self.BASE_PATH = base_path
        self.DARKMODE_ON = darkmode_on
        self.ASSETS_PATH = os.path.join( self.BASE_PATH, "assets" )
        self.SETTINGS_BUTTON_PNG_FOLDER = os.path.join( self.ASSETS_PATH, "settings_button" )
        
    
    @property
    def settings_button_png_path( self ) -> str:
        if self.DARKMODE_ON:
            return os.path.join( self.SETTINGS_BUTTON_PNG_FOLDER, "settings_darkmode.png" )
        else:
            return os.path.join( self.SETTINGS_BUTTON_PNG_FOLDER, "settings.png" )
    
    
    @property
    def settings_disabled_button_png_path( self ) -> str:
        if self.DARKMODE_ON:
            return os.path.join( self.SETTINGS_BUTTON_PNG_FOLDER, "settings_disabled_darkmode.png" )
        else:
            return os.path.join( self.SETTINGS_BUTTON_PNG_FOLDER, "settings_disabled.png" )
    
    
    @property
    def icon_path( self ) -> str:
        if self.DARKMODE_ON:
            return os.path.join( self.ASSETS_PATH, "icon_darkmode.ico" )
        else:
            return os.path.join( self.ASSETS_PATH, "icon.ico" )
    #def __init__
#class Assets