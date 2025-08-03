import sys

from PySide6.QtWidgets import QApplication

from src.Main_GUI import MainWindow

if __name__ == "__main__":
    app = QApplication( sys.argv )
    """app.setStyle("windows11")
    if "windows11" not in app.style().objectName():   #TODO make program look good on all operating systems
        app.setStyle("Fusion")
        app.setStyleSheet( "TODO" )"""
        
    main_window = MainWindow()
    main_window.debug_print("Starting Program")
    main_window.create_main_window()
    main_window.show()
    #main_window.select_form_manually("Nouns", "A-Deklination")#TODO only for debug remove when method works
    
    sys.exit( app.exec() )
#if __name__ == "__main__":