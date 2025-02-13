import tkinter as tk
from tkinter import messagebox
import random

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
        
root = tk.Tk()
root.resizable( False, False )
root.geometry("700x700")
app = LatinDeclensionApp( root )
root.mainloop()