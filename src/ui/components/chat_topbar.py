from PySide6.QtWidgets import QFrame, QWidget, QHBoxLayout, QComboBox

# ====== IMPORTACIONES PROPIAS ======
from ui.config import theme, icons
from ui.components.info_card import InfoCard
from ui.controllers.chat_topbar_controller import Chat_TopBarController

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
        self.model_openAI_combo.setEnabled(False)

        main_layout.addWidget(self.model_openAI_combo)

        # ======== Controlador | Chat TopBar ========= 

        self.controller = Chat_TopBarController(chat_topbar=self, main_window=main_window)
        self.model_openAI_combo.currentIndexChanged.connect(self.controller.Change_OpenAIModel)

        main_layout.addStretch(1)

        # ======== InfoCard | Tokens spent ========= 

        self.card_tokens = InfoCard(
            title="Tokens usados",
            value="0",
            accent_color=theme.BLUE_ALL_STAR,
            icon_path=icons.CARD_TOKENS
        )

        main_layout.addWidget(self.card_tokens)

        # ======== InfoCard | Cost ========= 

        self.card_tokens_price = InfoCard(
            title="Costo estimado",
            value="0.00",
            accent_color=theme.ORANGE_ALL_STAR,
            icon_path=icons.CARD_COST
        )

        main_layout.addWidget(self.card_tokens_price)