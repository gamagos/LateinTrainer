import os
import random
import shutil
import sys
import time
import tkinter as tk
from datetime import datetime
from PIL import Image
from tkinter import font, messagebox, ttk

import win32api
import win32con

from data.Data import Data
from logic.fileAndCacheHandler import fileAndCacheHandler

VERSION = "v1.2.0"

class GUI:
    def __init__( self, root ):
        #paths
        self.project_path = getattr( sys, "_MEIPASS", os.path.dirname( os.path.dirname( os.path.abspath( __file__ ) ) ) )
        self.font_cache_path = os.path.join( self.project_path, "data", "font_cache.json" )
        self.wrong_answers_per_case_path = os.path.join( self.project_path, "data", "wrong_answers_per_case.json")
        self.icon_path = os.path.abspath( os.path.join( self.project_path, "assets", "icon.ico" ) )
        self.settings_default_path = os.path.join( self.project_path, "data", "default_settings.csv" )
        self.settings_path = os.path.join( self.project_path, "data", "settings.csv" )
        self.debug_log_path = os.path.join( self.project_path, "logs", "debug_log.txt" )
        self.settingsPNG_path = os.path.join( self.project_path, "assets", "settings.png" )
        
        #settings
        self.debug = True      
        self.tests = False
        self.selected_option = tk.StringVar()
        
        #UI State
        self.frame_initialized_correctly = False
        self.resizing = False
        self.last_resize_time = 0
        self.root_width = 700
        self.root_prev_width = self.root_width
        self.root_height = 700
        self.root_prev_height = self.root_height
        
        #Data
        self.data = Data()
        self.declensions_nouns = self.data.declensions
        self.conjugations = self.data.conjugations
        self.declensions_adjectives = self.data.declensions_adjectives
        self.hic_haec_hoc = self.data.hic_haec_hoc
        self.qui_quae_quod = self.data.qui_quae_quod
        self.ille_illa_illud = self.data.ille_illa_illud
        self.ipse_ipsa_ipsum = self.data.ipse_ipsa_ipsum
        self.declension_forms = list( self.declensions_nouns.keys() )
        self.conjugation_forms = list( self.conjugations.keys() )
        self.declensions_adjectives_forms = list( self.declensions_adjectives.keys() )
        self.hic_haec_hoc_forms = list( self.hic_haec_hoc.keys() )
        self.qui_quae_quod_forms = list( self.qui_quae_quod.keys() )
        self.ille_illa_illud_forms = list( self.ille_illa_illud.keys() )
        self.ipse_ipsa_ipsum_forms = list( self.ipse_ipsa_ipsum.keys() )
        random.shuffle( self.declension_forms )
        random.shuffle( self.conjugation_forms )
        random.shuffle( self.hic_haec_hoc_forms )
        random.shuffle( self.qui_quae_quod_forms )
        random.shuffle( self.ille_illa_illud_forms )
        random.shuffle( self.ipse_ipsa_ipsum_forms )                        
        self.current_class_index = 0
        self.user_entries = {}
        self.results = {}
        self.answers_wrong = 0
        self.wrong_answers_per_case = {}
        
        #UI Elements
        self.form_labels = []
        self.entries = []
        
        #Cache and Performance
        self.FileAndChacheHandler = fileAndCacheHandler( self )
        self.font_cache = self.FileAndChacheHandler.load_cache()
        self.last_cache_clear = 0
        self.frameRate = self.get_refresh_rate()
        self.frameTime = 1 / self.frameRate
        
        self.root = root
        self.root.title( "Latin Trainer " + VERSION )
        self.root.bind( "<F3>", self.enable_debug )
        self.root.bind( "<F5>", self.enable_tests )
        self.root.bind( "<Configure>", self.on_resize )
        self.root.bind( "<Alt-F4>", self.on_close )
        self.root.iconbitmap( self.icon_path )
        self.root.protocol( "WM_DELETE_WINDOW", self.on_close )
        self.debug_print( "Root was initialized" )
        
        self.main_frame = tk.Frame( self.root, relief = "flat" )
        self.main_frame.bind( "<Enter>", self.on_scrollbars_enter )
        self.main_frame.bind( "<Leave>", self.on_scrollbars_leave )
        self.main_frame.place( relheight = 1, relwidth = 1, )
        
        self.canvas = tk.Canvas( self.main_frame, relief = "flat" )
        self.canvas.place( relheight = 0.95, relwidth = 0.95 )
        self.canvas.bind( "<Enter>", self.on_scrollbars_leave )
        self.canvas.bind( "<Leave>", self.on_scrollbars_enter )

        self.h_scrollbar = tk.Scrollbar( self.main_frame, orient = "horizontal", command = self.canvas.xview )
        self.h_scrollbar.place( relx = 0, rely = 0.97, relwidth = 0.97, height = 20 )

        self.v_scrollbar = tk.Scrollbar( self.main_frame, orient = "vertical", command = self.canvas.yview )
        self.v_scrollbar.place( relx = 0.97, rely = 0, relheight = 1, width = 20 )
        
        #UI initialisation methods
        self.canvas.config( yscrollcommand = self.v_scrollbar.set, xscrollcommand = self.h_scrollbar.set )
        
        self.FileAndChacheHandler.get_settings()
        self.previous_form = self.selected_option.get()
        self.form_select()
        self.create_widgets()
        self.adjust_canvas_window()
        self.debug_print( "Frame was filled" )
        
        self.canvas.bind_all( "<MouseWheel>", self.on_mouse_wheel )
        self.canvas.bind_all( "<Shift-MouseWheel>", self.on_shift_mouse_wheel )
        self.frame_initialized_correctly = True
        
        self.handle_resize()
        
        
    def form_select( self ):
        word_type = self.selected_option.get()
        if word_type == "Alle":
            choices = [ "Nomen", "Verben", "Adjektive", "hic haec hoc", "qui quae quod", "ille illa illud", "ipse ipsa ipsum" ]
            word_type = random.choice( choices )
            
        forms_mapping = {
            "Nomen": ( self.declension_forms, self.declensions_nouns ),
            "Verben": ( self.conjugation_forms, self.conjugations ),
            "Adjektive": ( self.declensions_adjectives_forms, self.declensions_adjectives ),
            "hic haec hoc": ( self.hic_haec_hoc_forms, self.hic_haec_hoc ),
            "qui quae quod": ( self.qui_quae_quod_forms, self.qui_quae_quod ),
            "ille illa illud": ( self.ille_illa_illud_forms, self.ille_illa_illud ),
            "ipse ipsa ipsum": ( self.ipse_ipsa_ipsum_forms, self.ipse_ipsa_ipsum )
        }

        if word_type in forms_mapping:
            forms_list, forms_dict = forms_mapping[ word_type ]
            self.current_key = forms_list[ self.current_class_index ]
            self.current_forms = forms_dict[ self.current_key ]
            self.curent_word_type_amount_of_forms = len( forms_list )
        else:
            messagebox.showerror( "Fehler: ", "Programm konnte die Form nicht auswählen.\nEinstellungen und Formen wurden auf Standard zurückgesetzt" )
            shutil.copyfile( self.settings_default_path, self.settings_path )
            self.FileAndChacheHandler.get_settings()
            self.form_select()

        self.previous_form = self.selected_option.get()
        
        
    def create_widgets( self ):
        self.content_frame = tk.Frame( self.canvas, relief = "flat" )
        self.canvas_window = self.canvas.create_window( ( 0, 0 ), window = self.content_frame, anchor = "nw" )
        
        self.title = tk.Label( self.content_frame, text = f"{ self.add_newline_if_too_long( self.current_key ) }",
                               anchor = "center", justify = "left" )
        self.title.place( relx = 0.032, rely = 0, relheight = 0.2, relwidth = 0.81, anchor = "nw" )
        
        self.combobox_select_form = ttk.Combobox( self.content_frame, textvariable = self.selected_option,
                                                  values = [ "Alle", "Nomen", "Verben", "Adjektive", "hic haec hoc", "qui quae quod", "ille illa illud", "ipse ipsa ipsum" ] ) 
        self.combobox_select_form.place( relx = 0.93 , rely = 0, relheight = 0.026, relwidth = 0.18, anchor = "ne" )
        self.combobox_select_form.state( ["readonly"] )
        self.combobox_select_form.bind( "<<ComboboxSelected>>", self.on_form_select )
        
        self.settings_button = tk.Button( self.content_frame, relief = "sunken" )
        self.settings_button.place( relx = 0.935, rely = 0, relheight = 0.05, relwidth = 0.05, anchor = "nw" )

        self.forms_frame = tk.Frame( self.content_frame )
        self.forms_frame.place( relx = 0.02, rely = 0.16, relwidth = 0.9, relheight = 0.7 )
        
        self.check_button = tk.Button( self.content_frame, text = "Überprüfen", command = self.check_answers )
        self.check_button.place( relx = 0.42, rely = 0.88, relheight = 0.08, relwidth = 0.24 )
        
        self.canvas.config( scrollregion = self.canvas.bbox( "all" ), relief = "flat" )
        
        self.combobox_select_form.tkraise()
        self.root.update_idletasks()
        
        self.populate_entries()


    def populate_entries( self ):
        separation_form_tabel = - 1
        for i, ( case_or_tempus, correct_answer ) in enumerate( self.current_forms.items() ):
            
            if case_or_tempus == "Nominativ_Plural" or case_or_tempus == "1._Person_Plural":
                separation_form_tabel += 1
                
            separation_form_tabel += 1
            self.form_labels.append( tk.Label( self.forms_frame, text = case_or_tempus.replace( "_", " " ), anchor = "w" ) )
            self.form_labels[ i ].place( relx = 0.01, rely = 0.09 * separation_form_tabel, relwidth = 0.4, relheight = 0.09 )
            
            self.entries.append( tk.Entry( self.forms_frame ) )
            
            if case_or_tempus == "Nominativ_Singular" or case_or_tempus == "1._Person_Singular":
                self.entries[ i ].insert( 0, correct_answer )
                self.entries[ i ].config( state = "disabled", disabledforeground = "gray" )
                
            self.entries[ i ].place( relx = 0.42, rely = 0.09 * separation_form_tabel, relwidth = 0.58, relheight = 0.09 )
            self.user_entries[ case_or_tempus ] = self.entries[ i ]
            
        if list( self.current_forms.keys() )[ 0 ] == "Nominativ_Singular":
            self.check_button.place( relx = 0.45, rely = 0.87, relheight = 0.08, relwidth = 0.24 )
        else:
            self.check_button.place( relx = 0.42, rely = 0.62, relheight = 0.08, relwidth = 0.24 )
            
        self.title.config( text = self.add_newline_if_too_long( self.current_key ) )
        self.handle_resize()
    
    
    def check_answers( self ):
        wrong = False
        self.wrong_answers_per_case[ f"{ self.current_key }" ] = self.answers_wrong
        
        for case_or_tempus, correct_answer in self.current_forms.items():
            
            if case_or_tempus == "Nominativ_Singular" or case_or_tempus == "1._Person_Singular":
                continue
            user_input = self.user_entries[ case_or_tempus ].get().strip()
            
            if user_input == correct_answer:
                self.user_entries[ case_or_tempus ].config( fg = "green", state = "disabled", disabledforeground = "green" )
                self.results[ case_or_tempus ] = True 
            else:
                wrong = True
                self.answers_wrong += 1
                self.user_entries[ case_or_tempus ].config( fg = "red", state = "disabled", disabledforeground = "red" )
                self.results[ case_or_tempus ] = False
                
        self.wrong_answers_per_case[ f"{ self.current_key }" ] += self.answers_wrong
        if wrong:
            self.check_button.config( text = "Show Solutions", command = self.show_solutions ) 
        else:
            self.answers_wrong = 0
            self.next_class()
            self.FileAndChacheHandler.save_settings()
    
    
    def show_solutions( self ):
        for case_or_tempus, correct_answer in self.current_forms.items():
            
            if case_or_tempus == "Nominativ_Singular" or self.results.get( case_or_tempus, True ) or case_or_tempus == "1._Person_Singular":
                continue
            
            user_input = self.user_entries[case_or_tempus].get().strip()
            
            if user_input != correct_answer:
                self.user_entries[ case_or_tempus ].config( fg = "blue", state = "normal" )
                self.user_entries[ case_or_tempus ].delete( 0, tk.END )
                self.user_entries[ case_or_tempus ].insert( 0, correct_answer )
                self.user_entries[ case_or_tempus ].config( state = "disabled", disabledforeground = "blue" )
        
        self.check_button.config( text = "Retry", command = self.retry )
    
    
    def retry( self ):
        for case, correct_answer in self.current_forms.items():
            
            if case == "nominativ_singular" or self.results.get( case, True ):
                continue
            
            self.user_entries[ case ].config( fg = "black", state = "normal" )
            self.user_entries[ case ].delete( 0, tk.END )
        
        self.check_button.config(text = "Check", command = self.check_answers)
    

    def next_class( self ):
        self.current_class_index += 1
        
        if self.current_class_index >= self.curent_word_type_amount_of_forms:
            self.current_class_index = 0
        else:
            self.form_select()
            
            for widget in self.forms_frame.winfo_children():
                widget.destroy()
                
            self.user_entries = {}
            self.results = {}
            self.form_labels = []
            self.entries = []
            self.populate_entries()
    
    
    def handle_resize( self ):
        self.debug_print( "Handling resize..." )
        self.resizing = True
        self.root.update_idletasks()
        self.get_root_size()
        self.debug_print( f"Root size: { self.root_width }x{ self.root_height }" )
        
        self.adjust_canvas_window()
        self.adjust_font_size( self.title, font_weight = "bold" )
        self.adjust_font_size( self.combobox_select_form, 0.83, 0.83 )
            
        for i in range( len( self.form_labels ) ):
            try:
                self.adjust_font_size( self.form_labels[ i ], 1, 1, self.form_labels[ 0 ].cget( "text" ), element_name = "form_labels" )
                self.adjust_font_size( self.entries[ i ], 0.75, 0.75, "entryplaceholder", element_name = "entries" )
            except Exception as e:
                self.debug_print( f"Error adjusting form labels or entries: { e }" )
        self.adjust_font_size( self.check_button, 0.72, 0.72 )
            
        self.root_prev_width = self.root_width
        self.root_prev_height =self.root_height
        
        self.root.update()
        self.resizing = False
        
        
    def adjust_font_size( self, widget, max_width_ratio = 0.72, max_height_ratio = 0.72, element_text = None, font_weight = "normal", element_name = None ):
        self.root.update_idletasks()
        cached_font_size = self.FileAndChacheHandler.get_cached_font_size( element_name )
        
        if element_name is None:
            element_name = widget.winfo_name()
        
        if cached_font_size is not None:
            font_size = cached_font_size
            widget.config( font = ( "Arial", font_size, font_weight ) )
            return font_size
            
        if element_text is None:
            element_text = widget.cget( "text" )
                
        widget_width = widget.winfo_width()
        widget_height = widget.winfo_height()
        max_width = int( widget_width * max_width_ratio )
        max_height = int( widget_height * max_height_ratio )
        font_size = 120
        
        temp_font = font.Font( family = "Arial", size = font_size, weight = font_weight )
        text_width = temp_font.measure( element_text )
        text_height = temp_font.metrics( "linespace" )
                  
        width_ratio = max_width/text_width
        height_ratio = max_height/text_height
        ratio = min( width_ratio, height_ratio )
        
        if 0.8 < ratio and ratio < 1.1:
            self.debug_print( f"ratio of { element_name } too small" )
            return font_size
        
        font_size = int( font_size * ratio )
        
        while True:
            temp_font = font.Font( family = "Arial", size = font_size, weight = font_weight )
            text_width = temp_font.measure( element_text )
            text_height = temp_font.metrics( "linespace" )
            if text_width <= max_width and text_height <= max_height:
                break
            
            if font_size < 8:
                font_size = 8
                break
            
            font_size -= 1
        
        widget.config( font = ( "Arial", font_size, font_weight ) )
        self.FileAndChacheHandler.cache_font_size( element_name, font_size )
        return font_size


    def adjust_canvas_window( self ):
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        new_width = canvas_width - 4
        new_height = canvas_height - 4
        
        self.canvas.itemconfig( self.canvas_window, width = new_width, height = new_height )
        self.canvas.config( scrollregion = self.canvas.bbox( "all" ) )
            
            
    def get_refresh_rate( self ):
        try:
            device = win32api.EnumDisplayDevices( None, 0 )
            settings = win32api.EnumDisplaySettings( device.DeviceName, win32con.ENUM_CURRENT_SETTINGS )
            
            if settings.DisplayFrequency <= 60:
                return 60
            else:
                return settings.DisplayFrequency
        
        except Exception as e:
            self.debug_print( f"Failed to get refresh rate: { e }" )
            return 60
        
        
    def get_root_size( self ):
        self.root_width = self.root.winfo_width()
        self.root_height = self.root.winfo_height()
        
        
    def add_newline_if_too_long( self, text, max_length = 33 ):
        words = text.split()
        result = []
        current_line = ""

        for word in words:
            if len( current_line ) + len( word ) + 1 > max_length:
                result.append( current_line.strip() )
                current_line = word + " "
            else:
                current_line += word + " "

        if current_line.strip():
            result.append( current_line.strip() )

        return "\n".join( result )
 
                    
    def on_frame_configure( self, event ):
        self.canvas.config( scrollregion = self.canvas.bbox( "all" ) )
        self.root.update()
    
    
    def on_form_select( self, event ):
        self.current_class_index = 0
        if self.previous_form != self.selected_option.get():
            self.next_class()
            self.FileAndChacheHandler.save_settings()


    def on_mouse_wheel( self, event ):
        self.canvas.yview_scroll( int ( -1 * ( event.delta / 120 ) ), "units" )
    
    
    def on_shift_mouse_wheel( self, event ):#       what is delta? and units?
        self.canvas.xview_scroll( int( -1 * ( event.delta / 120 ) ), "units" )
    
        
    def on_scrollbars_leave( self, event ):
        self.h_scrollbar.place_forget()
        self.v_scrollbar.place_forget()
        
        
    def on_scrollbars_enter( self, event ):
        self.h_scrollbar.place( relx = 0, rely = 0.97, relwidth = 0.97, height = 20 )
        self.v_scrollbar.place( relx = 0.97, rely = 0, relheight = 1, width = 20 )
    
    
    def on_resize( self, event ):
        now = time.time()
        self.get_root_size()
        width_diff = abs( self.root_width - self.root_prev_width )
        height_diff = abs( self.root_height - self.root_prev_height )
        minimum_diff = 2
        
        if now - self.last_resize_time < self.frameTime or self.resizing:
            return
        
        if width_diff >= minimum_diff or height_diff >= minimum_diff:
            self.last_resize_time = now
            self.handle_resize()
        
        
    def on_close( self, event=None ):
        if time.time() - self.last_cache_clear < ( 30 * 24 * 60 * 60 ):
            self.debug_print( "save and exit(on_close)" )
            self.debug_print( f"time till next clear: { ( ( 30 * 24 * 60 * 60 ) - ( time.time() - self.last_cache_clear ) ) / ( 24 * 60 * 60 ) } days" )
            self.FileAndChacheHandler.save_cache()
            self.FileAndChacheHandler.save_settings()
        else:
            self.debug_print( "chache got cleared" )
            self.FileAndChacheHandler.clear_cache_and_logs()
            self.FileAndChacheHandler.save_settings()
        self.root.quit()
            
            
    def debug_print( self, *toPrint ):
        time = str( datetime.now() ) + ": "
        if ( self.debug == True ):
            formatted_toPrints = []
            for arg in toPrint:
                if isinstance( arg, str ) and  (arg.startswith( "'" ) and arg.endswith( "'" ) ):
                    formatted_toPrints.append(arg)
                elif isinstance( arg, str ) and ( arg.startswith( "(" ) and arg.endswith( ")" ) ):
                    formatted_toPrints.append( arg )
                else:
                    formatted_toPrints.append( str( arg ) )
            output = " ".join( formatted_toPrints )
            print( time, output )
            self.FileAndChacheHandler.write_debug_log( time + "\n".join( formatted_toPrints ) )
            
    def enable_debug( self, event ):
        time = str( datetime.now() ) + ": "
        if self.debug == False:
            self.debug = True
            print( time, "Debug on" )
            info_Label = tk.Label( self.main_frame, text = "Debug on", font = ( "Arial", 25, "bold" ) )
            info_Label.place( relx = 0.5, rely = 0.5, height = 46, width = 150, anchor = "center" )
            self.root.update()
            self.root.after( 1000, info_Label.place_forget() )
            self.FileAndChacheHandler.save_settings()              
        else:
            self.debug = False
            print( time, "Debug off" )
            info_Label = tk.Label( self.main_frame, text = "Debug off", font = ( "Arial", 25, "bold" ) )
            info_Label.place( relx = 0.5, rely = 0.5, height = 46, width = 150, anchor = "center" )
            self.root.update()
            self.root.after( 1000, info_Label.place_forget() )
            self.FileAndChacheHandler.save_settings()
                
                
    def enable_tests( self, event ):
        time = str( datetime.now() ) + ": "
        if self.tests == False:
            self.tests = True
            print( time, "Tests on" )
            info_Label = tk.Label( self.main_frame, text = "Tests on", font = ( "Arial", 25, "bold" ) )
            info_Label.place( relx = 0.5, rely = 0.5, height = 46, width = 150, anchor = "center" )
            self.root.update()
            self.root.after( 1000, info_Label.place_forget() )
            self.FileAndChacheHandler.save_settings()                
        else:
            self.tests = False
            print( time, "Tests off" )
            info_Label = tk.Label( self.main_frame, text = "Tests off", font = ( "Arial", 25, "bold" ) )
            info_Label.place( relx = 0.5, rely = 0.5, height = 46, width = 150, anchor = "center" )
            self.root.update()
            self.root.after( 1000, info_Label.place_forget() )
            self.FileAndChacheHandler.save_settings()