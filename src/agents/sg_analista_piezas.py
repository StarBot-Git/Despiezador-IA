from __future__ import annotations
import json
from typing import Any
from agents.base_agent import BaseAgent

class Analista_Piezas(BaseAgent):

    SG_SYSTEM_PROMPT = "Eres un analista tecnico experto en planos y muebles de carpinteria."
    SG_MODEL = "gpt-4.1-mini"
    SG_RESPONSE_FORMAT = "json_object"
    SG_TEMPERATURE = 0.5

    def __init__(self):
        super().__init__(
            system_prompt=self.SG_SYSTEM_PROMPT, 
            model=self.SG_MODEL,
            default_tools=[],
            temperature=self.SG_TEMPERATURE
        )

    def Disassemble(self, files = None):
        prompt = f"""
        Eres un Analista de Piezas experto en carpintería y fabricación modular.
        Recibirás la información procesada del módulo "Instructor de Modelación",
        además de los planos de carpinteria y su contenido OCR.

        Tu trabajo es:

        1. Identificar qué tipo de mueble es.
        2. Extraer y listar todos los componentes del mueble:
            - Estructurales (caja, laterales, fondos, entrepaños, ...)
            - Frontales (puertas, frentes, ...)
            - Internos (repisas, soportes, divisiones, ...)
            - Accesorios (bisagras, brazos neumáticos, correderas, ...)
            - Modulos (Mueble bajo, Mueble alto, Mini Bar, Lavajillas)
        3. Indicar la cantidad de cada componente.
        4. Identificar la configuración general del mueble:
            - Tipo de apertura, cantidad de puertas, tipo de cantos
            - Presencia de repisas, cajones, divisiones
        5. Detectar si el plano presenta piezas duplicadas, faltantes o inconsistencias.
        6. Mantener la respuesta exclusivamente en JSON válido.
        7. Extrae la mayor cantidad de componentes posibles ya que la idea es poder reconstruir el modelo a partir de tu resultado.
        8. No tengas en cuenta componente electronicos. Somos una empresa de carpinteria entonces nos interesa lo relacionado a la madera y herrajes.
        9. Los electrodomesticos pueden ir en comentarios.
        10. En 'viabilidad' pon un porcentaje de fiabilidad de tus resultados y da una breve explicacion de que hizo falta para poder ser 100%.
        
        reglas:
        - Un módulo con una ">" o "<" en su vista indica una puerta.
        - Un módulo con "X" indica dos puertas (doble puerta).
        - Las "X" siempre están dentro del rectángulo que representa el módulo.
        - Cuando las “X” están separadas en dos áreas, representan dos puertas independientes.
        - Estos símbolos aplican tanto para módulos altos, bajos, laterales o superiores.
        - Si un módulo no tiene “X”, normalmente es un nicho abierto o repisa sin puertas.
        
        Formato exacto de salida:

        {{
        "mueble_tipo": "...",
        "componentes": [
            {{"nombre": "...", "tipo": "...", "cantidad": ...}}
        ],
        "configuracion": "..."
        "comentarios": "..."
        "viabilidad": "..."
        }}

        No agregues texto fuera del JSON. En 'comentarios' confirma si pudiste usar el/los archivos adjuntos y detalles que creas explicar.
        """

        # --- Ejecutar agente ---
        print("[AI_Refiner] Enviando informe preliminar al modelo IA...")
        
        model_Output = self.run(prompt=prompt, files=files)

        return model_Output