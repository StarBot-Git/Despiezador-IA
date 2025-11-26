from PySide6.QtCore import Qt, QSize
from PySide6.QtWidgets import *
from PySide6.QtGui import QIcon

# ====== IMPORTACIONES PROPIAS ======
from core import config
from ui.config import theme, icons
from core.ai_client import AIClient

from ui.components.window_topbar import Window_TopBar
from ui.components.sidebar import SideBar
from ui.components.chat_topbar import Chat_TopBar
from ui.components.chat_area import ChatWidget
from ui.controllers.chat_controller import ChatController
# from ui.workers.ai_worker import AIWorker  # <--- IMPORTAR EL WORKER

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # ======== Configuracion inicial ========

        self.setWindowTitle(config.APP_NAME)
        self.resize(theme.WINDOW_WIDTH, theme.WINDOW_HEIGHT)
        self.setWindowIcon(QIcon(icons.LOGO))

        self.agent_IA = None
        self.furniture_name = ""
        self.output_dir = ""
        self.input_dir = ""
        self.tokens = 0
        self.tokens_price = 0.0
        self.ai_client = AIClient()
        
        self.ai_worker = None  # <--- Guardar referencia al worker

        # ======== Layout principal ========

        central = QWidget(self)

        root = QVBoxLayout(central)
        root.setContentsMargins(0,0,0,0)
        root.setSpacing(0)

        # ======== Top Bar ========

        self.window_topbar = Window_TopBar(self)
        self.window_topbar.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.window_topbar.setFixedHeight(50)

        root.addWidget(self.window_topbar, alignment=Qt.AlignTop)

        # ======== Subcontenedor | Sidebar + Content/Table ========

        main_container = QHBoxLayout()
        main_container.setContentsMargins(16,0,16,16)
        main_container.setSpacing(12)

        root.addLayout(main_container)

        # ======== Side Bar ========

        self.sidebar = SideBar(parent=self, ai_client=self.ai_client)
        self.sidebar.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        self.sidebar.setFixedWidth(285)

        main_container.addWidget(self.sidebar, 0)

        vsep = QFrame(self); vsep.setObjectName("SideDivider"); vsep.setFrameShape(QFrame.VLine)
        main_container.addWidget(vsep)

        # ========= Chat Container ========

        self.chat_container = QWidget(self)
        self.chat_container.setObjectName("ChatContentArea")

        chat_content_layout = QVBoxLayout(self.chat_container)
        chat_content_layout.setContentsMargins(8, 8, 8, 8)
        chat_content_layout.setSpacing(8)

        # ========= TopBar | Chat Container =========

        self.chat_topbar = Chat_TopBar(self.chat_container, main_window=self)
        self.chat_topbar.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.chat_topbar.setFixedHeight(75)

        chat_content_layout.addWidget(self.chat_topbar)

        # ========= Separador horizontal  | Decorativo ========

        divider = QFrame(self)
        divider.setObjectName("TopDivider")
        divider.setFrameShape(QFrame.HLine)

        chat_content_layout.addWidget(divider)

        # ========= Chat Area =========

        self.chat_area = ChatWidget()
        self.chat_area.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        chat_content_layout.addWidget(self.chat_area)

        
        # ========= Controlador Chat Area ========

        self.chat_controller = ChatController(self)

        # ========= Separador horizontal  | Decorativo ========

        divider = QFrame(self)
        divider.setObjectName("TopDivider")
        divider.setFrameShape(QFrame.HLine)

        chat_content_layout.addWidget(divider)

        # ========= Message Area =========

        input_layout = QHBoxLayout()
        input_layout.setContentsMargins(0, 0, 0, 0)
        input_layout.setSpacing(12)

        self.input_field = QTextEdit()
        self.input_field.setPlaceholderText("Escribe tu mensaje aquí...")
        self.input_field.setMinimumHeight(42)
        self.input_field.setMaximumHeight(120)
        self.input_field.setObjectName("message-TextArea")

        self.send_button = QPushButton("  Enviar")
        self.send_button.setCursor(Qt.PointingHandCursor)
        self.send_button.setMinimumHeight(42)
        self.send_button.setIcon(QIcon("assets/icons/paper_plane.png"))
        self.send_button.setIconSize(QSize(18, 18))
        self.send_button.setObjectName("message-SendButton")

        self.send_button.clicked.connect(self.chat_controller.Handle_SendMessage)

        input_layout.addWidget(self.input_field)
        input_layout.addWidget(self.send_button)

        chat_content_layout.addLayout(input_layout)

        main_container.addWidget(self.chat_container, 1)

        self.setCentralWidget(central)
