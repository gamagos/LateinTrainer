import tkinter as tk

from logic.GUI import GUI

root = tk.Tk()
root.geometry( "700x700" )
app = GUI( root )

root.mainloop()