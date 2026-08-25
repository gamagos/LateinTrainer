from contextlib import contextmanager
from pickletools import pyset

from PySide6.QtCore import QSize
from PySide6.QtGui import QIcon, QFont, Qt
from PySide6.QtWidgets import QGridLayout, QHBoxLayout, QLabel, QLineEdit, QMainWindow, QSizePolicy, QSpacerItem, QToolButton, QWidget

from Trainer.Constants import Paths, AssetFolders, LightModeAssets, DarkModeAssets
from Trainer.gui_pyuic.Main_Window_ui import Ui_Main_Windows
from Trainer.Logic import Logic
from Trainer.Utils.DebugUtils import DebugUtils
from Trainer.Utils.DictUtils import DictUtils
from Trainer.Utils.GeneralUtils import GeneralUtils
from Trainer.Utils.PySide6Utils import PySide6Utils

#TODO make spacer not go to translation
class MainWindow( QMainWindow, Logic ):
    def __init__( self ) -> None:
        DebugUtils.debug_print( DebugUtils.Tag.INIT, f"{self.__class__.__name__ }" )

        #init stuff
        super().__init__()
        self.ui_trainer_main_window = None
        dict_utils_instance: DictUtils = DictUtils()
        self.PySide6Utils: PySide6Utils = PySide6Utils( dict_utils_instance )

        #variable definitions for other methods
        self.form_labels: list[ QLabel ] = []
        self.form_line_edits: list[ QLineEdit ] = []

        #variables
        self.current_form_index: int = 0
        
        #TODO find a way to get system wide settings for darkmode
        
    """
    SYNOPSIS:
        Basically main method for starting the GUI
    """        
    def create_main_window( self ) -> None:
        if self.ui_trainer_main_window is None:
            self.ui_trainer_main_window = Ui_Main_Windows()
            self.ui_trainer_main_window.setupUi( self )
            
            #Window configuration
            self.setWindowTitle( "Shitty Latin Forms Trainer" )
            
            icon_path: str
            settings_button_path: str
            if self.darkmode_on:
                icon_path = DarkModeAssets.ICON.value
                settings_button_path = DarkModeAssets.SETTINGS_BUTTON.value
            else:
                icon_path = LightModeAssets.ICON.value
                settings_button_path = LightModeAssets.SETTINGS_BUTTON.value
                
            self.trainer_main_window_icon = QIcon( icon_path )
            self.setWindowIcon( self.trainer_main_window_icon )
            
            #buttons
            trainer_settings_button_icon = QIcon( settings_button_path )
            self.ui_trainer_main_window.Settings_Button.setIcon( trainer_settings_button_icon )
            self.ui_trainer_main_window.Settings_Button.setIconSize( QSize( 50, 50 ))
            
            self.ui_trainer_main_window.Form_Select.setPopupMode( QToolButton.ToolButtonPopupMode.InstantPopup )
            forms_dict = self.get_dict_from_json( Paths.FORMS_JSON_PATH.value, "forms" )
            self.Form_Select_Menu = self.PySide6Utils.dict_to_QMenu( forms_dict )
            self.ui_trainer_main_window.Form_Select.setMenu( self.Form_Select_Menu )
            
            #TODO add tests
            self.scroll_area_widget_layout = QGridLayout( parent = self.ui_trainer_main_window.Scroll_Area_Widget_Contents )
            self.ui_trainer_main_window.Scroll_Area_Widget_Contents.setLayout( self.scroll_area_widget_layout )
            self.generate_forms_table_in_gridlayout( forms_dict[ "Nouns" ][ "A-Declension" ], "A-Declension", self.scroll_area_widget_layout )
        
    """
    SYNOPSIS:
        Method for generating the table containing the forms and text entry fields
        with labels and entries in the gridLayout inside the ScrollArea.
    Args:
        forms (dict): the dict with all forms to be loaded. Depth = 1 max!
        title (str): Name of the category of the forms displayed
        layout (QGridLayout): The gridlayout in which the table is to be generated
        font_family (str, optional): Defaults to "Bahnschrift".
        font_size (int, optional): Defaults to 17.
        font_weight (QFont.Weight, optional): Defaults to QFont.Weight.Normal.
        min_width (int, optional): Minimum width of the individual labels. Defaults to 215.
        min_height (int, optional): Minimum height of the individual labels. Defaults to 32.
    """
    #TODO add more dynamic resizing methods
    def generate_forms_table_in_gridlayout(
        self,
        forms: dict,
        title: str,
        layout: QGridLayout,
        font_family: str = "Bahnschrift",
        font_size: int = 17,
        font_weight: QFont.Weight = QFont.Weight.Normal,
        min_width: int = 215,
        min_height: int = 32,
    ) -> None:
        self.ui_trainer_main_window.Form_Title.setText( title ) # type: ignore
        self.hspacer1 = QSpacerItem( 20, 0 )
        self.hspacer2 = QSpacerItem( 93, 0 )
        self.vspacer1 = QSpacerItem( 0, 10 )
        layout.addItem( self.hspacer1, 0, 0 )
        layout.addItem( self.hspacer2, 0, 3 )
        layout.addItem( self.vspacer1, 0, 1, columnSpan = 2 )

        self.forms_labels: list[ GeneralUtils.GamagosQLabel ] = []
        arguments_set_label_attributes: GeneralUtils.GamagosQLabel.ArgumentsFor_set_label_attributes = GeneralUtils.GamagosQLabel.ArgumentsFor_set_label_attributes(
            minimum_width = min_width,
            minimum_height = min_height,
            font_family = font_family,
            font_size = font_size,
            font_weight = font_weight
        )
        # +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-
        #
        # Loops through all the forms of the current Conjugation/Declination/...
        # and creates the corresponding labels, text entry fields... for them
        #
        # +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-
        i_extra = 0
        key: str = "" #TODO write comments and docstrings
        for i, key in enumerate( forms.keys() ):
            formatted_key = key.replace( "_", " " )
            self.forms_labels.append( GeneralUtils.GamagosQLabel( f"{ formatted_key }" ))
            self.forms_labels[i].set_label_attributes( arguments_set_label_attributes )         #TODO make spacer labels to QSpacerItem
            # ======================================================================================================
            # Add a spacer between the plural and singular cases, if applicable
            # ======================================================================================================
            if key == "Nominative_Plural":
                spacer_label = GeneralUtils.GamagosQLabel("")
                spacer_label.set_label_attributes( arguments_set_label_attributes )

                layout.addWidget( spacer_label, i + i_extra, 1 )
                i_extra += 1
            # ======================================================================================================
            # Change the style and position for the widget containing the translation 
            # ======================================================================================================
            elif key == "Translation":
                #translation label
                font = QFont( font_family, font_size, QFont.Weight.Thin )
                translation_label = QLabel( self.forms_labels[i].text() )
                translation_label.setFont( font )
                translation_label.setText( f"{ self.forms_labels[i].text() }: { forms[ key ] } " )
            
            # ======================================================================================================
            # Add the labels for the forms and their corresponding text entry fields
            # ======================================================================================================
            if key != "Translation":
                layout.addWidget( self.forms_labels[i], i + i_extra, 1, Qt.AlignmentFlag.AlignRight )
                #LineEdit
                self.form_line_edits.append( QLineEdit() )
                current_line_edit = self.form_line_edits[i - 1]
                current_line_edit.setSizePolicy( QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Preferred )
                current_line_edit.setMinimumWidth( min_width )
                current_line_edit.setMaximumWidth( 300 ) #TODO improve resizing logic a ton and add tests
                layout.addWidget( current_line_edit, i + i_extra, 2 )
                
            # ======================================================================================================
            # Add widget for the translation 
            # ======================================================================================================
            if i == len( forms.keys() ) - 1:
                i_extra += 1
                translation_widget = QWidget()
                translation_hbox_layout = QHBoxLayout( translation_widget )
                layout.addWidget( translation_widget, i + i_extra, 1, 1, 2, Qt.AlignmentFlag.AlignCenter )
                translation_widget.setLayout( translation_hbox_layout )
                translation_hbox_layout.addWidget( translation_label, alignment = Qt.AlignmentFlag.AlignCenter )

    def on_resize( self ) -> None:
        print( "not yet finished" ) #TODO <-- that before the comment
#class MainWindow

# I should use less AI but it's so confusing because it can be useful but I know it's mostly bad
# and it probably make me less efficient even