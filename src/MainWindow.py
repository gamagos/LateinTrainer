from contextlib import contextmanager

from PySide6.QtCore import QSize
from PySide6.QtGui import QIcon, QFont, Qt
from PySide6.QtWidgets import QGridLayout, QHBoxLayout, QLabel, QLineEdit, QMainWindow, QSizePolicy, QSpacerItem, QToolButton, QWidget

from src.Utils import DictUtils
from src.gui_pyuic.Main_Window_ui import Ui_Main_Windows
from src.Assets import Assets
from src.Logic import Logic
from src.Utils.PySide6Utils import PySide6Utils


class MainWindow( QMainWindow, Logic ):
    def __init__( self ) -> None:
        print( f"[INIT] { self.__class__.__name__ }" )
        super().__init__()
        self.ui_trainer_main_window = None
        self.Assets = Assets( self.BASE_PATH, self.darkmode_on )
        dict_utils_instance = DictUtils()
        self.PySide6Utils = PySide6Utils( dict_utils_instance )

        self.form_labels: list[ QLabel ] = []
        self.form_line_edits: list[ QLineEdit ] = []

        #variables
        self.current_form_index = 0
        
        #TODO find a way to get system wide settings
    #def __init__

        
    def create_main_window( self ) -> None:
        if self.ui_trainer_main_window is None:
            self.ui_trainer_main_window = Ui_Main_Windows()
            self.ui_trainer_main_window.setupUi( self )
            
            #Window configuration
            self.setWindowTitle( "Shitty Latin Forms Trainer" )
            self.trainer_main_window_icon = QIcon( self.Assets.icon_path )
            self.setWindowIcon( self.trainer_main_window_icon )
            
            #buttons
            trainer_settings_button_icon = QIcon( self.Assets.settings_button_png_path )
            self.ui_trainer_main_window.Settings_Button.setIcon( trainer_settings_button_icon )
            self.ui_trainer_main_window.Settings_Button.setIconSize( QSize( 50, 50 ))
            
            self.ui_trainer_main_window.Form_Select.setPopupMode( QToolButton.ToolButtonPopupMode.InstantPopup )
            forms_dict = self.get_dict_from_json( self.forms_json_path, "forms" )
            self.Form_Select_Menu = self.PySide6Utils.dict_to_QMenu( forms_dict )
            self.ui_trainer_main_window.Form_Select.setMenu( self.Form_Select_Menu )
            
            #TODO add tests
            self.scroll_area_widget_layout = QGridLayout( parent = self.ui_trainer_main_window.Scroll_Area_Widget_Contents )
            self.ui_trainer_main_window.Scroll_Area_Widget_Contents.setLayout( self.scroll_area_widget_layout )
            self.generate_forms_table_in_gridlayout( forms_dict[ "Nouns" ][ "A-Declension" ], "A-Declension", self.scroll_area_widget_layout )
    #def creat_main_window    
        
    #TODO add more dynamic resizing methods
    def generate_forms_table_in_gridlayout(
        self,
        forms: dict,
        title: str,
        layout: QGridLayout,
        font_family: str = "Bahnschrift",
        font_size: int = 17,
        font_wheight: QFont.Weight = QFont.Weight.Normal,
        min_width: int = 215,
        min_height: int = 32,
    ) -> None:
        
        @contextmanager # * Make this more scalable if set_label_attributes is used more than once
        def monkey_patch_set_label_attributes():
            def set_label_attributes(
                self: QLabel,
                minimum_width: int = min_width,
                minimum_height: int = min_height,
                maximum_width: int = None,
                maximum_height: int = None,
                alignementflag_1: Qt.AlignmentFlag = Qt.AlignmentFlag.AlignLeft,
                alignmentflag_2: Qt.AlignmentFlag = Qt.AlignmentFlag.AlignVCenter
            ) -> QLabel:
                form_label_font = QFont( font_family, font_size, font_wheight )
                self.setAlignment( alignementflag_1 )
                self.setAlignment( alignmentflag_2 )
                self.setFont( form_label_font )
                self.setMinimumSize( minimum_width, minimum_height )
                self.setSizePolicy( QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.MinimumExpanding )
                if maximum_width:
                    self.setMaximumWidth( maximum_width )
                if maximum_height:
                    self.setMaximumHeight( maximum_height )
                return self
            #def set_label_attributes
            QLabel.set_label_attributes = set_label_attributes
            try:
                yield
            finally:
                if hasattr( QLabel, "set_label_attributes" ):
                    delattr( QLabel, "set_label_attributes" )
        #def monkey_patch_set_label_attributes

        self.ui_trainer_main_window.Form_Title.setText( title )
        
        self.hspacer1 = QSpacerItem( 20, 0 )
        self.hspacer2 = QSpacerItem( 93, 0 )
        self.vspacer1 = QSpacerItem( 0, 10 )
        layout.addItem( self.hspacer1, 0, 0 )
        layout.addItem( self.hspacer2, 0, 3 )
        layout.addItem( self.vspacer1, 0, 1, columnSpan = 2 )

        self.forms_labels: list[ QLabel ] = []
        i_extra = 0
        key: str #TODO write comments and docstrings
        for i, key in enumerate( forms.keys() ):
            formatted_key = key.replace( "_", " " )
            
            with monkey_patch_set_label_attributes():
                self.forms_labels.append( QLabel( f"{ formatted_key }" ))
                self.forms_labels[i].set_label_attributes()
            #TODO make spacer labels to QSpacerItem
            
            if key == "Nominative_Plural":
                with monkey_patch_set_label_attributes():
                    spacer_label = QLabel("")
                    spacer_label.set_label_attributes( minimum_height = 10, maximum_height = 15 )

                layout.addWidget( spacer_label, i + i_extra, 1 )
                i_extra += 1
            elif key == "Translation":
                #translation label
                font = QFont( font_family, font_size, QFont.Weight.Thin )
                translation_label = QLabel( self.forms_labels[i].text() )
                translation_label.setFont( font )
                translation_label.setText( f"{ self.forms_labels[i].text() }: { forms[ key ] } " )
            
            if key != "Translation":
                layout.addWidget( self.forms_labels[i], i + i_extra, 1, Qt.AlignmentFlag.AlignRight )
                #LineEdit
                self.form_line_edits.append( QLineEdit() )
                current_line_edit = self.form_line_edits[i - 1]
                current_line_edit.setSizePolicy( QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Preferred )
                current_line_edit.setMinimumWidth( min_width )
                current_line_edit.setMaximumWidth( 300 ) #TODO improve resizing logic a ton and add tests
                layout.addWidget( current_line_edit, i + i_extra, 2 )
                
            if i == len( forms.keys() ) - 1:
                i_extra += 1
                translation_widget = QWidget()
                translation_hbox_layout = QHBoxLayout( translation_widget )
                layout.addWidget( translation_widget, i + i_extra, 1, 1, 2, Qt.AlignmentFlag.AlignCenter )
                translation_widget.setLayout( translation_hbox_layout )
                translation_hbox_layout.addWidget( translation_label, alignment = Qt.AlignmentFlag.AlignCenter )
        #for i, key in enumerate( forms.keys() )


    def on_resize( self ) -> None:
        print( "not yet finished" )#TODO
#class MainWindow

# I should use less AI but it's so confusing because it can be useful but I know it's mostly bad
# and it probably make me less efficient even