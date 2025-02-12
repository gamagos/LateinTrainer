import tkinter as tk
from tkinter import messagebox
import random

# Deklinationen Daten mit allen fünf lateinischen Deklinationen, einschließlich I-Stamm und Neutrum-Varianten
deklinationen = {
    "A-Deklination": {
        "nominativ_singular": "puella",
        "genitiv_singular": "puellae",
        "dativ_singular": "puellae",
        "akkusativ_singular": "puellam",
        "ablativ_singular": "puella",
        "nominativ_plural": "puellae",
        "genitiv_plural": "puellarum",
        "dativ_plural": "puellis",
        "akkusativ_plural": "puellas",
        "ablativ_plural": "puellis",
    },
    
    "O-Deklination": {
        "nominativ_singular": "dominus",
        "genitiv_singular": "domini",
        "dativ_singular": "domino",
        "akkusativ_singular": "dominum",
        "ablativ_singular": "domino",
        "nominativ_plural": "domini",
        "genitiv_plural": "dominorum",
        "dativ_plural": "dominis",
        "akkusativ_plural": "dominos",
        "ablativ_plural": "dominis",
    },
    
    "O-Deklination Neutrum": {
        "nominativ_singular": "bellum",
        "genitiv_singular": "belli",
        "dativ_singular": "bello",
        "akkusativ_singular": "bellum",
        "ablativ_singular": "bello",
        "nominativ_plural": "bella",
        "genitiv_plural": "bellorum",
        "dativ_plural": "bellis",
        "akkusativ_plural": "bella",
        "ablativ_plural": "bellis",
    },
    
    "Konsonantische Deklination": {
        "nominativ_singular": "rex",
        "genitiv_singular": "regis",
        "dativ_singular": "regi",
        "akkusativ_singular": "regem",
        "ablativ_singular": "rege",
        "nominativ_plural": "reges",
        "genitiv_plural": "regum",
        "dativ_plural": "regibus",
        "akkusativ_plural": "reges",
        "ablativ_plural": "regibus",
    },
    
    "Konsonantische Deklination Neutrum": {
        "nominativ_singular": "corpus",
        "genitiv_singular": "corporis",
        "dativ_singular": "corpori",
        "akkusativ_singular": "corpus",
        "ablativ_singular": "corpore",
        "nominativ_plural": "corpora",
        "genitiv_plural": "corporum",
        "dativ_plural": "corporibus",
        "akkusativ_plural": "corpora",
        "ablativ_plural": "corporibus",
    },
    "Konsonantische Deklination Neutrum mit Genitiv Plural -ium": {
        "nominativ_singular": "animal",
        "genitiv_singular": "animalis",
        "dativ_singular": "animali",
        "akkusativ_singular": "animal",
        "ablativ_singular": "animali",
        "nominativ_plural": "animalia",
        "genitiv_plural": "animalium",
        "dativ_plural": "animalibus",
        "akkusativ_plural": "animalia",
        "ablativ_plural": "animalibus",
    },
    
    "I-Deklination": {
        "nominativ_singular": "civis",
        "genitiv_singular": "civis",
        "dativ_singular": "civi",
        "akkusativ_singular": "civem",
        "ablativ_singular": "cive",
        "nominativ_plural": "cives",
        "genitiv_plural": "civium",
        "dativ_plural": "civibus",
        "akkusativ_plural": "cives",
        "ablativ_plural": "civibus",
    },
    
    "I-Deklination Neutrum": {
        "nominativ_singular": "mare",
        "genitiv_singular": "maris",
        "dativ_singular": "mari",
        "akkusativ_singular": "mare",
        "ablativ_singular": "mari",
        "nominativ_plural": "maria",
        "genitiv_plural": "marium",
        "dativ_plural": "maribus",
        "akkusativ_plural": "maria",
        "ablativ_plural": "maribus",
    },
    
    "U-Deklination": {
        "nominativ_singular": "manus",
        "genitiv_singular": "manus",
        "dativ_singular": "manui",
        "akkusativ_singular": "manum",
        "ablativ_singular": "manu",
        "nominativ_plural": "manus",
        "genitiv_plural": "manuum",
        "dativ_plural": "manibus",
        "akkusativ_plural": "manus",
        "ablativ_plural": "manibus",
    },
    
    "E-Deklination": {
        "nominativ_singular": "res",
        "genitiv_singular": "rei",
        "dativ_singular": "rei",
        "akkusativ_singular": "rem",
        "ablativ_singular": "re",
        "nominativ_plural": "res",
        "genitiv_plural": "rerum",
        "dativ_plural": "rebus",
        "akkusativ_plural": "res",
        "ablativ_plural": "rebus",
    },
}

