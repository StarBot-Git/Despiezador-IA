from __future__ import annotations
import json
from typing import Any
from utils.types import Report
from agents.base_agent import BaseAgent
from config.prompts import Instructor_Modelacion_Prompt

class Instructor_Modelacion(BaseAgent):

    SG_SYSTEM_PROMPT = "Eres un asistente tecnico experto en analisis de planos de carpinteria."
    SG_MODEL = "gpt-4.1-mini"
    SG_TEMPERATURE = 0.3

    def __init__(self):
        super().__init__(
            system_prompt=self.SG_SYSTEM_PROMPT, 
            model=self.SG_MODEL,
            default_tools=[],
            temperature=self.SG_TEMPERATURE
            )
        
    def Report(self, report:Report, report_text: str) -> Report:
        # --- Prompt ---
        
        prompt = Instructor_Modelacion_Prompt(report_txt=report_text)

        # --- Ejecutar agente ---
        print("[AI_Refiner] Enviando informe preliminar al modelo IA...")
        
        model_Output = self.run(prompt=prompt)

        # Aplicar resultados al objeto Report
        for ai_file in model_Output.files:
            for original in report.files:
                if ai_file.name == original.name:

                    # Vistas
                    original.detected_views = ai_file.detected_views

                    # Comentarios (extend)
                    original.comments.extend(ai_file.comments)

                    # has_text
                    original.has_text = ai_file.has_text

        # Descripción general
        report.general_description = model_Output.general_description

        # Conclusiones
        report.conclusions = {
            "estado": model_Output.conclusions.estado,
            "razones": model_Output.conclusions.razones
        }

        # Convertir a dict
        # if data:
        #     data = model_Output.model_dump()
        # else:
        #     data = json.loads(model_Output)

        # # Ahora sí funciona
        # for ai_file in data.get("files", []):
        #     for original in report.files:
        #         if ai_file.get("name") == original.name:
        #             if "detected_views" in ai_file:
        #                 original.detected_views = ai_file["detected_views"]

        #             if "comments" in ai_file:
        #                 original.comments.extend(ai_file["comments"])

        #             if "has_text" in ai_file:
        #                 original.has_text = ai_file["has_text"]

        # if "general_description" in data:
        #     report.general_description = data["general_description"]

        # if "conclusions" in data:
        #     report.conclusions = data["conclusions"]

        return report