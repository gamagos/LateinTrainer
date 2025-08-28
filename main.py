import sys

from PySide6.QtWidgets import QApplication

from src.MainWindow import MainWindow
from src.Utils.DebugUtils import DebugUtils


class Main:
    """Main class. Only holds the main function for now.
    """    
    @staticmethod
    def main():
        """Main program code."""
        Tag = DebugUtils.Tag
        
        app = QApplication( sys.argv )
        """app.setStyle("windows11")
        if "windows11" not in app.style().objectName():   #TODO make program look good on all operating systems
            app.setStyle("Fusion")
            app.setStyleSheet( "TODO" )"""
            
        main_window = MainWindow()
        DebugUtils.debug_print(Tag.INFO, "Starting Program")
        main_window.create_main_window()
        main_window.show()
        #main_window.select_form_manually("Nouns", "A-Deklination")#TODO only for debug remove when method works
        
        sys.exit( app.exec() )
        
        
if __name__ == "__main__":
    Main.main()
#if __name__ == "__main__":

#SAO season 1 best