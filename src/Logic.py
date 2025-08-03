import os

from src.FileManager import FileManager


class Logic( FileManager ):
    def __init__( self ) -> None:
        super().__init__()
        
        self.data_path = os.path.join( self.BASE_PATH, "data" )
        self.forms_json_path = os.path.join( self.data_path, "forms.json" )
        self.FORMS_DICT_NAME = "forms"
        
    def select_form_manually( self, user_word_type: str = None, user_form: str = None ) -> dict:
        def get_by_form( form ):
            word_types = self.get_dict_from_json( self.forms_json_path, self.FORMS_DICT_NAME ).keys()
            for word_type in word_types:
                try:
                    loaded_forms = self.get_dict_from_json( self.forms_json_path, self.FORMS_DICT_NAME, word_type, form )
                except Exception:
                    break
            return loaded_forms
                                                   
        if user_word_type and user_form:                      
            loaded_forms = self.get_dict_from_json( self.forms_json_path, self.FORMS_DICT_NAME, user_word_type, user_form )
        elif user_word_type:
            loaded_forms = self.get_dict_from_json( self.forms_json_path, self.FORMS_DICT_NAME, user_word_type )
        elif user_form:
            get_by_form( user_form )
        else:
            loaded_forms = {}
        loaded_forms = self.shuffle_dict( loaded_forms )
        return loaded_forms
#class Logic