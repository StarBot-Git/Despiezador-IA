from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QSizePolicy, QFrame, QComboBox, QScrollArea, QFileDialog, QHBoxLayout
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon
from pathlib import Path
import json

from config import settings
from ui.components.fileitem_widget import FileItemWidget
from ui.components.model_combobox import IconComboBox 
from ui.controllers.furniture_controller import Furniture_Controller
from ui.controllers.sg_model_controller import StarGPTModelController

class SideBar(QWidget):
    def __init__(self, parent:QWidget|None = None):
        super().__init__(parent)

        self.setObjectName("SideBar")
        self.setAttribute(Qt.WA_StyledBackground, True)

        self.uploaded_files = []
        self.furniture_name = ""
        self.output_dir = ""
        self.input_dir = ""
        self.agent_IA = None

        print(parent.__class__.__name__)

        # ======== Layout principal ========

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0,10,0,10)
        main_layout.setSpacing(12)
        main_layout.setAlignment(Qt.AlignTop)

        # ======== Model Info Container ========

        info_container = QWidget()

        info_layout = QVBoxLayout(info_container)
        info_layout.setSpacing(12)
        info_layout.setAlignment(Qt.AlignCenter)

        # ------ Icon Container ------

        icon_wrapper = QWidget()
        icon_wrapper.setObjectName("SideBar-IconWrapper")
        icon_wrapper.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        wrapper_layout = QVBoxLayout(icon_wrapper)
        wrapper_layout.setContentsMargins(10, 10, 10, 10)   # padding interno
        wrapper_layout.setAlignment(Qt.AlignCenter)

        # ------ Icon ------

        model_icon = QLabel()
        model_icon.setFixedSize(40,40)
        model_icon.setObjectName("SideBar-ModelIcon")
        #model_icon.setAlignment(Qt.AlignCenter)
        model_icon.setPixmap(QIcon(settings.OPEN_AI_LOGO_DIR).pixmap(40,40))

        wrapper_layout.addWidget(model_icon)

        row = QHBoxLayout()
        row.addStretch(1)
        row.addWidget(icon_wrapper)
        row.addStretch(1)

        info_layout.addLayout(row)

        # ------ Title ------

        self.model_title = QLabel("STAR GPT")
        self.model_title.setObjectName("SideBar-ModelTitle")
        self.model_title.setAlignment(Qt.AlignCenter)

        info_layout.addWidget(self.model_title)

        main_layout.addWidget(info_container)

        # ======== Separador Horizontal ========

        divider = QFrame(self)
        divider.setObjectName("TopDivider")
        divider.setFrameShape(QFrame.HLine)

        main_layout.addWidget(divider)

        # ======== Options Container ========

        options_container = QWidget()

        options_layout = QVBoxLayout(options_container)
        options_layout.setContentsMargins(0,0,0,0)
        options_layout.setSpacing(12)

        # ------ Label | Select Furniture ------

        furniture_label = QLabel("Seleccione un mueble:")
        furniture_label.setObjectName("SideBar-OptionLabels")

        options_layout.addWidget(furniture_label)

        # ------ ComboBox | Furnitures -----

        self.furniture_combo = QComboBox()
        self.furniture_combo.setObjectName("SideBar-ComboBoxes")

        self.furniture_controller = Furniture_Controller(sidebar=self)
        self.furniture_controller.Load_FurnitureFolders(settings.INPUT_DIR)

        self.furniture_combo.currentIndexChanged.connect(self.furniture_controller.Change_Furniture)

        options_layout.addWidget(self.furniture_combo)

        # ------ Label | Select Model ------

        model_label = QLabel("Modelo de IA:")
        model_label.setObjectName("SideBar-OptionLabels")

        options_layout.addWidget(model_label)        
        
        # ------ ComboBox | Models ------

        self.model_combo = IconComboBox(self)
        # self.model_combo.add_item("Instructor de Modelacion", settings.INSTRUCTOR_ICON_CB)
        self.model_combo.add_item("STAR GPT", settings.IA_ICON_DIR)
        self.model_combo.add_item("Analista de Piezas", settings.ANALISTA_ICON_CB)
        #self.model_combo.model.item(1).setEnabled(False)
        self.model_combo.add_item("Supervisor de Piezas", settings.SUPERVISOR_ICON_CB)
        self.model_combo.model.item(2).setEnabled(False)

        self.model_combo_controller = StarGPTModelController(sidebar=self, main_window=parent)

        self.model_combo.currentIndexChanged.connect(self.model_combo_controller.Change_Model)

        self.model_combo.setEnabled(False)

        options_layout.addWidget(self.model_combo)

        main_layout.addWidget(options_container)

        # ======== Separador Horizontal ========

        divider = QFrame(self)
        divider.setObjectName("TopDivider")
        divider.setFrameShape(QFrame.HLine)

        main_layout.addWidget(divider)

        # ------ Label | Project Files ------

        project_files_label = QLabel("Archivos del proyecto")
        project_files_label.setObjectName("SideBar-OptionLabels")

        main_layout.addWidget(project_files_label)

        # ----------------------------------------------
        # Contenedor scrollable para archivos

        scroll_area = QScrollArea()
        scroll_area.setObjectName("FileListScrollArea")
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setMaximumHeight(200)
        
        # Widget contenedor de la lista
        self.files_container = QWidget()
        self.files_container.setObjectName("FilesContainer")
        self.files_layout = QVBoxLayout(self.files_container)
        self.files_layout.setContentsMargins(0, 0, 0, 0)
        self.files_layout.setSpacing(8)
        self.files_layout.setAlignment(Qt.AlignTop)
        
        scroll_area.setWidget(self.files_container)
        main_layout.addWidget(scroll_area)
        
        # ======== Botón: Adjuntar Archivos ========
        upload_btn = QPushButton(" Adjuntar Archivos")
        upload_btn.setObjectName("SideBarUploadButton")
        upload_btn.setCursor(Qt.PointingHandCursor)
        upload_btn.setIcon(QIcon(settings.UPLOAD_ICON_DIR))
        upload_btn.setIconSize(QSize(16,16))
        upload_btn.clicked.connect(self.open_file_dialog)

        main_layout.addWidget(upload_btn)
        
        # Texto de formatos permitidos
        # formats_label = QLabel("PDF, PNG, JPG")
        # formats_label.setObjectName("SideBarFormatsLabel")
        # formats_label.setAlignment(Qt.AlignCenter)
        
        # main_layout.addWidget(formats_label)


        # ======== fIN ========

        #main_layout.addStretch(1)

    def open_file_dialog(self):
        """Abre el diálogo para seleccionar archivos"""
        files, _ = QFileDialog.getOpenFileNames(
            self,
            "Seleccionar archivos",
            "",
            "Archivos permitidos (*.pdf *.png *.jpg *.jpeg);;Todos los archivos (*)"
        )
        
        if files:
            for file in files:
                if file not in self.get_uploaded_files():
                    self.add_file(file)
                    print(f"añadi:{file}")
    
    def add_file(self, filepath: str):
        """Añade un archivo a la lista"""
        self.uploaded_files.append(filepath)
        
        # Crear widget del archivo
        file_widget = FileItemWidget(filepath)
        file_widget.remove_clicked.connect(self.remove_file)
        
        self.files_layout.addWidget(file_widget)
    
    def remove_file(self, filepath: str):
        """Elimina un archivo de la lista"""
        if filepath in self.uploaded_files:
            self.uploaded_files.remove(filepath)
        
        # Buscar y eliminar el widget
        for i in range(self.files_layout.count()):
            widget = self.files_layout.itemAt(i).widget()
            if isinstance(widget, FileItemWidget) and widget.filepath == filepath:
                widget.deleteLater()
                break
    
    def get_uploaded_files(self):
        """Retorna la lista de archivos subidos"""
        return self.uploaded_files.copy()
    
    def clear_files(self):
        """Limpia todos los archivos de la lista"""
        self.uploaded_files.clear()
        while self.files_layout.count():
            item = self.files_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

    def save_output_JSON(self, response_obj):
        file_JSON = f"{self.output_dir}\\{self.furniture_name}_piezas.json"

        #print(disassemble_obj)

        with open(file_JSON, "w", encoding="utf-8") as f:
            json.dump(response_obj.dict(), f, indent=4, ensure_ascii=False)