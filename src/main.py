import os
import sys
import tkinter as tk
from tkinter import messagebox, ttk

from logic.fileAndCacheHandler import fileAndCacheHandler
from logic.GUI import GUI

"""
# TODO remove on compilation to dist
try:
    root = tk.Tk()
    root.geometry( "700x700" )
    app = GUI( root )
    FileAndCacheHandler = fileAndCacheHandler( app )
    root.mainloop()
except Exception as e:
    print( f"\n--------------------SEVERE ERROR--------------------\n{ e }" )
    fileAndCacheHandler.write_debug_log( None, f"\n--------------------SEVERE ERROR--------------------\n{ e }",
                                        path = os.path.join( getattr( sys, "_MEIPASS", os.path.dirname( os.path.abspath( __file__ ) ) ), "logs", "debug_log.txt" ) )
    messagebox.showerror( "Fehler: ", f"{ e }" )
"""

root = tk.Tk()
root.geometry( "700x700" )
app = GUI( root )
FileAndCacheHandler = fileAndCacheHandler( app )
app.debug_print( "!!!@gamagos Please use the real main.py this is a workaround to make vsc throw the errors" )
root.mainloop()