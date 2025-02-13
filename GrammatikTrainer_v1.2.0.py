import LatinTrainerGUI

import tkinter as tk
        
root = tk.Tk()
root.resizable( False, False )
root.geometry("700x800")

app = LatinTrainerGUI.LatinTrainerGUI( root )

root.mainloop()