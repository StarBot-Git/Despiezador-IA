import json

from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QSizePolicy, QFrame, QComboBox, QScrollArea, QFileDialog, QHBoxLayout
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon
from pathlib import Path

# ====== IMPORTACIONES PROPIAS ======
from ui.config import icons
from core import config
from ui.controllers.sidebar_controller import SideBarController
from ui.components.fileitem_widget import FileItemWidget
from ui.components.model_combobox import IconComboBox 
#from ui.controllers.furniture_controller import Furniture_Controller
#from ui.controllers.sg_model_controller import StarGPTModelController

class SideBar(QWidget):
    def __init__(self, parent:QWidget|None = None, ai_client = None):
        super().__init__(parent)

        self.setObjectName("SideBar")
        self.setAttribute(Qt.WA_StyledBackground, True)

        self.uploaded_files = []
        self.furniture_name = ""
        self.output_dir = ""
        self.input_dir = ""
        self.agent_IA = None

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
        model_icon.setPixmap(QIcon(icons.OPENAI_LOGO).pixmap(40,40))

        wrapper_layout.addWidget(model_icon)

        # ------ Aux ------

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

        # ------ Controlador | SideBar -------

        self.controller = SideBarController(sidebar=self, main_window=parent, ai_client=ai_client)

        # ------ Label | Select Furniture ------

        furniture_label = QLabel("Seleccione un mueble:")
        furniture_label.setObjectName("SideBar-OptionLabels")

        options_layout.addWidget(furniture_label)

        # ------ ComboBox | Furnitures -----

        self.furniture_combo = QComboBox()
        self.furniture_combo.setObjectName("SideBar-ComboBoxes")

        self.controller.Load_FurnitureFolders(config.INPUT_DIR)

        self.furniture_combo.currentIndexChanged.connect(self.controller.Change_Furniture)

        options_layout.addWidget(self.furniture_combo)

        # ------ Label | Select Model ------

        model_label = QLabel("Modelo de IA:")
        model_label.setObjectName("SideBar-OptionLabels")

        options_layout.addWidget(model_label)        
        
        # ------ ComboBox | Models ------

        self.model_combo = IconComboBox(self)
        # self.model_combo.add_item("Instructor de Modelacion", settings.INSTRUCTOR_ICON_CB)
        self.model_combo.add_item("STAR GPT", icons.IA_ICON)
        self.model_combo.add_item("Analista de Piezas", icons.ANALISTA)
        #self.model_combo.model.item(1).setEnabled(False)
        self.model_combo.add_item("Supervisor de Piezas", icons.SUPERVISOR)
        self.model_combo.model.item(2).setEnabled(False)

        self.model_combo.currentIndexChanged.connect(self.controller.Change_SG_Model)

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
        scroll_area.setMinimumHeight(100)
        
        # Widget contenedor de la lista
        self.files_container = QWidget()
        self.files_container.setObjectName("FilesContainer")
        self.files_container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.files_layout = QVBoxLayout(self.files_container)
        self.files_layout.setContentsMargins(0, 0, 0, 0)
        self.files_layout.setSpacing(8)
        self.files_layout.setAlignment(Qt.AlignTop)
        
        scroll_area.setWidget(self.files_container)
        main_layout.addWidget(scroll_area, 1)

        main_layout.addStretch()
        
        # ======== Botón: Adjuntar Archivos ========
        upload_btn = QPushButton(" Adjuntar Archivos")
        upload_btn.setObjectName("SideBarUploadButton")
        upload_btn.setCursor(Qt.PointingHandCursor)
        upload_btn.setIcon(QIcon(icons.UPLOAD_ICON))
        upload_btn.setIconSize(QSize(16,16))
        upload_btn.clicked.connect(self.controller.OpenFile_Dialog)

        main_layout.addWidget(upload_btn)
        
        # ======== fIN ========