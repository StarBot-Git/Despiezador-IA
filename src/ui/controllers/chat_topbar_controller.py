from core import models_openAI_config as models

class Chat_TopBarController:
    def __init__(self, chat_topbar, main_window):
        self.chat_topbar = chat_topbar
        self.main_window = main_window

    def Load_OpenAIModel(self):
        models_list = []
        
        for _, model_info in models.OPENAI_MODELS.items():
            #print(model_info["display_name"])
            models_list.append(model_info["display_name"])

        self.chat_topbar.model_openAI_combo.addItems(models_list)

    """
        """
    def Change_OpenAIModel(self):
        model = self.chat_topbar.model_openAI_combo.currentText()

        if self.main_window.agent_IA:
            current_model = models.OPENAI_MODELS_BY_DISPLAY[model]
            print(f"De [{model}] sale: {current_model}")

            self.main_window.agent_IA.model = current_model

    """
    """
    def Update_Tokens(self, tokens):
        self.main_window.tokens += int(tokens)

        self.chat_topbar.card_tokens.lbl_value.setText(f"{self.main_window.tokens:,}".replace(",", " "))

    """
    """
    def Update_Cost(self, tokens_in, tokens_out):
        openAI_model = models.OPENAI_MODELS_BY_NAME[self.main_window.agent_IA.model]

        precio_token_entrada = openAI_model["input_price"] / 1_000_000
        precio_token_salida  = openAI_model["output_price"]  / 1_000_000

        price = tokens_in * precio_token_entrada \
            + tokens_out * precio_token_salida
        
        self.main_window.tokens_price += float(price)

        print(self.main_window.tokens_price)

        self.chat_topbar.card_tokens_price.lbl_value.setText( str( round(self.main_window.tokens_price,3) ) )