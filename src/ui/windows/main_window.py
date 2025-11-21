from PySide6.QtCore import Qt, QSize
from PySide6.QtWidgets import *
from PySide6.QtGui import QIcon

# ====== IMPORTACIONES PROPIAS ======
from core import config
from ui.config import theme, icons
from ui.components.window_topbar import Window_TopBar
from ui.components.sidebar import SideBar
from ui.components.chat_topbar import Chat_TopBar
from ui.components.chat_area import ChatWidget
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
        #root.addWidget(self.window_topbar)

        root.addWidget(self.window_topbar, alignment=Qt.AlignTop)

        # ======== Subcontenedor | Sidebar + Content/Table ========

        main_container = QHBoxLayout()
        main_container.setContentsMargins(16,0,16,16)
        main_container.setSpacing(12)

        root.addLayout(main_container)

        # ======== Side Bar ========

        self.sidebar = SideBar(self)
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
        self.input_field.setStyleSheet("""
            QTextEdit {
                background: #F5F7F9;
                border: 1px solid #E0E6EB;
                border-radius: 20px;
                padding: 10px 16px;
                font-size: 14px;
                color: #133855;
            }
            QTextEdit:focus {
                border: 1px solid #C5D4E0;
                background: #FFFFFF;
            }
        """)

        self.send_button = QPushButton("  Enviar")
        self.send_button.setCursor(Qt.PointingHandCursor)
        self.send_button.setMinimumHeight(42)
        self.send_button.setIcon(QIcon("assets/icons/paper_plane.png"))
        self.send_button.setIconSize(QSize(18, 18))

        self.send_button.setStyleSheet("""
            QPushButton {
                background: #0F3A55;
                color: white;
                border-radius: 20px;
                padding: 0 18px;
                font-size: 14px;
                font-weight: 600;
            }
            QPushButton:hover {
                background: #174C71;
            }
            QPushButton:pressed {
                background: #0B2C40;
            }
        """)

        #self.send_button.clicked.connect(self.handle_send_message)

        input_layout.addWidget(self.input_field)
        input_layout.addWidget(self.send_button)

        chat_content_layout.addLayout(input_layout)

        main_container.addWidget(self.chat_container, 1)

        self.setCentralWidget(central)

    # def handle_send_message(self):
    #     """Método actualizado con Threading"""
    #     text = self.input_field.toPlainText().strip()

    #     if not text:
    #         return

    #     # Deshabilitar el botón mientras procesa
    #     self.send_button.setEnabled(False)
    #     self.send_button.setText("  Procesando...")
        
    #     # Agregar mensaje del usuario
    #     self.chat_area.add_message(text, role="user")
        
    #     # Limpiar el campo de entrada
    #     self.input_field.clear()
        
    #     # Agregar mensaje temporal "IA escribiendo..."
    #     self.chat_area.add_message("✍️ Analizando...", role="assistant")

    #     # Crear y configurar el worker thread
    #     self.ai_worker = AIWorker(self.agent_IA, text)
        
    #     # Conectar las señales
    #     self.ai_worker.finished.connect(self.on_ai_response)
    #     self.ai_worker.error.connect(self.on_ai_error)
        
    #     # Iniciar el thread (no bloquea la interfaz)
    #     self.ai_worker.start()

    # def on_ai_response(self, output_obj, price, tokens):
    #     """Se ejecuta cuando el worker termina exitosamente"""

    #     print("HOLA 2")
        
    #     # Remover el mensaje temporal "Analizando..."
    #     self.chat_area.remove_last_message()
        
    #     # Convertir respuesta a texto legible
    #     output_msg = self.agent_IA.json_to_message(output_obj.dict())
        
    #     # Agregar respuesta de la IA
    #     self.chat_area.add_message(output_msg, role="assistant")
        
    #     # Guardar el JSON
    #     self.sidebar.save_output_JSON(output_obj)

    #     self.tokens += int(tokens)
    #     self.tokens_price += float(price)

    #     print(self.tokens_price)

    #     self.chat_topbar.card_tokens.lbl_value.setText(f"{self.tokens:,}".replace(",", " "))
    #     self.chat_topbar.card_tokens_price.lbl_value.setText( str( round(self.tokens_price,3) ) )
        
    #     # Rehabilitar el botón
    #     self.send_button.setEnabled(True)
    #     self.send_button.setText("  Enviar")
        
    #     print(f"[{self.agent_IA.__class__.__name__}] Respuesta recibida exitosamente")

    # def on_ai_error(self, error_msg):
    #     """Se ejecuta si hay un error en el worker"""
        
    #     # Remover el mensaje temporal
    #     self.chat_area.remove_last_message()
        
    #     # Mostrar error
    #     self.chat_area.add_message(f"❌ Error: {error_msg}", role="assistant")
        
    #     # Rehabilitar el botón
    #     self.send_button.setEnabled(True)
    #     self.send_button.setText("  Enviar")
        
    #     print(f"[ERROR] {error_msg}")

