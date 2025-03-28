import math
import os
import random
import shutil
import sys
import threading
import time
import tkinter as tk
from datetime import datetime
from tkinter import font, messagebox, ttk

import win32api
import win32con
from PIL import Image, ImageTk

from logic.fileAndCacheHandler import fileAndCacheHandler

VERSION = "v1.2.0"

class GUI:
    def __init__( self, root ):
        #paths
        self.project_path = getattr( sys, "_MEIPASS", os.path.dirname( os.path.dirname( os.path.abspath( __file__ ) ) ) )
        self.forms_path = os.path.join( self.project_path, "data", "forms.json" )
        self.font_cache_path = os.path.join( self.project_path, "data", "font_cache.json" )
        self.wrong_answers_per_case_path = os.path.join( self.project_path, "data", "wrong_answers_per_case.json")
        self.icon_path = os.path.abspath( os.path.join( self.project_path, "assets", "icon.ico" ) )
        self.settings_default_path = os.path.join( self.project_path, "data", "default_settings.csv" )
        self.settings_path = os.path.join( self.project_path, "data", "settings.csv" )
        self.debug_log_path = os.path.join( self.project_path, "logs", "debug_log.txt" )
        self.settingsPNG_path = os.path.join( self.project_path, "assets/settings_button", "settings.png" )
        self.settings_disbledPNG_path = os.path.join( self.project_path, "assets/settings_button", "settings_disabled.png" )
        self.settings_button_image = Image.open( self.settingsPNG_path )
        self.autoSelect_switchPNGs_paths = [ os.path.join( self.project_path, "assets/autoSelect_switch", "switch_0.png" ),
                                  os.path.join( self.project_path, "assets/autoSelect_switch", "switch_1.png" ),
                                  os.path.join( self.project_path, "assets/autoSelect_switch", "switch_2.png" ),
                                  os.path.join( self.project_path, "assets/autoSelect_switch", "switch_3.png" ),
                                  os.path.join( self.project_path, "assets/autoSelect_switch", "switch_4.png" )]
        
        #settings
        self.debug = True      
        self.tests = False
        self.first_start = False
        self.selected_option = tk.StringVar()
        self.autoSelect_on = False
        
        #UI State
        self.frame_initialized_correctly = False
        self.resizing = False
        self.last_resize_time = 0
        self.root_width = 700
        self.root_prev_width = self.root_width
        self.root_height = 700
        self.root_prev_height = self.root_height
        style = ttk.Style()
        style.theme_use( "clam" )
        style.configure( "Settings.TButton", relief = "flat", borderwidth = 0, padding = 0, background = "white", focuscolor = "white",
                        highlightthickness = 0, highlightcolor = "white" )
        style.map( "Settings.TButton",
                   background = [ ( "disabled", "white" ), ( "!disabled", "white" ) ],
                   foreground = [ ( "disabled", "white" ), ( "!disabled", "white" ) ], )
        
        #Cache and Performance
        self.FileAndChacheHandler = fileAndCacheHandler( self )
        self.font_cache = self.FileAndChacheHandler.load_cache()
        self.last_cache_clear = 0
        self.frameRate = self.get_refresh_rate()
        self.frameTime = 1 / self.frameRate
        
        #Data
        self.forms = self.FileAndChacheHandler.load_json( self.forms_path )[ "forms" ]
        self.choices = [ "Alle", "Nomen", "Verben", "Adjektive", "hic haec hoc", "qui quae quod", "ille illa illud", "ipse ipsa ipsum", "Gerundien", "Gerundiven" ]
        self.current_class_index = 0
        self.user_entries = {}
        self.results = {}
        self.answers_wrong = 0
        self.wrong_answers_per_case = {}
        
        #UI Elements
        self.form_labels = []
        self.entries = []
        self.autoSelect_image = None
        self.settings_window = None
        
        self.root = root
        self.root.title( "Latein Formen Trainer " + VERSION )
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
        
        self.canvas = tk.Canvas( self.main_frame, relief = "flat", borderwidth = 0, highlightthickness = 0 ,highlightcolor = "white" )
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
        
        if self.first_start == True:
            self.reset_auto_select_progress()
            
        self.previous_form = self.selected_option.get()
        self.form_select()
        self.create_widgets()
        self.adjust_canvas_window()
        self.debug_print( "Frame was filled" )
        
        self.canvas.bind_all( "<MouseWheel>", self.on_mouse_wheel )
        self.canvas.bind_all( "<Shift-MouseWheel>", self.on_shift_mouse_wheel )
        
        self.frame_initialized_correctly = True
        
        self.handle_resize()
        
    
    #UI
    def create_widgets( self ):
        self.content_frame = tk.Frame( self.canvas, relief = "flat", borderwidth = 0, highlightthickness = 0 )
        self.content_frame.bind( "<Enter>", self.check_answers )
        self.canvas_window = self.canvas.create_window( ( 0, 0 ), window = self.content_frame, anchor = "nw" )
        
        self.title = tk.Label( self.content_frame, text = f"{ self.add_newline_if_too_long( self.current_key ) }",
                               anchor = "center", justify = "left" )
        self.title.place( relx = 0.48, rely = 0.09, relheight = 0.17, relwidth = 0.93, anchor = "center" )
        
        self.combobox_select_form = ttk.Combobox( self.content_frame, textvariable = self.selected_option,
                                                  values = self.choices ) 
        self.combobox_select_form.place( relx = 0.93 , rely = 0, relheight = 0.026, relwidth = 0.18, anchor = "ne" )
        self.combobox_select_form.state( ["readonly"] )
        self.combobox_select_form.bind( "<<ComboboxSelected>>", self.on_form_select )
        
        self.settings_button = ttk.Button( self.content_frame, style = "Settings.TButton", takefocus = 0, command = self.on_open_settings )
        self.settings_button.place( relx = 0.934, rely = 0, height = 25, width = 25 )

        self.forms_frame = tk.Frame( self.content_frame )
        self.forms_frame.place( relx = 0.02, rely = 0.16, relwidth = 0.9, relheight = 0.7 )
        
        self.check_button = tk.Button( self.content_frame, text = "Überprüfen", command = self.check_answers, anchor = "center" )
        self.check_button.place( relx = 0.48, rely = 0.9, relheight = 0.08, relwidth = 0.24, anchor = "center" )
        
        self.canvas.config( scrollregion = self.canvas.bbox( "all" ), relief = "flat" )
        
        self.combobox_select_form.tkraise()
        self.root.update_idletasks()
        
        self.title.config( text = self.add_newline_if_too_long( self.current_key ) )
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
            self.check_button.place( relx = 0.48, rely = 0.9, relheight = 0.08, relwidth = 0.24 )
        else:
            self.check_button.place( relx = 0.48, rely = 0.62, relheight = 0.08, relwidth = 0.24 )
            
        self.handle_resize()
    
    
    def handle_resize( self ):
        self.debug_print( "Handling resize..." )
        self.resizing = True
        self.root.update_idletasks()
        self.get_root_size()
        self.debug_print( f"Root size: { self.root_width }x{ self.root_height }" )
        
        self.adjust_canvas_window()
        self.title.config( text = self.current_key )
        self.adjust_font_size( self.title, font_weight = "bold" )
        self.adjust_font_size( self.combobox_select_form, 0.83, 0.83 )
        self.adjust_image_button_size( self.settings_button_image )
            
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
            widget.config( font = ( "Arial", cached_font_size, font_weight ) )
            return cached_font_size
            
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
        self.FileAndChacheHandler.cache_size( element_name, font_size )
        return font_size


    def adjust_canvas_window( self ):
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        new_width = canvas_width - 4
        new_height = canvas_height - 4
        
        self.canvas.itemconfig( self.canvas_window, width = new_width, height = new_height )
        self.canvas.config( scrollregion = self.canvas.bbox( "all" ) )
        
        
    def adjust_image_button_size( self, buttonImage, size = 0.05 ):
        self.root.update_idletasks()
        self.get_root_size()
        root_avg_size = ( self.root_width + self.root_width ) / 2
        new_width = root_avg_size * size
 
        if new_width > 60.0:
            new_width = 60
        
        resized_image = buttonImage.resize( ( math.floor( new_width ) - 1, math.floor( new_width ) - 1 ), Image.Resampling.LANCZOS )
        final_image = ImageTk.PhotoImage( resized_image )
        self.settings_button.config( image = final_image )
        self.settings_button.image = final_image

        self.settings_button.place(  relx = 0.934, rely = 0, width = new_width, height = new_width, anchor = "nw" ) #2 times width because its a square
        return new_width
    

    def play_animation( self, widget, image_paths, direction_forward = True, duration = 0.06 ):
        def animation():
            fward = 1 if direction_forward else -1  # Set the step based on direction
            start = 0 if direction_forward else len(image_paths) - 1
            end = len(image_paths) if direction_forward else -1

            frame_duration = duration / len( image_paths )
            for i in range( start, end, fward ):
                start_time = time.perf_counter()
                
                image = Image.open( image_paths[i] )       
                image_width, image_height = image.size
                image = image.resize( ( math.floor( image_width * 0.1 ), math.floor( image_height * 0.1 ) ), Image.Resampling.LANCZOS )
                final_image = ImageTk.PhotoImage( image )
                self.root.after( 0, widget.config( image = final_image ) )
                self.root.after( 0, setattr, widget, "image", final_image )
                self.root.update()
                
                while time.perf_counter() - start_time < frame_duration:
                    time.sleep( self.frameTime )
        threading.Thread( target = animation, daemon = True ).start()       
        
        
    #event handlers
    def on_open_settings( self ):
        self.settings_button.config( command = self.dummy_method )
        self.settings_button_image = Image.open( self.settings_disbledPNG_path )
        self.adjust_image_button_size( self.settings_button_image )
        
        self.settings_window = tk.Toplevel( self.root )
        self.settings_window.geometry( "300x450" )
        self.settings_window.resizable( False, False )
        self.settings_window.title( "Einstellungen" )
        self.settings_window.iconbitmap( self.icon_path )
        self.settings_window.protocol( "WM_DELETE_WINDOW", lambda: self.on_close_settings( self.settings_window ) )
        
        check_for_updates_button = tk.Button( self.settings_window, text = "Check for Updates", font = ( "Arial", 12 ) )
        check_for_updates_button.place( relx = 0, rely = 0 )
        
        forms_settings_label = tk.Label( self.settings_window, text = "-----------------------Form Einstellungen-----------------------", font = ( "Arial", 10 ) )
        forms_settings_label.place( relx = 0, rely = 0.11 )

        autoSelect_switch = tk.Label( self.settings_window, takefocus = 0 )
        image = Image.open( self.autoSelect_switchPNGs_paths[ 4 ] ) if self.autoSelect_on else Image.open( self.autoSelect_switchPNGs_paths[ 0 ] )
        image_width, image_height = image.size
        image = image.resize( ( math.floor( image_width * 0.1 ), math.floor( image_height * 0.1 ) ), Image.Resampling.LANCZOS )
        self.autoSelect_image = ImageTk.PhotoImage( image )
        autoSelect_switch.config( image = self.autoSelect_image )
        autoSelect_switch.image = self.autoSelect_image
        autoSelect_switch.bind( "<Button-1>", lambda event: self.on_autoSelect_switch( event, autoSelect_switch ) )
        autoSelect_switch.place( relx = 0.4, rely = 0.17 )
        
        autoSelect_label = tk.Label( self.settings_window, text = "Autoselect", font = ( "Arial", 12 ) )
        autoSelect_label.place( relx = 0.04, rely = 0.17 )
        
        autoSelect_reset_Button = tk.Button( self.settings_window, text = "Autoselect Fortschritt zurücksetzen", font = ( "Arial", 12 ), command = self.reset_auto_select_progress )
        autoSelect_reset_Button.place( relx = 0.04, rely = 0.24 )
        
    
    def on_close_settings( self, settings_window ):
        self.settings_button.config( command = self.on_open_settings )
        self.settings_button_image = Image.open( self.settingsPNG_path )
        self.adjust_image_button_size( self.settings_button_image )
        self.FileAndChacheHandler.save_settings()
        settings_window.destroy()
        
        
    def on_autoSelect_switch( self, event, widget ):
        self.autoSelect_on = not self.autoSelect_on
        self.debug_print( "auto_select_on =", self.autoSelect_on )
        self.play_animation( widget, self.autoSelect_switchPNGs_paths, self.autoSelect_on )
        widget.bind( "<Button-1>", lambda event: self.on_autoSelect_switch( event, widget ) )
        self.FileAndChacheHandler.save_settings()
                
    
    def on_frame_configure( self, event ):
        self.canvas.config( scrollregion = self.canvas.bbox( "all" ) )
        self.root.update()
    
    
    def on_form_select( self, event ):
        self.current_class_index = 0
        if self.previous_form != self.selected_option.get():
            self.next_class()
            self.FileAndChacheHandler.save_settings()


    def on_resize( self, event ):
        now = time.time()
        self.get_root_size()
        width_diff = abs( self.root_width - self.root_prev_width )
        height_diff = abs( self.root_height - self.root_prev_height )
        minimum_diff = 1
        
        if now - self.last_resize_time < self.frameTime or self.resizing:
            return
        
        if width_diff >= minimum_diff or height_diff >= minimum_diff:
            self.last_resize_time = now
            self.handle_resize()
        
    def on_close( self, event=None ):
        if time.time() - self.last_cache_clear < ( 30 * 24 * 60 * 60 ):
            self.debug_print( "save and exit" )
            self.debug_print( f"time till next clear: { ( ( 30 * 24 * 60 * 60 ) - ( time.time() - self.last_cache_clear ) ) / ( 24 * 60 * 60 ) } days" )
            self.FileAndChacheHandler.save_cache()
            self.FileAndChacheHandler.save_settings()
        else:
            self.debug_print( "chache got cleared" )
            self.FileAndChacheHandler.clear_cache_and_logs()
            self.FileAndChacheHandler.save_settings()
        self.root.quit()
            
                 
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
    
    
    #logic
    def form_select( self ):
        word_type = self.selected_option.get()
        if word_type == "Alle":
            word_type = random.choice( self.choices )
        
        if not self.autoSelect_on:
            forms_mapping = {
                "Nomen": ("Nouns", list( random.sample( list( self.forms["Nouns"].keys() ), len( self.forms["Nouns"] ) ) ) ),
                "Verben": ("Conjugations", list( random.sample( list( self.forms["Conjugations"].keys() ), len( self.forms["Conjugations"] ) ) ) ),
                "Adjektive": ("Adjectives", list( random.sample( list( self.forms["Adjectives"].keys() ), len( self.forms["Adjectives"] ) ) ) ),
                "hic haec hoc": ("hic_haec_hoc", list( random.sample( list( self.forms["hic_haec_hoc"].keys() ), len( self.forms["hic_haec_hoc"] ) ) ) ),
                "qui quae quod": ("qui_quae_quod", list( random.sample( list( self.forms["qui_quae_quod"].keys() ), len( self.forms["qui_quae_quod"] ) ) ) ),
                "ille illa illud": ("ille_illa_illud", list( random.sample( list( self.forms[ "ille_illa_illud" ].keys() ), len( self.forms[ "ille_illa_illud" ] ) ) ) ),
                "ipse ipsa ipsum": ("ipse_ipsa_ipsum", list( random.sample( list( self.forms[ "ipse_ipsa_ipsum" ].keys() ), len( self.forms[ "ipse_ipsa_ipsum" ] ) ) ) ),
                "Gerundien": ("Gerunds", list( random.sample( list( self.forms["Gerunds"].keys() ), len( self.forms["Gerunds"] ) ) ) ),
                "Gerundiven": ("Gerundives", list( random.sample( list( self.forms["Gerundives"].keys() ), len( self.forms["Gerundives"] ) ) ) ),
            }
        else:
            forms_mapping = {
                "Nomen": ("Nouns", list( self.forms[ "Nouns" ].keys() ) ),
                "Verben": ("Conjugations", list( self.forms[ "Conjugations" ].keys() ) ),
                "Adjektive": ("Adjectives", list( self.forms[ "Adjectives" ].keys() ) ),
                "hic haec hoc": ("hic_haec_hoc", list( self.forms[ "hic_haec_hoc" ].keys() ) ),
                "qui quae quod": ("qui_quae_quod", list( self.forms[ "qui_quae_quod" ].keys() ) ),
                "ille illa illud": ("ille_illa_illud", list( self.forms[ "ille_illa_illud" ].keys() ) ),
                "ipse ipsa ipsum": ("ipse_ipsa_ipsum", list( self.forms[ "ipse_ipsa_ipsum" ].keys() ) ),
                "Gerundien": ("Gerunds", list( self.forms["Gerunds"].keys() ) ),
                "Gerundiven": ("Gerundives", list( self.forms["Gerundives"].keys() ) ),
            }
            
        if word_type in forms_mapping:
            key, sub_dicts_array = forms_mapping[ word_type ]
            self.current_key = sub_dicts_array[ self.current_class_index ]
            self.current_forms = self.forms[ key ][ sub_dicts_array[ self.current_class_index ] ]
            self.curent_word_type_amount_of_forms = sub_dicts_array.__len__()
        else:
            messagebox.showerror( "Fehler: ", "Programm konnte die Form nicht auswählen.\nEinstellungen und Formen wurden auf Standard zurückgesetzt" )
            shutil.copyfile( self.settings_default_path, self.settings_path )
            self.FileAndChacheHandler.get_settings()
            self.form_select()

        self.previous_form = self.selected_option.get()
        
        
    def check_answers( self, event ):
        wrong = False
        self.wrong_answers_per_case[ self.current_key ] = self.answers_wrong
        
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
                
        self.wrong_answers_per_case[ self.current_key ] += self.answers_wrong
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
            
            
    def enable_autoSelect( self ):
        pass
            
            
    def reset_auto_select_progress( self ):
        self.root.grab_set()
        c0ntinue =  messagebox.askyesno( "Warnung", "Aller Autoselect Lern Fortschritt wird hiermit zurückgesetzt.\n"
                                        "Das heißt das Program wird nicht mehr wissen wie gut sie in welchen Formen sind.\n\n"
                                        "Trotzdem fortfahren?" )
        self.root.grab_release()
        self.settings_window.deiconify()
        print( c0ntinue )
        if not c0ntinue:
            return
        self.debug_print( "auto_select_progress was reset" )
        for key in self.forms:
            
            if key not in self.wrong_answers_per_case:
                self.wrong_answers_per_case[ key ] = {}
                            
            for key2 in self.forms[ key ]:
                self.wrong_answers_per_case[ key ][ key2 ] = 1000
        self.first_start = False
        self.FileAndChacheHandler.save_settings()
        
        
    def add_newline_if_too_long( self, text, max_length = 30 ):
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
    
    
    def dummy_method( self, *args ):
        pass
            
    
    #getters setters     
    def get_root_size( self ):
        self.root_width = self.root.winfo_width()
        self.root_height = self.root.winfo_height()
        
        
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
 
    
    #debug             
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