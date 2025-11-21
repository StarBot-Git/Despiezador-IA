import json

class BaseAgent:
    def __init__(self, ai_client, system_prompt, model, temperature=0.3):
        #_____________________________________________________________

        self.ai_client = ai_client
        self.model = model
        self.system_prompt = system_prompt
        self.temperature = temperature
        self.files = []

        self.messages = [{"role": "system", "content": system_prompt}]

        #_____________________________________________________________

    """
        Add_Files():
    """
    def Add_Files(self, files: list[dict]):
        if files:
            for file_id, file_type in files:
                input_type = "input_file" if file_type == 'pdf' else "input_image"

                self.files.append({"type": input_type, "file_id": file_id})
                print(f"[{self.__class__.__name__}] Añadio: {file_id}")

            # ------ Añdir | Archivos ------
            if self.files:
                self.messages.append({"role": "user", "content": self.files})

    """
        Clear_FileHistory():
    """
    def Clear_FileHistory(self):
        new_history = []

        for msg in self.messages:
            content = msg.get("content")

            # Si no es una lista, seguro no contiene archivos
            if not isinstance(content, list):
                new_history.append(msg)
                continue

            # Ver si algún ítem es archivo
            contains_file = any(
                isinstance(x, dict) and x.get("type") in ("input_file", "input_image")
                for x in content
            )

            if not contains_file:
                new_history.append(msg)

        self.messages = new_history
        self.files = []

        print(f"[{self.__class__.__name__}] Archivos del historial limpiados.")

    """
        Run():
    """
    def Run(self, prompt):
        print(f"[{self.__class__.__name__}] Hizo su peticion a OpenAI: {self.model}")

        # ------ Añadir | Prompt ------
        self.messages.append({"type": "input_text", "text": prompt})

        print(self.messages)

        # ------ OpenAI | Solicitud ------
        response = self.ai_client.Send_Request(
            model=self.model, input=self.messages, text_format=self.text_format, temperature=self.temperature
        )

        parsed = response.output_parsed

        assistant_json = parsed.model_dump_json()

        self.messages.append({"role": "assistant", "content": assistant_json})

        return parsed, response.usage


# class BaseAgent:
#     def __init__(self, system_prompt, model, temperature, default_tools, files):
#         self.model = model
#         self.system_prompt = system_prompt
#         self.default_tools = default_tools or []
#         self.messages = [{"role": "system", "content": system_prompt}]
#         self.temperature = temperature
#         self.files = files

#     def run(self, prompt):

#         print(f"[{self.__class__.__name__}] Hizo su peticion a OpenAI: {self.model}")

#         model_name = self.__class__.__name__

#         for key, data in config.OPENAI_MODELS.items():
#                 if data.get("name") == self.model:
#                     model_selected = key

#         content = []
#         #content.append({"type":"input_text", "text":prompt, "variables":variables})
#         content.append({"type":"input_text", "text":prompt})

#         if self.files:
#             for file_id, file_type in self.files.items():
#                 input_type = "input_file" if file_type == 'pdf' else "input_image"
#                 content.append({"type": input_type, "file_id": file_id})

#         self.messages.append({"role":"user", "content":content})

#         #print(self.messages)

#         response = send_request(model=self.model, input = self.messages, model_name=model_name, temperature=self.temperature)

#         # --- ASSISTANT CONTENT | Respuesta completa de la IA ---
#         # output_assistant_msg = json.dumps(response.model_dump(), ensure_ascii=False, indent=2)
#         # self.messages.append({"role":"assistant", "content":output_assistant_msg})

#         output = response.output_parsed

#         output_assistant_msg = json.dumps(output.dict(), ensure_ascii=False, indent=2)
#         self.messages.append({"role":"assistant", "content":output_assistant_msg})

#         print(f"TOKENS ENTRADA: {response.usage.input_tokens}")
#         print(f"TOKENS SALIDA: {response.usage.output_tokens}")
#         print(f"TOTAL: {response.usage.total_tokens}")

#         model_data = config.OPENAI_MODELS[model_selected]

#         print(model_data)

#         costo = calcular_costo(response.usage.input_tokens, response.usage.output_tokens, model_data["input_price"], model_data["output_price"])

#         print(f"EL COSTO ES: {costo}")

#         print("HOLA 0")

#         return output, costo, response.usage.total_tokens