# Conjugation data with all Latin conjugations
conjugations = {
    "1st Conjugation": {
        "present_singular_1st": "amo",
        "present_singular_2nd": "amas",
        "present_singular_3rd": "amat",
        "present_plural_1st": "amamus",
        "present_plural_2nd": "amatis",
        "present_plural_3rd": "amant",
        "imperfect_singular_1st": "amabam",
        "imperfect_singular_2nd": "amabas",
        "imperfect_singular_3rd": "amabat",
        "imperfect_plural_1st": "amabamus",
        "imperfect_plural_2nd": "amabatis",
        "imperfect_plural_3rd": "amabant",
        "future_singular_1st": "amabo",
        "future_singular_2nd": "amabis",
        "future_singular_3rd": "amabit",
        "future_plural_1st": "amabimus",
        "future_plural_2nd": "amabitis",
        "future_plural_3rd": "amabunt",
    }
}

class LatinDeclensionApp:
    def __init__( self, root ):
        self.root = root
        self.root.title( "Latin Declension Trainer" )
        
        self.ORIGINAL_SCALE = 1.5  # Original scale factor
        self.ui_scale = self.ORIGINAL_SCALE  # Adjusted scale factor
        self.initial_width = self.root.winfo_screenwidth() // 2
        self.initial_height = self.root.winfo_screenheight() // 2
        self.root.geometry( f"{self.initial_width}x{self.initial_height}" )
        
        self.classes = list( deklinationen.keys() )
        random.shuffle( self.classes )  # Shuffle the order of declensions
        self.current_class_index = 0
        self.current_declension = deklinationen[ self.classes[ self.current_class_index ] ]
        
        self.entries = {}
        self.results = {}  # Variable to save whether the answer was right or wrong
        self.selected_option = tk.StringVar( value="Nouns-Declension" )  # Variable to save the selected option
        self.create_widgets()
        
        self.root.bind( "<Configure>", self.on_resize )
    
    def create_widgets( self ):
        self.main_frame = tk.Frame( self.root )
        self.main_frame.pack( fill="both", expand=True )
        
        self.label = tk.Label( self.main_frame, text=f"            {self.classes[self.current_class_index]}", font=("Arial", int( 20 * self.ui_scale ), "bold") )   #weird spaces because of offset in UI
        self.label.grid( row=0, column=0, pady=10, sticky="w" )  # Use grid layout
        
        self.option_menu = tk.OptionMenu( self.main_frame, self.selected_option, "Nouns-Declension", "Verbs-Konjugation" )
        self.option_menu.config( font=("Arial", 14) )  # Fixed font size
        self.option_menu.grid( row=0, column=1, pady=10, sticky="w" )  # Use grid layout
        
        self.frame = tk.Frame( self.main_frame )
        self.frame.grid( row=1, column=0, columnspan=2, sticky="nsew" )  # Use grid layout
        self.main_frame.grid_rowconfigure( 1, weight=1 )
        self.main_frame.grid_columnconfigure( 0, weight=1 )
        
        self.populate_entries()
        
        self.check_button = tk.Button( self.main_frame, text="Check", font=("Arial", int( 14 * self.ui_scale )), command=self.check_answers )
        self.check_button.grid( row=2, column=0, columnspan=2, pady=10 )  # Use grid layout
    
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
    
    def on_resize( self, event ):
        if event.widget == self.root:
            new_width = event.width
            new_height = event.height
            width_ratio = new_width / self.initial_width
            height_ratio = new_height / self.initial_height
            self.ui_scale = ( width_ratio + height_ratio ) / 2 * self.ORIGINAL_SCALE  # Adjust scale factor to use average
            
            self.label.config( font=("Arial", int( 20 * self.ui_scale ), "bold") )
            for widget in self.frame.winfo_children():
                if isinstance( widget, tk.Label ) or isinstance( widget, tk.Entry ):
                    widget.config( font=("Arial", int( 14 * self.ui_scale )) )
            self.check_button.config( font=("Arial", int( 14 * self.ui_scale )) )
            
            self.adjust_ui_elements()
    
    def adjust_ui_elements( self ):
        while self.is_overflowing():
            self.ui_scale -= 0.1
            self.label.config( font=("Arial", int( 20 * self.ui_scale ), "bold") )
            for widget in self.frame.winfo_children():
                if isinstance( widget, tk.Label ) or isinstance( widget, tk.Entry ):
                    widget.config( font=("Arial", int( 14 * self.ui_scale )) )
            self.check_button.config( font=( "Arial", int( 14 * self.ui_scale )) )
    
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
            self.current_declension = deklinationen[ self.classes[ self.current_class_index ] ]
            
            for widget in self.frame.winfo_children():
                widget.destroy()
                
            self.entries = {}
            self.results = {}  # Reset results for the new class
            self.label.config( text=f"            {self.classes[self.current_class_index]}" )   #weird spaces because of offset
            self.populate_entries()
        
root = tk.Tk()
root.resizable( False, False )
root.geometry("700x700")
app = LatinDeclensionApp( root )
root.mainloop()