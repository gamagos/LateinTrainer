import tkinter as tk
from tkinter import messagebox
import random

# Declension data with all five Latin declensions, including I-stem and neuter variants
declensions = {
    "A-Declension": {
        "nominative_singular": "puella",
        "genitive_singular": "puellae",
        "dative_singular": "puellae",
        "accusative_singular": "puellam",
        "ablative_singular": "puella",
        "nominative_plural": "puellae",
        "genitive_plural": "puellarum",
        "dative_plural": "puellis",
        "accusative_plural": "puellas",
        "ablative_plural": "puellis",
    },
    
    "      O-Declension": {
        "nominative_singular": "dominus",
        "genitive_singular": "domini",
        "dative_singular": "domino",
        "accusative_singular": "dominum",
        "ablative_singular": "domino",
        "nominative_plural": "domini",
        "genitive_plural": "dominorum",
        "dative_plural": "dominis",
        "accusative_plural": "dominos",
        "ablative_plural": "dominis",
    },
    
    "O-Declension Neuter": {
        "nominative_singular": "bellum",
        "genitive_singular": "belli",
        "dative_singular": "bello",
        "accusative_singular": "bellum",
        "ablative_singular": "bello",
        "nominative_plural": "bella",
        "genitive_plural": "bellorum",
        "dative_plural": "bellis",
        "accusative_plural": "bella",
        "ablative_plural": "bellis",
    },
    
    "Consonant-Declension": {
        "nominative_singular": "rex",
        "genitive_singular": "regis",
        "dative_singular": "regi",
        "accusative_singular": "regem",
        "ablative_singular": "rege",
        "nominative_plural": "reges",
        "genitive_plural": "regum",
        "dative_plural": "regibus",
        "accusative_plural": "reges",
        "ablative_plural": "regibus",
    },
    
    "Consonant-Declension Neuter": {
        "nominative_singular": "corpus",
        "genitive_singular": "corporis",
        "dative_singular": "corpori",
        "accusative_singular": "corpus",
        "ablative_singular": "corpore",
        "nominative_plural": "corpora",
        "genitive_plural": "corporum",
        "dative_plural": "corporibus",
        "accusative_plural": "corpora",
        "ablative_plural": "corporibus",
    },
    "Consonant-Declension Neuter with Genitive Plural -ium": {
        "nominative_singular": "animal",
        "genitive_singular": "animalis",
        "dative_singular": "animali",
        "accusative_singular": "animal",
        "ablative_singular": "animali",
        "nominative_plural": "animalia",
        "genitive_plural": "animalium",
        "dative_plural": "animalibus",
        "accusative_plural": "animalia",
        "ablative_plural": "animalibus",
    },
    
    "I-Declension": {
        "nominative_singular": "civis",
        "genitive_singular": "civis",
        "dative_singular": "civi",
        "accusative_singular": "civem",
        "ablative_singular": "cive",
        "nominative_plural": "cives",
        "genitive_plural": "civium",
        "dative_plural": "civibus",
        "accusative_plural": "cives",
        "ablative_plural": "civibus",
    },
    
    "I-Declension Neuter": {
        "nominative_singular": "mare",
        "genitive_singular": "maris",
        "dative_singular": "mari",
        "accusative_singular": "mare",
        "ablative_singular": "mari",
        "nominative_plural": "maria",
        "genitive_plural": "marium",
        "dative_plural": "maribus",
        "accusative_plural": "maria",
        "ablative_plural": "maribus",
    },
    
    "U-Declension": {
        "nominative_singular": "manus",
        "genitive_singular": "manus",
        "dative_singular": "manui",
        "accusative_singular": "manum",
        "ablative_singular": "manu",
        "nominative_plural": "manus",
        "genitive_plural": "manuum",
        "dative_plural": "manibus",
        "accusative_plural": "manus",
        "ablative_plural": "manibus",
    },
    
    "E-Declension": {
        "nominative_singular": "res",
        "genitive_singular": "rei",
        "dative_singular": "rei",
        "accusative_singular": "rem",
        "ablative_singular": "re",
        "nominative_plural": "res",
        "genitive_plural": "rerum",
        "dative_plural": "rebus",
        "accusative_plural": "res",
        "ablative_plural": "rebus",
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
        
        self.classes = list( declensions.keys() )
        random.shuffle( self.classes )  # Shuffle the order of declensions
        self.current_class_index = 0
        self.current_declension = declensions[ self.classes[ self.current_class_index ] ]
        
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
            
            if case == "nominative_singular":
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
            
            if case == "nominative_singular":
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
            
            if case == "nominative_singular" or self.results.get( case, True ):
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
            
            if case == "nominative_singular" or self.results.get( case, True ):
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
            self.current_declension = declensions[ self.classes[ self.current_class_index ] ]
            
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