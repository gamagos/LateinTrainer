from __future__ import annotations

from enum import Enum
import inspect
import os

from datetime import datetime
from typing import Union
from typing_extensions import TypeForm

from src.Constants import ANSICodes, Paths

class DebugUtils:
    """
    A class with many utilities and constants used for debugging
    """    
    current_logs_file = None    
    
    class Tag(Enum):
        """
        Basically an Enum only that I wanted the actual values
        displayed so I spared myself the hassle
        of having to write .value everywhere by making it to regular constants.
        """
        DEBUG = f"{ANSICodes.generate_ANSI_24bit_color(194, 194, 0)}[DEBUG]{ANSICodes.RESET}"
        ERROR = f"{ANSICodes.generate_ANSI_24bit_color(255, 50, 50)}[ERROR]{ANSICodes.RESET}"
        INFO = f"{ANSICodes.generate_ANSI_24bit_color(150, 189, 255)}[INFO]{ANSICodes.RESET}"
        INIT = f"{ANSICodes.generate_ANSI_24bit_color(0, 203, 255)}[INIT]{ANSICodes.RESET}"
        IMPORT = f"{ANSICodes.generate_ANSI_24bit_color(200, 50, 255)}[IMPORT]{ANSICodes.RESET}"
        WARNING = f"{ANSICodes.generate_ANSI_24bit_color(255, 120, 10)}[WARNING]{ANSICodes.RESET}" #! Note to self, make sure these colors look good on both bright and dark terminal themes(aim for luminance of ~50%), if that is possible without making the color look ugly
    #class Tag
        
        
    def __init__( self ) -> None:
        print( f"{ DebugUtils.Tag.INIT } { self.__class__.__name__ }" )
        self.debug: bool = True        
        
        
    @staticmethod
    def create_log_file( logs_folder: str = None ) -> str:
        """A method for creating a logs file with checking if
        creation was a success

        Args:
            logs_folder (str, optional): The folder that the log files are to be placed in

        Returns:
            str: The path to the logs file
        """        
        if not DebugUtils.current_logs_file:        
            log_time = str(datetime.now()).replace(' ', '_').replace('-', '_').replace(':', '_').replace('.', '_')
            if logs_folder:
                log_path = os.path.join( logs_folder, f"log{log_time}.log" )
            else:
                logs_folder = os.path.join( Paths.BASE_PATH.value, "logs" )  #TODO add autodeletion logic by time
                log_path = os.path.join( logs_folder, f"log{log_time}.log" )

            if not os.path.exists(logs_folder):
                try:
                    os.mkdir(logs_folder)
                except Exception as error:
                    DebugUtils.debug_print(DebugUtils.Tag.ERROR, "Unable to create logs folder")
                    raise OSError("Unable to create logs folder", error)

            if not os.path.exists(log_path):
                with open( log_path, "w" ) as file:
                    file.write("")
                    
            if not os.path.exists(log_path):
                DebugUtils.debug_print(DebugUtils.Tag.ERROR, "Unable to create log file")
                raise FileNotFoundError("Unable to create log file")
            else:
                DebugUtils.current_logs_file = log_path
                return log_path
        else:
            return DebugUtils.current_logs_file

    
    @staticmethod
    def write_log( *to_write: Union[ tuple , list ], logs_folder: str = None ) -> bool:
        """
        Writes to_write to log file

        Args:
            to_write: A list, tuple or single element to write to the log file

        Returns:
            bool: Wether the operation was successful
        """
        log_path = DebugUtils.create_log_file(logs_folder)
        
        def write_one() -> bool:
            """Writes a single element to log

            Returns:
                bool: Wether the operation was a success
            """            
            try:
                with open( log_path, "a" ) as File:
                    File.write( f"{to_write}\n" )
                return True
            except Exception as error:
                DebugUtils.debug_print( DebugUtils.Tag.ERROR, error, write_log = False )
                return False
            
        def write_many() -> bool:
            """The method to write to log when we have multiple element in to_write

            Returns:
                bool: If the operation was a success
            """            
            try:
                with open( log_path, "a" ) as File:
                    lines = []
                    for line in to_write:
                        lines.append( f"{ line }\n" )
                    File.writelines( lines )
                return True
            except Exception as error:
                DebugUtils.debug_print( DebugUtils.Tag.ERROR, error, write_logs = False )
                return False  
        
        if isinstance( to_write, str ):
            write_one()
        elif isinstance( to_write, list ) or isinstance( to_write, tuple ):
            write_many()
        else:
            return False
    #def write_log    
        
        
    @staticmethod
    def debug_print(
        tag: Tag = Tag.INFO,
        *to_print: Union[ tuple, list, str ],
        write_logs: bool = True,
        print_timestamps: bool = False,
    ) -> None:
        """
        Print debug messages with caller information
        tags and logging.
        
        Args:
            message: The message(s) to print
            tag: What kind of print it is (Tag)
            write_log: Whether to write this to the log file or not
        """        
        if not to_print:
            return
        
        if not isinstance( tag, DebugUtils.Tag ):
            raise TypeError("debug_print(): tag must be of type Utils.DebugUtils.Tag")    

        caller_frame = inspect.currentframe().f_back
        caller_info = ""
        if caller_frame:    #TODO improve caller info
            function_name = caller_frame.f_code.co_name
            frame_locals = caller_frame.f_locals
            if "self" in frame_locals:
                class_name = frame_locals["self"].__class__.__name__
                caller_info = f"{ class_name }.{ function_name }()"
            else:
                caller_info = f"{ function_name }()"
                #TODO split this up in more methods
        time = str( datetime.now() ) + ": "
        formatted_toPrints = []
        for arg in to_print:
            if isinstance( arg, str ):
                arg = f"{tag.value} {caller_info}: {arg}"
                formatted_toPrints.append( arg )
            else:
                try:
                    formatted_toPrints.append(f"{tag.value} {caller_info}: {str(arg)}")
                except Exception:
                    pass#TODO
        output = " ".join( formatted_toPrints )
        if print_timestamps:
            print(f"{time}{output}")
        else:
            print( output )
            
        if write_logs:
            DebugUtils.write_log(f"{time}{output}")
#class DebugUtils

#It would have been so helpful if I'd found a font like Fira Code or JetBrains Mono sooner man