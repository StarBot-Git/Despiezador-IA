from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QIcon
from pathlib import Path
from config import settings

class FileItemWidget(QWidget):
    """Widget individual para cada archivo en la lista"""
    remove_clicked = Signal(str)  # Señal para eliminar archivo
    
    def __init__(self, filepath: str, parent: QWidget | None = None):
        super().__init__(parent)
        self.filepath = filepath
        self.filename = Path(filepath).name
        self.setObjectName("FileItem")
        self.setAttribute(Qt.WA_StyledBackground, True)
        
        # Layout horizontal
        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 10, 12, 10)
        layout.setSpacing(10)
        
        # Botón de eliminar (X)
        self.remove_btn = QPushButton("×")
        self.remove_btn.setObjectName("FileItemRemoveBtn")
        self.remove_btn.setFixedSize(20, 20)
        self.remove_btn.setCursor(Qt.PointingHandCursor)
        self.remove_btn.clicked.connect(lambda: self.remove_clicked.emit(self.filepath))
        
        # Icono del archivo
        icon_label = QLabel()
        icon_label.setFixedSize(20, 20)
        icon_label.setObjectName("FileItemIcon")
        
        # Determinar icono según extensión
        ext = Path(filepath).suffix.lower()
        if ext == '.pdf':
            icon_label.setPixmap(QIcon(settings.PDF_ICON_DIR).pixmap(20, 20))
        elif ext in ['.png', '.jpg', '.jpeg']:
            icon_label.setPixmap(QIcon(settings.IMAGE_ICON_DIR).pixmap(20, 20))
        else:
            icon_label.setPixmap(QIcon(settings.FILE_ICON_DIR).pixmap(20, 20))
        
        # Nombre del archivo
        name_label = QLabel(self.filename)
        name_label.setObjectName("FileItemName")
        
        # Añadir widgets
        layout.addWidget(self.remove_btn)
        layout.addWidget(icon_label)
        layout.addWidget(name_label, 1)