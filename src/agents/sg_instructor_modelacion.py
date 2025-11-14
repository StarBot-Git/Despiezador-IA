from __future__ import annotations
import json
from typing import Any
from utils.types import Report
from agents.base_agent import BaseAgent

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
        prompt = f"""
        Eres un analista experto en planos de carpintería y modelado técnico.
        Recibirás la información extraída automáticamente de un conjunto de planos,
        y deberás revisar, corregir o completar los datos para producir un informe más coherente y útil.
        Tu tarea es analizar la informacion presentanda en "INFORMACION A ANALIZAR" y comparar con "[Texto extraído del archivo]", 
        este texto fue extraido por OCR de los planos, con lo cual hay que hacer validacion de la coherencia de la informacion total, con la informacion del plano.
        Parte de tu trabajo es confirmar que las vistas detectadas son correctas según el texto extraído por OCR.

        Tu objetivo:
        - En terminos de vistas, NO debes inferir, suponer, completar ni adivinar información faltante.
        Solo acepta como verdadero lo que aparezca explícito en el texto.
        - Si ves que alguna vista detectada no tiene respaldo en el texto, elimínala.
        - Analizar los textos OCR y las vistas detectadas.
        - Identificar si existen vistas: "planta", "alzado", "corte", "isometrica".
        - Detectar si hay cotas (palabras como "mm", "cm", "Ø").
        - Corregir errores en el JSON (por ejemplo, eliminar vistas falsas o duplicadas).
        - Mejorar la descripción general del mueble con base en el texto.
        - Mantener todo en ESPAÑOL.
        - No repitas claves ni incluyas texto fuera del JSON.
        - En "razones" debes citar la frase exacta del OCR donde se menciona cada vista. Si no hay frase, no se acepta.
        - No completes ni mejores las vistas detectadas si no hay texto que lo avale.
        - Si se extrajo informacion de cotas(valores numericos) en el OCR, menciónalo en los comentarios.

        INFORMACIÓN A ANALIZAR:
        -----------------------------------
        {report_text}
        -----------------------------------

        Responde únicamente con un JSON estructurado que siga este formato:

        {{
        "files": [
            {{
            "name": "...",
            "detected_views": ["planta", "alzado"],
            "has_text": true,
            "comments": ["OCR exitoso", "Cotas detectadas (mm/cm)"]
            }}
        ],
        "general_description": "Texto breve en español con el tipo de mueble y vistas detectadas.",
        "conclusions": {{
            "estado": "viable | parcialmente viable | no viable",
            "razones": ["explicación 1", "explicación 2", ..., "explicación N"]
        }}
        }}
        """

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