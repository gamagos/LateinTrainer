import LatinTrainerGUI
import tkinter as tk
        
root = tk.Tk()
root.resizable( False, False )
root.geometry("800x700")

app = LatinTrainerGUI.LatinTrainerGUI( root )

root.mainloop()