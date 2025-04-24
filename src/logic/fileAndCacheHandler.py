from __future__ import annotations

import json
import os
import shutil
import time
from tkinter import messagebox

from numpy import double, empty
from yaml import Event


class FileAndCacheHandler:
    def __init__( self, gui_instance: "GUI" ) -> None: #type: ignore
        self.gui_instance = gui_instance
                
        
    def get_settings( self ) -> None:
        #settings.csv 
        if  not os.path.exists( self.gui_instance.settings_path ) or os.path.getsize( self.gui_instance.settings_path ) == 0:
            with open( self.gui_instance.settings_path, "w" ) as file:
                shutil.copyfile( self.gui_instance.settings_default_path, self.gui_instance.settings_path )
                self.gui_instance.debug_print( "settings were restored(empty)" )
        else:
            try:
                with open( self.gui_instance.settings_path, "r" ) as file:
                    contents = file.readlines()
                    self.gui_instance.debug = "True" == contents[ 0 ].split( "=" )[ 1 ].strip()
                    self.gui_instance.tests = "True" == contents[ 1 ].split( "=" )[ 1 ].strip()
                    self.gui_instance.selected_option.set( contents[ 2 ].split( "=" )[ 1 ].strip() )
                    self.gui_instance.last_cache_clear = double( contents[ 3 ].split( "=" )[ 1 ].strip() )
                    self.gui_instance.first_start = "True" == contents[ 4 ].split( "=" )[ 1 ].strip()
                    self.gui_instance.autoSelect_on = "True" == contents[ 5 ].split( "=" )[ 1 ].strip()
                    self.gui_instance.last_update = double( contents[ 6 ].split( "=" )[ 1 ].strip() )
                    self.gui_instance.autoUpdate_on = "True" == contents[ 7 ].split( "=" )[ 1 ].strip()
                    self.gui_instance.debug_print( "settings were read successfully:" )
                    self.gui_instance.debug_print( " ".join( [ item.split( "=" )[ 1 ].strip() for item in contents ] ) )
                                  
            except Exception as e:
                with open( self.gui_instance.settings_path, "w" ) as file:
                    shutil.copyfile( self.gui_instance.settings_default_path, self.gui_instance.settings_path )
                    self.gui_instance.debug_print( f"settings were restored(error in settings file): { e }" )
        
        #autoSelect_progress.json
        if not os.path.exists( self.gui_instance.autoSelect_progress_path ) or os.path.getsize( self.gui_instance.autoSelect_progress_path ) == 0:
            with open( self.gui_instance.autoSelect_progress_path, "w", encoding = "utf-8" ) as file:
                json.dump( {}, file, indent = 4, ensure_ascii = False )
                self.gui_instance.debug_print( "autoSelect_progress.json was reset(empty)" )
                self.gui_instance.reset_auto_select_progress()
                return {"Error autoSelect_progress.json is empty"}
        else:
            try:
                with open( self.gui_instance.autoSelect_progress_path, "r", encoding = "utf-8" ) as file:    
                    self.gui_instance.autoSelect_progress = json.load( file )
            except Exception as e:
                with open( self.gui_instance.autoSelect_progress_path, "w", encoding = "utf-8" ) as file:    
                    json.dump( {}, file, indent = 4, ensure_ascii = False )
                    self.gui_instance.debug_print( f"wrong_answeres_per_case.json was reset(error in file): { e }" )
                
                    
                    
    def save_settings( self, event: Event = None ) -> None:
        try:
            #settings.csv
            with open( self.gui_instance.settings_path, "r+" ) as file:
                settings = file.readlines()
                settings[ 0 ] = f"debug={ self.gui_instance.debug }\n"
                settings[ 1 ] = f"tests={ self.gui_instance.tests }\n"
                settings[ 2 ] = f"selected_option={ self.gui_instance.selected_option.get() }\n"
                settings[ 4 ] = f"first_start={ self.gui_instance.first_start }\n"
                settings[ 5 ] = f"autoSelect_on={ self.gui_instance.autoSelect_on }\n"
                settings[ 6 ] = f"last_update={ self.gui_instance.last_update }\n"
                settings[ 7 ] = f"autoUpdate_on={ self.gui_instance.autoUpdate_on }"
                file.seek( 0 )
                file.writelines( settings )
                file.truncate()
                
            #wrong_answer_per_case.json
            with open( self.gui_instance.autoSelect_progress_path ,"w", encoding = "utf-8" ) as file:
                json.dump( self.gui_instance.autoSelect_progress, file, indent = 4, ensure_ascii = False )
                
        except Exception as e:
            self.gui_instance.debug_print( f"failed to save settings: { e }" )
            
            
    def load_json( self, path: str ) -> dict:
        try:
            with open( path, "r", encoding = "utf-8" ) as f:
                return json.load( f )
        except Exception as e:
            self.gui_instance.debug_print( f"Error loading forms.json: { e }" )
            messagebox.showerror( "Fehler", f"Fehler beim laden von forms.json\n{ e }" )
            
                                
    def load_cache( self ) -> dict:
        if os.path.exists( self.gui_instance.font_cache_path ):
            try:
                with open( self.gui_instance.font_cache_path,"r" ) as file:
                    return json.load( file )
            except Exception as e:
                self.gui_instance.debug_print( f"load_cache: Error reading font_cache.json, file was reset: { e }" )
                with open( self.gui_instance.font_cache_path, "w", encoding = "utf-8" ) as file:
                    json.dump( {}, file, indent = 4, ensure_ascii = False )
                return {}
        else:
            self.gui_instance.debug_print( "font_cache.json does not exist!" )
            return {}
        
        
    def cache_size( self, element_name: str, size: int ) -> None:
        if self.gui_instance.frame_initialized_correctly == True:
            self.gui_instance.get_root_size()
            key = f"{ self.gui_instance.root_width }x{ self.gui_instance.root_height }"
            if key not in self.gui_instance.font_cache:
                self.gui_instance.font_cache[ key ] = {}
            self.gui_instance.font_cache[ key ][ element_name ] = size
    
    
    def save_cache( self ) -> None:
        with open( self.gui_instance.font_cache_path ,"w", encoding = "utf-8" ) as file:
            json.dump( self.gui_instance.font_cache, file, indent = 4, ensure_ascii=False )
            
            
    def clear_cache_and_logs( self ) -> None:
        with open( self.gui_instance.font_cache_path, "w", encoding="utf-8" ) as file:
            json.dump( {}, file, indent = 4, ensure_ascii=False )
        with open( self.gui_instance.debug_log_path, "w" ) as file:
            file.writelines( "" )
        
        with open( self.gui_instance.settings_path, "r+" ) as file:
            contents = file.readlines()
            contents[ 3 ] = f"last_clear_cache={ time.time() }\n"
            file.truncate( 0 )
            file.seek( 0 )
            file.writelines( contents )
              
        
    def get_cached_font_size( self, element_name: str ) -> int:
        try:
            self.gui_instance.get_root_size()
            key = f"{ self.gui_instance.root_width }x{ self.gui_instance.root_height }"
            return self.gui_instance.font_cache[ key ][ element_name ]
        except Exception as e:
            return None
        

    def write_debug_log( self, *toWrite: tuple, path: str = None ) -> None:
        toWrites = list( toWrite )
        if not toWrites:
            return
        
        # Convert None to string "None" and handle empty strings
        toWrites = [str(x) if x is not None else "" for x in toWrites]
                 
        if path is None:
            path = self.gui_instance.debug_log_path
            
        if not os.path.exists( path ):
            os.makedirs( os.path.dirname( path ), exist_ok = True )
            with open( path, "w" ) as file:
                file.write( "" )
        
        if not os.path.getsize( path ) == 0:
            toWrites[ 0 ] = "\n" + toWrites[ 0 ]
        
        with open( path, "a" ) as file:
            file.writelines( toWrites )