import os
import random
import shutil
import sys
import time
import tkinter as tk
from datetime import datetime
from tkinter import font, messagebox, ttk

import win32api
import win32con

from data.Data import Data
from logic.fileAndCacheHandler import fileAndCacheHandler


class GUI:
    def __init__( self, root ):
        self.debug = True         
        self.tests = False
        self.last_cache_clear = 0
        self.project_path = getattr( sys, "_MEIPASS", os.path.dirname( os.path.dirname( os.path.abspath( __file__ ) ) ) )
        self.settings_location = os.path.join( self.project_path, "data", "settings.csv" )
        self.font_cache_location = os.path.join( self.project_path, "data", "font_cache.json" )
        self.settings_default_location = os.path.join( self.project_path, "data", "default_settings.csv" )
        self.FileAndChacheHandler = fileAndCacheHandler( self )
        self.font_cache = self.FileAndChacheHandler.load_cache()
        self.icon_path = os.path.abspath( os.path.join( self.project_path, "assets", "icon.ico" ) )
        version = "v1.0.0"
        self.data = Data()
        self.form_labels = []
        self.entries = []
        self.last_resize_time = 0
        self.resizing = False
        self.root_width = 700
        self.root_prev_width = self.root_width
        self.root_height = 700
        self.root_prev_height = self.root_height
        
        self.first_form_label = tk.Label( text = "this is only a placeholder label for adjust_form_label_font_size()" )
        
        self.declensions_nouns = self.data.declensions
        self.conjugations = self.data.conjugations
        self.declensions_adjectives = self.data.declensions_adjectives
        #pronouns
        self.hic_haec_hoc = self.data.hic_haec_hoc
        self.qui_quae_quod = self.data.qui_quae_quod
        self.ille_illa_illud = self.data.ille_illa_illud
        self.ipse_ipsa_ipsum = self.data.ipse_ipsa_ipsum
        
        self.root = root
        self.root.title( "Latin Trainer " + version )
        self.root.bind( "<F3>", self.enable_debug )
        self.root.bind( "<Configure>", self.on_resize )
        self.root.iconbitmap( self.icon_path )
        self.root.protocol( "WM_DELETE_WINDOW", self.on_close )
        self.debug_print( "Root was initialized" )
        
        self.main_frame = tk.Frame( self.root, relief = "flat" )
        self.main_frame.bind( "<Enter>", self.on_scrollbars_enter )
        self.main_frame.bind( "<Leave>", self.on_scrollbars_leave )
        self.main_frame.place( relheight = 1, relwidth = 1, )
        
        self.canvas = tk.Canvas( self.main_frame, relief = "flat" )
        self.canvas.place( relheight = 0.97, relwidth = 0.97 )
        self.canvas.bind( "<Enter>", self.on_scrollbars_leave )
        self.canvas.bind( "<Leave>", self.on_scrollbars_enter )

        self.h_scrollbar = tk.Scrollbar( self.main_frame, orient = "horizontal", command = self.canvas.xview )
        self.h_scrollbar.place( relx = 0, rely = 0.97, relwidth = 0.97, height = 7 )

        self.v_scrollbar = tk.Scrollbar( self.main_frame, orient = "vertical", command = self.canvas.yview )
        self.v_scrollbar.place( relx = 0.97, rely = 0, relheight = 1, width = 7 )
        
        self.canvas.config( yscrollcommand = self.v_scrollbar.set, xscrollcommand = self.h_scrollbar.set )

        self.ORIGINAL_SCALE = 1.5 
        self.ui_scale = self.ORIGINAL_SCALE  
        
        self.frameRate = self.get_refresh_rate()
        self.frameTime = 1 / self.frameRate
        
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
        self.current_class_index = 0
        self.selected_option = tk.StringVar()
        self.previous_form = self.selected_option.get()
        self.user_entries = {}
        self.results = {}
        
        self.FileAndChacheHandler.get_settings()
        self.form_select()
        self.debug_print( "Form was selected" )
        self.create_widgets()
        self.adjust_canvas_window()
        self.debug_print( "Frame was filled" ) 
        
        self.canvas.bind_all( "<MouseWheel>", self.on_mouse_wheel )
        self.canvas.bind_all( "<Shift-MouseWheel>", self.on_shift_mouse_wheel )
        
        
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
            shutil.copyfile( self.settings_default_location, self.settings_location )
            self.FileAndChacheHandler.get_settings()
            self.form_select()

        self.previous_form = self.selected_option.get()
        
        
    def create_widgets( self ):
        self.content_frame = tk.Frame( self.canvas, relief = "flat" )
        self.canvas_window = self.canvas.create_window( ( 0, 0 ), window = self.content_frame, anchor = "nw" )
        
        self.title = tk.Label( self.content_frame, text = f"{ self.add_newline_if_too_long( self.current_key ) }",
                              font = ( "Arial", int( 19 * self.ui_scale ), "bold" ), anchor = "center", justify = "left" )
        self.title.place( relx = 0.032, rely = 0, relheight = 0.2, relwidth = 0.81, anchor = "nw" )
        
        self.combobox_select_form = ttk.Combobox( self.content_frame, textvariable = self.selected_option,
                                                  values = [ "Alle", "Nomen", "Verben", "Adjektive", "hic haec hoc", "qui quae quod", "ille illa illud", "ipse ipsa ipsum" ],
                                                  font = ( "Arial", int( 8 * self.ui_scale ) ) ) 
        self.combobox_select_form.place( relx = 0.96 , rely = 0, relheight = 0.026, relwidth = 0.18, anchor = "ne" )
        self.combobox_select_form.state( ["readonly"] )
        self.combobox_select_form.bind( "<<ComboboxSelected>>", self.on_form_select )

        self.forms_frame = tk.Frame( self.content_frame )
        self.forms_frame.place( relx = 0.02, rely = 0.16, relwidth = 0.9, relheight = 0.7 )
        
        self.check_button = tk.Button( self.content_frame, text = "Überprüfen", command = self.check_answers )
        self.check_button.place( relx = 0.45, rely = 0.88, relheight = 0.08, relwidth = 0.24 )
        
        self.canvas.config( scrollregion = self.canvas.bbox( "all" ), relief = "flat" )
        
        self.combobox_select_form.tkraise()
        self.root.update_idletasks()
        
        self.populate_entries()


    def populate_entries( self ):
        separation_form_tabel = -1
        for i, ( case_or_tempus, correct_answer ) in enumerate( self.current_forms.items() ):
            
            if case_or_tempus == "Nominativ_Plural" or case_or_tempus == "1._Person_Plural":
                separation_form_tabel += 1
                
            separation_form_tabel += 1
            self.form_labels.append( tk.Label( self.forms_frame, text = case_or_tempus.replace( "_", " " ), font = ( "Arial", int( 14 * self.ui_scale ) ), anchor = "sw" ) )
            self.form_labels[ i ].place( relx = 0.01, rely = 0.09 * separation_form_tabel, relwidth = 0.4, relheight = 0.09 )
            
            self.entries.append( tk.Entry( self.forms_frame, font = ( "Arial", int( 14 * self.ui_scale ) ) ) )
            
            if case_or_tempus == "Nominativ_Singular":
                self.entries[ i ].insert( 0, correct_answer )
                self.entries[ i ].config( state = "disabled", disabledforeground = "gray" )
                
            self.entries[ i ].place( relx = 0.41, rely = 0.09 * separation_form_tabel, relwidth = 0.6, relheight = 0.09 )
            self.user_entries[ case_or_tempus ] = self.entries[ i ]
            
        self.title.config( text = self.add_newline_if_too_long( self.current_key ) )
    
    
    def check_answers( self ):
        wrong = False
        
        for case_or_tempus, correct_answer in self.current_forms.items():
            
            if case_or_tempus == "Nominativ_Singular" or case_or_tempus == "1._Person_Singular":
                continue
            user_input = self.user_entries[ case_or_tempus ].get().strip()
            
            if user_input == correct_answer:
                self.user_entries[ case_or_tempus ].config(fg = "green", state = "disabled", disabledforeground = "green")
                self.results[ case_or_tempus ] = True 
            else:
                wrong = True
                self.user_entries[ case_or_tempus ].config(fg = "red", state = "disabled", disabledforeground = "red")
                self.results[ case_or_tempus ] = False
        
        if wrong:
            self.check_button.config( text = "Show Solutions", command = self.show_solutions ) 
        else:
            self.next_class()
    
    
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
    
    
    def retry(self):
        for case, correct_answer in self.current_forms.items():
            
            if case == "nominativ_singular" or self.results.get( case, True ):
                continue
            
            self.user_entries[ case ].config( fg = "black", state = "normal" )
            self.user_entries[ case ].delete( 0, tk.END )
        
        self.check_button.config(text="Check", command=self.check_answers)
    

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
            self.populate_entries()
          
                    
    def on_frame_configure( self, event ):
        self.canvas.config( scrollregion = self.canvas.bbox( "all" ) )
        self.root.update()
    
    
    def on_form_select( self, event ):
        self.current_class_index = 0
        if self.previous_form != self.selected_option.get():
            self.next_class()
            self.FileAndChacheHandler.save_current_form()


    def on_mouse_wheel( self, event ):
        self.canvas.yview_scroll( int ( -1 * ( event.delta / 120 ) ), "units" )
    
    
    def on_shift_mouse_wheel( self, event ):#       what is delta? and units?
        self.canvas.xview_scroll( int( -1 * ( event.delta / 120 ) ), "units" )
    
        
    def on_scrollbars_leave( self, event ):
        self.h_scrollbar.place_forget()
        self.v_scrollbar.place_forget()
        
        
    def on_scrollbars_enter( self, event ):
        self.h_scrollbar.place( relx = 0, rely = 0.97, relwidth = 0.97, relheight = 0.03 )
        self.v_scrollbar.place( relx = 0.97, rely = 0, relheight = 1, relwidth = 0.03 )
        
        
    def on_close( self ):
        if time.time() - self.last_cache_clear < ( 30 * 24 * 60 * 60 ):
            self.debug_print( "save and exit(on_close)" )
            self.debug_print( f"time till next clear: { ( ( 30 * 24 * 60 * 60 ) - ( time.time() - self.last_cache_clear ) ) / ( 24 * 60 * 60 ) } days" )
            self.FileAndChacheHandler.save_cache()
        else:
            self.debug_print( "chache got cleared" )
            self.FileAndChacheHandler.clear_cache()
        self.root.quit()
    
    
    def on_resize( self, event ):
        now = time.time()
        
        if now - self.last_resize_time < self.frameTime or self.resizing:
            return
        
        self.last_resize_time = now
        self.handle_resize()
    
    
    def handle_resize( self ):
        self.resizing = True
        self.get_root_size()
        width_diff = abs( self.root_width - self.root_prev_width )
        height_diff = abs( self.root_height - self.root_prev_height )
        minimum_diff =  3
        
        if width_diff >= minimum_diff or height_diff >= minimum_diff:
            self.adjust_check_button_font_size()
            self.adjust_combobox_font_size()
            self.adjust_form_label_font_size()
            self.adjust_title_font_size()
            self.adjust_canvas_window()
            
            self.root_prev_width = self.root_width
            self.root_prev_height =self.root_height
        
        self.resizing = False


    def adjust_check_button_font_size( self, base_font_size = 100 ):
        element_name = "check_button"
        cached_font_size = self.FileAndChacheHandler.get_font_size( element_name )
        
        if cached_font_size is not None:
            font_size = cached_font_size
            self.check_button.config( font = ( "Arial", font_size ) )
            return
        
        element_text = self.check_button.cget( "text" )
            
        widget_width = self.check_button.winfo_width()
        widget_height = self.check_button.winfo_height()
        max_width_ratio = 0.72
        max_height_ratio = 0.72
        max_width = int( widget_width * max_width_ratio )
        max_height = int( widget_height * max_height_ratio )
        font_size = base_font_size
        
        temp_font = font.Font( family = "Arial", size = font_size )
        text_width = temp_font.measure( element_text )
        text_height = temp_font.metrics( "linespace" )
                  
        width_ratio = max_width/text_width
        height_ratio = max_height/text_height
        ratio = min( width_ratio, height_ratio )
        if 0.8 < ratio and ratio < 1.1:
            return
        
        font_size = int( font_size * ratio )
        
        while True:
            temp_font = font.Font( family = "Arial", size = font_size )
            text_width = temp_font.measure( element_text )
            text_height = temp_font.metrics( "linespace" )
            if text_width <= max_width and text_height <= max_height:
                break
            
            if font_size < 8:
                font_size = 8
                break
            
            font_size -= 1
        
        self.check_button.config( font = ( "Arial", font_size ) )
        self.FileAndChacheHandler.cache_font_size( element_name, font_size )
        
        
    def adjust_font_size( self, base_font_size = 100 ):
        print( "make single method for font size anjustement and then delete the others" )
        element_name = "combobox"
        cached_font_size = self.FileAndChacheHandler.get_font_size( element_name )
        
        if cached_font_size is not None:
            font_size = cached_font_size
            self.combobox_select_form.config( font = ( "Arial", font_size ) )
            return
               
        element_text = self.combobox_select_form.cget( "text" )
            
        widget_width = self.combobox_select_form.winfo_width()
        widget_height = self.combobox_select_form.winfo_height()
        max_width_ratio = 0.8
        max_height_ratio = 0.8
        max_width = int( widget_width * max_width_ratio )
        max_height = int( widget_height * max_height_ratio )
        font_size = base_font_size
        
        temp_font = font.Font( family = "Arial", size = font_size )
        text_width = temp_font.measure( element_text )
        text_height = temp_font.metrics( "linespace" )
                  
        width_ratio = max_width/text_width
        height_ratio = max_height/text_height
        ratio = min( width_ratio, height_ratio )
        if 0.8 < ratio and ratio < 1.1:
            return
        
        font_size = int( font_size * ratio )
        
        while True:
            temp_font = font.Font( family = "Arial", size = font_size )
            text_width = temp_font.measure( element_text )
            text_height = temp_font.metrics( "linespace" )
            if text_width <= max_width and text_height <= max_height:
                break
            
            if font_size < 8:
                font_size = 8
                break
            
            font_size -= 1
        
        self.combobox_select_form.config( font = ( "Arial", font_size ) )
        self.FileAndChacheHandler.cache_font_size( element_name, font_size )
        
        
    def adjust_combobox_font_size( self, base_font_size = 100 ):
        element_name = "combobox"
        cached_font_size = self.FileAndChacheHandler.get_font_size( element_name )
        
        if cached_font_size is not None:
            font_size = cached_font_size
            self.combobox_select_form.config( font = ( "Arial", font_size ) )
            return
               
        element_text = self.combobox_select_form.cget( "text" )
            
        widget_width = self.combobox_select_form.winfo_width()
        widget_height = self.combobox_select_form.winfo_height()
        max_width_ratio = 0.8
        max_height_ratio = 0.8
        max_width = int( widget_width * max_width_ratio )
        max_height = int( widget_height * max_height_ratio )
        font_size = base_font_size
        
        temp_font = font.Font( family = "Arial", size = font_size )
        text_width = temp_font.measure( element_text )
        text_height = temp_font.metrics( "linespace" )
                  
        width_ratio = max_width/text_width
        height_ratio = max_height/text_height
        ratio = min( width_ratio, height_ratio )
        if 0.8 < ratio and ratio < 1.1:
            return
        
        font_size = int( font_size * ratio )
        
        while True:
            temp_font = font.Font( family = "Arial", size = font_size )
            text_width = temp_font.measure( element_text )
            text_height = temp_font.metrics( "linespace" )
            if text_width <= max_width and text_height <= max_height:
                break
            
            if font_size < 8:
                font_size = 8
                break
            
            font_size -= 1
        
        self.combobox_select_form.config( font = ( "Arial", font_size ) )
        self.FileAndChacheHandler.cache_font_size( element_name, font_size )
        
        
    def adjust_form_label_font_size( self, base_font_size = 100 ):
        try:
            widget_width = self.form_labels[ 0 ].winfo_width()
            widget_height = self.form_labels[ 0 ].winfo_height()
        except:
            self.debug_print( "self.populate_entries not run yet" )
            return
        
        element_name = "form_labels"
        cached_font_size = self.FileAndChacheHandler.get_font_size( element_name )
        
        if cached_font_size is not None:
            self.forms_labels_font_size = cached_font_size
            for i in range( len( self.form_labels ) ):
                self.form_labels[ i ].config( font = ( "Arial", self.forms_labels_font_size ) )
            return
        
        element_text = self.form_labels[ 0 ].cget( "text" )
        
        max_width_ratio = 0.9
        max_height_ratio = 0.9
        max_width = int( widget_width * max_width_ratio )
        max_height = int( widget_height * max_height_ratio )
        self.forms_labels_font_size = base_font_size
        
        temp_font = font.Font( family = "Arial", size = self.forms_labels_font_size )
        text_width = temp_font.measure( element_text )
        text_height = temp_font.metrics( "linespace" )
                  
        width_ratio = max_width/text_width
        height_ratio = max_height/text_height
        ratio = min( width_ratio, height_ratio )
        if 0.8 < ratio and ratio < 1.1:
            return
        
        self.forms_labels_font_size = int( self.forms_labels_font_size * ratio )
        
        while True:
            temp_font = font.Font( family = "Arial", size = self.forms_labels_font_size )
            text_width = temp_font.measure( element_text )
            text_height = temp_font.metrics( "linespace" )
            if text_width <= max_width and text_height <= max_height:
                break
            
            self.forms_labels_font_size -= 1
            
            if self.forms_labels_font_size < 8:
                self.forms_labels_font_size = 8
                break
        
        for i in range( len( self.form_labels ) ):
            self.form_labels[ i ].config( font = ( "Arial", self.forms_labels_font_size ) )
        self.FileAndChacheHandler.cache_font_size( element_name, self.forms_labels_font_size )
            
            
    def adjust_title_font_size( self, base_font_size = 100 ):
        element_name = "title"
        cached_font_size = self.FileAndChacheHandler.get_font_size( element_name )
        
        if cached_font_size is not None:
            font_size = cached_font_size
            self.title.config( font = ( "Arial", font_size, "bold" ) )
            return
        
        element_text = self.title.cget( "text" )
            
        widget_width = self.title.winfo_width()
        widget_height = self.title.winfo_height()
        max_width_ratio = 0.75
        max_height_ratio = 0.75
        max_width = int( widget_width * max_width_ratio )
        max_height = int( widget_height * max_height_ratio )
        font_size = base_font_size
        
        temp_font = font.Font( family = "Arial", size = font_size, weight = "bold" )
        text_width = temp_font.measure( element_text )
        text_height = temp_font.metrics( "linespace" )
                  
        width_ratio = max_width/text_width
        height_ratio = max_height/text_height
        ratio = min( width_ratio, height_ratio )
        if 0.9 < ratio and ratio < 1.1:
            return
        
        font_size = int( font_size * ratio )
        
        while True:
            temp_font = font.Font( family = "Arial", size = font_size, weight = "bold" )
            text_width = temp_font.measure( element_text )
            text_height = temp_font.metrics( "linespace" )
             
            if text_width <= max_width and text_height <= max_height:
                break
            
            font_size -= 1
            if font_size < 10:
                font_size = 10
                break
            
        self.title.config( font = ( "Arial", font_size, "bold" ) )
        self.FileAndChacheHandler.cache_font_size( element_name, font_size )
    
    
    def adjust_canvas_window( self ):
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        new_width = canvas_width - 2      
        new_height = canvas_height - 2
        
        self.canvas.itemconfig( self.canvas_window, width = new_width, height = new_height )
        self.canvas.config(scrollregion = self.canvas.bbox( "all" ) )
            
            
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
            
            
    def debug_print( self, toPrint ):
        time = str( datetime.now() ) + ": "
        if ( self.debug == True ):
            print( time, toPrint )
            
    def enable_debug( self, event ):
        time = str( datetime.now() ) + ": "
        if self.debug == False:
            self.debug = True
            print( time, "Debug on" )
            info_Label = tk.Label( self.main_frame, text = "Debug on", font = ( "Arial", 25, "bold" ) )
            info_Label.place( relx = 0.5, rely = 0.5, height = 46, width = 150, anchor = "center" )
            self.root.update()
            self.root.after( 1900, info_Label.place_forget() )
            with open( self.settings_location, "r+" ) as file:
                settings = file.readlines()
                settings[ 0 ] = "debug=True\n"
                file.seek( 0 )
                file.writelines( settings )
                file.truncate()
                
        else:
            self.debug = False
            print( time, "Debug off" )
            info_Label = tk.Label( self.main_frame, text = "Debug off", font = ( "Arial", 25, "bold" ) )
            info_Label.place( relx = 0.5, rely = 0.5, height = 46, width = 150, anchor = "center" )
            self.root.update()
            self.root.after( 1900, info_Label.place_forget() )
            with open( self.settings_location, "r+" ) as file:
                settings = file.readlines()
                settings[0] = "debug=False\n"
                file.seek(0)
                file.writelines( settings )
                file.truncate()