import LatinTrainerGUI

import tkinter as tk

LatinTrainerGUI1 = LatinTrainerGUI.LatinDeclensionApp
        
root = tk.Tk()
root.resizable( False, False )
root.geometry("700x700")
app = LatinTrainerGUI1( root )
root.mainloop()