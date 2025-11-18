from __future__ import annotations
import json
from typing import Any
from agents.base_agent import BaseAgent
from config.prompts import Analista_Piezas_Prompt

class Analista_Piezas(BaseAgent):
    SG_MODEL = "gpt-5-mini"
    SG_RESPONSE_FORMAT = "json_object"
    SG_TEMPERATURE = 0.5

    def __init__(self):
        super().__init__(
            system_prompt=Analista_Piezas_Prompt(), 
            model=self.SG_MODEL,
            default_tools=[],
            temperature=self.SG_TEMPERATURE
        )

    def Disassemble(self, files = None, report_text:str = None):
        # --- Prompt ---
        prompt = f"""
            Analiza los planos adjuntos y genera el JSON del mueble según las reglas del sistema. 
            Incluye los componentes y su clasificación exacta según los dibujos. 
            No agregues texto fuera del JSON.
        """

        # --- Ejecutar agente ---
        print("[AI_Refiner] Enviando informe preliminar al modelo IA...")
        
        model_Output = self.run(prompt=prompt, files=files)

        return model_Output