import tkinter as tk
import time

from logic.GUI import GUI

root = tk.Tk()
root.geometry( "700x700" )
app = GUI( root )
root.after( 1, app.handle_resize() )

root.mainloop()