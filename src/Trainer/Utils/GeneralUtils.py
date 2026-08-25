# Default modules
import PySide6.QtCore
import PySide6.QtGui
import PySide6.QtWidgets
import typing
from dataclasses import dataclass

# Pip modules
from PySide6.QtGui import QFont, Qt
from PySide6.QtWidgets import QLabel, QSizePolicy

# Project Modules
from Trainer.Utils.DebugUtils import DebugUtils

class GeneralUtils:    
    def __init__( self ) -> None:
        DebugUtils.debug_print( DebugUtils.Tag.INIT, f"{ self.__class__.__name__ }" )
        self.darkmode_on = True
        
    """
    SYNOPSIS:
        This is a dummy method it is meant to be an empty placeholder for event bound methods
    """
    def dummy( *args ) -> None:
        return
    
    """
    SYNOPSIS:
        This is a dummy class, meant for use as a placeholder
    """
    class Dummy:
        pass
    
    class GamagosQLabel(QLabel):            
        """
        SYNOPSIS:
            Sets a bunch of values for a label at once
            so the later code is more readable.
        ARGUMENTS:
            argumentsAsClass (GeneralUtils.ArgumentsFor_set_label_attributes): An instance of the GeneralUtils.ArgumentsFor_set_label_attributes
                that has these members. See the class' docstring for more:
                
                minimum_width (int, optional): The minimum width of the label. Defaults to min_width.
                minimum_height (int, optional): The minimum height of the label. Defaults to min_height.
                maximum_width (int, optional): The maximum width of the label. Defaults to 0. 0 means no maximum width
                maximum_height (int, optional): The maximum height of the label. Defaults to 0. 0 means no maximum height
                alignementflag_1 (Qt.AlignmentFlag, optional): Horizontal alignment flag. Defaults to Qt.AlignmentFlag.AlignLeft.
                alignmentflag_2 (Qt.AlignmentFlag, optional): Vertical alignment flag. Defaults to Qt.AlignmentFlag.AlignVCenter. #TODO complete this documentation
                font_family: Font family to use for text in label. Defaults to Bahnschrift 
                font_size: Font size to use for text in label. Defaults to 17
                font_weight: Font weight to use for text in label. Defaults to QFont.Weight.Normal
        RETURNS:
            The modified Label
        """              
        def set_label_attributes(
            self,
            argumentsAsClass
        ):
            form_label_font = QFont( argumentsAsClass.font_family, argumentsAsClass.font_size, argumentsAsClass.font_weight )
            self.setAlignment( argumentsAsClass.alignmentflag_1 )
            self.setAlignment( argumentsAsClass.alignmentflag_2 )
            self.setFont( form_label_font )
            self.setMinimumSize( argumentsAsClass.minimum_width, argumentsAsClass.minimum_height )
            self.setSizePolicy( QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.MinimumExpanding )
            if argumentsAsClass.maximum_width:
                self.setMaximumWidth( argumentsAsClass.maximum_width )
            if argumentsAsClass.maximum_height:
                self.setMaximumHeight( argumentsAsClass.maximum_height )
            return self
        
        """
        SYNOPSIS:
            Dataclass for holding the parameters of the above method named
            "set_label_attributes" to make reuse of similar parameters easy
            and avoiding clutter in method calls. 
            Since the method has a lot of parameters.
        MEMBERS:
            minimum_width (int, optional): The minimum width of the label. Defaults to min_width.
            minimum_height (int, optional): The minimum height of the label. Defaults to min_height.
            maximum_width (int, optional): The maximum width of the label. Defaults to 0. 0 means no maximum width
            maximum_height (int, optional): The maximum height of the label. Defaults to 0. 0 means no maximum height
            alignementflag_1 (Qt.AlignmentFlag, optional): Horizontal alignment flag. Defaults to Qt.AlignmentFlag.AlignLeft.
            alignmentflag_2 (Qt.AlignmentFlag, optional): Vertical alignment flag. Defaults to Qt.AlignmentFlag.AlignVCenter.
            font_family: Font family to use for text in label. Defaults to Bahnschrift 
            font_size: Font size to use for text in label. Defaults to 17
            font_weight: Font weight to use for text in label. Defaults to QFont.Weight.Normal
        """
        @dataclass
        class ArgumentsFor_set_label_attributes:
            minimum_width: int = 0
            minimum_height: int = 0
            maximum_width: int = 0
            maximum_height: int = 0
            alignmentflag_1: Qt.AlignmentFlag = Qt.AlignmentFlag.AlignLeft
            alignmentflag_2: Qt.AlignmentFlag = Qt.AlignmentFlag.AlignVCenter
            font_family: str = "Bahnschrift"
            font_size: int = 17
            font_weight: QFont.Weight = QFont.Weight.Normal
                