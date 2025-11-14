from .ai_client import send_request

class BaseAgent:
    def __init__(self, system_prompt, model, temperature, default_tools):
        self.model = model
        self.system_prompt = system_prompt
        self.default_tools = default_tools or []
        self.messages = [{"role": "system", "content": system_prompt}]
        self.temperature = temperature

    def run(self, prompt, variables=None, files=None, tools=None, detail=None):

        print(f"[{self.__class__.__name__}] Hizo su peticion a OpenAI")

        model_name = self.__class__.__name__

        content = []
        #content.append({"type":"input_text", "text":prompt, "variables":variables})
        content.append({"type":"input_text", "text":prompt})

        if files:
            for f in files:
                content.append({"type":"input_file", "file_id": f})

        self.messages.append({"role":"user", "content":content})

        response = send_request(model=self.model, input = self.messages, model_name=model_name, temperature=self.temperature)

        output = response.output_parsed

        return output