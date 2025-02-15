from threading import main_thread
import Data
import tkinter as tk
from tkinter import messagebox
import random

class LatinTrainerGUI:
    def __init__( self, root ):
        data_instance = Data.Data()
        self.deklinationen = data_instance.deklinationen
        
        self.root = root
        self.root.title( "Latin Trainer" )
        
        self.main_frame = tk.Frame( root )
        self.main_frame.place( relheight = 1, relwidth = 1 )
        
        self.canvas = tk.Canvas( self.main_frame )
        self.canvas.place( relheight = 0.95, relwidth = 0.95 )

        self.h_scrollbar = tk.Scrollbar( self.main_frame, orient="horizontal", command=self.canvas.xview )
        self.h_scrollbar.place( relx = 0, rely = 0.95, relwidth = 0.95, height = 20 )

        self.v_scrollbar = tk.Scrollbar( self.main_frame, orient="vertical", command=self.canvas.yview )
        self.v_scrollbar.place( relx = 0.95, rely = 0, relheight = 0.95, width = 20 )
        
        self.canvas.config( yscrollcommand=self.v_scrollbar.set, xscrollcommand=self.h_scrollbar.set )
        
        self.ORIGINAL_SCALE = 1.5 
        self.ui_scale = self.ORIGINAL_SCALE  
        
        self.declension_classes = list( self.deklinationen.keys() )
        random.shuffle( self.declension_classes )                                                                  # Shuffle the order of declensions
        self.current_class_index = 0
        self.current_declension = self.deklinationen[ self.declension_classes[ self.current_class_index ] ]
        
        self.entries = {}
        self.results = {}                                                                                          # Variable to save whether the answer was right or wrong
        self.selected_option = tk.StringVar( value = "Nomen-Deklinationen" )  
        
        self.create_widgets()
        self.resize_content_frame(None)
        
        
    #puts stuff in the window that will always be there
    def create_widgets( self ):
        self.content_frame = tk.Frame( self.canvas )
        self.canvas_window = self.canvas.create_window( ( 0, 0 ), window = self.content_frame, anchor="nw" )
        
        self.label = tk.Label( self.content_frame, text = f"{ self.declension_classes[ self.current_class_index ] }", font = ( "Arial", int( 20 * self.ui_scale ), "bold" ) )   #weird spaces because of offset in UI
        self.label.place( x = 10, y = 10 )
        
        self.option_menu = tk.OptionMenu( self.content_frame, self.selected_option, "Nomen-Deklinationen", "Verben-Konjugation" )
        self.option_menu.config( font = ( "Arial", 10 ) ) 
        self.option_menu.place( relx = 0.9, y = 15 )
        
        self.forms_frame = tk.Frame( self.content_frame )
        self.forms_frame.place( x = 10, y = 50, relwidth = 0.9, relheight = 0.7 )
        
        self.populate_entries()
        
        self.check_button = tk.Button(self.content_frame, text="Überprüfen", font=("Arial", int(14 * self.ui_scale)), command=self.check_answers)
        self.check_button.place( relx = 0.45, rely = 0.8 )
        
        self.content_frame.update_idletasks()
        self.canvas.config( scrollregion = self.canvas.bbox( "all" ) )
        self.content_frame.bind( "<Configure>", self.on_frame_configure )
        self.root.bind( "<Configure>", self.resize_content_frame )


    def resize_content_frame(self, event):
        root_width = self.root.winfo_width()
        root_height = self.root.winfo_height()
        
        new_width = root_width - self.v_scrollbar.winfo_width() - 2                           # Leave space for the vertical scrollbar
        new_height = root_height - self.h_scrollbar.winfo_height() - 2                        # Leave space for the horizontal scrollbar
        
        self.canvas.itemconfig( self.canvas_window, width=new_width, height=new_height )
        self.canvas.config(scrollregion=self.canvas.bbox( "all" ) )

    def on_frame_configure( self, event ):
        self.canvas.config( scrollregion = self.canvas.bbox( "all" ) )
    
    
    #puts the temporary stuff in the frame
    def populate_entries( self ):
        for i, ( case_or_tempus, correct_answer ) in enumerate( self.current_declension.items() ):
            label = tk.Label( self.forms_frame, text=case_or_tempus.replace( "_", " " ).capitalize(), font=( "Arial", int(14 * self.ui_scale ) ) )
            label.place( x = 10, y = 30 * i )
            entry = tk.Entry( self.forms_frame, font = ( "Arial", int( 14 * self.ui_scale ) ) )
            
            if case_or_tempus == "nominativ_singular":
                entry.insert( 0, correct_answer )
                entry.config( state="disabled", disabledforeground="gray" )
                
            entry.place( x = 200, y = 30 * i )
            self.entries[ case_or_tempus ] = entry
    
    
    def check_answers( self ):
        wrong = False
        
        for case_or_tempus, correct_answer in self.current_declension.items():
            
            if case_or_tempus == "nominativ_singular":
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
            messagebox.showinfo( "Correct!", "You got all answers right!" )
            self.next_class()
    
    
    def show_solutions( self ):
        for case, correct_answer in self.current_declension.items():
            
            if case == "nominativ_singular" or self.results.get( case, True ):
                continue
            
            user_input = self.entries[case].get().strip()
            
            if user_input != correct_answer:
                self.entries[ case ].config( fg = "blue", state = "normal" )
                self.entries[ case ].delete( 0, tk.END )
                self.entries[ case ].insert( 0, correct_answer )
                self.entries[ case ].config( state = "disabled", disabledforeground = "blue" )
        
        self.check_button.config(text="Retry", command=self.retry)
    
    
    def retry(self):
        for case, correct_answer in self.current_declension.items():
            
            if case == "nominativ_singular" or self.results.get(case, True):
                continue
            
            self.entries[case].config(fg="black", state="normal")
            self.entries[case].delete(0, tk.END)
        
        self.check_button.config(text="Check", command=self.check_answers)
    
    
    #removes the temporary stuff from the frame
    def next_class( self ):
        self.current_class_index += 1
        
        if self.current_class_index >= len(self.declension_classes):
            messagebox.showinfo("Done", "You have completed all declensions!")
            self.root.quit()
            
        else:
            self.current_declension = self.deklinationen[self.declension_classes[self.current_class_index]]
            
            for widget in self.forms_frame.winfo_children():
                widget.destroy()
                
            self.entries = {}
            self.results = {}                                                                                                 # Reset results for the new class
            self.label.config(text=f"{self.declension_classes[self.current_class_index]}")
            self.populate_entries()