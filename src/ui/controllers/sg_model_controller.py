import os

from agents.sg_analista_piezas import Analista_Piezas
from agents.ai_client import load_file, upload_file

class StarGPTModelController:
    def __init__(self, sidebar, main_window):
        self.sidebar = sidebar
        self.main_window = main_window

    def Change_Model(self):
        selected_model = self.sidebar.model_combo.get_value()
        print(f"es: {selected_model}")

        if not selected_model == "STAR GPT":
            self.sidebar.model_title.setText(selected_model)

            #print(self.sidebar.uploaded_files)
            files_data = self.Load_File_IDs(paths=self.sidebar.uploaded_files, furniture_name=self.sidebar.furniture_name)

            if selected_model == "Analista de Piezas":
                self.main_window.agent_IA = Analista_Piezas(files_data)
                self.main_window.input_field.setText(self.main_window.agent_IA.SG_USER_PROMPT)

    def Load_File_IDs(self, paths=None, furniture_name=""):
        file_data = {}

        for p in paths:
            local_filename = f"{furniture_name}-{os.path.splitext(os.path.basename(p))[0]}"
            
            file_id = load_file(local_filename)
            
            if file_id == None:
                file_id = upload_file(local_FileName=local_filename, path=p)
            
            # Obtener la extensión y clasificarla
            extension = os.path.splitext(p)[1].lower()  # .jpg, .png, .pdf, etc.
            
            if extension == '.pdf':
                file_type = 'pdf'
            elif extension in ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp']:
                file_type = 'img'
            else:
                file_type = 'other'  # Por si acaso hay otros tipos
            
            file_data[file_id] = file_type

        #print(file_data)
        
        return file_data