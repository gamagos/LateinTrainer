from typing import Callable

from PySide6.QtGui import QAction
from PySide6.QtWidgets import QMenu

from src.Utils import Utils

class PySide6Utils( Utils ):
    def __init__( self ) -> None:
        super().__init__()
    #def __init__
        

    def dict_to_QMenu( self, dictionary: dict, parent: QMenu = None, action_callback: Callable = None ) -> QMenu:
        if not isinstance( dictionary, dict ):
            raise TypeError( f"Expected dict, got { type( dictionary ).__name__ }" )
        
        top_menu = QMenu( parent )
        for key, value in dictionary.items():
            if self.get_dict_minimum_depth( dictionary ) > 1:    
                submenu = self.dict_to_QMenu( value, top_menu )
                submenu.setTitle( str( key ).replace( "_", " " ).title() )
                top_menu.addMenu( submenu )
            elif self.get_dict_minimum_depth( dictionary ) <= 1:
                action = QAction( str( key ).replace( "_", " " ).title(), top_menu )
                if isinstance( action_callback, Callable ) and action_callback:
                    action.triggered.connect( lambda checked, key = key: action_callback( key ))
                top_menu.addAction( action )
                
        return top_menu
    #def dict_to_QMenu
#class Pyiside6Utils