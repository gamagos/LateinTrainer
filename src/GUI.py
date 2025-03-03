import os
import random
import shutil
import sys
import tkinter as tk
from datetime import datetime
from tkinter import messagebox, ttk

from data.Data import Data


class GUI:
    def __init__( self, root ):
        self.project_path = getattr( sys, "_MEIPASS", os.path.dirname( os.path.dirname( os.path.abspath( __file__ ) ) ) )
        self.settings_location = os.path.join( self.project_path, "data", "settings.csv" )
        self.settings_default_location = os.path.join( self.project_path, "data", "default_settings.csv" )
        self.icon_path = os.path.join( self.project_path, "assets", "icon.ico" )
        self.debug = True         
        self.tests = False        
        version = "v1.6.2"    
        self.data = Data()
        
        self.declensions_nouns = self.data.declensions
        self.conjugations = self.data.conjugations
        self.declensions_adjectives = self.data.declensions_adjectives
        #pronouns
        self.hic_haec_hoc = self.data.hic_haec_hoc
        self.qui_quae_quod = self.data.qui_quae_qoud
        self.ille_illa_illud = self.data.ille_illa_illud
        self.ipse_ipsa_ipsum = self.data.ipse_ipsa_ipsum
        
        self.root = root
        self.root.title( "Latin Trainer " + version )
        self.root.bind( "<F3>", self.enable_debug )
        self.root.iconbitmap( self.icon_path )
        self.debug_print( "Root was initialized" )
        
        self.main_frame = tk.Frame( root )
        self.main_frame.place( relheight = 1, relwidth = 1 )
        
        self.canvas = tk.Canvas( self.main_frame )
        self.canvas.place( relheight = 0.93, relwidth = 0.93 )
        self.canvas.bind( "<Enter>", self.on_canvas_enter )
        self.canvas.bind( "<Leave>", self.on_canvas_leave )

        self.h_scrollbar = tk.Scrollbar( self.main_frame, orient = "horizontal", command = self.canvas.xview )
        self.h_scrollbar.place( relx = 0, rely = 0.97, relwidth = 0.97, relheight = 0.03 )

        self.v_scrollbar = tk.Scrollbar( self.main_frame, orient = "vertical", command = self.canvas.yview )
        self.v_scrollbar.place( relx = 0.97, rely = 0, relheight = 1, relwidth = 0.03 )
        
        self.canvas.config( yscrollcommand = self.v_scrollbar.set, xscrollcommand = self.h_scrollbar.set )
        
        self.ORIGINAL_SCALE = 1.5 
        self.ui_scale = self.ORIGINAL_SCALE  
        
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
        
        self.get_settings()
        
        self.form_select()
        self.debug_print( "Form was selected" )
                
        self.entries = {}
        self.results = {}                                     # Variable to save whether the answer was right or wrong
        
        self.create_widgets()
        self.resize_content_frame( None )
        self.debug_print( "Frame was filled" ) 
        
        self.canvas.bind_all( "<MouseWheel>", self.on_mouse_wheel )
        self.canvas.bind_all( "<Shift-MouseWheel>", self.on_shift_mouse_wheel )
        
        
    def get_settings( self ):    
        if ( os.path.getsize( self.settings_location ) == 0 ):
            with open( self.settings_location, "w" ) as file:
                shutil.copyfile( self.settings_default_location, self.settings_location )
                print( "settings were restored(empty)" )
        else:
            try:
                with open( self.settings_location, "r" ) as file:
                    self.contents = file.readlines()
                    self.debug = "True" == self.contents[ 0 ].split( "=" )[ 1 ].strip()
                    self.tests = "True" == self.contents[ 1 ].split( "=" )[ 1 ].strip()
                    self.selected_option.set( self.contents[ 2 ].split( "=" )[ 1 ].strip() )
                    print( "settings were read successfully" )
                    self.debug_print( " ".join( [ item.split( "=" )[ 1 ].strip() for item in self.contents ] ) )
                                  
            except Exception as e:
                with open( self.settings_location, "w" ) as file:
                    shutil.copyfile( self.settings_default_location, self.settings_location )
                    print( f"settings were restored(error in settings file): { e }" )
        
        
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
            self.get_settings()
            self.form_select()

        self.previous_form = self.selected_option.get()
        
        
    def create_widgets( self ):
        self.content_frame = tk.Frame( self.canvas )
        self.canvas_window = self.canvas.create_window( ( 0, 0 ), window = self.content_frame, anchor = "nw" )
        
        self.titel = tk.Label( self.content_frame, text = f"{ self.current_key }",
                              font = ( "Arial", int( 19 * self.ui_scale ), "bold" ), anchor = "n", justify = "left" )
        self.titel.place( relx = 0.032, rely = 0.031, relheight = 0.19, relwidth = 0.81 )
        self.titel.bind( "<Configure>", self.adjust_titel_font_size )
        
        self.combobox_select_form = ttk.Combobox( self.content_frame, textvariable = self.selected_option, values = [ "Alle", "Nomen", "Verben", "Adjektive", "hic haec hoc", "qui quae quod", "ille illa illud", "ipse ipsa ipsum" ] ) 
        self.combobox_select_form.place( relx = 0.96 , rely = 0, relheight = 0.025, relwidth = 0.18, anchor = "ne" )
        self.combobox_select_form.state( ["readonly"] )
        self.combobox_select_form.bind( "<<ComboboxSelected>>", self.on_form_select )

        self.forms_frame = tk.Frame( self.content_frame )
        self.forms_frame.place( relx = 0.02, rely = 0.16, relwidth = 0.9, relheight = 0.7 )
        
        self.populate_entries()
        
        self.check_button = tk.Button( self.content_frame, text = "Überprüfen", command = self.check_answers )
        self.check_button.place( relx = 0.45, rely = 0.75, relheight = 0.08, relwidth = 0.24 )
        self.check_button.bind( "<Configure>", self.adjust_button_font_size )
        
        self.content_frame.update_idletasks()
        self.canvas.config( scrollregion = self.canvas.bbox( "all" ) )
        self.content_frame.bind( "<Configure>", self.on_frame_configure )
        self.root.bind( "<Configure>", self.resize_content_frame )
        
        self.combobox_select_form.tkraise()
        self.root.update()


    #puts the temporary stuff in the frame
    def populate_entries( self ):
        self.separation_form_tabel = -1
        for i, ( case_or_tempus, correct_answer ) in enumerate( self.current_forms.items() ):
            
            if case_or_tempus == "Nominativ_Plural" or case_or_tempus == "1._Person_Plural":
                self.separation_form_tabel += 1
                
            self.separation_form_tabel += 1          
            form_label = tk.Label( self.forms_frame, text = case_or_tempus.replace( "_", " " ), font = ( "Arial", int( 14 * self.ui_scale ) ), anchor = "nw", justify = "left" )
            form_label.place( relx = 0.013, rely = 0.07 * self.separation_form_tabel, relwidth = 0.4, relheight = 0.08 )
            form_label.bind( "<Configure>", self.adjust_forms_label_font_size )
            
            entry = tk.Entry( self.forms_frame, font = ( "Arial", int( 14 * self.ui_scale ) ) )
            
            if case_or_tempus == "Nominativ_Singular":
                entry.insert( 0, correct_answer )
                entry.config( state = "disabled", disabledforeground = "gray" )
                
            entry.place( relx = 0.4, rely = 0.07 * self.separation_form_tabel, relwidth = 0.6, relheight = 0.08 )
            self.entries[ case_or_tempus ] = entry
            
        self.titel.config( text = f"{ self.current_key }" )
            
            
    def adjust_titel_font_size( self, event ):
        widget = event.widget
        font_size = int( 20 )       #TODO make a good method to select label size
        widget.config( font = ( "Arial", font_size, "bold" ) )


    def adjust_button_font_size( self, event ):
        widget = event.widget
        font_size = int( widget.winfo_height() * 0.4 )
        widget.config( font = ( "Arial", font_size ) )
        
        
    def adjust_forms_label_font_size( self, event ):
        widget = event.widget
        font_size = int( widget.winfo_height() *  0.5 )
        widget.config( font = ( "Arial", font_size ) )
        
    
    def on_frame_configure( self, event ):
        self.canvas.config( scrollregion = self.canvas.bbox( "all" ) )
        self.root.update()
    
    
    def on_form_select( self, event ):
        self.current_class_index = 0
        if self.previous_form != self.selected_option.get():
            self.next_class()
            
            with open( self.settings_location, "r+" ) as file:
                settings = file.readlines()
                settings[ 2 ] = f"selected_option={ self.selected_option.get() }"
                file.seek( 0 )
                file.writelines( settings )
                file.truncate()
    
    
    def resize_content_frame(self, event):
        root_width = self.root.winfo_width()
        root_height = self.root.winfo_height()
        
        new_width = root_width - self.v_scrollbar.winfo_width() - 4                    
        new_height = root_height - self.h_scrollbar.winfo_height() - 4                      
        
        self.canvas.itemconfig( self.canvas_window, width = new_width, height = new_height )
        self.canvas.config(scrollregion = self.canvas.bbox( "all" ) )


    def on_mouse_wheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    
    
    def on_shift_mouse_wheel(self, event):
        self.canvas.xview_scroll(int(-1*(event.delta/120)), "units")
        
    #make bigger hitbox, make go away after inactive, make go away after frame leave
    def on_canvas_enter( self, event ):
        self.h_scrollbar.place_forget()
        self.v_scrollbar.place_forget()
        
        
    def on_canvas_leave( self, event ):
        self.h_scrollbar.place( relx = 0, rely = 0.97, relwidth = 0.97, relheight = 0.03 )
        self.v_scrollbar.place( relx = 0.97, rely = 0, relheight = 1, relwidth = 0.03 )
    
    
    def check_answers( self ):
        wrong = False
        
        for case_or_tempus, correct_answer in self.current_forms.items():
            
            if case_or_tempus == "Nominativ_Singular" or case_or_tempus == "1._Person_Singular":
                continue
            user_input = self.entries[ case_or_tempus ].get().strip()
            
            if user_input == correct_answer:
                self.entries[ case_or_tempus ].config(fg = "green", state = "disabled", disabledforeground = "green")
                self.results[ case_or_tempus ] = True 
            else:
                wrong = True
                self.entries[ case_or_tempus ].config(fg = "red", state = "disabled", disabledforeground = "red")
                self.results[ case_or_tempus ] = False
        
        if wrong:
            self.check_button.config( text = "Show Solutions", command = self.show_solutions ) 
        else:
            self.next_class()
    
    
    def show_solutions( self ):
        for case_or_tempus, correct_answer in self.current_forms.items():
            
            if case_or_tempus == "Nominativ_Singular" or self.results.get( case_or_tempus, True ) or case_or_tempus == "1._Person_Singular":
                continue
            
            user_input = self.entries[case_or_tempus].get().strip()
            
            if user_input != correct_answer:
                self.entries[ case_or_tempus ].config( fg = "blue", state = "normal" )
                self.entries[ case_or_tempus ].delete( 0, tk.END )
                self.entries[ case_or_tempus ].insert( 0, correct_answer )
                self.entries[ case_or_tempus ].config( state = "disabled", disabledforeground = "blue" )
        
        self.check_button.config(text="Retry", command=self.retry)
    
    
    def retry(self):
        for case, correct_answer in self.current_forms.items():
            
            if case == "nominativ_singular" or self.results.get(case, True):
                continue
            
            self.entries[case].config(fg="black", state="normal")
            self.entries[case].delete(0, tk.END)
        
        self.check_button.config(text="Check", command=self.check_answers)
    

    def next_class( self ):
        self.current_class_index += 1
        
        if self.current_class_index >= self.curent_word_type_amount_of_forms:
            self.current_class_index = 0
        else:
            self.form_select()
            
            for widget in self.forms_frame.winfo_children():
                widget.destroy()
                
            self.entries = {}
            self.results = {}         
            self.populate_entries()
            
    def debug_print( self, toPrint ):
        time = str( datetime.now() ) + ": "
        if ( self.debug == True ):
            print( time, toPrint )
            
    def enable_debug( self, event ):
        time = str( datetime.now() ) + ": "
        if self.debug == False:
            self.debug = True
            print( time, "Debug on" )
            self.info_Label = tk.Label( self.main_frame, text = "Debug on", font = ( "Arial", 25, "bold" ) )
            self.info_Label.place( relx = 0.5, rely = 0.5, height = 46, width = 150, anchor = "center" )
            self.root.update()
            self.root.after( 1900, self.info_Label.place_forget() )
            with open( self.settings_location, "r+" ) as file:
                settings = file.readlines()
                settings[0] = "debug=True\n"
                file.seek(0)
                file.writelines( settings )
                file.truncate()
                
        else:
            self.debug = False
            print( time, "Debug off" )
            self.info_Label = tk.Label( self.main_frame, text = "Debug off", font = ( "Arial", 25, "bold" ) )
            self.info_Label.place( relx = 0.5, rely = 0.5, height = 46, width = 150, anchor = "center" )
            self.root.update()
            self.root.after( 1900, self.info_Label.place_forget() )
            with open( self.settings_location, "r+" ) as file:
                settings = file.readlines()
                settings[0] = "debug=False\n"
                file.seek(0)
                file.writelines( settings )
                file.truncate()