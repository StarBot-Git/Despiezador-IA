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
        #_____________________________________________________________

        if files:
            for file_id, file_type in files.items():
                input_type = "input_file" if file_type == 'pdf' else "input_image"

                self.files.append({"type": input_type, "file_id": file_id})
                print(f"[{self.__class__.__name__}] Añadio: {file_id}")

        #_____________________________________________________________

    """
        Clear_FileHistory():
    """
    def Clear_FileHistory(self):
        #_______________________________________________________________________________

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

        #_______________________________________________________________________________

    """
        Run():
    """
    def Run(self, prompt):
        #_______________________________________________________________________________

        print(f"[{self.__class__.__name__}] Hizo su peticion a OpenAI: {self.model}")
        content = []

        # ------ Añadir | Prompt ------
        content.append({"type": "input_text", "text": prompt})
        content.extend(self.files)
        # self.messages.append()

        if content:
            self.messages.append({"role": "user", "content": content})

        print(self.messages)

        # ------ OpenAI | Solicitud ------
        response = self.ai_client.Send_Request(
            model=self.model, input=self.messages, text_format=self.text_format, temperature=self.temperature
        )

        parsed = response.output_parsed

        assistant_json = parsed.model_dump_json()

        self.messages.append({"role": "assistant", "content": assistant_json})

        return parsed, response.usage
    
        #_______________________________________________________________________________
