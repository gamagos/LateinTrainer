from __future__ import annotations

import os
import sys
import tkinter as tk
from tkinter import messagebox, ttk

from logic.FileAndCacheHandler import FileAndCacheHandler
from logic.GUI import GUI

# TODO remove on compilation to dist
try:
    root = tk.Tk()
    
    def report_callback_exception( exc, val, tb ):
        print( f"\n--------------------SEVERE ERROR--------------------\n{val}" )
        leFileAndCacheHandler.write_debug_log( None, f"\n--------------------SEVERE ERROR--------------------\n{val}",
                                            path = os.path.join( getattr( sys, "_MEIPASS", 
                                            os.path.dirname( os.path.abspath( __file__ ) ) ), "logs", "debug_log.txt" ) )
        messagebox.showerror( "Fehler", str( val ) )
        root.quit()
    
    root.report_callback_exception = report_callback_exception
    root.geometry( "700x700" )
    app = GUI( root )
    leFileAndCacheHandler = FileAndCacheHandler( app )
    root.mainloop()
except Exception as e:
    print( f"\n--------------------SEVERE ERROR--------------------\n{ e }" )
    leFileAndCacheHandler.write_debug_log( None, f"\n--------------------SEVERE ERROR--------------------\n{ e }",
                                        path = os.path.join( getattr( sys, "_MEIPASS", os.path.dirname( os.path.abspath( __file__ ) ) ), "logs", "debug_log.txt" ) )
    messagebox.showerror( "Fehler", f"{ e }" )
    root.quit()

"""
root = tk.Tk()
root.geometry( "700x700" )
app = GUI( root )
app.debug_print( "\n\n!!!!!!!!@gamagos Please use the real main.py this is a workaround to make vsc throw the errors!!!!!!!!\n" )
root.mainloop()
"""