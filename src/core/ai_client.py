from openai import OpenAI
from pathlib import Path

class AIClient:
    def __init__(self, openai_client):
        self.client = openai_client

    """
        Send_Request():
    """
    def Send_Request(self, model, input, text_format=None, temperature=0.3):
        #print(f"[IA] Temperature: {temperature}")
        return self.client.responses.parse(model=model, input=input, text_format=text_format)