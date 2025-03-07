import tkinter as tk

from src.logic.GUI import GUI

root = tk.Tk()
root.geometry( "700x700" )
app = GUI( root )
root.geometry(f"{ app.root_width }x{ app.root_height }")

root.mainloop()