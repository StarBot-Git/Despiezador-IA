import os
import shutil
from pathlib import Path
from PySide6.QtWidgets import QFileDialog
from PySide6.QtCore import Qt

from utils.paths import Normalize_Path, Ensure_OutputsRoot
from utils.scanner import Scan_InputFolder
from core import config, models_openAI_config
from agents.analista.analista_piezas import Analista_Piezas
from agents.parametrizador.parametrizador_modulos import ParametrizadorModulos
from core.file_manager import OpenAIFileManager
from ui.components.fileitem_widget import FileItemWidget


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
            print(f"[Mueble] Se selecciono: {furniture_name}")

            furniture_path = config.INPUT_DIR / furniture_name
            output_path = config.OUTPUT_DIR / furniture_name

            if os.path.isdir(furniture_path):
                self.sidebar.input_dir = self.main_window.input_dir = Normalize_Path(furniture_path)           # utils.paths | Normaliza ruta
                self.sidebar.output_dir = self.main_window.output_dir = Ensure_OutputsRoot(output_path)         # utils.paths | Asegura existencia de la ruta
            else:
                return

            paths = Scan_InputFolder(furniture_path)

            paths_str = [str(p) for p in paths]

            if paths_str:
                for file in paths_str:
                    if file not in self.Get_Uploaded_Files():
                        self.Add_File(file)

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
    def _copy_to_furniture_folder(self, filepath: str) -> Path:
        """
        Copia el archivo al directorio del mueble si no est? ya dentro.
        Devuelve la ruta final (original si no se copi?).
        """
        target_dir = getattr(self.sidebar, "input_dir", "")
        
        if not target_dir:
            return Path(filepath)

        target_dir = Path(target_dir)
        src_path = Path(filepath)

        try:
            src_in_target = src_path.resolve().is_relative_to(target_dir.resolve())
        except AttributeError:
            try:
                src_path.resolve().relative_to(target_dir.resolve())
                src_in_target = True
            except ValueError:
                src_in_target = False

        if src_in_target:
            return src_path

        target_dir.mkdir(parents=True, exist_ok=True)

        dest_path = target_dir / src_path.name
        counter = 1
        while dest_path.exists():
            dest_path = target_dir / f"{src_path.stem}_{counter}{src_path.suffix}"
            counter += 1

        shutil.copy2(src_path, dest_path)
        print(f"[Archivos] Copiado a carpeta del mueble: {dest_path}")
        return dest_path
    
    """

    """
    def Add_File(self, filepath: str):
        """A?ade un archivo a la lista"""
        filepath = str(self._copy_to_furniture_folder(filepath))
        self.sidebar.uploaded_files.append(filepath)
        
        # Crear widget del archivo
        file_widget = FileItemWidget(filepath)
        file_widget.remove_clicked.connect(self.Remove_File)
        
        self.sidebar.files_layout.addWidget(file_widget)
        self.Update_AgentFiles()
    
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
        
        self.Update_AgentFiles()

    """
        Update_AgentFiles():
        Refresca los archivos asociados al agente IA con la lista actual.
    """
    def Update_AgentFiles(self):
        agent = self.main_window.agent_IA
        furniture_name = getattr(self.sidebar, "furniture_name", "")

        if agent is None:
            return

        if not furniture_name or furniture_name == "Seleccione un mueble...":
            return

        files_data = self.Load_File_IDs(paths=self.sidebar.uploaded_files,furniture_name=furniture_name)

        agent.Clear_FileHistory()
        
        files_data
        agent.Add_Files(files_data)

    # ------ Control | Modelo StarGPT ------
    
    """
        Change_SG_Model():
    """
    def Change_SG_Model(self):
        selected_model = self.sidebar.model_combo.get_value()
        self.sidebar.model_title.setText(selected_model)

        print(f"[Modelo] Se selecciono: {selected_model}")

        if not selected_model == "STAR GPT":
            files_data = self.Load_File_IDs(paths=self.sidebar.uploaded_files, furniture_name=self.sidebar.furniture_name)

            print(f"[Archivos] Se cargaron los archivos: {files_data}")

            if selected_model == "Analista de Piezas":
                self.main_window.agent_IA = Analista_Piezas(self.ai_client)
                self.main_window.agent_IA.Add_Files(files_data)
                self.main_window.input_field.setText(self.main_window.agent_IA.SG_USER_PROMPT)

            elif selected_model == "Parametrizador de Modulos":
                self.main_window.agent_IA = ParametrizadorModulos(self.ai_client)
                self.main_window.agent_IA.Add_Files(files_data)
                self.main_window.input_field.setText(self.main_window.agent_IA.SG_USER_PROMPT)
                
                
            model_display_name = models_openAI_config.OPENAI_MODELS_BY_NAME[self.main_window.agent_IA.model]

            index = self.main_window.chat_topbar.model_openAI_combo.findText(model_display_name["display_name"], Qt.MatchFixedString | Qt.MatchCaseSensitive)

            if index >= 0:
                self.main_window.chat_topbar.model_openAI_combo.setCurrentIndex(index)

            print(f"[{selected_model}] configurado!")
            self.main_window.chat_topbar.model_openAI_combo.setEnabled(True)

            if selected_model == "Parametrizador de Modulos":
                self.main_window.chat_controller.Handle_SendMessage()
        
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
            
            file_id = self.openAI_fileManager.Load_File(local_FileName=local_filename, path=p)
            
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
