from core import config

class ModelOpenAI_Controller:
    def __init__(self, chat_topbar, main_window):
        self.chat_topbar = chat_topbar
        self.main_window = main_window

    def Change_OpenAIModel(self):
        model = self.chat_topbar.model_openAI_combo.currentText()

        if self.main_window.agent_IA:
            print(f"De [{model}] sale: {config.OPENAI_MODELS[model]["name"]}")
            self.main_window.agent_IA.model = config.OPENAI_MODELS[model]["name"]