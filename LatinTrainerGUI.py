from threading import main_thread
import Data
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import random

class LatinTrainerGUI:
    def __init__( self, root ):
        self.data_instance = Data.Data()
        self.deklinationen = self.data_instance.deklinationen
        
        self.root = root
        self.root.title( "Latin Trainer" )
        
        self.main_frame = tk.Frame( root )
        self.main_frame.place( relheight = 1, relwidth = 1 )
        
        self.canvas = tk.Canvas( self.main_frame )
        self.canvas.place( relheight = 0.95, relwidth = 0.95 )

        self.h_scrollbar = tk.Scrollbar( self.main_frame, orient = "horizontal", command = self.canvas.xview )
        self.h_scrollbar.place( relx = 0, rely = 0.97, relwidth = 0.976, relheight = 0.023 )

        self.v_scrollbar = tk.Scrollbar( self.main_frame, orient = "vertical", command = self.canvas.yview )
        self.v_scrollbar.place( relx = 0.97, rely = 0, relheight = 1, relwidth = 0.023 )
        
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
        
        self.canvas.bind_all("<MouseWheel>", self.on_mouse_wheel)
        self.canvas.bind_all("<Shift-MouseWheel>", self.on_shift_mouse_wheel)
        
        
    #puts stuff in the window that will always be there
    def create_widgets( self ):
        self.content_frame = tk.Frame( self.canvas )
        self.canvas_window = self.canvas.create_window( ( 0, 0 ), window = self.content_frame, anchor="nw" )
        
        self.label = tk.Label( self.content_frame, text = f"{ self.declension_classes[ self.current_class_index ] }",
                              font = ( "Arial", int( 18 * self.ui_scale ), "bold" ), anchor = "nw", justify = "left" )
        self.label.place( relx = 0.032, rely = 0.031, relheight = 0.19, relwidth = 0.71 )
        self.label.bind( "<Configure>", self.adjust_label_font_size )
        
        self.training_selection = ttk.Combobox( self.content_frame, textvariable = self.selected_option, values = [ "Nomen-Deklinationen", "Verben-Konjugation" ] ) 
        self.training_selection.place( relx = 0.974 , rely = 0, relheight = 0.023, relwidth = 0.181, anchor = "ne" )

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
        
        self.training_selection.tkraise()
        self.root.update()


    #puts the temporary stuff in the frame
    def populate_entries( self ):
        for i, ( case_or_tempus, correct_answer ) in enumerate( self.current_declension.items() ):
            label = tk.Label( self.forms_frame, text=case_or_tempus.replace( "_", " " ).capitalize(), font=( "Arial", int(14 * self.ui_scale ) ), anchor="nw", justify = "left" )
            label.place( relx = 0.013, rely = 0.065 * i, relwidth = 0.4, relheight = 0.06 )
            entry = tk.Entry( self.forms_frame, font = ( "Arial", int( 14 * self.ui_scale ) ) )
            
            if case_or_tempus == "nominativ_singular":
                entry.insert( 0, correct_answer )
                entry.config( state="disabled", disabledforeground="gray" )
                
            entry.place( relx = 0.36, rely = 0.065 * i )
            self.entries[ case_or_tempus ] = entry
            
            
    def adjust_label_font_size(self, event):
        widget = event.widget
        font_size = int(widget.winfo_height() * 0.2 )
        widget.config(font=("Arial", font_size))


    def adjust_button_font_size(self, event):
        widget = event.widget
        font_size = int(widget.winfo_height() * 0.4 )
        widget.config(font=("Arial", font_size))
    
    
    def on_frame_configure( self, event ):
        self.canvas.config( scrollregion = self.canvas.bbox( "all" ) )
        self.root.update()
    
    
    def resize_content_frame(self, event):
        root_width = self.root.winfo_width()
        root_height = self.root.winfo_height()
        
        new_width = root_width - self.v_scrollbar.winfo_width() - 2                           # Leave space for the vertical scrollbar
        new_height = root_height - self.h_scrollbar.winfo_height() - 2                        # Leave space for the horizontal scrollbar
        
        self.canvas.itemconfig( self.canvas_window, width=new_width, height=new_height )
        self.canvas.config(scrollregion=self.canvas.bbox( "all" ) )


    def on_mouse_wheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    
    
    def on_shift_mouse_wheel(self, event):
        self.canvas.xview_scroll(int(-1*(event.delta/120)), "units")
    
    
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