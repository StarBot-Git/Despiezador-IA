from PySide6.QtWidgets import QFrame, QLabel, QWidget, QHBoxLayout, QPushButton, QSizePolicy, QComboBox
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon

from config import settings
from ui.components.info_card import InfoCard
from ui.controllers.model_openAI_controller import ModelOpenAI_Controller

# En TopBar.__init__
class Chat_TopBar(QFrame):
    def __init__(self, parent:QWidget|None = None, main_window=None):
        super().__init__(parent)
        self.setObjectName("Chat_TopBar")

        # ======== Layout principal ========= 
        
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 12, 0, 12)
        main_layout.setSpacing(12)

        # ======== ComboBox | Modelos OpenAI ========= 

        self.model_openAI_combo = QComboBox()
        self.model_openAI_combo.setObjectName("ChatTopBar-ModelOpenAICB")
        self.model_openAI_combo.addItems(["GPT-5 mini","GPT-4 nano"])

        main_layout.addWidget(self.model_openAI_combo)

        self.model_openAI_controller = ModelOpenAI_Controller(chat_topbar=self, main_window=main_window)
        self.model_openAI_combo.currentIndexChanged.connect(self.model_openAI_controller.Change_OpenAIModel)


        main_layout.addStretch(1)

        # ======== InfoCard | Tokens spent ========= 

        self.card_tokens = InfoCard(
            title="Tokens usados",
            value="0",
            accent_color=settings.BLUE_ALL_STAR,
            icon_path=settings.CARD_TOKENS_DIR
        )

        main_layout.addWidget(self.card_tokens)

        # ======== InfoCard | Cost ========= 

        self.card_tokens_price = InfoCard(
            title="Costo estimado",
            value="0.00",
            accent_color=settings.ORANGE_ALL_STAR,
            icon_path=settings.CARD_COST_DIR
        )

        main_layout.addWidget(self.card_tokens_price)