from typing import Callable

from PySide6.QtGui import QAction
from PySide6.QtWidgets import QMenu

from src.Utils import DictUtils


class PySide6Utils:
    def __init__( self, dict_utils_instance: DictUtils ) -> None:
        self.dict_utils_instance = dict_utils_instance
        print( f"[INIT] { self.__class__.__name__ }" )
    #def __init__
        

    def dict_to_QMenu( self, dictionary: dict, parent: QMenu = None, action_callback: Callable[[ str, str ], None ] = None, top_key: str = "All" ) -> QMenu:
        if not isinstance( dictionary, dict ):
            raise TypeError( f"Expected dict, got { type( dictionary ).__name__ }" )
        
        #TODO make multiple word_types checkboxable
        top_menu = QMenu( parent )
        i = 0
        for key, value in dictionary.items():
            cleaned_key = str( key ).replace( "_", " " ).title()
            
            action = QAction( parent = top_menu )
            if i == 0:
                action.setText( "All" )
                top_menu.addAction( action )
                if isinstance( action_callback, Callable ) and action_callback:
                    action.triggered.connect( lambda checked, top_key = top_key, key = "All": action_callback( key ))
            
            if self.dict_utils_instance.get_dict_minimum_depth( dictionary ) > 1:
                submenu = self.dict_to_QMenu( value, top_menu, action_callback, key )
                submenu.setTitle( cleaned_key )
                top_menu.addMenu( submenu )
            elif self.dict_utils_instance.get_dict_minimum_depth( dictionary ) <= 1:
                action = QAction( cleaned_key, top_menu )
                if isinstance( action_callback, Callable ) and action_callback:
                    action.triggered.connect( lambda checked, top_key = top_key, key = key: action_callback( top_key, key ))
                top_menu.addAction( action )
                
            i += 1
        #for key, value in dictionary.items()
                
        return top_menu
    #def dict_to_QMenu
#class Pyiside6Utils