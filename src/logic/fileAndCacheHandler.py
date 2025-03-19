import json
import os
import shutil
import time

from numpy import double


class fileAndCacheHandler:
    def __init__( self, gui_instance ):
        self.gui_instance = gui_instance
                
        
    def get_settings( self ):    
        if  not os.path.exists( self.gui_instance.settings_path ) or os.path.getsize( self.gui_instance.settings_path ) == 0:
            with open( self.gui_instance.settings_path, "w" ) as file:
                shutil.copyfile( self.gui_instance.settings_default_path, self.gui_instance.settings_path )
                print( "settings were restored(empty)" )
        else:
            try:
                with open( self.gui_instance.settings_path, "r" ) as file:
                    contents = file.readlines()
                    self.gui_instance.debug = "True" == contents[ 0 ].split( "=" )[ 1 ].strip()
                    self.gui_instance.tests = "True" == contents[ 1 ].split( "=" )[ 1 ].strip()
                    self.gui_instance.selected_option.set( contents[ 2 ].split( "=" )[ 1 ].strip() )
                    self.gui_instance.last_cache_clear = double( contents[ 3 ].split( "=" )[ 1 ].strip() )
                    self.gui_instance.debug_print( "settings were read successfully:" )
                    self.gui_instance.debug_print( " ".join( [ item.split( "=" )[ 1 ].strip() for item in contents ] ) + "\n" )
                                  
            except Exception as e:
                with open( self.gui_instance.settings_path, "w" ) as file:
                    shutil.copyfile( self.gui_instance.settings_default_path, self.gui_instance.settings_path )
                    self.gui_instance.debug_print( f"settings were restored(error in settings file): { e }" )
                    
                    
    def save_current_form( self ):
        with open( self.gui_instance.settings_path, "r+" ) as file:
                contents = file.readlines()
                contents[ 2 ] = f"selected_option={ self.gui_instance.selected_option.get() }\n"
                file.seek( 0 )
                file.truncate()
                file.writelines( contents )
                    
            
    def load_cache( self ):
        if os.path.exists( self.gui_instance.font_cache_path ):
            try:
                with open( self.gui_instance.font_cache_path,"r" ) as file:
                    return json.load( file )
            except Exception as e:
                self.gui_instance.debug_print( f"load_cache: Error reading font_cache.json, file was reset: { e }" )
                with open( self.gui_instance.font_cache_path, "w" ) as file:
                    json.dump( {}, file, indent = 4 )
                return {}
        else:
            self.gui_instance.debug_print( "font_cache.json does not exist!" )
            return {}
        
        
    def cache_font_size( self, element_name, font_size ):
        if self.gui_instance.frame_initialized_correctly == True:
            self.gui_instance.get_root_size()
            key = f"{ self.gui_instance.root_width }x{ self.gui_instance.root_height }"
            if key not in self.gui_instance.font_cache:
                self.gui_instance.font_cache[ key ] = {}
            self.gui_instance.font_cache[ key ][ element_name ] = font_size
    
    
    def save_cache( self ):
        with open( self.gui_instance.font_cache_path ,"w" ) as file:
            json.dump( self.gui_instance.font_cache, file, indent = 4 )
            
            
    def clear_cache( self ):
        with open( self.gui_instance.font_cache_path, "w" ) as file:
            json.dump( {}, file, indent = 4 )
        
        with open( self.gui_instance.settings_path, "r+" ) as file:
            contents = file.readlines()
            contents[ 3 ] = f"last_clear_cache={ time.time() }\n"
            file.truncate( 0 )
            file.seek( 0 )
            file.writelines( contents )
              
        
    def get_font_size( self, element_name ):
        try:
            self.gui_instance.get_root_size()
            key = f"{ self.gui_instance.root_width }x{ self.gui_instance.root_height }"
            return self.gui_instance.font_cache[ key ][ element_name ]
        except Exception as e:
            self.gui_instance.debug_print( f"Error: font size not cached yet or failed to get cached font size: { e }" )
            return None