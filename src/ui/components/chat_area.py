from PySide6.QtWidgets import QWidget, QVBoxLayout, QScrollArea
from ui.components.message_bubble import MessageBubble

class ChatWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Scroll con contenedor interno
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

        # Layout principal
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.scroll)

    def add_message(self, text, role="assistant"):
        bubble = MessageBubble(text, role)
        self.layout.insertWidget(self.layout.count() - 1, bubble)

        # Auto scroll al final
        self.scroll.verticalScrollBar().setValue(
            self.scroll.verticalScrollBar().maximum()
        )

    def remove_last_message(self):
        """
        Remueve el último mensaje del chat.
        Útil para eliminar mensajes temporales como "Analizando..."
        """
        if self.layout.count() > 1:  # Debe haber al menos 1 mensaje + stretch
            # El último item es el stretch, el penúltimo es el mensaje
            last_msg_index = self.layout.count() - 2
            last_item = self.layout.itemAt(last_msg_index)
            
            if last_item and last_item.widget():
                widget = last_item.widget()
                self.layout.removeWidget(widget)
                widget.deleteLater()