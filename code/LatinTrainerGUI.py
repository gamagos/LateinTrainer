import select
from threading import main_thread
import Data
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import random

class LatinTrainerGUI:
    def __init__( self, root ):
        version = "v1.4.1"
        self.data = Data.Data()
        
        self.declensions_nouns = self.data.declensions
        self.conjugations = self.data.conjugations
        #self.declensions_adjectives = self.data.declensions_adjectives
        #self.hic_haec_hoc = self.data.hic_haec_hoc
        #self.qui_quae_quod = self.data.qui_quae_qoud
        #self.ille_illa_illud = self.data.ille_illa_illud
        #self.ipse_ipsa_ipsum = self.data.ipse_ipsa_ipsum
        
        self.root = root
        self.root.title( "Latin Trainer " + version )
        
        self.main_frame = tk.Frame( root )
        self.main_frame.place( relheight = 1, relwidth = 1 )
        
        self.canvas = tk.Canvas( self.main_frame )
        self.canvas.place( relheight = 0.96, relwidth = 0.96 )

        self.h_scrollbar = tk.Scrollbar( self.main_frame, orient = "horizontal", command = self.canvas.xview )
        self.h_scrollbar.place( relx = 0, rely = 0.97, relwidth = 0.976, relheight = 0.023 )

        self.v_scrollbar = tk.Scrollbar( self.main_frame, orient = "vertical", command = self.canvas.yview )
        self.v_scrollbar.place( relx = 0.97, rely = 0, relheight = 1, relwidth = 0.023 )
        
        self.canvas.config( yscrollcommand = self.v_scrollbar.set, xscrollcommand = self.h_scrollbar.set )
        
        self.ORIGINAL_SCALE = 1.5 
        self.ui_scale = self.ORIGINAL_SCALE  
        
        self.declension_forms = list( self.declensions_nouns.keys() )
        self.conjugation_forms = list( self.conjugations.keys() )
        self.hic_haec_hoc_forms = list( self.hic_haec_hoc.keys() )
        self.qui_quae_quod_forms = list( self.qui_quae_quod.keys() )
        random.shuffle( self.declension_forms )
        random.shuffle( self.conjugation_forms )
        random.shuffle( self.hic_haec_hoc_forms )
        random.shuffle( self.qui_quae_quod_forms )                                          
        self.current_class_index = 0
        self.selected_option = tk.StringVar( value = "Alle" )
        self.previous_form = self.selected_option.get()
        
        self.form_select()
                
        self.entries = {}
        self.results = {}                                     # Variable to save whether the answer was right or wrong
        
        self.create_widgets()
        self.resize_content_frame( None )
        
        self.canvas.bind_all( "<MouseWheel>", self.on_mouse_wheel )
        self.canvas.bind_all( "<Shift-MouseWheel>", self.on_shift_mouse_wheel )
        
        
    def form_select( self ):         
        if self.selected_option.get() == "Alle":
            choices = [ "Nomen", "Verben" ] 
            word_type = random.choice( choices )

            if word_type == "Nomen":
                self.current_key = self.declension_forms[ self.current_class_index ]
                self.current_forms = self.declensions_nouns[ self.current_key ]
                self.curent_word_type_amount_of_forms = len( self.declension_forms )
                
            elif word_type == "Verben":
                self.current_key = self.conjugation_forms[ self.current_class_index ]
                self.current_forms = self.conjugations[ self.current_key ]
                self.curent_word_type_amount_of_forms = len( self.conjugation_forms )
                
            self.previous_form = self.selected_option.get()

        elif self.selected_option.get() == "Nomen":
            self.current_key = self.declension_forms[ self.current_class_index ]
            self.current_forms = self.declensions_nouns[ self.current_key ]
            self.curent_word_type_amount_of_forms = len( self.declension_forms )
            
        elif self.selected_option.get() == "Verben":
            self.current_key = self.conjugation_forms[ self.current_class_index ]
            self.current_forms = self.conjugations[ self.current_key ]
            self.curent_word_type_amount_of_forms = len( self.conjugation_forms )
            
            self.previous_form = self.selected_option.get()
        else:
            messagebox.showerror( "Fehler:\n Programm konnte die Form nicht auswählen" )
        
        
    #puts stuff in the window that will always be there
    def create_widgets( self ):
        self.content_frame = tk.Frame( self.canvas )
        self.canvas_window = self.canvas.create_window( ( 0, 0 ), window = self.content_frame, anchor = "nw" )
        
        self.titel = tk.Label( self.content_frame, text = f"{ self.current_key }",
                              font = ( "Arial", int( 19 * self.ui_scale ), "bold" ), anchor = "n", justify = "left" )
        self.titel.place( relx = 0.032, rely = 0.031, relheight = 0.19, relwidth = 0.81 )
        self.titel.bind( "<Configure>", self.adjust_titel_font_size )
        
        self.combobox_select_form = ttk.Combobox( self.content_frame, textvariable = self.selected_option, values = [ "Alle", "Nomen", "Verben" ] ) 
        self.combobox_select_form.place( relx = 0.974 , rely = 0, relheight = 0.025, relwidth = 0.18, anchor = "ne" )
        self.combobox_select_form.state( ["readonly"] )
        self.combobox_select_form.bind( "<<ComboboxSelected>>", self.on_form_select )

        self.forms_frame = tk.Frame( self.content_frame )
        self.forms_frame.place( relx = 0.02, rely = 0.16, relwidth = 0.9, relheight = 0.7 )
        
        self.populate_entries()
        
        self.check_button = tk.Button( self.content_frame, text="Überprüfen", command=self.check_answers )
        self.check_button.place( relx = 0.45, rely = 0.8, relheight = 0.08, relwidth = 0.24 )
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
                
            entry.place( relx = 0.39, rely = 0.07 * self.separation_form_tabel, relwidth = 0.6, relheight = 0.08 )
            self.entries[ case_or_tempus ] = entry
            
            self.titel.config( text = f"{ self.current_key }" )
            
            
    def adjust_titel_font_size( self, event ):
        widget = event.widget
        font_size = int( widget.winfo_height() / len( widget.cget("text")) * 6 )
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
        if self.previous_form != self.selected_option.get():
            self.next_class()
        print( self.previous_form + " != " + self.selected_option.get() )
    
    
    def resize_content_frame(self, event):
        root_width = self.root.winfo_width()
        root_height = self.root.winfo_height()
        
        new_width = root_width - self.v_scrollbar.winfo_width() - 2                       
        new_height = root_height - self.h_scrollbar.winfo_height() - 2                      
        
        self.canvas.itemconfig( self.canvas_window, width=new_width, height=new_height )
        self.canvas.config(scrollregion=self.canvas.bbox( "all" ) )


    def on_mouse_wheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    
    
    def on_shift_mouse_wheel(self, event):
        self.canvas.xview_scroll(int(-1*(event.delta/120)), "units")
    
    
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
            messagebox.showinfo( "Fertig", "Du es geschafft!" )
            self.root.quit()
        else:
            self.form_select()
            
            for widget in self.forms_frame.winfo_children():
                widget.destroy()
                
            self.entries = {}
            self.results = {}         
            self.populate_entries()