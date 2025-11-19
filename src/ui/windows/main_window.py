from PySide6.QtCore import Qt
from PySide6.QtWidgets import *
from PySide6.QtGui import QIcon
from ui.components.sidebar import SideBar
from config import settings
from ui.components.topbar import TopBar

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # ======== Configuracion inicial ========

        self.setWindowTitle(settings.APP_NAME) # Nombre de la aplicacion
        self.resize(settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT) # Tamaño inicial
        self.setWindowIcon(QIcon(settings.LOGO_DIR)) # Logo All Star | Barra de la App

        # ======== Layout principal ========

        central = QWidget(self)

        root = QVBoxLayout(central)
        root.setContentsMargins(0,0,0,0)
        root.setSpacing(0)

        # ======== Top Bar ========

        self.topbar = TopBar(self)
        self.topbar.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.topbar.setFixedHeight(50)
        root.addWidget(self.topbar)

        root.addWidget(self.topbar, alignment=Qt.AlignTop)

        # ======== Subcontenedor | Sidebar + Content/Table ========
            # - Sidebar (panel de selección)
            # - Separador vertical (decorativo)
            # - Content/Table (vista dinámica)

        main_container = QHBoxLayout()
        main_container.setContentsMargins(16,16,16,16)   # <--- CAMBIO
        main_container.setSpacing(12)                 # <--- CAMBIO


        root.addLayout(main_container)

        # ======== Side Bar ========

        self.sidebar = SideBar(self) # Panel Lateral | .py externo
        self.sidebar.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        self.sidebar.setFixedWidth(285)

        #self._SelectionPanelController = SelectionPanelController(self, self.DB) # Controlador del panel de selección
        #self._SelectionPanelController.Start_SP() # Cargar datos iniciales proveniente de la base de datos

        main_container.addWidget(self.sidebar, 0)

        vsep = QFrame(self); vsep.setObjectName("SideDivider"); vsep.setFrameShape(QFrame.VLine)
        main_container.addWidget(vsep)

        # ========= Chat Container ========

        self.chat_container = QWidget(self)
        self.chat_container.setObjectName("ContentArea")

        chat_content_layout = QVBoxLayout(self.chat_container)
        chat_content_layout.setContentsMargins(8, 8, 8, 8)
        chat_content_layout.setSpacing(8)

        main_container.addWidget(self.chat_container, 1)


        # layout = QHBoxLayout(central_widget)

        # # --- Sidebar ---
        # self.sidebar = SideBar()
        # layout.addWidget(self.sidebar)

        # # --- Área central (placeholder) ---
        # self.main_area = QWidget()
        # self.main_area.setStyleSheet("background: #FFFFFF; border-radius: 8px;")
        # layout.addWidget(self.main_area)

        self.setCentralWidget(central)
