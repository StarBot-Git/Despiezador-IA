from PySide6.QtWidgets import QFrame, QLabel, QWidget, QHBoxLayout, QPushButton, QSizePolicy
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon
from config import settings

# En TopBar.__init__
class TopBar(QFrame):
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

        # ======== Botones |  =========

        # ======== FIN =========

        main_layout.addStretch(1)