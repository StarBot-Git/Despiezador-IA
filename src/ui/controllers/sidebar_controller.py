import os
import json
from pathlib import Path
from PySide6.QtWidgets import QFileDialog

from utils.paths import Normalize_Path, Ensure_OutputsRoot
from utils.scanner import Scan_InputFolder
from core import config
from agents.analista.analista_piezas import Analista_Piezas
from core.file_manager import OpenAIFileManager
from ui.components.fileitem_widget import FileItemWidget
#from core.ai_client import load_file, upload_file


class SideBarController:
    def __init__(self, sidebar, main_window, ai_client):
        self.sidebar = sidebar
        self.main_window = main_window
        self.ai_client = ai_client
        self.openAI_fileManager = OpenAIFileManager(self.ai_client.client)

    # ------ Control | Muebles ------

    """
        Load_FurnitureFolders():
        Busca y lista las carpetas iniciales disponibles
    """
    def Load_FurnitureFolders(self, input_path="Input"):
        self.sidebar.furniture_combo.clear()
        self.sidebar.furniture_combo.addItem("Seleccione un mueble...")

        if not os.path.exists(input_path):
            print(f"LA RUTA NO EXISTE")
            return
        
        for folder in os.listdir(input_path):
            full_path = os.path.join(input_path, folder)

            if os.path.isdir(full_path):
                self.sidebar.furniture_combo.addItem(folder)
    
    """
        Change_Furniture():
    """
    def Change_Furniture(self):
        # ------ Cargar los archivos -------
        self.Clear_Files()
        self.sidebar.furniture_name = self.main_window.furniture_name = furniture_name = self.sidebar.furniture_combo.currentText()

        if not furniture_name == "Seleccione un mueble...":
            print(f"{furniture_name}")

            furniture_path = config.INPUT_DIR / furniture_name
            output_path = config.OUTPUT_DIR / furniture_name

            if os.path.isdir(furniture_path):
                self.sidebar.input_dir = self.main_window.input_dir = Normalize_Path(furniture_path)           # utils.paths | Normaliza ruta
                self.sidebar.output_dir = self.main_window.output_dir = Ensure_OutputsRoot(output_path)         # utils.paths | Asegura existencia de la ruta
            else:
                return

            paths = Scan_InputFolder(furniture_path)

            print(paths)

            paths_str = [str(p) for p in paths]

            if paths_str:
                for file in paths_str:
                    if file not in self.Get_Uploaded_Files():
                        self.Add_File(file)
                        #print(f"añadi:{file}")

            self.sidebar.uploaded_files = paths_str

            if not self.main_window.agent_IA == None:
                files_data = self.Load_File_IDs(paths=self.sidebar.uploaded_files, furniture_name=self.sidebar.furniture_name)
                self.main_window.agent_IA.files = files_data

            # ------ Activar | Modelos StarGPT ------
            self.sidebar.model_combo.setEnabled(True)
            self.main_window.window_topbar.btn_folder.setEnabled(True)

        else:
            self.sidebar.uploaded_files = []
            self.sidebar.model_combo.setEnabled(False)
            self.main_window.window_topbar.btn_folder.setEnabled(False)
    
    """
        clear_files():
    """
    def Clear_Files(self):
        """Limpia todos los archivos de la lista"""
        self.sidebar.uploaded_files.clear()

        while self.sidebar.files_layout.count():
            item = self.sidebar.files_layout.takeAt(0)

            if item.widget():
                item.widget().deleteLater()

    """

    """    
    def Get_Uploaded_Files(self):
        """Retorna la lista de archivos subidos"""
        return self.sidebar.uploaded_files.copy()

    """

    """
    def Add_File(self, filepath: str):
        """Añade un archivo a la lista"""
        self.sidebar.uploaded_files.append(filepath)
        
        # Crear widget del archivo
        file_widget = FileItemWidget(filepath)
        file_widget.remove_clicked.connect(self.Remove_File)
        
        self.sidebar.files_layout.addWidget(file_widget)
    
    """

    """
    def Remove_File(self, filepath: str):
        """Elimina un archivo de la lista"""
        if filepath in self.sidebar.uploaded_files:
            self.sidebar.uploaded_files.remove(filepath)
        
        # Buscar y eliminar el widget
        for i in range(self.sidebar.files_layout.count()):
            widget = self.sidebar.files_layout.itemAt(i).widget()
            if isinstance(widget, FileItemWidget) and widget.filepath == filepath:
                widget.deleteLater()
                break
        

    # ------ Control | Modelo StarGPT ------
    
    """
        Change_SG_Model():
    """
    def Change_SG_Model(self):
        selected_model = self.sidebar.model_combo.get_value()
        print(f"es: {selected_model}")

        if not selected_model == "STAR GPT":
            self.sidebar.model_title.setText(selected_model)

            #print(self.sidebar.uploaded_files)
            files_data = self.Load_File_IDs(paths=self.sidebar.uploaded_files, furniture_name=self.sidebar.furniture_name)

            print(files_data)

            if selected_model == "Analista de Piezas":
                self.main_window.agent_IA = Analista_Piezas(self.ai_client)
                self.main_window.agent_IA.Add_Files(files_data)
                self.main_window.input_field.setText(self.main_window.agent_IA.SG_USER_PROMPT)

            self.main_window.chat_topbar.model_openAI_combo.setEnabled(True)
        
        else:
            self.main_window.agent_IA = None
            self.main_window.chat_topbar.model_openAI_combo.setEnabled(False)

    """
        Load_File_IDs():
    """
    def Load_File_IDs(self, paths=None, furniture_name=""):
        file_data = {}

        for p in paths:
            local_filename = f"{furniture_name}-{os.path.splitext(os.path.basename(p))[0]}"
            
            file_id = self.openAI_fileManager.Load_File(local_filename)
            
            if file_id == None:
                file_id = self.openAI_fileManager.Upload_File(local_FileName=local_filename, path=p)
            
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
    
    # ------ Control | Subir Archivos ------

    """
    
    """
    def OpenFile_Dialog(self):
        files, _ = QFileDialog.getOpenFileNames(
            self.sidebar,
            "Seleccionar archivos",
            "",
            "Archivos permitidos (*.pdf *.png *.jpg *.jpeg);;Todos los archivos (*)"
        )
        
        if files:
            for file in files:
                if file not in self.Get_Uploaded_Files():
                    self.Add_File(file)
                    print(f"añadi:{file}")