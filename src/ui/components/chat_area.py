from PySide6.QtWidgets import QWidget, QVBoxLayout, QScrollArea

class ChatWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # ========= Scroll Area ========

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setStyleSheet("border: none;")

        self.container = QWidget()
        self.container.setObjectName("ChatArea")
        self.layout = QVBoxLayout(self.container)
        self.layout.setContentsMargins(12, 12, 12, 12)
        self.layout.setSpacing(8)
        self.layout.addStretch()

        self.scroll.setWidget(self.container)

        # ========= Main Layout ========

        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.scroll)