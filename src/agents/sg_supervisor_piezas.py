from __future__ import annotations
import json
from typing import Any
from agents.base_agent import BaseAgent
from config.prompts import Supervisor_Piezas_Prompt

class Supervisor_Piezas(BaseAgent):
    SG_MODEL = "gpt-5-mini"
    SG_RESPONSE_FORMAT = "json_object"
    SG_TEMPERATURE = 0.5
    
    def __init__(self):
        super().__init__(
            system_prompt=Supervisor_Piezas_Prompt(), 
            model=self.SG_MODEL,
            default_tools=[],
            temperature=self.SG_TEMPERATURE
        )

    def Disassemble_Corrected(self, files=None, json_text:str=None):
        prompt = f"""
            Este es el JSON producido por el Analista de Piezas:

            {json_text}
        """

        print("[AI | Supervisor de piezas] Enviando informe preliminar al modelo IA...")

        model_Output = self.run(prompt=prompt, files=files)

        return model_Output