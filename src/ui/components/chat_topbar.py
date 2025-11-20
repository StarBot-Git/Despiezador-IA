from PySide6.QtWidgets import QFrame, QLabel, QWidget, QHBoxLayout, QPushButton, QSizePolicy, QComboBox
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon

from config import settings
from ui.components.info_card import InfoCard

# En TopBar.__init__
class Chat_TopBar(QFrame):
    def __init__(self, parent:QWidget|None = None):
        super().__init__(parent)
        self.setObjectName("Chat_TopBar")

        # ======== Layout principal ========= 
        
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 12, 0, 12)
        main_layout.setSpacing(12)

        # ======== ComboBox | Modelos OpenAI ========= 

        self.model_openAI_combo = QComboBox()
        self.model_openAI_combo.setObjectName("ChatTopBar-ModelOpenAICB")
        self.model_openAI_combo.addItems(["GPT-5","GPT-5.1","GPT-4", "GPT-3.5"])

        main_layout.addWidget(self.model_openAI_combo)

        main_layout.addStretch(1)

        # ======== InfoCard | Tokens spent ========= 

        card_tokens = InfoCard(
            title="Tokens usados",
            value="xx.xx",
            accent_color=settings.BLUE_ALL_STAR,
            icon_path=settings.CARD_TOKENS_DIR
        )

        main_layout.addWidget(card_tokens)

        # ======== InfoCard | Cost ========= 

        card_tokens = InfoCard(
            title="Costo estimado",
            value="xx.xx",
            accent_color=settings.ORANGE_ALL_STAR,
            icon_path=settings.CARD_COST_DIR
        )

        main_layout.addWidget(card_tokens)