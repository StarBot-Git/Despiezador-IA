import os
from pathlib import Path

from utils.paths import Normalize_Path, Ensure_OutputsRoot
from utils.scanner import Scan_InputFolder
from config import settings

class Furniture_Controller:
    def __init__(self, sidebar, main_window):
        self.sidebar = sidebar
        self.main_window = main_window

    def Change_Furniture(self):

        # ------ Cargar los archivos -------

        self.sidebar.clear_files()
        self.sidebar.furniture_name = self.main_window.furniture_name = furniture_name = self.sidebar.furniture_combo.currentText()

        if not furniture_name == "Seleccione un mueble...":
            print(f"{furniture_name}")

            furniture_path = settings.INPUT_DIR / furniture_name
            output_path = settings.OUTPUT_DIR / furniture_name

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
                    if file not in self.sidebar.get_uploaded_files():
                        self.sidebar.add_file(file)
                        #print(f"añadi:{file}")

            self.sidebar.uploaded_files = paths_str

            if not self.main_window.agent_IA == None:
                files_data = self.sidebar.model_combo_controller.Load_File_IDs(paths=self.sidebar.uploaded_files, furniture_name=self.sidebar.furniture_name)
                self.main_window.agent_IA.files = files_data

            # ------ Activar | Modelos StarGPT ------
            self.sidebar.model_combo.setEnabled(True)
            self.main_window.window_topbar.btn_folder.setEnabled(True)

        else:
            self.sidebar.uploaded_files = []
            self.sidebar.model_combo.setEnabled(False)
            self.main_window.window_topbar.btn_folder.setEnabled(False)
            
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