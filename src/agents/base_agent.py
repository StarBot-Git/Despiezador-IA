from .ai_client import send_request

class BaseAgent:
    def __init__(self, system_prompt, model, response_format, default_tools):
        self.model = model
        self.system_prompt = system_prompt
        self.response_format = response_format
        self.default_tools = default_tools or []
        self.messages = [{"role": "system", "content": system_prompt}]

    def run(self, prompt, variables=None, files=None, tools=None, detail=None):
        content = []
        #content.append({"type":"input_text", "text":prompt, "variables":variables})
        content.append({"type":"input_text", "text":prompt})

        if files:
            for f in files:
                content.append({"type":"input_file", "file_id": f})

        self.messages.append({"role":"user", "content":prompt})

        # attachments = []
        # if files:
        #     for f in files:
        #         attachments.append({"file_id":f, "tools": tools or self.default_tools})

        response = send_request(model=self.model, input = self.messages, response_format=self.response_format)

        output = response.output_parsed

        return output