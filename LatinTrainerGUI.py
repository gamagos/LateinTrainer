import data
import tkinter as tk
from tkinter import messagebox

import random

class LatinTrainerGUI:
    def __init__( self, root ):
        data_instance = data.data()
        self.deklinationen = data_instance.deklinationen
        
        self.root = root
        self.root.title( "Latin Declension Trainer" )
        
        self.canvas = tk.Canvas( root )
        self.canvas.pack( side = "left", fill = "both", expand = True )

        self.v_scrollbar = tk.Scrollbar( root, orient = "vertical", command = self.canvas.yview )
        self.v_scrollbar.pack( side = "right", fill = "y" )
        
        self.canvas.config( yscrollcommand = self.scrollbar.set )
        
        self.ORIGINAL_SCALE = 1.5  # Original scale factor
        self.ui_scale = self.ORIGINAL_SCALE  # Adjusted scale factor
        
        self.classes = list( self.deklinationen.keys() )
        random.shuffle( self.classes )  # Shuffle the order of declensions
        self.current_class_index = 0
        self.current_declension = self.deklinationen[ self.classes[ self.current_class_index ] ]
        
        self.entries = {}
        self.results = {}  # Variable to save whether the answer was right or wrong
        self.selected_option = tk.StringVar( value="Nouns-Declension" )  # Variable to save the selected option
        self.create_widgets()
    
    def create_widgets( self ):
        self.main_frame = tk.Frame( self.root )
        self.canvas.create_window( ( 0, 0 ), window = self.main_frame, anchor = "nw" )
        
        self.label = tk.Label( self.main_frame, text=f"          {self.classes[self.current_class_index]}", font=("Arial", int( 20 * self.ui_scale ), "bold") )   #weird spaces because of offset in UI
        self.label.grid( row=0, column=0, pady=10, sticky="w" )  # Use grid layout
        
        self.option_menu = tk.OptionMenu( self.main_frame, self.selected_option, "Nouns-Declension", "Verbs-Konjugation" )
        self.option_menu.config( font = ( "Arial", 10 ) )  # Fixed font size
        self.option_menu.grid( row=0, column=1, pady=10, sticky="w" )  # Use grid layout
        
        self.frame = tk.Frame( self.main_frame )
        self.frame.grid( row=1, column = 0, columnspan = 2, sticky = "nsew" )  # Use grid layout
        self.main_frame.grid_rowconfigure( 1, weight = 1 )
        self.main_frame.grid_columnconfigure( 0, weight = 1 )
        
        self.populate_entries()
        
        self.check_button = tk.Button( self.main_frame, text="Check", font=("Arial", int( 14 * self.ui_scale )), command=self.check_answers )
        self.check_button.grid( row=2, column=0, columnspan=2, pady=10,  )  # Use grid layout
        
        self.main_frame.update_idletasks()
        self.canvas.config( scrollregion = self.canvas.bbox( "all" ) )
        self.main_frame.bind( "<Configure>", self.self_on_frame_configure )

    def self_on_frame_configure( self, event ):
        self.canvas.config( scrollregion = self.canvas.bbox( "all" ) )
    
    def populate_entries( self ):
        for i, ( case, correct_answer ) in enumerate( self.current_declension.items() ):
            label = tk.Label( self.frame, text=case.replace( "_", " " ).capitalize(), font=("Arial", int( 14 * self.ui_scale )) )
            label.grid( row=i, column=0, padx=5, pady=5, sticky="e" )  # Use grid layout
            entry = tk.Entry( self.frame, font=("Arial", int( 14 * self.ui_scale )) )
            
            if case == "nominativ_singular":
                entry.insert( 0, correct_answer )
                entry.config( state="disabled", disabledforeground="gray" )
                
            entry.grid( row=i, column=1, padx=5, pady=5, sticky="w" )  # Use grid layout
            self.entries[ case ] = entry
    
    def is_overflowing( self ):
        self.root.update_idletasks()
        return self.frame.winfo_reqwidth() > self.root.winfo_width() or self.frame.winfo_reqheight() > self.root.winfo_height()
    
    def check_answers( self ):
        wrong = False
        
        for case, correct_answer in self.current_declension.items():
            
            if case == "nominativ_singular":
                continue
            user_input = self.entries[ case ].get().strip()
            
            if user_input == correct_answer:
                self.entries[ case ].config( fg="green", state="disabled", disabledforeground="green" )
                self.results[ case ] = True 
                
            else:
                wrong = True
                self.entries[ case ].config( fg="red", state="disabled", disabledforeground="red" )
                self.results[ case ] = False
        
        if wrong:
            self.check_button.config( text="Show Solutions", command=self.show_solutions )
            
        else:
            messagebox.showinfo( "Correct!", "You got all answers right!" )
            self.next_class()
    
    def show_solutions( self ):
        for case, correct_answer in self.current_declension.items():
            
            if case == "nominativ_singular" or self.results.get( case, True ):
                continue
            
            user_input = self.entries[ case ].get().strip()
            
            if user_input != correct_answer:
                self.entries[ case ].config( fg="blue", state="normal" )
                self.entries[ case ].delete( 0, tk.END )
                self.entries[ case ].insert( 0, correct_answer )
                self.entries[ case ].config( state="disabled", disabledforeground="blue" )
        
        self.check_button.config( text="Retry", command=self.retry )
    
    def retry( self ):
        for case, correct_answer in self.current_declension.items():
            
            if case == "nominativ_singular" or self.results.get( case, True ):
                continue
            
            self.entries[ case ].config( fg="black", state="normal" )
            self.entries[ case ].delete( 0, tk.END )
        
        self.check_button.config( text="Check", command=self.check_answers )
    
    def next_class( self ):
        self.current_class_index += 1
        
        if self.current_class_index >= len( self.classes ):
            messagebox.showinfo( "Done", "You have completed all declensions!" )
            self.root.quit()
            
        else:
            self.current_declension = self.deklinationen[ self.classes[ self.current_class_index ] ]
            
            for widget in self.frame.winfo_children():
                widget.destroy()
                
            self.entries = {}
            self.results = {}  # Reset results for the new class
            self.label.config( text=f"          {self.classes[self.current_class_index]}" )   #weird spaces because of offset
            self.populate_entries()