from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QSizePolicy
from PySide6.QtGui import QPixmap, QColor
from PySide6.QtCore import Qt


class InfoCard(QWidget):
    def __init__(self, title: str, value: str,
                 bg_color="#FFFFFF",
                 border_color="#D0D0D0",
                 text_color="#133855",
                 accent_color="#C7664C",
                 icon_path: str = None,
                 parent=None):

        super().__init__(parent)

        self.setObjectName("InfoCard")
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setMinimumSize(80, 60)   # Ajusta a tu gusto
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)


        # --- Layout principal ---
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(12, 2, 12, 2)
        main_layout.setSpacing(0)

        # --- Cabecera (Icono + título) ---
        header = QHBoxLayout()
        header.setSpacing(6)

        if icon_path:
            icon = QLabel()
            pix = QPixmap(icon_path).scaled(20, 20, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            icon.setPixmap(pix)
            header.addWidget(icon)

        self.lbl_title = QLabel(title)
        self.lbl_title.setStyleSheet(f"color:{text_color}; font-size:12px; font-weight:600;")
        header.addWidget(self.lbl_title)
        header.addStretch()

        # --- Valor ---
        self.lbl_value = QLabel(value)
        self.lbl_value.setAlignment(Qt.AlignLeft)
        self.lbl_value.setStyleSheet(f"color:{accent_color}; font-size:18px; font-weight:700;")

        # Añadir al layout
        main_layout.addLayout(header)
        main_layout.addWidget(self.lbl_value)

        # --- Estilos dinámicos ---
        self.setStyleSheet(f"""
            #InfoCard {{
                background: {bg_color};
                border: 1px solid {border_color};
                border-radius: 8px;
            }}
        """)
