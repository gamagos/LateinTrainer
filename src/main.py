from __future__ import annotations

import os
import sys
import tkinter as tk
import traceback
from tkinter import messagebox

from logic.FileAndCacheHandler import FileAndCacheHandler
from logic.GUI import GUI

logs_path = os.path.join( getattr( sys, "_MEIPASS",
        os.path.dirname( os.path.abspath( __file__ ) ) ), "logs", "debug_log.txt"
    )
# TODO remove on compilation to dist
try:
    root = tk.Tk()
    root.geometry( "700x700" )
    app = GUI( root )
    leFileAndCacheHandler = FileAndCacheHandler( app )
    
    def report_callback_exception( exc, val, tb ):
        error_details = "".join( traceback.format_exception( exc, val, tb ) )
        error_msg = f"\n--------------------SEVERE ERROR--------------------\n"
        error_msg += f"Error Type: {exc.__name__}\n"
        error_msg += f"Error Message: {val}\n"
        error_msg += f"Traceback:\n{error_details}"
        try:
            print( error_msg )
            leFileAndCacheHandler.write_debug_log( None, error_msg, path = logs_path )
        except Exception as e:
            print( f"Logging failed: {str(e)}")
            messagebox.showerror( "unerwartet Fehler",
                f"Ursprünglicher Fehler: {val}\nLogging Fehler: {str(e)}"                     
            )
        messagebox.showerror( "Fehler", str( val ) )
    
    root.report_callback_exception = report_callback_exception
    root.mainloop()
    
except Exception as e:
    error_details = "".join( traceback.format_tb( e.__traceback__ ) )
    error_msg = f"\n--------------------SEVERE ERROR--------------------\n"
    error_msg += f"Error Type: {type(e).__name__}\n"
    error_msg += f"Error Message: {str(e)}\n"
    error_msg += f"Traceback:\n{error_details}"
    print( error_msg )
    try:
        leFileAndCacheHandler.write_debug_log( None, error_msg, path = logs_path )
    except Exception as log_error:
        print(f"Failed to write to log: {log_error}")
    messagebox.showerror( "Fehler", f"{e}" )

"""
root = tk.Tk()
root.geometry( "700x700" )
app = GUI( root )
app.debug_print( "\n\n!!!!!!!!@gamagos Please use the real main.py this is a workaround to make vsc throw the errors!!!!!!!!\n" )
root.mainloop()
"""
print( "Quitting..." )
sys.exit(0)