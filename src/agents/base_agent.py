from agents.ai_client import send_request
from utils.tokens_ai import *
from config import settings

import json

class BaseAgent:
    def __init__(self, system_prompt, model, temperature, default_tools, files):
        self.model = model
        self.system_prompt = system_prompt
        self.default_tools = default_tools or []
        self.messages = [{"role": "system", "content": system_prompt}]
        self.temperature = temperature
        self.files = files

    def run(self, prompt):

        print(f"[{self.__class__.__name__}] Hizo su peticion a OpenAI: {self.model}")

        model_name = self.__class__.__name__

        for key, data in settings.OPENAI_MODELS.items():
                if data.get("name") == self.model:
                    model_selected = key

        content = []
        #content.append({"type":"input_text", "text":prompt, "variables":variables})
        content.append({"type":"input_text", "text":prompt})

        if self.files:
            for file_id, file_type in self.files.items():
                input_type = "input_file" if file_type == 'pdf' else "input_image"
                content.append({"type": input_type, "file_id": file_id})

        self.messages.append({"role":"user", "content":content})

        #print(self.messages)

        response = send_request(model=self.model, input = self.messages, model_name=model_name, temperature=self.temperature)

        # --- ASSISTANT CONTENT | Respuesta completa de la IA ---
        # output_assistant_msg = json.dumps(response.model_dump(), ensure_ascii=False, indent=2)
        # self.messages.append({"role":"assistant", "content":output_assistant_msg})

        output = response.output_parsed

        output_assistant_msg = json.dumps(output.dict(), ensure_ascii=False, indent=2)
        self.messages.append({"role":"assistant", "content":output_assistant_msg})

        print(f"TOKENS ENTRADA: {response.usage.input_tokens}")
        print(f"TOKENS SALIDA: {response.usage.output_tokens}")
        print(f"TOTAL: {response.usage.total_tokens}")

        model_data = settings.OPENAI_MODELS[model_selected]

        print(model_data)

        costo = calcular_costo(response.usage.input_tokens, response.usage.output_tokens, model_data["input_price"], model_data["output_price"])

        print(f"EL COSTO ES: {costo}")

        print("HOLA 0")

        return output, costo, response.usage.total_tokens