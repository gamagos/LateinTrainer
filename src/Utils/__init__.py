from .DebugUtils import DebugUtils
from .DictUtils import DictUtils
from .FileUtils import FileUtils
from .GeneralUtils import GeneralUtils
from .PySide6Utils import PySide6Utils 
#TODO find good way to improve debug printing without having to create so many instance everywhere

DebugUtils.debug_print(DebugUtils.Tag.IMPORT, f"Importing {__name__}")

# Sword Art Online is the best Anime ever