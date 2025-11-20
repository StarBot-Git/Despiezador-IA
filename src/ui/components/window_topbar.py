from PySide6.QtWidgets import QFrame, QLabel, QWidget, QHBoxLayout, QPushButton, QSizePolicy
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon

from config import settings
from ui.controllers.topbar_controller import open_folder


# En TopBar.__init__
class Window_TopBar(QFrame):
    def __init__(self, parent:QWidget|None = None):
        super().__init__(parent)
        self.setObjectName("TopBar")

        # ======== Layout principal ========= 
        
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(24, 12, 24, 12)
        main_layout.setSpacing(12)

        # ======== Titulo de barra =========

        self._title = QLabel(settings.APP_NAME, self)
        self._title.setObjectName("TopBar-Title")

        main_layout.addWidget(self._title, 0, Qt.AlignVCenter)

        main_layout.addStretch(1)

        # ======== Botones |  =========

        self.btn_folder = QPushButton("")
        self.btn_folder.clicked.connect(lambda: open_folder(parent.input_dir, parent.furniture_name))
        self.set_Button_Style(self.btn_folder, icon_path=settings.FOLDER_ICON_DIR)
        main_layout.addWidget(self.btn_folder, 0, Qt.AlignVCenter)

        # ======== FIN =========

    def set_Button_Style(self, button:QPushButton, icon_path:str = "", enabled:bool = False):
        # === Estilo base | Button ===
        button.setObjectName("Button_Style")
        button.setEnabled(enabled)
        button.setMinimumHeight(32)
        button.setCursor(Qt.PointingHandCursor)

        if icon_path:
            button.setIcon(QIcon(icon_path)) 
            button.setIconSize(QSize(24, 24))  