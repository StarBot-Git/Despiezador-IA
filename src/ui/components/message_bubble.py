from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QSizePolicy
from PySide6.QtCore import Qt
import markdown

class MessageBubble(QWidget):
    def __init__(self, text: str, role="assistant", parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_StyledBackground, True)

        self.role = role
        self.text = markdown.markdown(text)

        # --- Estilos según tipo ---
        if role == "assistant":
            bg = "#0F3A55"
            text_color = "white"
            align = Qt.AlignLeft
        else:
            bg = "#C7664C"
            text_color = "white"
            align = Qt.AlignRight

        # --- Layout horizontal para alinear ---
        wrapper = QHBoxLayout(self)
        wrapper.setContentsMargins(0, 4, 0, 4)

        # --- Burbuja interna ---
        bubble = QWidget()
        bubble.setObjectName("Bubble")
        bubble.setStyleSheet(f"""
            QWidget#Bubble {{
                background: {bg};
                border-radius: 14px;
            }}
        """)
        bubble.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)

        bubble_layout = QVBoxLayout(bubble)
        bubble_layout.setContentsMargins(14, 10, 14, 10)

        label = QLabel()
        label.setTextFormat(Qt.RichText)   # MUY IMPORTANTE
        label.setText(self.text)
        label.setWordWrap(True)
        label.setStyleSheet(f"color:{text_color}; font-size:14px;")
        bubble_layout.addWidget(label)

        # Alinear burbuja según el rol
        if role == "assistant":
            wrapper.addWidget(bubble, 0, align)
            wrapper.addStretch()
        else:
            wrapper.addStretch()
            wrapper.addWidget(bubble, 0, align)
